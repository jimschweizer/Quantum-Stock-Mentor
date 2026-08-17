"""
Live Market Data Fetcher for RJ-Stock — Alpha Vantage Integration.

Fetches real OHLCV daily price history via Alpha Vantage (free tier),
caches to JSON files in Sovereign Code/data/, and falls back to
deterministic seeded simulation when API key is absent or rate-limited.

Zero external dependencies — uses only urllib.request, json, os, math, random.
"""

import os
import json
import math
import random
import time
import urllib.request
import urllib.error

try:
    from .config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS, ALL_TICKERS
except ImportError:
    from config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS, ALL_TICKERS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Cache directory: Sovereign Code/data/ (relative to backend/)
_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

_ALPHA_VANTAGE_BASE = "https://www.alphavantage.co/query"
_REQUEST_TIMEOUT = 15  # seconds

# Daily bars change at most once per trading day (EOD); 6h TTL keeps the
# cache fresh enough for a demo/education tool without hammering the
# Alpha Vantage free tier (25 requests/day).
_DAILY_CACHE_TTL_SECONDS = 6 * 3600


def _get_alpha_vantage_key():
    """
    Reads ALPHA_VANTAGE_API_KEY from os.environ and root .env file.
    Same dual-source pattern used by agents.py for OpenAI/Anthropic keys.
    """
    key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if key:
        return key

    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        os.path.join(os.getcwd(), ".env")
    ]
    for path in env_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ALPHA_VANTAGE_API_KEY="):
                            val = line.split("=", 1)[1].strip().strip('"\'')
                            if val:
                                return val
            except OSError:
                continue
    return None


# ---------------------------------------------------------------------------
# Cache Layer
# ---------------------------------------------------------------------------

def _ensure_cache_dir():
    """Creates the cache directory if it doesn't exist."""
    os.makedirs(_CACHE_DIR, exist_ok=True)


def _get_cache_path(ticker):
    """Returns the absolute path to a ticker's cached JSON file."""
    return os.path.join(_CACHE_DIR, f"{ticker.upper()}_daily.json")


def _load_cache(ticker):
    """
    Loads cached OHLCV data from disk.
    Returns the parsed dict or None if missing/corrupted.
    """
    path = _get_cache_path(ticker)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        # Validate structure
        if "data" in cached and "close" in cached["data"] and len(cached["data"]["close"]) > 0:
            return cached
        return None
    except (json.JSONDecodeError, OSError, KeyError, TypeError):
        # TypeError: cache JSON is valid but shaped wrong (e.g. "data" is a list)
        return None


def _save_cache(ticker, ohlcv_data, source="alpha_vantage"):
    """
    Writes OHLCV data + metadata to the JSON cache file.
    ohlcv_data: dict with keys {dates, open, high, low, close, volume}
    """
    _ensure_cache_dir()
    cache_obj = {
        "ticker": ticker.upper(),
        "source": source,
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "data": ohlcv_data
    }
    path = _get_cache_path(ticker)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cache_obj, f, indent=2)
    except OSError as e:
        print(f"[Data Fetcher] Warning: Could not write cache for {ticker}: {e}")


def _is_cache_fresh(cached):
    """
    Returns True if the cached payload is within the TTL window.
    A malformed/missing timestamp is treated as stale (forces a refresh attempt).
    """
    last_updated = cached.get("last_updated")
    if not last_updated:
        return False
    try:
        fetched_ts = time.mktime(time.strptime(last_updated, "%Y-%m-%dT%H:%M:%S"))
    except (ValueError, TypeError, OverflowError, OSError):
        return False
    return (time.time() - fetched_ts) < _DAILY_CACHE_TTL_SECONDS


# ---------------------------------------------------------------------------
# Alpha Vantage API
# ---------------------------------------------------------------------------

