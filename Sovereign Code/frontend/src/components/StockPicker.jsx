import React, { useState } from 'react';

export default function StockPicker({ analysis, loading, onRunAnalysis, userXP = 150, userSkillLevel = "Beginner Apprentice", onCompleteCheckitem }) {
  const [checkedItems, setCheckedItems] = useState({});

  if (loading) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '60px' }}>
        <h3 style={{ color: 'var(--accent-cyan)', marginBottom: '12px' }}>🤖 5-Agent Swarm Analyzing Stock...</h3>
        <p style={{ color: 'var(--text-muted)' }}>Trading Director • Quant Analyst • Sentiment Agent • Risk Manager • Execution Agent</p>
      </div>
    );
  }

  if (!analysis) return null;

  const { stock_info, director, quant, sentiment, risk, execution, upskill_tips } = analysis;

  const toggleCheck = (itemId) => {
    const isNewCheck = !checkedItems[itemId];
    setCheckedItems(prev => ({
      ...prev,
      [itemId]: isNewCheck
    }));

    if (isNewCheck && onCompleteCheckitem) {
      onCompleteCheckitem(50); // Reward 50 XP per completed analysis item
    }
  };

  const checklist = upskill_tips?.step_4?.checklist || [];
  const completedCount = Object.values(checkedItems).filter(Boolean).length;
  const totalCount = checklist.length;
  const progressPct = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header Banner */}
      <div className="glass-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <h1 style={{ fontSize: '2rem', background: 'var(--gradient-quantum)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              {stock_info.ticker}
            </h1>
            <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>{stock_info.name}</span>
            <span className="badge badge-cyan">{stock_info.sector}</span>
          </div>
          <p style={{ marginTop: '8px', color: 'var(--text-muted)' }}>{stock_info.description}</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--accent-green)' }}>
            ${stock_info.price.toFixed(2)}
          </div>
          <button className="btn-primary" onClick={onRunAnalysis} style={{ marginTop: '8px' }}>
            🔄 Re-run Agent Swarm
          </button>
        </div>
      </div>

      {/* 5-Agent Swarm Grid */}
      <div className="dashboard-grid" style={{ padding: 0 }}>
        
        {/* Agent 1: Trading Director */}
        <div className="glass-card">
          <div className="badge badge-purple" style={{ marginBottom: '12px' }}>👑 Trading Director</div>
          <h3 style={{ marginBottom: '8px', color: 'var(--accent-cyan)' }}>Recommendation: {director.recommendation}</h3>
          <p style={{ fontSize: '0.9rem', lineHeight: '1.5', color: 'var(--text-main)', marginBottom: '16px' }}>
            {director.market_thesis}
          </p>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--accent-purple)' }}>
            <small style={{ color: 'var(--accent-purple)', fontWeight: 'bold' }}>🎓 Beginner Translation:</small>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>{director.beginner_summary}</p>
          </div>
        </div>

        {/* Agent 2: Quant Analyst */}
        <div className="glass-card">
          <div className="badge badge-cyan" style={{ marginBottom: '12px' }}>📊 Quant Analyst</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
            <div>
              <small style={{ color: 'var(--text-muted)' }}>RSI (14-day)</small>
              <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: quant.rsi > 70 ? 'var(--accent-red)' : quant.rsi < 30 ? 'var(--accent-green)' : 'var(--accent-cyan)' }}>
                {quant.rsi}
              </div>
            </div>
            <div>
              <small style={{ color: 'var(--text-muted)' }}>20-Day SMA</small>
              <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>${quant.sma20}</div>
            </div>
            <div>
              <small style={{ color: 'var(--text-muted)' }}>Volatility</small>
              <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{quant.volatility_pct}%</div>
            </div>
            <div>
              <small style={{ color: 'var(--text-muted)' }}>Probability Score</small>
              <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--accent-green)' }}>
                {int(quant.probability_score * 100)}%
              </div>
            </div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--accent-cyan)' }}>
            <small style={{ color: 'var(--accent-cyan)', fontWeight: 'bold' }}>🎓 RSI Insight:</small>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>{quant.beginner_note}</p>
          </div>
        </div>

        {/* Agent 3: Sentiment Agent */}
        <div className="glass-card">
          <div className="badge badge-green" style={{ marginBottom: '12px' }}>🌐 Sentiment Agent</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px' }}>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--accent-green)' }}>
              {int(sentiment.sentiment_score * 100)}
              <span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>/100</span>
            </div>
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>News Sentiment:</div>
              <small style={{ color: 'var(--text-muted)' }}>{sentiment.news_sentiment}</small>
            </div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--accent-green)' }}>
            <small style={{ color: 'var(--accent-green)', fontWeight: 'bold' }}>🎓 Market Perception:</small>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>{sentiment.beginner_summary}</p>
          </div>
        </div>

        {/* Agent 4 & 5: Risk & Execution Preview */}
        <div className="glass-card">
          <div className="badge badge-amber" style={{ marginBottom: '12px' }}>🛡️ Risk & Execution Safety</div>
          <div style={{ marginBottom: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Recommended Position Size:</span>
              <strong style={{ color: 'var(--accent-cyan)' }}>{risk.recommended_shares} shares (${risk.total_position_value})</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Stop Loss Protection:</span>
              <strong style={{ color: 'var(--accent-red)' }}>${risk.stop_loss_price}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Take Profit Target:</span>
              <strong style={{ color: 'var(--accent-green)' }}>${risk.take_profit_price}</strong>
            </div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--accent-amber)' }}>
            <small style={{ color: 'var(--accent-amber)', fontWeight: 'bold' }}>🎓 Risk Rule:</small>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>{risk.beginner_explanation}</p>
          </div>
        </div>

      </div>

      {/* PORTFOLIO UPSKILLING SECTION: Beginner to Intermediate Stepper */}
      {upskill_tips && (
        <div className="upskill-container">
          <div className="upskill-header">
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '1.4rem' }}>⚡</span>
                <h2 style={{ fontSize: '1.4rem', color: 'var(--accent-cyan)' }}>
                  Portfolio Upskill Path: {upskill_tips.stock_ticker}
                </h2>
                <span className="badge badge-purple">{upskill_tips.upskill_level}</span>
                {upskill_tips.beta_estimate && (
                  <span className="badge badge-cyan">Beta ~{upskill_tips.beta_estimate}</span>
                )}
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginTop: '4px' }}>
                Step-by-step guidance tailored to upskill your trading strategy from basic technicals to intermediate portfolio construction.
              </p>
            </div>

            <div style={{ minWidth: '220px', textAlign: 'right' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '6px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Analysis Mastery:</span>
                <strong style={{ color: 'var(--accent-green)' }}>{progressPct}% ({completedCount}/{totalCount})</strong>
              </div>
              <div className="xp-progress-bar">
                <div className="xp-progress-fill" style={{ width: `${progressPct}%` }}></div>
              </div>
            </div>
          </div>

          <div className="upskill-steps-grid">
            
            {/* Step 1: Foundation */}
            <div className="upskill-step-card" style={{ borderLeft: '3px solid var(--accent-blue)' }}>
              <span className="badge badge-cyan" style={{ marginBottom: '8px' }}>
                {upskill_tips.step_1.badge}
              </span>
              <h4 style={{ color: 'var(--text-main)', marginBottom: '6px' }}>
                {upskill_tips.step_1.title}
              </h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                {upskill_tips.step_1.description}
              </p>
            </div>

            {/* Step 2: Intermediate Technical & Valuation Upgrade */}
            <div className="upskill-step-card" style={{ borderLeft: '3px solid var(--accent-purple)' }}>
              <span className="badge badge-purple" style={{ marginBottom: '8px' }}>
                {upskill_tips.step_2.badge}
              </span>
              <h4 style={{ color: 'var(--text-main)', marginBottom: '6px' }}>
                {upskill_tips.step_2.title}
              </h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                {upskill_tips.step_2.description}
              </p>
            </div>

            {/* Step 3: Portfolio Hedging & Sector Correlation */}
            <div className="upskill-step-card" style={{ borderLeft: '3px solid var(--accent-amber)' }}>
              <span className="badge badge-amber" style={{ marginBottom: '8px' }}>
                {upskill_tips.step_3.badge}
              </span>
              <h4 style={{ color: 'var(--text-main)', marginBottom: '6px' }}>
                {upskill_tips.step_3.title}
              </h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                {upskill_tips.step_3.description}
              </p>
            </div>

          </div>

          {/* Step 4: Interactive Pre-Trade Upskill Checklist */}
          <div style={{ marginTop: '20px', background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="badge badge-green">Step 4: Interactive Checklist</span>
                <h4 style={{ color: 'var(--accent-green)', fontSize: '0.95rem' }}>
                  Pre-Trade Execution Verification (+50 XP per item)
                </h4>
              </div>
              <small style={{ color: 'var(--text-muted)' }}>Click items as you review them</small>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '10px' }}>
              {checklist.map((item) => {
                const isChecked = !!checkedItems[item.id];
                return (
                  <div
                    key={item.id}
                    className={`checklist-item ${isChecked ? 'checked' : ''}`}
                    onClick={() => toggleCheck(item.id)}
                  >
                    <input
                      type="checkbox"
                      checked={isChecked}
                      onChange={() => {}} // handled by div container
                      style={{ marginTop: '3px', cursor: 'pointer' }}
                    />
                    <span style={{ fontSize: '0.85rem', color: isChecked ? 'var(--text-main)' : 'var(--text-muted)', textDecoration: isChecked ? 'none' : 'none' }}>
                      {item.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}

function int(val) {
  return Math.round(val);
}
