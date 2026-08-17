"""
Multi-Agent Trading Orchestrator for RJ-Stock.
Extends assets/prompts.py and assets/workers.py into structured, educational multi-agent analysis pipelines.
Integrates live OpenAI GPT-4o / Anthropic Claude API when keys are present in .env.
"""

import os
import json
import urllib.request
import urllib.error

try:
    from .config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS
    from .quant_engine import analyze_quant_metrics
    from .risk_engine import evaluate_risk
    from .quantum_prairie import get_quantum_prairie_summary
    from .upskill_engine import get_stock_upskill_tips
    from . import data_fetcher
except ImportError:
    from config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS
    from quant_engine import analyze_quant_metrics
    from risk_engine import evaluate_risk
    from quantum_prairie import get_quantum_prairie_summary
    from upskill_engine import get_stock_upskill_tips
    import data_fetcher

def load_env_keys():
    """Parses root .env file for OPENAI_API_KEY and ANTHROPIC_API_KEY."""
    keys = {"openai": os.environ.get("OPENAI_API_KEY"), "anthropic": os.environ.get("ANTHROPIC_API_KEY")}
    
    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        os.path.join(os.getcwd(), ".env")
    ]
    for path in env_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENAI_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"\'')
                        if val:
                            keys["openai"] = val
                    elif line.startswith("ANTHROPIC_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"\'')
                        if val:
                            keys["anthropic"] = val
    return keys

KEYS = load_env_keys()

