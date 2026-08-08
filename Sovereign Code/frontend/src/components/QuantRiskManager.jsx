import React, { useState } from 'react';

export default function QuantRiskManager({ ticker, price = 14.85 }) {
  const [accountSize, setAccountSize] = useState(10000);
  const [riskTolerancePct, setRiskTolerancePct] = useState(2.0);
  const [volatility, setVolatility] = useState(5.0);

  const maxDollarRisk = (accountSize * (riskTolerancePct / 100)).toFixed(2);
  const stopLossDistancePct = Math.max(0.03, Math.min(0.12, (volatility / 100) * 1.5));
  const stopLossPrice = (price * (1 - stopLossDistancePct)).toFixed(2);
  const riskPerShare = price - stopLossPrice;
  const shares = riskPerShare > 0 ? Math.floor(maxDollarRisk / riskPerShare) : 1;
  const totalPositionValue = (shares * price).toFixed(2);
  const takeProfitPrice = (price + (riskPerShare * 2.5)).toFixed(2);

  // Intermediate Volatility Comparison Calculations
  const beginnerNaiveShares = Math.floor((accountSize * 0.10) / price); // Naive 10% capital allocation
  const naiveDollarRisk = (beginnerNaiveShares * (price - stopLossPrice)).toFixed(2);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-card">
        <h2 style={{ color: 'var(--accent-cyan)', marginBottom: '8px' }}>🛡️ Interactive Risk & Position Sizing Calculator</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>
          Adjust your total capital and risk parameters below to calculate exact position sizing for <strong>{ticker}</strong> at <strong>${price.toFixed(2)}</strong> per share.
        </p>

        <div className="dashboard-grid" style={{ padding: 0 }}>
          {/* Controls */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-main)', fontWeight: 'bold' }}>
                Account Portfolio Size: <span style={{ color: 'var(--accent-cyan)' }}>${accountSize.toLocaleString()}</span>
              </label>
              <input
                type="range"
                min="1000"
                max="100000"
                step="1000"
                value={accountSize}
                onChange={(e) => setAccountSize(Number(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--accent-cyan)' }}
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-main)', fontWeight: 'bold' }}>
                Max Risk Tolerance Per Trade: <span style={{ color: 'var(--accent-purple)' }}>{riskTolerancePct}%</span> (${maxDollarRisk})
              </label>
              <input
                type="range"
                min="0.5"
                max="5.0"
                step="0.5"
                value={riskTolerancePct}
                onChange={(e) => setRiskTolerancePct(Number(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--accent-purple)' }}
              />
              <small style={{ color: 'var(--text-muted)' }}>Wall Street Golden Rule: Never risk more than 1-2% of total account on 1 trade.</small>
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-main)', fontWeight: 'bold' }}>
                Stock Volatility Estimate: <span style={{ color: 'var(--accent-amber)' }}>{volatility}%</span>
              </label>
              <input
                type="range"
                min="2.0"
                max="15.0"
                step="0.5"
                value={volatility}
                onChange={(e) => setVolatility(Number(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--accent-amber)' }}
              />
            </div>
          </div>

          {/* Results Summary */}
          <div className="glass-card" style={{ background: 'rgba(0, 243, 255, 0.03)', border: '1px solid rgba(0, 243, 255, 0.2)' }}>
            <h3 style={{ color: 'var(--accent-cyan)', marginBottom: '16px' }}>📐 Position Calculation Output</h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px dashed var(--border-color)', paddingBottom: '8px' }}>
                <span>Recommended Shares:</span>
                <strong style={{ fontSize: '1.2rem', color: 'var(--accent-green)' }}>{shares} shares</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px dashed var(--border-color)', paddingBottom: '8px' }}>
                <span>Total Capital Allocated:</span>
                <strong>${totalPositionValue} ({((totalPositionValue / accountSize) * 100).toFixed(1)}% of portfolio)</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px dashed var(--border-color)', paddingBottom: '8px' }}>
                <span>Stop Loss Price:</span>
                <strong style={{ color: 'var(--accent-red)' }}>${stopLossPrice} (-{(stopLossDistancePct * 100).toFixed(1)}%)</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px dashed var(--border-color)', paddingBottom: '8px' }}>
                <span>Take Profit Target:</span>
                <strong style={{ color: 'var(--accent-green)' }}>${takeProfitPrice} (+{((takeProfitPrice / price - 1) * 100).toFixed(1)}%)</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Reward-to-Risk Ratio:</span>
                <strong style={{ color: 'var(--accent-purple)' }}>1 : 2.5 (Positive Expectancy)</strong>
              </div>
            </div>

            <div style={{ marginTop: '20px', background: 'rgba(255,255,255,0.05)', padding: '12px', borderRadius: '8px' }}>
              <strong style={{ color: 'var(--accent-cyan)' }}>🎓 Why Stop Loss Matters:</strong>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Setting a stop loss at ${stopLossPrice} guarantees that even if the stock plummets, your total loss is strictly limited to ${maxDollarRisk}, protecting 98% of your trading capital.
              </p>
            </div>
          </div>
        </div>

        {/* INTERMEDIATE UPSKILL COMPARISON WIDGET */}
        <div style={{ marginTop: '28px', background: 'rgba(168, 85, 247, 0.05)', padding: '20px', borderRadius: '14px', border: '1px solid rgba(168, 85, 247, 0.3)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <span className="badge badge-purple">⚡ Risk Upskill Spotlight</span>
            <h3 style={{ color: 'var(--accent-purple)', fontSize: '1.15rem' }}>
              Beginner vs. Intermediate Position Sizing Strategy
            </h3>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '12px' }}>
            <div style={{ background: 'rgba(239, 68, 68, 0.05)', padding: '14px', borderRadius: '10px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
              <strong style={{ color: 'var(--accent-red)' }}>🔴 Beginner Naive Sizing:</strong>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '6px', lineHeight: '1.5' }}>
                Buying a fixed 10% position ({beginnerNaiveShares} shares of {ticker}).
              </p>
              <div style={{ marginTop: '8px', fontSize: '0.85rem', color: 'var(--accent-red)' }}>
                <strong>Actual Downside Risk: ${naiveDollarRisk} ({((naiveDollarRisk / accountSize)*100).toFixed(1)}% of account!)</strong>
              </div>
            </div>

            <div style={{ background: 'rgba(16, 185, 129, 0.05)', padding: '14px', borderRadius: '10px', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
              <strong style={{ color: 'var(--accent-green)' }}>🟢 Intermediate Quant Sizing:</strong>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '6px', lineHeight: '1.5' }}>
                Volatility-Adjusted position size ({shares} shares of {ticker}).
              </p>
              <div style={{ marginTop: '8px', fontSize: '0.85rem', color: 'var(--accent-green)' }}>
                <strong>Controlled Risk: Exactly ${maxDollarRisk} ({riskTolerancePct}% of account)</strong>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
