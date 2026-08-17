import React, { useState, useEffect } from 'react';
import TickerBar from './components/TickerBar';
import StockPicker from './components/StockPicker';
import QuantRiskManager from './components/QuantRiskManager';
import QuantumPrairieHub from './components/QuantumPrairieHub';
import TradeSimulator from './components/TradeSimulator';
import TradingAcademy from './components/TradingAcademy';

// Fallback universe if backend server is starting
const DEFAULT_STOCKS = {
  pure_play: [
    { ticker: "IONQ", name: "IonQ Inc.", sector: "Quantum Hardware", price: 14.85, description: "Leading trapped-ion quantum computing developer." },
    { ticker: "RGTI", name: "Rigetti Computing", sector: "Superconducting", price: 2.15, description: "Superconducting quantum processors." },
    { ticker: "QBTS", name: "D-Wave Quantum", sector: "Quantum Annealing", price: 1.95, description: "Quantum annealing systems for optimization." },
    { ticker: "QUBT", name: "Quantum Computing Inc.", sector: "Photonic Quantum", price: 4.10, description: "Dirac-3 photonic quantum system deployer." }
  ],
  prairie_giants: [
    { ticker: "IBM", name: "IBM Corp", sector: "Enterprise Tech", price: 204.50, description: "Founding member of Chicago Quantum Exchange.", prairie_role: "Chicago Quantum Exchange founding partner" },
    { ticker: "NVDA", name: "NVIDIA Corp", sector: "Accelerated Compute", price: 128.40, description: "cuQuantum SDK & IQMP compute provider.", prairie_role: "Midwest quantum simulation partner" },
    { ticker: "MSFT", name: "Microsoft Corp", sector: "Cloud & Quantum", price: 448.20, description: "Azure Quantum cloud platform.", prairie_role: "Midwest cloud infrastructure partner" },
    { ticker: "GOOGL", name: "Alphabet Inc.", sector: "Quantum AI", price: 178.60, description: "Sycamore processor & UChicago lab research.", prairie_role: "Research partner with UChicago" }
  ]
};

