# ⚛️ RJ-Stock: AI Quantum Stock Picker, Risk Manager & Discovery App

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/)
[![React 19](https://img.shields.io/badge/react-19.0.0-61dafb.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/vite-8.2.1-646cff.svg)](https://vitejs.dev/)
[![OpenAI GPT-4o](https://img.shields.io/badge/AI-OpenAI_GPT--4o-green.svg)](https://openai.com/)
[![Anthropic Claude](https://img.shields.io/badge/AI-Claude_3.5_Sonnet-purple.svg)](https://anthropic.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**RJ-Stock** is an educational, multi-agent AI quantitative stock picking, risk management, and portfolio upskilling platform. Built specifically for beginners looking to elevate their stock trading skills to intermediate levels while exploring high-growth technological sectors, the platform spotlights **Quantum Computing** stocks and the emerging **Midwest Quantum Prairie** technology corridor across Illinois and Indiana.

---

## 🚀 Key Features

- ⚡ **Portfolio Upskilling Engine (Beginner ➔ Intermediate)**:
  - **4-Step Progressive Improvement Tips**: Tailored guidance for *every stock pick* covering Baseline Metrics, Intermediate Technicals/Valuation, Portfolio Hedging, and Execution Discipline.
  - **Multi-Horizon Trend Learning Analytics (1D, 7D, 30D)**: Real-time 1-Day (Daily Noise), 7-Day (Weekly Swing), and 30-Day (Monthly Baseline Anchor) price trends paired with a Multi-Timeframe Alignment Score (0-100%) to educate traders on avoiding single-day noise traps.
  - **Interactive Pre-Trade Checklist**: Actionable pre-order verification steps that reward +50 XP per item with live analysis progress tracking.
  - **Intermediate Trading Academy Track**: Deep dives into Beta ($\beta$) & Volatility Hedging, RSI Divergence & False Breakouts, and ATR Dynamic Stop-Loss Sizing.
  - **Risk Upskill Spotlight Widget**: Interactive comparison contrasting naive fixed position sizing against quant volatility-adjusted position sizing.

- 🤖 **5-Agent Swarm Intelligence**:
  1. 👑 **Trading Director**: Synthesizes market data, technical scores, and news sentiment to generate buy/hold/sell investment theses using live **OpenAI GPT-4o** or **Anthropic Claude 3.5 Sonnet**.
  2. 📊 **Quant Analyst & Multi-Horizon Trend Engine**: Calculates Relative Strength Index (RSI), 1-Day, 7-Day, and 30-Day Simple Moving Averages (SMA), Volatility, Multi-Timeframe Confluence, Probability Scores, and Pivot/Support/Resistance levels.
  3. 🌐 **Sentiment Agent**: Gauges news media, retail community, and institutional analyst sentiment (0 to 100 scale).
  4. 🛡️ **Risk Manager**: Enforces Wall Street's **1-2% Portfolio Risk Rule**, dynamic position sizing, maximum drawdown estimation, and stop-loss placement.
  5. 🎫 **Execution Agent**: Formats automated paper trading limit order tickets with protective safety nets.

- 🌾 **Midwest "Quantum Prairie" Spotlight**:
  - **Pure-Play Quantum Stocks**: `IONQ` (IonQ Inc.), `RGTI` (Rigetti Computing), `QBTS` (D-Wave Quantum), `QUBT` (Quantum Computing Inc.).
  - **Quantum Prairie & Tech Giants**: `IBM` (Chicago Quantum Exchange founding partner), `NVDA` (cuQuantum & IQMP partner), `MSFT` (Azure Quantum), `GOOGL` (Google Quantum AI).
  - **Regional Anchor Deep-Dive**: Spotlights the Illinois Quantum & Microelectronics Park (IQMP), Chicago Quantum Exchange (CQE), interstate optical Quantum Corridor network, UChicago, Argonne National Lab, and Fermilab.

- 💎 **Glassmorphic Discovery Web App**:
  - Interactive ticker feed and real-time stock switching.
  - Interactive Position Size & Stop-Loss Calculator with adjustable portfolio capital ($1k-$100k) and risk tolerance sliders.
  - Paper Trading Order Execution Simulator.
  - Beginner & Intermediate Trading Academy with guided lesson tracks.

---

## 📁 Repository Structure

All generated code is organized under `Sovereign Code/`:

```
RJ-Stock/
├── assets/                       # Legacy prompt templates & worker prototypes
│   ├── prompts.py                # Agent prompt definitions
│   └── workers.py                # Early agent worker definitions
├── Sovereign Code/
│   ├── KNOWLEDGE_GRAPH.md        # System architecture, data flow & domain Knowledge Graph
│   ├── backend/                  # Python REST API & Multi-Agent Swarm Core
│   │   ├── app.py                # Zero-dependency Python HTTP server (Port 8000)
│   │   ├── agents.py             # 5-Agent Pipeline with OpenAI & Anthropic API support
│   │   ├── upskill_engine.py     # 4-Step Stock Pick Portfolio Upskilling Engine
│   │   ├── quant_engine.py       # RSI, SMA, Volatility & Support/Resistance algorithms
│   │   ├── risk_engine.py        # Position sizing & Stop Loss math engine
│   │   ├── quantum_prairie.py    # Midwest Quantum ecosystem knowledge base
│   │   ├── config.py             # Stock universe definitions & ticker metadata
│   │   └── test_backend.py       # Pipeline verification script
│   └── frontend/                 # Vite + React Glassmorphic UI Dashboard
│       ├── src/
│       │   ├── components/
│       │   │   ├── TickerBar.jsx         # Live stock ticker feed
│       │   │   ├── StockPicker.jsx       # 5-Agent Analysis & Stepped Upskill Path
│       │   │   ├── QuantRiskManager.jsx  # Interactive risk & position sizing calculator
│       │   │   ├── QuantumPrairieHub.jsx # Midwest Quantum Prairie spotlight
│       │   │   ├── TradeSimulator.jsx    # Simulated paper order ticket execution
│       │   │   └── TradingAcademy.jsx    # Beginner & Intermediate trading lessons
│       │   ├── App.jsx
│       │   └── index.css                 # Dark-mode glassmorphism design system
│       ├── package.json
│       └── vite.config.js
├── README.md                     # GitHub documentation
└── GEMINI.md                     # Antigravity Agent pairing history & guidelines
```

---

## ⚡ Quickstart & Installation

### Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### 1. Environment Setup
Create or update your `.env` file in the root directory:
```env
OPENAI_API_KEY="your-openai-api-key"
# ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 2. Start the Backend API Server
```powershell
python "Sovereign Code/backend/app.py"
```
*Server starts on `http://localhost:8000`*

### 3. Start the Frontend Dashboard
```powershell
cd "Sovereign Code/frontend"
npm install
npm run dev
```
*Open `http://localhost:5173/` in your browser.*

---

## 🎓 Portfolio Trading Skills Covered

1. **Relative Strength Index (RSI)**:
   - `RSI > 70`: Overbought (potential pull-back ahead).
   - `RSI < 30`: Oversold (potential bounce opportunity).
   - `RSI 45 - 65`: Healthy momentum corridor.

2. **The 1-2% Portfolio Risk Rule**:
   - Never risk more than 1% to 2% of total account equity on a single trade.
   - Example: On a $10,000 account, maximum dollar risk per trade is strictly $200.

3. **Beta ($\beta$) & Volatility Hedging**:
   - Pair speculative pure-play quantum stocks ($\beta > 2.0$) with low-beta Prairie anchors (IBM, NVDA) to manage portfolio standard deviation.

4. **ATR Volatility-Adjusted Stop-Loss Sizing**:
   - Calculate stop loss distance dynamically using Average True Range to prevent premature stop-outs during market noise.

---

## ⚠️ Disclaimer

*RJ-Stock is designed strictly for educational and simulation purposes. Stock trading involves substantial risk of loss and is not suitable for every investor. Always conduct independent due diligence before making financial decisions.*
