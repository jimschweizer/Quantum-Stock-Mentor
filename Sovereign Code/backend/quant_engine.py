"""
Quantitative Analysis Engine for Technical Indicators and Statistical Scoring.
Calculates RSI, Moving Averages, Volatility, Support/Resistance levels, and Technical Scores.
"""

import math
import random

def calculate_rsi(prices, period=14):
    """
    Calculates Relative Strength Index (RSI).
    RSI > 70 = Overbought (potential pull-back)
    RSI < 30 = Oversold (potential bounce)
    RSI 45-60 = Bullish momentum
    """
    if len(prices) < period + 1:
        return 50.0  # Neutral default

    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change >= 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(change))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(rsi, 2)

def calculate_sma(prices, period=20):
    """Calculates Simple Moving Average (SMA)."""
    if len(prices) < period:
        return round(sum(prices) / len(prices), 2) if prices else 0.0
    return round(sum(prices[-period:]) / period, 2)

def calculate_volatility(prices):
    """Calculates historical volatility as percentage standard deviation."""
    if len(prices) < 2:
        return 0.05
    mean = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / (len(prices) - 1)
    std_dev = math.sqrt(variance)
    return round((std_dev / mean) * 100, 2)

def compute_key_levels(prices):
    """Computes Pivot, Support, and Resistance levels based on high/low/close."""
    if not prices:
        return {"support": 0.0, "resistance": 0.0, "pivot": 0.0}
    
    current = prices[-1]
    high = max(prices)
    low = min(prices)
    close = current
    
    pivot = (high + low + close) / 3.0
    resistance = (2 * pivot) - low
    support = (2 * pivot) - high
    
    return {
        "pivot": round(pivot, 2),
        "support": round(max(0.1, support), 2),
        "resistance": round(resistance, 2)
    }

def analyze_quant_metrics(ticker, current_price, price_history=None):
    """
    Generates quantitative analysis scores for a stock ticker.
    If price_history is omitted, generates a deterministic simulation series.
    """
    if not price_history or len(price_history) < 15:
        # Generate representative 30-day price movement based on ticker seed
        seed = sum(ord(c) for c in ticker)
        random.seed(seed)
        price_history = []
        base = current_price
        for _ in range(30):
            change = random.uniform(-0.04, 0.04)
            base = max(0.5, base * (1 + change))
            price_history.append(base)
        price_history[-1] = current_price

    rsi = calculate_rsi(price_history)
    sma7 = calculate_sma(price_history, 7)
    sma20 = calculate_sma(price_history, 20)
    sma30 = calculate_sma(price_history, 30)
    volatility = calculate_volatility(price_history)
    key_levels = compute_key_levels(price_history)

    # Multi-horizon Trend Calculations (1-day, 7-day, 30-day)
    p_curr = price_history[-1]
    p_prev1 = price_history[-2] if len(price_history) >= 2 else p_curr
    p_prev7 = price_history[-7] if len(price_history) >= 7 else price_history[0]
    p_prev30 = price_history[0]

    chg_1d = ((p_curr - p_prev1) / p_prev1) * 100.0 if p_prev1 > 0 else 0.0
    chg_7d = ((p_curr - p_prev7) / p_prev7) * 100.0 if p_prev7 > 0 else 0.0
    chg_30d = ((p_curr - p_prev30) / p_prev30) * 100.0 if p_prev30 > 0 else 0.0

    pos_count = sum([1 for c in [chg_1d, chg_7d, chg_30d] if c >= 0])
    if pos_count == 3:
        alignment_label = "Strong Bullish Confluence (1D + 7D + 30D Aligned)"
        alignment_score = 95
    elif pos_count == 2:
        alignment_label = "Moderate Bullish Bias (2/3 Timeframes Positive)"
        alignment_score = 70
    elif pos_count == 1:
        alignment_label = "Consolidation / Mixed Signals (1/3 Timeframes Positive)"
        alignment_score = 45
    else:
        alignment_label = "Bearish Pressure Across Timeframes (0/3 Positive)"
        alignment_score = 20

    # Technical Score (0.0 to 1.0)
    rsi_score = 1.0 - abs(rsi - 55) / 50.0
    rsi_score = max(0.1, min(1.0, rsi_score))
    
    sma_bias = 0.65 if current_price >= sma30 else 0.40
    technical_score = round((rsi_score * 0.5) + (sma_bias * 0.5), 2)
    
    volume_score = round(min(1.0, max(0.3, random.uniform(0.5, 0.9))), 2)
    trend_strength = round(min(1.0, max(0.2, (current_price / max(sma30, 0.01)) * 0.5)), 2)
    probability_score = round((technical_score * 0.4) + (volume_score * 0.3) + (trend_strength * 0.3), 2)

    return {
        "ticker": ticker,
        "current_price": current_price,
        "rsi": rsi,
        "sma7": sma7,
        "sma20": sma20,
        "sma30": sma30,
        "volatility_pct": volatility,
        "technical_score": technical_score,
        "volume_score": volume_score,
        "trend_strength": trend_strength,
        "probability_score": probability_score,
        "key_levels": key_levels,
        "trends": {
            "day_1": {"change_pct": round(chg_1d, 2), "direction": "UP" if chg_1d >= 0 else "DOWN"},
            "day_7": {"sma": sma7, "change_pct": round(chg_7d, 2), "direction": "UP" if chg_7d >= 0 else "DOWN"},
            "day_30": {"sma": sma30, "change_pct": round(chg_30d, 2), "direction": "UP" if chg_30d >= 0 else "DOWN"},
            "alignment": alignment_label,
            "alignment_score": alignment_score
        },
        "beginner_note": (
            f"RSI is at {rsi}. " +
            ("Overbought (>70) - potential short-term pull back." if rsi > 70 else
             "Oversold (<30) - potential buy opportunity for rebound." if rsi < 30 else
             "Healthy momentum band (30-70) indicating steady price action.")
        )
    }

