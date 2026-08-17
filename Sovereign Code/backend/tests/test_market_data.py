"""
Unit tests for data_fetcher.py — Alpha Vantage parsing, cache layer, TTL,
and the cache → API → stale-cache → simulation fallback chain (H1 regressions).

Sandbox notes:
- Cache files are written DIRECTLY into Sovereign Code/data/ (already gitignored
  and writable in sandboxed/CI environments where temp dirs / tests/ may be
  read-only). All tests use synthetic TEST* tickers so they can never collide
  with the real 8-ticker cache, and every file is removed in teardown.

Stdlib unittest only (no pip dependencies). Run from the repo root:
    python -m unittest discover -s "Sovereign Code/backend/tests"
"""

import json
import os
import sys
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import data_fetcher as df

# Synthetic tickers never present in the real universe -> cache files
# TEST1_daily.json ... live directly under the real (gitignored) data dir.
TEST_TICKERS = ["TEST1", "TEST2", "TEST3"]


def _ohlcv(n=20):
    """Synthetic OHLCV series, n trading days."""
    return {
        "dates": [f"2026-07-{i + 1:02d}" for i in range(n)],
        "open": [10.0 + i * 0.1 for i in range(n)],
        "high": [10.5 + i * 0.1 for i in range(n)],
        "low": [9.5 + i * 0.1 for i in range(n)],
        "close": [10.0 + i * 0.1 for i in range(n)],
        "volume": [1000000 + i for i in range(n)],
    }


def _av_response(days=20):
    """Canned Alpha Vantage TIME_SERIES_DAILY payload (>= 15 days required by the fetcher)."""
    ts = {}
    for i in range(days):
        close = 10.0 + i * 0.1
        ts[f"2026-07-{i + 1:02d}"] = {
            "1. open": f"{close - 0.10:.2f}",
            "2. high": f"{close + 0.20:.2f}",
            "3. low": f"{close - 0.30:.2f}",
            "4. close": f"{close:.2f}",
            "5. volume": str(1000000 + i),
        }
    return {"Meta Data": {"2. Symbol": "TEST"}, "Time Series (Daily)": ts}


AV_3DAY = {
    "Meta Data": {"2. Symbol": "IONQ"},
    "Time Series (Daily)": {
        "2026-08-14": {"1. open": "14.50", "2. high": "15.00", "3. low": "14.40", "4. close": "14.85", "5. volume": "4200000"},
        "2026-08-15": {"1. open": "14.85", "2. high": "15.20", "3. low": "14.70", "4. close": "15.10", "5. volume": "5100000"},
        "2026-08-16": {"1. open": "15.10", "2. high": "15.30", "3. low": "14.90", "4. close": "15.05", "5. volume": "3900000"},
    },
}

AV_RATE_LIMIT = {"Note": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day."}
AV_ERROR = {"Error Message": "Invalid API call. Please retry or visit the documentation."}
AV_PREMIUM = {"Information": "The **TIME_SERIES_DAILY** endpoint is a premium endpoint. Please visit our Premium Membership page."}


def _fake_response(payload):
    """Context-manager response stub whose .read() yields JSON bytes."""
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(payload).encode("utf-8")
    resp.__enter__.return_value = resp
    return resp


def _cleanup_test_caches():
    """Removes any TEST* cache files left behind by tests."""
    for ticker in TEST_TICKERS:
        path = df._get_cache_path(ticker)
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass


def _age_cache(ticker, hours_old):
    """Rewrites an existing cache file with a last_updated timestamp hours_old in the past."""
    path = df._get_cache_path(ticker)
    with open(path, "r", encoding="utf-8") as f:
        cached = json.load(f)
    cached["last_updated"] = time.strftime(
        "%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - hours_old * 3600)
    )
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cached, f)


class DataFetcherTestCase(unittest.TestCase):
    """Base: hermetic API key (never touch .env or the network) + clean TEST caches."""

    def setUp(self):
        self._orig_get_key = df._get_alpha_vantage_key
        self._orig_all_tickers = df.ALL_TICKERS
        df._get_alpha_vantage_key = lambda: "TEST_KEY"
        _cleanup_test_caches()

    def tearDown(self):
        _cleanup_test_caches()
        df._get_alpha_vantage_key = self._orig_get_key
        df.ALL_TICKERS = self._orig_all_tickers


# ---------------------------------------------------------------------------
# Alpha Vantage parsing
# ---------------------------------------------------------------------------

