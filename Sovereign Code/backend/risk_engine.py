"""
Risk Assessment Engine for Position Sizing and Trade Parameter Calculation.
Implements 1-2% Account Risk Rule, Stop Loss, Take Profit, and Drawdown Risk scoring.
"""

def evaluate_risk(ticker, current_price, account_size=10000.0, risk_tolerance_pct=2.0, volatility_pct=5.0):
    """
    Calculates recommended position sizing and risk management levels.
    
    - Account Risk Rule: Maximum capital allowed to lose on a single trade is risk_tolerance_pct % of account.
    - Stop Loss: Placed based on volatility (typically 1.5x - 2x daily volatility below entry price).
    - Take Profit: Designed for at least a 2:1 Reward-to-Risk ratio.
    """
    max_dollar_risk = account_size * (risk_tolerance_pct / 100.0)
    
    # Distance to stop loss as percentage based on volatility
    stop_loss_distance_pct = max(0.03, min(0.12, (volatility_pct / 100.0) * 1.5))
    stop_loss_price = round(current_price * (1.0 - stop_loss_distance_pct), 2)
    risk_per_share = current_price - stop_loss_price
    
    if risk_per_share > 0:
        recommended_shares = int(max_dollar_risk / risk_per_share)
    else:
        recommended_shares = 1

    total_position_value = round(recommended_shares * current_price, 2)
    max_portfolio_allocation_pct = round((total_position_value / account_size) * 100, 2)
    
    # 2.5x Risk-Reward Target
    take_profit_price = round(current_price + (risk_per_share * 2.5), 2)
    max_drawdown_risk_pct = round(stop_loss_distance_pct * 100, 2)
    
    overall_risk_score = round(min(1.0, (volatility_pct / 10.0) * 0.5 + (max_portfolio_allocation_pct / 20.0) * 0.5), 2)

    return {
        "ticker": ticker,
        "current_price": current_price,
        "account_size": account_size,
        "risk_tolerance_pct": risk_tolerance_pct,
        "max_dollar_risk": round(max_dollar_risk, 2),
        "recommended_shares": recommended_shares,
        "total_position_value": total_position_value,
        "portfolio_allocation_pct": max_portfolio_allocation_pct,
        "stop_loss_price": stop_loss_price,
        "take_profit_price": take_profit_price,
        "risk_reward_ratio": "1 : 2.5",
        "max_drawdown_risk_pct": max_drawdown_risk_pct,
        "overall_risk_score": overall_risk_score,
        "risk_category": "High Risk / Growth" if overall_risk_score > 0.6 else "Moderate Risk" if overall_risk_score > 0.3 else "Low Risk / Defensive",
        "beginner_explanation": (
            f"If you trade ${total_position_value:.2f} ({recommended_shares} shares), your maximum risk is strictly capped at "
            f"${max_dollar_risk:.2f} using a Stop Loss at ${stop_loss_price:.2f}. "
            f"If the price reaches your Take Profit target at ${take_profit_price:.2f}, your expected profit is ${(recommended_shares * risk_per_share * 2.5):.2f}."
        )
    }
