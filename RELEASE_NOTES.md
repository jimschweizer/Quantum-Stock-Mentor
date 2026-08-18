# 🚀 Quantum-Stock-Mentor v0.1-beta — Initial Beta Release

Welcome to the initial beta release of **Quantum-Stock-Mentor**! This platform is an educational, multi-agent AI quantitative stock picking, risk management, and portfolio upskilling dashboard designed to guide beginner traders into intermediate quantitative portfolio strategies.

---

## ⚡ What's New in v0.1-beta

### 🎓 1. Stepped Portfolio Upskilling Engine (Beginner ➔ Intermediate)
- **4-Step Progressive Improvement Tips**: Every stock pick provides tailored skill-up guidance:
  - **Step 1 (Beginner Foundation)**: RSI baseline momentum & single-trade capital risk caps.
  - **Step 2 (Intermediate Technical Upgrade)**: Beta ($\beta$) scaling, RSI divergence signals, and volatility-adjusted stop losses.
  - **Step 3 (Portfolio Hedging)**: Barbell portfolio strategy pairing high-upside Pure Plays with low-beta Prairie Anchors.
  - **Step 4 (Pre-Trade Checklist)**: Interactive verification checklist (+50 XP per item) with live analysis mastery tracking.
- **Intermediate Trading Academy**: Guided lesson tracks on Beta & Volatility Hedging, RSI Divergence, and ATR Dynamic Stop-Loss Sizing.
- **Risk Upskill Spotlight Widget**: Interactive comparison contrasting naive fixed position sizing against quant volatility-adjusted position sizing.

### 🤖 2. 5-Agent Swarm Intelligence Pipeline
- **👑 Trading Director**: Formulates buy/hold/sell investment theses using live **OpenAI GPT-4o**, **Anthropic Claude 3.5 Sonnet**, or a local fallback synthesis engine.
- **📊 Quant Analyst**: Computes 14-day RSI, 20-day SMA, Volatility (% std dev), Probability Scores, and Pivot/Support/Resistance key levels.
- **🌐 Sentiment Agent**: Evaluates news media, retail community, and institutional analyst sentiment (0-100 score).
- **🛡️ Risk Manager**: Enforces Wall Street's **1-2% Portfolio Risk Rule**, dynamic position sizing, and maximum drawdown caps.
- **🎫 Execution Agent**: Generates structured paper trading limit order execution tickets.

### 🌾 3. Midwest "Quantum Prairie" Ecosystem Integration
- **Pure-Play Pioneers**: `IONQ` (IonQ Inc.), `RGTI` (Rigetti), `QBTS` (D-Wave), `QUBT` (Quantum Computing Inc.).
- **Quantum Prairie Giants**: `IBM` (CQE founding partner), `NVDA` (cuQuantum & IQMP partner), `MSFT` (Azure Quantum), `GOOGL` (UChicago partner).
- **Infrastructure Spotlight**: Deep-dive metadata covering the Illinois Quantum & Microelectronics Park (IQMP), Chicago Quantum Exchange (CQE), Argonne National Lab, Fermilab, and the 400 Gbps interstate Quantum Corridor fiber network.

### 🎨 4. Glassmorphic Web App & Offline Architecture
- Built with **React 19**, **Vite 8**, and a **Vanilla CSS Glassmorphism Design System**.
- Zero-dependency Python REST API backend designed for native local execution across PC, Android, and Mac environments.

---

## 🛠️ Quickstart

```powershell
# 1. Start Backend API (Port 8000)
python "Sovereign Code/backend/app.py"

# 2. Start Frontend Dev Server (Port 5173) — npm or npx
cd "Sovereign Code/frontend"
npm install        # one-time per checkout (npx still needs local node_modules)
npm run dev        # npm form
# npx form (runs the same local Vite): npx vite
# NOTE: `npx --yes vite@8` alone fails on a fresh checkout — vite.config.js
# imports 'vite' + '@vitejs/plugin-react' from local node_modules.
```

---

*Disclaimer: Quantum-Stock-Mentor is designed strictly for educational and simulation purposes. Stock trading involves risk of financial loss.*