class AlphaVantageParseTest(DataFetcherTestCase):

    def test_parse_success_normalizes_ohlcv(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(AV_3DAY)):
            ohlcv = df._fetch_from_alpha_vantage("IONQ")
        self.assertIsNotNone(ohlcv)
        self.assertEqual(ohlcv["dates"], ["2026-08-14", "2026-08-15", "2026-08-16"])
        self.assertEqual(ohlcv["open"], [14.5, 14.85, 15.1])
        self.assertEqual(ohlcv["high"], [15.0, 15.2, 15.3])
        self.assertEqual(ohlcv["low"], [14.4, 14.7, 14.9])
        self.assertEqual(ohlcv["close"], [14.85, 15.1, 15.05])
        self.assertEqual(ohlcv["volume"], [4200000, 5100000, 3900000])

    def test_parse_rate_limit_returns_none(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(AV_RATE_LIMIT)):
            self.assertIsNone(df._fetch_from_alpha_vantage("IONQ"))

    def test_parse_error_message_returns_none(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(AV_ERROR)):
            self.assertIsNone(df._fetch_from_alpha_vantage("IONQ"))

    def test_parse_premium_endpoint_returns_none(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(AV_PREMIUM)):
            self.assertIsNone(df._fetch_from_alpha_vantage("IONQ"))

    def test_parse_missing_time_series_returns_none(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response({"Meta Data": {}})):
            self.assertIsNone(df._fetch_from_alpha_vantage("IONQ"))

    def test_no_key_does_not_call_network(self):
        df._get_alpha_vantage_key = lambda: None
        with mock.patch("urllib.request.urlopen") as m:
            self.assertIsNone(df._fetch_from_alpha_vantage("IONQ"))
        m.assert_not_called()

    def test_http_error_returns_none(self):
        err = df.urllib.error.HTTPError("url", 429, "Too Many Requests", {}, None)
        with mock.patch("urllib.request.urlopen", side_effect=err):
            self.assertIsNone(df._fetch_from_alpha_vantage("IONQ"))

    def test_network_error_returns_none(self):
        err = df.urllib.error.URLError("no network")
        with mock.patch("urllib.request.urlopen", side_effect=err):
            self.assertIsNone(df._fetch_from_alpha_vantage("IONQ"))


# ---------------------------------------------------------------------------
# Cache layer
# ---------------------------------------------------------------------------

class CacheLayerTest(DataFetcherTestCase):

    def test_cache_round_trip(self):
        df._save_cache("TEST1", _ohlcv(), source="alpha_vantage")
        cached = df._load_cache("TEST1")
        self.assertIsNotNone(cached)
        self.assertEqual(cached["source"], "alpha_vantage")
        self.assertEqual(cached["data"]["close"], _ohlcv()["close"])
        self.assertIn("last_updated", cached)

    def test_load_cache_missing_returns_none(self):
        self.assertIsNone(df._load_cache("TEST1"))

    def test_load_cache_corrupted_json_returns_none(self):
        path = df._get_cache_path("TEST1")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("{definitely not json")
        self.assertIsNone(df._load_cache("TEST1"))

    def test_load_cache_empty_close_returns_none(self):
        path = df._get_cache_path("TEST1")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"source": "alpha_vantage", "data": {"close": []}}, f)
        self.assertIsNone(df._load_cache("TEST1"))

    def test_load_cache_wrong_shape_does_not_crash(self):
        # Regression: valid JSON with "data" as a list used to raise TypeError
        path = df._get_cache_path("TEST1")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"data": [1, 2, 3]}, f)
        self.assertIsNone(df._load_cache("TEST1"))


# ---------------------------------------------------------------------------
# TTL / staleness (H1)
# ---------------------------------------------------------------------------

class TtlTest(DataFetcherTestCase):

    def test_is_cache_fresh_within_ttl(self):
        now = time.strftime("%Y-%m-%dT%H:%M:%S")
        self.assertTrue(df._is_cache_fresh({"last_updated": now}))

    def test_is_cache_fresh_older_than_ttl(self):
        old = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 24 * 3600))
        self.assertFalse(df._is_cache_fresh({"last_updated": old}))

    def test_is_cache_fresh_malformed_timestamp(self):
        self.assertFalse(df._is_cache_fresh({"last_updated": "garbage"}))
        self.assertFalse(df._is_cache_fresh({}))


# ---------------------------------------------------------------------------
# fetch_price_history fallback chain (H1)
# ---------------------------------------------------------------------------