export default function App() {
  const [activeTab, setActiveTab] = useState('picker'); // 'picker', 'risk', 'prairie', 'simulator', 'academy'
  const [selectedTicker, setSelectedTicker] = useState('IONQ');
  const [stocks, setStocks] = useState(DEFAULT_STOCKS);
  const [analysis, setAnalysis] = useState(null);
  const [prairieData, setPrairieData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userXP, setUserXP] = useState(150); // XP points for completing upskill checklists
  const [dataFreshness, setDataFreshness] = useState({ source: 'simulated', lastUpdated: null, stale: false });

  // Fetch stock universe & Prairie data on mount
  useEffect(() => {
    fetch('http://localhost:8000/api/stocks')
      .then(res => res.json())
      .then(data => setStocks(data))
      .catch(() => setStocks(DEFAULT_STOCKS));

    fetch('http://localhost:8000/api/quantum-prairie')
      .then(res => res.json())
      .then(data => setPrairieData(data))
      .catch(() => {
        setPrairieData({
          title: "The Quantum Prairie (Midwest Quantum Hub)",
          region: "Illinois, Indiana, Wisconsin & Great Lakes Region",
          overview: "Premier quantum research and commercialization corridor in the Midwest.",
          key_anchors: [
            { name: "Illinois Quantum & Microelectronics Park (IQMP)", location: "Chicago, IL", type: "Quantum Park", highlights: "Multi-billion dollar park anchored by PsiQuantum." },
            { name: "Chicago Quantum Exchange (CQE)", location: "Chicago, IL", type: "Consortium", highlights: "Hub connecting UChicago, Argonne, Fermilab, and IBM." },
            { name: "Quantum Corridor", location: "IL to IN", type: "Optical Network", highlights: "Commercial 400 Gbps quantum-safe optical network with QUBT." }
          ],
          key_companies: [
            { name: "PsiQuantum", status: "Private Anchor", focus: "Photonic quantum computer at IQMP." },
            { name: "Infleqtion", status: "Publicly Listed", focus: "Neutral-atom quantum sensing." },
            { name: "Quantum Computing Inc. (QUBT)", status: "Public (NASDAQ)", focus: "Dirac-3 photonic quantum system." }
          ]
        });
      });
  }, []);

  const handleCompleteCheckitem = (points) => {
    setUserXP(prev => prev + points);
  };

  // Fetch multi-agent analysis whenever selectedTicker changes
  const runAgentAnalysis = (ticker) => {
    setLoading(true);
    fetch(`http://localhost:8000/api/analyze/${ticker}`)
      .then(res => res.json())
      .then(data => {
        setAnalysis(data);
        setDataFreshness({
          source: data.data_source || 'simulated',
          lastUpdated: data.last_updated || null,
          stale: !!data.data_stale
        });
        setLoading(false);
      })
      .catch(() => {
        // Client fallback simulator if API is starting
        const all = [...stocks.pure_play, ...stocks.prairie_giants];
        const stockInfo = all.find(s => s.ticker === ticker) || { ticker, name: ticker, price: 15.0, description: "Quantum Tech" };
        const stopLoss = (stockInfo.price * 0.93).toFixed(2);
        setAnalysis({
          ticker: ticker,
          stock_info: stockInfo,
          data_source: 'simulated',
          last_updated: null,
          director: {
            agent_name: "Trading-Director",
            recommendation: "BUY (Growth Accumulation)",
            market_thesis: `Thesis for ${ticker}: Positioned strongly in quantum tech momentum with strong Midwest partner backing.`,
            beginner_summary: `The Director ranks ${ticker} as a BUY based on technical strength and regional Prairie integration.`
          },
          quant: {
            rsi: 54.2,
            sma7: (stockInfo.price * 0.98).toFixed(2),
            sma20: (stockInfo.price * 0.96).toFixed(2),
            sma30: (stockInfo.price * 0.94).toFixed(2),
            volatility_pct: 4.8,
            probability_score: 0.78,
            key_levels: {
              pivot: stockInfo.price.toFixed(2),
              support: (stockInfo.price * 0.92).toFixed(2),
              resistance: (stockInfo.price * 1.08).toFixed(2)
            },
            trends: {
              day_1: { change_pct: 1.45, direction: "UP" },
              day_7: { change_pct: 3.20, direction: "UP" },
              day_30: { change_pct: 8.75, direction: "UP" },
              alignment: "Strong Bullish Confluence (1D + 7D + 30D Aligned)",
              alignment_score: 95
            },
            beginner_note: `RSI is healthy at 54.2, showing steady momentum without being overbought.`
          },
          sentiment: {
            sentiment_score: 0.85,
            news_sentiment: "Very Positive (Midwest Quantum Corridor expansion news)",
            beginner_summary: "Market sentiment is 85/100, supported by news coverage and institutional interest."
          },
          risk: {
            recommended_shares: Math.floor(200 / (stockInfo.price * 0.05)),
            total_position_value: (Math.floor(200 / (stockInfo.price * 0.05)) * stockInfo.price).toFixed(2),
            stop_loss_price: stopLoss,
            take_profit_price: (stockInfo.price * 1.15).toFixed(2),
            beginner_explanation: `Risk is capped at $200 with a Stop Loss set at $${stopLoss}.`
          },
          execution: {
            ticker: ticker,
            action: "BUY_LIMIT",
            order_type: "Limit Order",
            quantity: Math.floor(200 / (stockInfo.price * 0.05)),
            entry_price: (stockInfo.price * 0.995).toFixed(2),
            estimated_total: (Math.floor(200 / (stockInfo.price * 0.05)) * stockInfo.price * 0.995).toFixed(2),
            stop_loss: stopLoss,
            take_profit: (stockInfo.price * 1.15).toFixed(2)
          },
          upskill_tips: {
            stock_ticker: ticker,
            beta_estimate: ticker === 'IBM' ? 0.85 : 2.15,
            upskill_level: "Beginner ➔ Intermediate",
            step_1: {
              title: "Step 1: Baseline Metric Foundation (Beginner)",
              description: `For ${ticker}, your anchor metrics are RSI (54.2) and current price ($${stockInfo.price.toFixed(2)}). Keep single-trade risk under 2%.`,
              badge: "Beginner Baseline"
            },
            step_2: {
              title: "Step 2: Technical & Valuation Upgrade (Intermediate)",
              description: `Intermediate Upgrade: Evaluate RSI Divergence and scale Stop-Loss based on Volatility (4.8%) rather than static percentage points.`,
              badge: "Intermediate Tech"
            },
            step_3: {
              title: "Step 3: Portfolio Hedging & Sector Correlation",
              description: `Portfolio Strategy: Pair speculative pure-play quantum stocks with Prairie Tech Giants (NVDA/IBM) to stabilize portfolio standard deviation.`,
              badge: "Portfolio Strategy"
            },
            step_4: {
              title: "Step 4: Actionable Pre-Trade Execution Checklist",
              badge: "Execution Discipline",
              checklist: [
                { id: "risk_rule", label: "Verify maximum risk per trade does not exceed 1-2% of total portfolio value." },
                { id: "rsi_check", label: "Confirm RSI (54.2) is in healthy buy territory (<70)." },
                { id: "stop_loss_check", label: `Set automated Stop-Loss order at $${stopLoss} to enforce risk discipline.` },
                { id: "ecosystem_check", label: `Verify regional ecosystem integration for ${ticker}.` }
              ]
            }
          }
        });
        setLoading(false);
        setDataFreshness({ source: 'simulated', lastUpdated: null, stale: false });
      });
  };

  // Refresh market data on-demand via Alpha Vantage
  const refreshData = (ticker) => {
    fetch('http://localhost:8000/api/refresh-data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker })
    })
      .then(res => res.json())
      .then(() => runAgentAnalysis(ticker))
      .catch(err => console.warn('Refresh failed, using cached data:', err));
  };

  useEffect(() => {
    runAgentAnalysis(selectedTicker);
  }, [selectedTicker]);

  const currentPrice = analysis?.stock_info?.price || 15.0;
  const userSkillLevel = userXP >= 300 ? "Intermediate Trader (Level 2)" : "Beginner Apprentice (Level 1)";

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Header */}
      <header style={{ padding: '16px 24px', background: 'rgba(10, 12, 22, 0.95)', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '1.6rem' }}>⚛️</span>
          <div>
            <h1 style={{ fontSize: '1.3rem', background: 'var(--gradient-quantum)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', fontWeight: 'bold' }}>
              RJ-Stock AI Platform
            </h1>
            <small style={{ color: 'var(--text-muted)' }}>AI Stock Picker • Quant Risk Manager • Portfolio Upskill Engine</small>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <span className="badge badge-green">⚡ XP: {userXP} PTS</span>
          <span className="badge badge-cyan">{userSkillLevel}</span>
          <span className="badge badge-purple">Midwest Quantum Corridor</span>
        </div>
      </header>

      {/* Live Ticker Bar */}
      <TickerBar stocks={stocks} selectedTicker={selectedTicker} onSelectTicker={setSelectedTicker} />

      {/* Navigation Tabs */}
      <nav className="nav-tabs">
        <button className={`tab-btn ${activeTab === 'picker' ? 'active' : ''}`} onClick={() => setActiveTab('picker')}>
          🤖 AI Stock Picker & Thesis
        </button>
        <button className={`tab-btn ${activeTab === 'risk' ? 'active' : ''}`} onClick={() => setActiveTab('risk')}>
          🛡️ Quant & Risk Manager
        </button>
        <button className={`tab-btn ${activeTab === 'prairie' ? 'active' : ''}`} onClick={() => setActiveTab('prairie')}>
          🌾 Quantum Prairie Spotlight
        </button>
        <button className={`tab-btn ${activeTab === 'simulator' ? 'active' : ''}`} onClick={() => setActiveTab('simulator')}>
          🚀 Trade Order Simulator
        </button>
        <button className={`tab-btn ${activeTab === 'academy' ? 'active' : ''}`} onClick={() => setActiveTab('academy')}>
          🎓 Beginner Trading Academy
        </button>
      </nav>

      {/* Main View Area */}
      <main style={{ flex: 1, padding: '24px', maxWidth: '1400px', margin: '0 auto', width: '100%' }}>
        {activeTab === 'picker' && (
          <StockPicker
            analysis={analysis}
            loading={loading}
            onRunAnalysis={() => runAgentAnalysis(selectedTicker)}
            onRefreshData={() => refreshData(selectedTicker)}
            dataFreshness={dataFreshness}
            userXP={userXP}
            userSkillLevel={userSkillLevel}
            onCompleteCheckitem={handleCompleteCheckitem}
          />
        )}
        {activeTab === 'risk' && (
          <QuantRiskManager
            ticker={selectedTicker}
            price={currentPrice}
          />
        )}
        {activeTab === 'prairie' && (
          <QuantumPrairieHub
            prairieData={prairieData}
          />
        )}
        {activeTab === 'simulator' && (
          <TradeSimulator
            executionOrder={analysis?.execution}
          />
        )}
        {activeTab === 'academy' && (
          <TradingAcademy />
        )}
      </main>

      {/* Footer */}
      <footer style={{ padding: '16px 24px', background: 'rgba(10, 12, 22, 0.95)', borderTop: '1px solid var(--border-color)', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
        RJ-Stock Educational AI Platform • Built for Sovereign Code • Disclaimer: For educational & simulation purposes only.
      </footer>
    </div>
  );
}