def _fetch_from_alpha_vantage(ticker):
    """
    Calls Alpha Vantage TIME_SERIES_DAILY endpoint.
    Returns normalized OHLCV dict or None on any error.

    Response keys from Alpha Vantage:
      "1. open", "2. high", "3. low", "4. close", "5. volume"
    """
    api_key = _get_alpha_vantage_key()
    if not api_key:
        return None

    url = (
        f"{_ALPHA_VANTAGE_BASE}"
        f"?function=TIME_SERIES_DAILY"
        f"&symbol={ticker.upper()}"
        f"&outputsize=compact"
        f"&apikey={api_key}"
    )

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "RJ-Stock/0.1")
        with urllib.request.urlopen(req, timeout=_REQUEST_TIMEOUT) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        print(f"[Data Fetcher] Alpha Vantage HTTP {e.code} for {ticker}")
        return None
    except urllib.error.URLError as e:
        print(f"[Data Fetcher] Alpha Vantage network error for {ticker}: {e.reason}")
        return None
    except Exception as e:
        print(f"[Data Fetcher] Alpha Vantage unexpected error for {ticker}: {e}")
        return None

    # Check for rate-limit or error messages
    if "Note" in data:
        print(f"[Data Fetcher] Alpha Vantage rate limit hit: {data['Note'][:80]}...")
        return None
    if "Error Message" in data:
        print(f"[Data Fetcher] Alpha Vantage error for {ticker}: {data['Error Message']}")
        return None
    if "Information" in data:
        print(f"[Data Fetcher] Alpha Vantage info: {data['Information'][:80]}...")
        return None

    # Parse the time series
    ts_key = "Time Series (Daily)"
    if ts_key not in data:
        print(f"[Data Fetcher] Alpha Vantage response missing '{ts_key}' for {ticker}")
        return None

    time_series = data[ts_key]
    if not time_series:
        return None

    # Sort dates ascending (oldest first) for consistent price_history ordering
    sorted_dates = sorted(time_series.keys())

    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []

    for date_str in sorted_dates:
        day = time_series[date_str]
        dates.append(date_str)
        opens.append(float(day["1. open"]))
        highs.append(float(day["2. high"]))
        lows.append(float(day["3. low"]))
        closes.append(float(day["4. close"]))
        volumes.append(int(float(day["5. volume"])))

    ohlcv = {
        "dates": dates,
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
        "volume": volumes
    }

    print(f"[Data Fetcher] OK - Fetched {len(dates)} days of live data for {ticker}")
    return ohlcv


# ---------------------------------------------------------------------------
# Deterministic Simulation Fallback
# ---------------------------------------------------------------------------

