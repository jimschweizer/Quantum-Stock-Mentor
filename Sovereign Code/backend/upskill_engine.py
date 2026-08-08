"""
Portfolio Upskilling Engine for RJ-Stock.
Generates step-by-step improvement tips for stock picks to elevate users
from Beginner to Intermediate portfolio traders.
"""

def get_stock_upskill_tips(ticker, stock_info, quant_data, risk_data):
    """
    Returns 4 structured, progressive upskill steps for a stock pick.
    """
    ticker_upper = ticker.upper()
    rsi = quant_data.get("rsi", 50)
    volatility = quant_data.get("volatility_pct", 5.0)
    price = stock_info.get("price", 15.0)
    trends = quant_data.get("trends", {})
    alignment_str = trends.get("alignment", "Confluence Check")
    is_prairie_giant = "prairie_role" in stock_info or ticker_upper in ["IBM", "NVDA", "MSFT", "GOOGL"]
    
    # Baseline Beta estimate based on sector profile
    beta = 0.85 if ticker_upper == "IBM" else (1.45 if is_prairie_giant else 2.35)

    # Step 1: Baseline Foundation (Beginner)
    step1_title = "Step 1: Metric Foundation (Beginner)"
    step1_desc = (
        f"For {ticker_upper}, your primary anchor is RSI ({rsi}) and 1-Day price change ({trends.get('day_1', {}).get('change_pct', 0)}%). "
        f"In beginner trading, avoid knee-jerk reactions to single-day noise. RSI below 30 signals oversold, while above 70 suggests overbought."
    )

    # Step 2: Intermediate Technical & Multi-Horizon Trend Alignment
    step2_title = "Step 2: Multi-Horizon Trend (1D, 7D, 30D) & Valuation Upgrade"
    if is_prairie_giant:
        step2_desc = (
            f"Intermediate Upgrade: Current trend alignment is '{alignment_str}'. "
            f"Analyze 7-Day swing ({trends.get('day_7', {}).get('change_pct', 0)}%) and 30-Day baseline ({trends.get('day_30', {}).get('change_pct', 0)}%). "
            f"Ensure 1D momentum does not fight the broader 30-Day trend baseline before entering positions."
        )
    else:
        step2_desc = (
            f"Intermediate Upgrade: Pure-Play Quantum stocks like {ticker_upper} experience high Beta (~{beta:.2f}) and {volatility}% volatility. "
            f"Current trend alignment is '{alignment_str}'. Use 30-Day SMA (${quant_data.get('sma30', price):.2f}) and ATR/Support "
            f"(${quant_data.get('key_levels', {}).get('support', price * 0.9):.2f}) to avoid getting stopped out by 1-Day intraday noise."
        )

    # Step 3: Portfolio Correlation & Hedging Strategy
    step3_title = "Step 3: Portfolio Hedging & Sector Correlation"
    if is_prairie_giant:
        step3_desc = (
            f"Portfolio Tip: {ticker_upper} acts as a Stabilizing Anchor in a tech portfolio. "
            f"Combine anchor positions like {ticker_upper} with 15-20% allocation in pure-play quantum pioneers "
            f"to capture explosive upside while dampening overall portfolio drawdown."
        )
    else:
        step3_desc = (
            f"Portfolio Tip: {ticker_upper} is a High-Upside / High-Beta Speculative Growth pick. "
            f"Hedge this position by pairing it with a Midwest Quantum Prairie Giant (e.g. NVDA or IBM). "
            f"Keep speculative pure-play quantum picks below 5-10% of total portfolio value."
        )

    # Step 4: Interactive Pre-Trade Execution Checklist
    checklist = [
        {
            "id": "risk_rule",
            "label": f"Verify maximum risk per trade does not exceed 1-2% of total portfolio value (Max risk: ${risk_data.get('total_position_value', 200)})."
        },
        {
            "id": "rsi_check",
            "label": f"Confirm RSI ({rsi}) is not overbought (>70) prior to market buy order placement."
        },
        {
            "id": "trend_check",
            "label": f"Verify Multi-Timeframe Trend Confluence: 1D ({trends.get('day_1', {}).get('direction', 'UP')}), 7D ({trends.get('day_7', {}).get('direction', 'UP')}), 30D ({trends.get('day_30', {}).get('direction', 'UP')}) — Status: {alignment_str}."
        },
        {
            "id": "stop_loss_check",
            "label": f"Set automated Stop-Loss order at ${risk_data.get('stop_loss_price', round(price*0.93, 2))} to enforce disciplined exit."
        },
        {
            "id": "ecosystem_check",
            "label": f"Verify ecosystem alignment ({stock_info.get('sector', 'Quantum Tech')}) fits overall sector allocation target."
        }
    ]

    return {
        "stock_ticker": ticker_upper,
        "beta_estimate": beta,
        "upskill_level": "Beginner ➔ Intermediate",
        "step_1": {
            "title": step1_title,
            "description": step1_desc,
            "badge": "Beginner Baseline"
        },
        "step_2": {
            "title": step2_title,
            "description": step2_desc,
            "badge": "Intermediate Tech"
        },
        "step_3": {
            "title": step3_title,
            "description": step3_desc,
            "badge": "Portfolio Strategy"
        },
        "step_4": {
            "title": "Step 4: Actionable Pre-Trade Analysis Checklist",
            "badge": "Execution Discipline",
            "checklist": checklist
        }
    }