class FetchChainTest(DataFetcherTestCase):

    def test_fresh_cache_served_without_api_call(self):
        df._save_cache("TEST1", _ohlcv(), source="alpha_vantage")
        with mock.patch("urllib.request.urlopen") as m:
            result = df.fetch_price_history("TEST1")
        m.assert_not_called()
        self.assertEqual(result["source"], "live")
        self.assertFalse(result["stale"])
        self.assertEqual(len(result["close"]), 20)

    def test_no_cache_fetches_from_api_and_writes_cache(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(_av_response())):
            result = df.fetch_price_history("TEST1")
        self.assertEqual(result["source"], "live")
        self.assertFalse(result["stale"])
        self.assertEqual(len(result["close"]), 20)
        self.assertIsNotNone(df._load_cache("TEST1"))  # persisted

    def test_api_failure_with_no_cache_uses_simulation(self):
        err = df.urllib.error.URLError("no network")
        with mock.patch("urllib.request.urlopen", side_effect=err):
            result = df.fetch_price_history("TEST1")
        self.assertEqual(result["source"], "simulated")
        self.assertFalse(result["stale"])
        self.assertIsNone(result["last_updated"])
        self.assertEqual(len(result["close"]), 180)  # default sim horizon

    def test_stale_cache_with_api_failure_flagged_stale(self):
        df._save_cache("TEST1", _ohlcv(), source="alpha_vantage")
        _age_cache("TEST1", hours_old=48)
        err = df.urllib.error.URLError("no network")
        with mock.patch("urllib.request.urlopen", side_effect=err):
            result = df.fetch_price_history("TEST1")
        self.assertEqual(result["source"], "live")   # old live data > simulation
        self.assertTrue(result["stale"])             # ...but honestly flagged

    def test_stale_cache_refreshed_when_api_ok(self):
        df._save_cache("TEST1", _ohlcv(), source="alpha_vantage")
        _age_cache("TEST1", hours_old=48)
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(_av_response())):
            result = df.fetch_price_history("TEST1")
        self.assertEqual(result["source"], "live")
        self.assertFalse(result["stale"])

    def test_api_too_few_rows_falls_back(self):
        # 3 rows < the 15-row acceptance threshold -> simulation
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(AV_3DAY)):
            result = df.fetch_price_history("TEST1")
        self.assertEqual(result["source"], "simulated")

    def test_no_key_uses_simulation_without_network(self):
        df._get_alpha_vantage_key = lambda: None
        with mock.patch("urllib.request.urlopen") as m:
            result = df.fetch_price_history("TEST1")
        m.assert_not_called()
        self.assertEqual(result["source"], "simulated")
        self.assertFalse(result["stale"])

    def test_simulation_deterministic_per_ticker(self):
        a = df.fetch_price_history("TEST1")
        b = df.fetch_price_history("TEST1")
        self.assertEqual(a["close"], b["close"])
        self.assertEqual(a["high"], b["high"])


# ---------------------------------------------------------------------------
# warm_up_market_cache (M1)
# ---------------------------------------------------------------------------

class WarmUpTest(DataFetcherTestCase):

    def test_warm_up_fetches_all_tickers(self):
        df.ALL_TICKERS = TEST_TICKERS
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(_av_response())):
            summary = df.warm_up_market_cache()
        self.assertEqual(len(summary), len(TEST_TICKERS))
        for ticker, info in summary.items():
            self.assertEqual(info["source"], "live", ticker)
            self.assertFalse(info["stale"], ticker)

    def test_warm_up_skips_fresh_caches(self):
        for ticker in TEST_TICKERS:
            df._save_cache(ticker, _ohlcv(), source="alpha_vantage")
        df.ALL_TICKERS = TEST_TICKERS
        with mock.patch("urllib.request.urlopen") as m:
            summary = df.warm_up_market_cache()
        m.assert_not_called()  # every ticker served from fresh cache
        self.assertTrue(all(v["source"] == "live" for v in summary.values()))

    def test_warm_up_without_key_is_harmless(self):
        df._get_alpha_vantage_key = lambda: None
        df.ALL_TICKERS = TEST_TICKERS
        with mock.patch("urllib.request.urlopen") as m:
            summary = df.warm_up_market_cache()
        m.assert_not_called()
        self.assertEqual(len(summary), len(TEST_TICKERS))
        self.assertTrue(all(v["source"] == "simulated" for v in summary.values()))


if __name__ == "__main__":
    unittest.main()