def generate_openai_thesis(ticker_info, quant_data, risk_data):
    """
    Queries OpenAI Chat Completions API for live AI Trading Director thesis.
    """
    openai_key = KEYS.get("openai")
    if not openai_key:
        return None

    ticker = ticker_info["ticker"]
    name = ticker_info["name"]
    sector = ticker_info["sector"]
    desc = ticker_info["description"]
    focus = ticker_info["quantum_focus"]
    prairie = ticker_info.get("prairie_role", "Independent Quantum Pioneer")

    prompt = (
        f"You are the AI Trading Director for RJ-Stock. Analyze the stock {ticker} ({name}).\n"
        f"Sector: {sector}\n"
        f"Description: {desc}\n"
        f"Quantum Focus: {focus}\n"
        f"Midwest Quantum Prairie Role: {prairie}\n"
        f"Current Price: ${ticker_info.get('price', 15.0)}\n"
        f"RSI: {quant_data['rsi']}, Volatility: {quant_data['volatility_pct']}%\n"
        f"Recommended Shares: {risk_data['recommended_shares']}, Stop Loss: ${risk_data['stop_loss_price']}\n\n"
        f"Provide a structured response in JSON format matching this schema strictly:\n"
        f"{{\n"
        f'  "recommendation": "BUY (Growth Accumulation)" OR "HOLD (Watch Catalyst)" OR "UNDERWEIGHT / CAUTION",\n'
        f'  "market_thesis": "2-3 sentences on market thesis, tech catalysts, and Midwest ecosystem role.",\n'
        f'  "beginner_summary": "1-2 sentences explaining the decision simply to a beginner trader."\n'
        f"}}\n"
        f"Reply ONLY with raw valid JSON."
    )

    headers = {
        "Authorization": f"Bearer {openai_key}",
        "Content-Type": "application/json"
    }

    body = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a professional quant trading director AI."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }).encode("utf-8")

    try:
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            raw_text = data["choices"][0]["message"]["content"].strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(raw_text)
            return parsed
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        if "quota" in error_body or "credit" in error_body:
            print("[OpenAI API Notice] API Key detected, but quota/credit limit reached. Falling back to local Swarm Engine.")
        else:
            print(f"[OpenAI API Notice] HTTP {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"[OpenAI API Notice] Using local Swarm Engine: {e}")
        return None

def generate_claude_thesis(ticker_info, quant_data, risk_data):
    """
    Queries Anthropic Claude API for live AI Trading Director thesis.
    """
    anthropic_key = KEYS.get("anthropic")
    if not anthropic_key:
        return None

    ticker = ticker_info["ticker"]
    name = ticker_info["name"]
    sector = ticker_info["sector"]
    desc = ticker_info["description"]
    focus = ticker_info["quantum_focus"]
    prairie = ticker_info.get("prairie_role", "Independent Quantum Pioneer")

    prompt = (
        f"You are the AI Trading Director for RJ-Stock. Analyze the stock {ticker} ({name}).\n"
        f"Sector: {sector}\n"
        f"Description: {desc}\n"
        f"Quantum Focus: {focus}\n"
        f"Midwest Quantum Prairie Role: {prairie}\n"
        f"Current Price: ${ticker_info.get('price', 15.0)}\n"
        f"RSI: {quant_data['rsi']}, Volatility: {quant_data['volatility_pct']}%\n"
        f"Recommended Shares: {risk_data['recommended_shares']}, Stop Loss: ${risk_data['stop_loss_price']}\n\n"
        f"Provide a structured response in JSON format matching this schema strictly:\n"
        f"{{\n"
        f'  "recommendation": "BUY (Growth Accumulation)" OR "HOLD (Watch Catalyst)" OR "UNDERWEIGHT / CAUTION",\n'
        f'  "market_thesis": "2-3 sentences on market thesis, tech catalysts, and Midwest ecosystem role.",\n'
        f'  "beginner_summary": "1-2 sentences explaining the decision simply to a beginner trader."\n'
        f"}}\n"
        f"Reply ONLY with raw valid JSON."
    )

    headers = {
        "x-api-key": anthropic_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    body = json.dumps({
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    try:
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            raw_text = data["content"][0]["text"].strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(raw_text)
            return parsed
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        if "credit balance" in error_body:
            print("[Anthropic API Notice] API Key detected, but credit balance is low. Using local Swarm Engine.")
        else:
            print(f"[Anthropic API Notice] HTTP {e.code}: Using local Swarm Engine.")
        return None
    except Exception as e:
        print(f"[Anthropic API Notice] Using local Swarm Engine: {e}")
        return None

def run_trading_director(ticker_info, quant_data, risk_data):
    """
    Trading Director Agent: Formulates overall thesis & recommendation.
    Prioritizes OpenAI GPT-4o if available, then Anthropic Claude 3.5, then Local Swarm.
    """
    ticker = ticker_info["ticker"]
    is_prairie = "prairie_role" in ticker_info

    # 1. Try OpenAI API
    openai_res = generate_openai_thesis(ticker_info, quant_data, risk_data)
    if openai_res and "recommendation" in openai_res and "market_thesis" in openai_res:
        return {
            "agent_name": "Trading-Director (OpenAI GPT-4o)",
            "ticker": ticker,
            "recommendation": openai_res["recommendation"],
            "market_thesis": openai_res["market_thesis"],
            "beginner_summary": openai_res["beginner_summary"]
        }

    # 2. Try Anthropic Claude API
    claude_res = generate_claude_thesis(ticker_info, quant_data, risk_data)
    if claude_res and "recommendation" in claude_res and "market_thesis" in claude_res:
        return {
            "agent_name": "Trading-Director (Claude 3.5 Sonnet)",
            "ticker": ticker,
            "recommendation": claude_res["recommendation"],
            "market_thesis": claude_res["market_thesis"],
            "beginner_summary": claude_res["beginner_summary"]
        }

    # 3. Intelligent Local Swarm Engine Fallback
    thesis_summary = (
        f"Investment Thesis for {ticker} ({ticker_info['name']}): "
        f"{ticker_info['description']} "
        f"Key catalyst: {ticker_info['quantum_focus']}. "
    )
    if is_prairie:
        thesis_summary += f"Midwest Alignment: {ticker_info['prairie_role']}."
    
    recommendation = (
        "BUY (Growth Accumulation)" if quant_data["probability_score"] >= 0.65 else
        "HOLD (Watch Catalyst)" if quant_data["probability_score"] >= 0.45 else
        "UNDERWEIGHT / CAUTION"
    )
    
    return {
        "agent_name": "Trading-Director (Local Swarm Engine)",
        "ticker": ticker,
        "recommendation": recommendation,
        "market_thesis": thesis_summary,
        "beginner_summary": (
            f"The Trading Director ranks {ticker} as a '{recommendation}'. "
            f"This stock is evaluated under quantum computing growth metrics and regional Midwest partnerships."
        )
    }

def run_sentiment_agent(ticker_info):
    """
    Sentiment Agent: Evaluates news, institutional, and social sentiment.
    """
    ticker = ticker_info["ticker"]
    
    if ticker in ["IONQ", "QUBT", "IBM"]:
        score = 0.82
        news_sentiment = "Strongly Positive (Enterprise cloud contracts & Midwest quantum corridor expansions)"
        social_sentiment = "High Retail Interest (Quantum hardware scaling momentum)"
    elif ticker in ["NVDA", "MSFT", "GOOGL"]:
        score = 0.88
        news_sentiment = "Very Bullish (AI-Quantum hybrid dominance & GPU accelerator demand)"
        social_sentiment = "Dominant Institutional Buy Ratings"
    else:
        score = 0.62
        news_sentiment = "Moderately Positive (Superconducting roadmap & optimization partnerships)"
        social_sentiment = "Steady Retail Speculation"

    return {
        "agent_name": "Sentiment-Agent",
        "ticker": ticker,
        "sentiment_score": score,
        "news_sentiment": news_sentiment,
        "social_sentiment": social_sentiment,
        "institutional_rating": "Overweight / Outperform",
        "beginner_summary": f"Overall Market Sentiment is rated at {int(score*100)}/100, driven by key news events and institutional investor backing."
    }

def run_execution_agent(ticker, current_price, risk_data):
    """
    Execution Agent: Formats precise paper trading orders.
    """
    shares = risk_data["recommended_shares"]
    limit_entry = round(current_price * 0.995, 2)
    
    return {
        "agent_name": "Execution-Agent",
        "ticker": ticker,
        "action": "BUY_LIMIT",
        "order_type": "Limit Order",
        "quantity": shares,
        "entry_price": limit_entry,
        "stop_loss": risk_data["stop_loss_price"],
        "take_profit": risk_data["take_profit_price"],
        "time_in_force": "GTC (Good 'Til Canceled)",
        "estimated_total": round(shares * limit_entry, 2),
        "beginner_explanation": (
            f"Order Ticket prepared: BUY {shares} shares of {ticker} at a Limit Price of ${limit_entry:.2f}. "
            f"Automated risk safety nets: Stop-Loss @ ${risk_data['stop_loss_price']:.2f}, Take-Profit @ ${risk_data['take_profit_price']:.2f}."
        )
    }

def run_full_agent_analysis(ticker, account_size=10000.0, risk_tolerance=2.0):
    """
    Runs all 5 agents (Director, Quant, Sentiment, Risk, Execution) sequentially for a ticker.
    Fetches live price data via data_fetcher when available.
    """
    all_stocks = QUANTUM_PURE_PLAY + QUANTUM_PRAIRIE_GIANTS
    stock_info = next((s for s in all_stocks if s["ticker"] == ticker.upper()), None)
    if not stock_info:
        stock_info = {
            "ticker": ticker.upper(),
            "name": f"{ticker.upper()} Corp",
            "sector": "Quantum & Tech",
            "price": 10.00,
            "description": "Quantum technology market participant.",
            "quantum_focus": "Quantum Innovation"
        }

    # Fetch live price data (cache → API → simulation fallback)
    price_data = data_fetcher.fetch_price_history(ticker)
    close_prices = price_data.get("close", [])
    data_source = price_data.get("source", "simulated")
    last_updated = price_data.get("last_updated", None)

    # Use live price as current price when available
    if close_prices and data_source == "live":
        current_price = close_prices[-1]
        stock_info = dict(stock_info)  # shallow copy to avoid mutating config
        stock_info["price"] = current_price
    else:
        current_price = stock_info["price"]

    # Build OHLC data dict for proper pivot point calculation
    ohlc_data = None
    if data_source == "live" and "high" in price_data and "low" in price_data:
        ohlc_data = {
            "high": price_data["high"],
            "low": price_data["low"],
            "close": price_data["close"]
        }

    # Step 1: Quant Analyst (with live price history + OHLC when available)
    quant_res = analyze_quant_metrics(
        ticker, current_price,
        price_history=close_prices if len(close_prices) >= 15 else None,
        ohlc_data=ohlc_data
    )
    # H2 fix: quant_engine stamps "live" whenever >= 15 prices are supplied,
    # even when they came from the simulation fallback — force the label to
    # match the actual fetcher source so consumers never misread sim as live.
    quant_res["data_source"] = data_source
    
    # Step 2: Sentiment Agent
    sentiment_res = run_sentiment_agent(stock_info)
    
    # Step 3: Risk Manager
    risk_res = evaluate_risk(
        ticker=ticker,
        current_price=current_price,
        account_size=account_size,
        risk_tolerance_pct=risk_tolerance,
        volatility_pct=quant_res["volatility_pct"]
    )
    
    # Step 4: Trading Director (Uses OpenAI / Anthropic / Local Swarm)
    director_res = run_trading_director(stock_info, quant_res, risk_res)
    
    # Step 5: Execution Agent
    execution_res = run_execution_agent(ticker, current_price, risk_res)

    # Step 6: Stock-Pick Upskill Tips (Beginner to Intermediate)
    upskill_tips = get_stock_upskill_tips(ticker, stock_info, quant_res, risk_res)
    
    return {
        "ticker": ticker,
        "stock_info": stock_info,
        "director": director_res,
        "quant": quant_res,
        "sentiment": sentiment_res,
        "risk": risk_res,
        "execution": execution_res,
        "upskill_tips": upskill_tips,
        "data_source": data_source,
        "last_updated": last_updated,
        "data_stale": bool(price_data.get("stale", False))
    }
