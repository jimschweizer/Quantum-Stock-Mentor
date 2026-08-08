import React, { useState } from 'react';

const BEGINNER_LESSONS = [
  {
    id: 'rsi',
    level: 'Beginner',
    title: '1. What is RSI (Relative Strength Index)?',
    badge: 'Technical Analysis',
    summary: 'RSI is a momentum metric measuring speed & change of price movements on a 0 to 100 scale.',
    content: (
      <div>
        <p><strong>The Golden Rules of RSI:</strong></p>
        <ul style={{ paddingLeft: '20px', marginTop: '8px', lineHeight: '1.6' }}>
          <li><strong style={{ color: 'var(--accent-red)' }}>RSI &gt; 70 (Overbought):</strong> The stock has climbed rapidly and may be due for a short-term pullback.</li>
          <li><strong style={{ color: 'var(--accent-green)' }}>RSI &lt; 30 (Oversold):</strong> The stock has been beaten down heavily and may be near a bottom or rebound zone.</li>
          <li><strong style={{ color: 'var(--accent-cyan)' }}>RSI 45 - 65 (Bullish Trend):</strong> Healthy momentum where buyers maintain control without panic buying.</li>
        </ul>
      </div>
    )
  },
  {
    id: 'risk',
    level: 'Beginner',
    title: '2. The 1-2% Portfolio Risk Rule',
    badge: 'Risk Management',
    summary: 'The single most important rule used by professional quant managers to avoid blowing up their account.',
    content: (
      <div>
        <p><strong>Never risk more than 1% to 2% of your total account on any single trade idea.</strong></p>
        <p style={{ marginTop: '8px', lineHeight: '1.6' }}>
          If you have a $10,000 portfolio, your maximum risk per trade should be strictly $100 to $200. This is NOT your total position size—it is the dollar amount lost <em>if your stop loss gets hit</em>.
        </p>
      </div>
    )
  },
  {
    id: 'stop_loss',
    level: 'Beginner',
    title: '3. Stop Loss vs. Take Profit Targets',
    badge: 'Order Execution',
    summary: 'Automated price triggers that remove emotion from your trading strategy.',
    content: (
      <div>
        <p><strong>Stop Loss:</strong> An automated exit order placed below your entry price. If the stock falls to this price, your broker sells automatically to cap your maximum loss.</p>
        <p style={{ marginTop: '8px' }}><strong>Take Profit:</strong> An exit order set above your entry price to automatically lock in profits when your price target is achieved.</p>
      </div>
    )
  },
  {
    id: 'prairie',
    level: 'Beginner',
    title: '4. Why the Midwest Quantum Prairie Matters',
    badge: 'Market Thesis',
    summary: 'The Great Lakes region is building the physical infrastructure backbone of commercial quantum computing.',
    content: (
      <div>
        <p style={{ lineHeight: '1.6' }}>
          The <strong>Quantum Prairie</strong> links world-leading research universities (UChicago, UIUC, Northwestern, Purdue) with DOE National Laboratories (Argonne & Fermilab), state-backed microelectronic parks (IQMP), and secure quantum-safe optical fiber networks (Quantum Corridor).
        </p>
        <p style={{ marginTop: '8px' }}>
          Major tech giants (IBM, Nvidia, Microsoft, Google) partner heavily with this ecosystem to build utility-scale quantum systems.
        </p>
      </div>
    )
  }
];