def _generate_simulated_history(ticker, current_price, days=180):
    """
    Generates a deterministic simulated OHLCV price history using a seeded
    random walk. Produces identical results for the same ticker across sessions.

    This is the existing simulation logic from quant_engine.py, restructured
    to return full OHLC format instead of close-only.
    """
    seed = sum(ord(c) for c in ticker.upper())
    random.seed(seed)

    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []

    base = current_price
    today = time.strftime("%Y-%m-%d")

    for i in range(days):
        # Generate date label (approximate, for display only)
        day_offset = days - i
        # Simple date approximation — not calendar-precise but sufficient for sim
        epoch = time.time() - (day_offset * 86400)
        date_str = time.strftime("%Y-%m-%d", time.localtime(epoch))

        daily_change = random.uniform(-0.04, 0.04)
        open_price = base
        close_price = max(0.5, base * (1 + daily_change))

        # Simulate intraday high/low from open/close
        spread = abs(close_price - open_price)
        high_price = max(open_price, close_price) + random.uniform(0, spread * 0.5)
        low_price = min(open_price, close_price) - random.uniform(0, spread * 0.5)
        low_price = max(0.1, low_price)  # Floor at $0.10

        volume = int(random.uniform(500000, 5000000))

        dates.append(date_str)
        opens.append(round(open_price, 4))
        highs.append(round(high_price, 4))
        lows.append(round(low_price, 4))
        closes.append(round(close_price, 4))
        volumes.append(volume)

        base = close_price

    # Anchor the last close to the current (config) price
    closes[-1] = current_price

    return {
        "dates": dates,
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
        "volume": volumes
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch_price_history(ticker, days=180):
    """
    Primary entry point for price data. Strategy: fresh cache → API → stale cache → simulation.

    Returns dict:
    {
        "dates": [...], "open": [...], "high": [...], "low": [...],
        "close": [...], "volume": [...],
        "source": "live" | "simulated",
        "last_updated": "2026-08-17T15:00:00" | None,
        "stale": bool   # True only when serving old live data past its TTL
    }
    """
    ticker = ticker.upper()

    # 1. Serve a fresh cache immediately (no API call — preserves offline-first)
    cached = _load_cache(ticker)
    if cached and _is_cache_fresh(cached):
        result = cached["data"].copy()
        result["source"] = "live" if cached.get("source") == "alpha_vantage" else "simulated"
        result["last_updated"] = cached.get("last_updated")
        result["stale"] = False
        return result

    # 2. Try Alpha Vantage API (also reached when cache is missing or stale)
    api_data = _fetch_from_alpha_vantage(ticker)
    if api_data and len(api_data.get("close", [])) >= 15:
        _save_cache(ticker, api_data, source="alpha_vantage")
        result = api_data.copy()
        result["source"] = "live"
        result["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        result["stale"] = False
        return result

    # 3a. Stale-cache fallback: API failed, but old live data is better than simulation
    if cached and cached.get("source") == "alpha_vantage":
        result = cached["data"].copy()
        result["source"] = "live"
        result["last_updated"] = cached.get("last_updated")
        result["stale"] = True
        return result

    # 3b. Deterministic simulation fallback
    stock_info = _find_stock_info(ticker)
    current_price = stock_info["price"] if stock_info else 10.00
    sim_data = _generate_simulated_history(ticker, current_price, days)
    result = sim_data.copy()
    result["source"] = "simulated"
    result["last_updated"] = None
    result["stale"] = False
    return result


def refresh_ticker_data(ticker):
    """
    Forces a fresh API fetch, bypassing cache. Returns the freshened data dict.
    If API fails, falls back to existing cache or simulation.
    """
    ticker = ticker.upper()

    api_data = _fetch_from_alpha_vantage(ticker)
    if api_data and len(api_data.get("close", [])) >= 15:
        _save_cache(ticker, api_data, source="alpha_vantage")
        result = api_data.copy()
        result["source"] = "live"
        result["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        result["stale"] = False
        return result

    # If API fails, return whatever we have (cache or sim)
    print(f"[Data Fetcher] Refresh failed for {ticker}, falling back to cached/simulated data")
    return fetch_price_history(ticker)


def get_current_price(ticker):
    """
    Returns (latest_close_price, source) where source is "live" or "simulated".
    """
    data = fetch_price_history(ticker)
    closes = data.get("close", [])
    if closes:
        return closes[-1], data.get("source", "simulated")

    # Absolute fallback to config price
    stock_info = _find_stock_info(ticker)
    price = stock_info["price"] if stock_info else 10.00
    return price, "simulated"


def warm_up_market_cache():
    """
    Pre-fetches market data for the full universe — called once at server startup.

    Skips tickers with a fresh cache (fetch_price_history serves those without
    any API call, preserving the Alpha Vantage free-tier daily quota); fetches
    missing or stale tickers. Harmless without an API key (falls back to
    deterministic simulation and writes nothing to disk).

    Returns a per-ticker summary dict for logging.
    """
    summary = {}
    for ticker in ALL_TICKERS:
        try:
            result = fetch_price_history(ticker)
            summary[ticker] = {
                "source": result.get("source", "simulated"),
                "stale": bool(result.get("stale", False)),
                "days": len(result.get("close", []))
            }
        except Exception as e:
            summary[ticker] = {"source": "error", "error": str(e)}

    live_count = sum(1 for v in summary.values() if v.get("source") == "live" and not v.get("stale"))
    print(f"[Data Fetcher] Warm-up complete: {live_count}/{len(summary)} tickers live")
    return summary


def get_quantum_universe():
    """
    Returns complete quantum stock universe with prices updated from cache
    when available. Preserves offline-first: uses config defaults when no
    cache exists.
    """
    import copy
    pure_play = copy.deepcopy(QUANTUM_PURE_PLAY)
    prairie_giants = copy.deepcopy(QUANTUM_PRAIRIE_GIANTS)

    for stock in pure_play + prairie_giants:
        ticker = stock["ticker"]
        cached = _load_cache(ticker)
        if cached and cached.get("source") == "alpha_vantage":
            closes = cached["data"].get("close", [])
            if closes:
                stock["price"] = closes[-1]
                stock["data_source"] = "live"
                stock["last_updated"] = cached.get("last_updated")
                stock["stale"] = not _is_cache_fresh(cached)
            else:
                stock["data_source"] = "simulated"
                stock["last_updated"] = None
                stock["stale"] = False
        else:
            stock["data_source"] = "simulated"
            stock["last_updated"] = None
            stock["stale"] = False

    return {
        "pure_play": pure_play,
        "prairie_giants": prairie_giants
    }


def get_stock_detail(ticker):
    """
    Returns stock info dict for a ticker with live price overlay if cached.
    Returns None if ticker is not in the curated universe.
    """
    import copy
    stock_info = _find_stock_info(ticker)
    if not stock_info:
        return None

    result = copy.deepcopy(stock_info)
    cached = _load_cache(ticker)
    if cached and cached.get("source") == "alpha_vantage":
        closes = cached["data"].get("close", [])
        if closes:
            result["price"] = closes[-1]
            result["data_source"] = "live"
            result["last_updated"] = cached.get("last_updated")
            result["stale"] = not _is_cache_fresh(cached)

    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_stock_info(ticker):
    """Looks up a ticker in the curated universe. Returns dict or None."""
    ticker = ticker.upper()
    for stock in QUANTUM_PURE_PLAY + QUANTUM_PRAIRIE_GIANTS:
        if stock["ticker"].upper() == ticker:
            return stock
    return None