const INTERMEDIATE_LESSONS = [
  {
    id: 'beta_hedging',
    level: 'Intermediate',
    title: '5. Beta & Volatility Hedging (Pure-Play vs Prairie Anchor)',
    badge: 'Intermediate Portfolio',
    summary: 'Balance high-beta speculative pure plays (IONQ, QBTS) with low-beta Prairie anchors (IBM, NVDA).',
    content: (
      <div>
        <p style={{ lineHeight: '1.6' }}>
          <strong>Understanding Beta (β):</strong> Beta measures a stock's volatility relative to the broader market (S&P 500).
        </p>
        <ul style={{ paddingLeft: '20px', marginTop: '8px', lineHeight: '1.6' }}>
          <li><strong style={{ color: 'var(--accent-purple)' }}>Pure-Play Quantum (Beta 2.0+):</strong> Moves twice as fast as the market. Massive upside potential, but vulnerable to heavy pullbacks.</li>
          <li><strong style={{ color: 'var(--accent-cyan)' }}>Prairie Giants (Beta 0.85 - 1.3):</strong> Steady institutional capital anchors that protect portfolio cash reserves.</li>
        </ul>
        <div style={{ background: 'rgba(0,243,255,0.05)', padding: '12px', borderRadius: '8px', marginTop: '12px', borderLeft: '3px solid var(--accent-cyan)' }}>
          <strong>Intermediate Tip:</strong> Structure a 70/30 barbell portfolio—70% in Prairie Tech Anchors (NVDA, IBM, MSFT) and 30% in high-upside Pure Plays (IONQ, RGTI, QBTS).
        </div>
      </div>
    )
  },
  {
    id: 'rsi_divergence',
    level: 'Intermediate',
    title: '6. Spotting RSI Divergence & False Breakouts',
    badge: 'Intermediate Technicals',
    summary: 'Move beyond basic RSI thresholds by analyzing momentum divergence against price action.',
    content: (
      <div>
        <p style={{ lineHeight: '1.6' }}>
          As an intermediate trader, static RSI &gt; 70 or &lt; 30 signals are not enough. High-momentum stocks often stay overbought during strong bull runs!
        </p>
        <p style={{ marginTop: '8px', lineHeight: '1.6' }}>
          <strong style={{ color: 'var(--accent-amber)' }}>Bearish Divergence:</strong> Price makes a NEW HIGH, but RSI makes a LOWER HIGH. This reveals buying fatigue—a major warning sign of an impending pullback.
        </p>
        <p style={{ marginTop: '8px', lineHeight: '1.6' }}>
          <strong style={{ color: 'var(--accent-green)' }}>Bullish Divergence:</strong> Price makes a NEW LOW, but RSI makes a HIGHER LOW. This indicates selling pressure is fading and accumulation is taking place.
        </p>
      </div>
    )
  },
  {
    id: 'atr_stop_loss',
    level: 'Intermediate',
    title: '7. ATR Volatility-Adjusted Stop Loss Sizing',
    badge: 'Intermediate Risk',
    summary: 'Replace rigid 5% stop-losses with Average True Range (ATR) dynamic stop loss placement.',
    content: (
      <div>
        <p style={{ lineHeight: '1.6' }}>
          Rigid percentage stop-losses (e.g. fixed 5%) often fail on high-volatility quantum stocks because normal daily volatility triggers accidental stop-outs.
        </p>
        <p style={{ marginTop: '8px', lineHeight: '1.6' }}>
          <strong>The ATR Formula:</strong> Set Stop Loss at <code>Entry Price - (2 × ATR)</code>.
        </p>
        <p style={{ marginTop: '8px', lineHeight: '1.6', color: 'var(--text-muted)' }}>
          This gives volatile stocks (like RGTI or QBTS) enough room to breathe while enforcing a mathematical risk cap!
        </p>
      </div>
    )
  }
];

export default function TradingAcademy() {
  const [activeTab, setActiveTab] = useState('intermediate'); // 'beginner' or 'intermediate'
  const [activeLesson, setActiveLesson] = useState('beta_hedging');

  const currentLessons = activeTab === 'beginner' ? BEGINNER_LESSONS : INTERMEDIATE_LESSONS;
  const lessonObj = currentLessons.find(l => l.id === activeLesson) || currentLessons[0];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <h1 style={{ fontSize: '2rem', background: 'var(--gradient-quantum)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: '8px' }}>
              🎓 Stock Portfolio Trading Academy
            </h1>
            <p style={{ color: 'var(--text-muted)' }}>
              Upskill step-by-step from beginner technicals to intermediate quant portfolio strategies.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              className={`btn-secondary ${activeTab === 'beginner' ? 'active' : ''}`}
              onClick={() => { setActiveTab('beginner'); setActiveLesson(BEGINNER_LESSONS[0].id); }}
              style={{ border: activeTab === 'beginner' ? '1px solid var(--accent-cyan)' : '1px solid var(--border-color)', background: activeTab === 'beginner' ? 'rgba(0,243,255,0.1)' : 'transparent' }}
            >
              🌱 Beginner Foundations
            </button>
            <button
              className={`btn-secondary ${activeTab === 'intermediate' ? 'active' : ''}`}
              onClick={() => { setActiveTab('intermediate'); setActiveLesson(INTERMEDIATE_LESSONS[0].id); }}
              style={{ border: activeTab === 'intermediate' ? '1px solid var(--accent-purple)' : '1px solid var(--border-color)', background: activeTab === 'intermediate' ? 'rgba(168,85,247,0.1)' : 'transparent' }}
            >
              ⚡ Intermediate Mastery
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-grid" style={{ padding: 0 }}>
        {/* Lesson Selector */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {currentLessons.map((les) => {
            const isSelected = activeLesson === les.id;
            return (
              <div
                key={les.id}
                className={`glass-card ${isSelected ? 'active' : ''}`}
                onClick={() => setActiveLesson(les.id)}
                style={{
                  cursor: 'pointer',
                  border: isSelected ? '1px solid var(--accent-cyan)' : '1px solid var(--border-color)',
                  background: isSelected ? 'rgba(0, 243, 255, 0.05)' : 'var(--bg-card)'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="badge badge-purple" style={{ marginBottom: '6px' }}>{les.badge}</span>
                  <span className="badge badge-cyan">{les.level}</span>
                </div>
                <h3 style={{ color: 'var(--text-main)', fontSize: '1.05rem', marginBottom: '4px' }}>{les.title}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>{les.summary}</p>
              </div>
            );
          })}
        </div>

        {/* Lesson Content View */}
        <div className="glass-card" style={{ borderLeft: '4px solid var(--accent-cyan)' }}>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
            <span className="badge badge-cyan">{lessonObj.badge}</span>
            <span className="badge badge-purple">{lessonObj.level} Level</span>
          </div>
          <h2 style={{ color: 'var(--accent-cyan)', marginBottom: '16px' }}>{lessonObj.title}</h2>
          <div style={{ fontSize: '1rem', color: 'var(--text-main)', lineHeight: '1.7' }}>
            {lessonObj.content}
          </div>
        </div>
      </div>
    </div>
  );
}
