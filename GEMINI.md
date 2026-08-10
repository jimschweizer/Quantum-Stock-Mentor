# GEMINI.md — RJ-Stock Expert-Level System Architecture & Persistent Knowledge

## Overview
This document is the **authoritative expert-level reference** for project **RJ-Stock** (`Quantum-Stock-Mentor`). It records the pair programming collaboration between **Jim Schweizer** (USER) and **Antigravity** (Google DeepMind Agentic AI Coding Assistant), and encodes the complete system architecture, algorithms, API integrations, component tree, design system, domain knowledge, and development conventions so that every future session starts at expert level.

**License**: MIT — Copyright (c) 2026 Jim Schweizer

---

## 🎯 User Intent & Request History

1. **Initial Goal**: Initialize project `RJ-Stock` by reviewing workflows in `assets/` (`prompts.py` and `workers.py`), walk through building an AI Stock picker, risk manager, and dashboard discovery app tailored for beginners learning stock trading, with special focus on Quantum Computing stocks and the Midwest **Quantum Prairie** ecosystem.
2. **Global System Rule Enforced**: Default output directory for all generated files set to `Sovereign Code/`.
3. **Execution Approval**: Implementation plan (`implementation_plan.md`) reviewed and approved by user.
4. **Bug Diagnosis & Fix**: Diagnosed and resolved a runtime `ReferenceError: None is not defined` in `StockPicker.jsx` via Vite dev server log analysis.
5. **API Integrations**: Tested and integrated both **Anthropic Claude 3.5 Sonnet** and **OpenAI GPT-4o** APIs via root `.env` configuration.
6. **Project Shutdown & Documentation**: Controlled shutdown of daemon processes and creation of `README.md` and `GEMINI.md`.
7. **Multi-Horizon Trend Learning Analytics (1D, 7D, 30D)**: Implemented 1-Day (Daily Noise), 7-Day (Weekly Swing), and 30-Day (Monthly Baseline) trend analytics, alignment scoring (0-100%), and interactive UI cards in `StockPicker.jsx`. Committed and pushed to GitHub (`c0a2d0a`).

---

## 📁 Repository Map

```
RJ-Stock/
├── .env                              # API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, WORKSPACE_DIR, WALLET_PRIVATE_KEY)
├── .gitignore                        # Excludes .env, node_modules, __pycache__, dist, logs, .vscode, .idea, .gemini
├── GEMINI.md                         # THIS FILE — Persistent expert-level project knowledge (auto-loaded as workspace rule)
├── README.md                         # GitHub-facing documentation with badges, quickstart, and skill coverage
├── RELEASE_NOTES.md                  # v0.1-beta release notes
├── LICENSE                           # MIT License
├── assets/                           # Legacy prototypes (reference only — NOT the active codebase)
│   ├── prompts.py                    # Original 5 system prompts + 6 dynamic prompt templates (swarms-based)
│   └── workers.py                    # Original swarms Agent declarations (gpt-4.1, gpt-4o-mini models)
├── Sovereign Code/                   # ★ ACTIVE CODEBASE — all new/modified code goes here
│   ├── KNOWLEDGE_GRAPH.md            # Architecture diagrams, ER matrix, upskill path, and domain graph
│   ├── backend/                      # Python REST API & Multi-Agent Swarm Core
│   │   ├── app.py                    # Zero-dependency HTTP server (http.server, Port 8000)
│   │   ├── agents.py                 # 5-Agent Pipeline + OpenAI/Anthropic/Local fallback cascade
│   │   ├── config.py                 # Stock universe definitions (QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS)
│   │   ├── data_fetcher.py           # get_quantum_universe(), get_stock_detail(ticker)
│   │   ├── quant_engine.py           # RSI, SMA, Volatility, Key Levels, Multi-Horizon Trends
│   │   ├── risk_engine.py            # Position sizing, stop-loss, take-profit (1-2% rule)
│   │   ├── upskill_engine.py         # 4-Step progressive trader education + pre-trade checklist
│   │   ├── quantum_prairie.py        # Midwest Quantum ecosystem knowledge base
│   │   └── test_backend.py           # Pipeline verification script
│   └── frontend/                     # Vite + React Glassmorphic UI Dashboard
│       ├── package.json              # React 19.2.8, Vite 8.2.0, oxlint 1.75.0
│       ├── vite.config.js            # @vitejs/plugin-react 6.0.4
│       └── src/
│           ├── App.jsx               # Root shell, state orchestrator, API fetcher, tab router
│           ├── index.css             # Dark-mode glassmorphism design system (CSS custom properties)
│           └── components/
│               ├── TickerBar.jsx     # Horizontal live ticker feed ribbon
│               ├── StockPicker.jsx   # 5-Agent swarm dashboard + upskill stepper + trend grid
│               ├── QuantRiskManager.jsx  # Interactive risk & position sizing calculator
│               ├── QuantumPrairieHub.jsx # Midwest Quantum Prairie spotlight
│               ├── TradeSimulator.jsx    # Paper trade order ticket simulator
│               └── TradingAcademy.jsx    # Beginner & Intermediate lesson curriculum
└── logs/                             # Runtime logs (gitignored)
```

---

## 🏗️ Backend Architecture (`Sovereign Code/backend/`)

### Module Dependency Graph
```
app.py ──imports──▶ agents.py ──imports──▶ config.py
  │                    │                     data_fetcher.py
  │                    ├──imports──▶ quant_engine.py
  │                    ├──imports──▶ risk_engine.py
  │                    └──imports──▶ upskill_engine.py
  └──imports──▶ data_fetcher.py
                quantum_prairie.py
```

### `config.py` — Stock Universe & Ticker Metadata
- **`QUANTUM_PURE_PLAY`**: `List[Dict]` — Pure-play quantum hardware/software stocks
  - `IONQ` ($14.85, "Trapped Ion Quantum Hardware", sector: "Quantum Computing")
  - `RGTI` ($2.15, "Superconducting Quantum Hardware")
  - `QBTS` ($1.95, "Quantum Annealing & Optimization")
  - `QUBT` ($4.10, "Photonic Quantum & Quantum Networks")
- **`QUANTUM_PRAIRIE_GIANTS`**: `List[Dict]` — Midwest ecosystem anchors
  - `IBM` ($204.50, "CQE Founding Partner & Heron Processors")
  - `NVDA` ($128.40, "cuQuantum SDK & IQMP Partner")
  - `MSFT` ($448.20, "Azure Quantum & Topological Qubit Research")
  - `GOOGL` ($178.60, "Sycamore Processor & Quantum AI")
- **`ALL_TICKERS`**: `List[str]` — Combined flat ticker list

### `data_fetcher.py` — Data Access
- `get_quantum_universe() -> Dict[str, List[Dict]]` — Returns `{ pure_play: [...], prairie_giants: [...] }`
- `get_stock_detail(ticker: str) -> Optional[Dict]` — Lookup by ticker symbol

### `quant_engine.py` — Technical Analysis Engine (165 lines)
**Functions:**
- `calculate_rsi(prices, period=14) -> float` — Wilder's smoothed RSI
- `calculate_sma(prices, period=20) -> float` — Simple Moving Average
- `calculate_volatility(prices) -> float` — Percentage standard deviation
- `compute_key_levels(prices) -> Dict[str, float]` — Floor pivot, support, resistance
- `analyze_quant_metrics(ticker, current_price, price_history=None) -> Dict` — Full analysis including multi-horizon trends

**Key Algorithms & Formulas:**

| Algorithm | Formula |
|-----------|---------|
| RSI (Wilder's) | `avg_gain[i] = (avg_gain[i-1] * 13 + gain[i]) / 14`; `RSI = 100 - 100/(1+RS)` |
| SMA-N | `SMA = mean(prices[-N:])` |
| Volatility % | `vol = (stdev(prices) / mean(prices)) * 100` |
| Pivot Point | `P = (High + Low + Close) / 3` |
| Support S1 | `S1 = (2 * P) - High` |
| Resistance R1 | `R1 = (2 * P) - Low` |
| RSI Score | `clamp(1.0 - abs(RSI - 55) / 50.0, 0.1, 1.0)` |
| SMA Bias | `0.65 if price >= SMA_30 else 0.40` |
| Technical Score | `RSI_Score * 0.5 + SMA_Bias * 0.5` |
| Trend Strength | `clamp(price / max(SMA_30, 0.01) * 0.5, 0.2, 1.0)` |
| Probability Score | `Tech * 0.4 + Volume * 0.3 + Trend * 0.3` |

**Multi-Horizon Trend Confluence Scoring:**

| Alignment | Score | Label |
|-----------|-------|-------|
| 3/3 positive | 95 | Strong Bullish Confluence |
| 2/3 positive | 70 | Moderate Bullish Bias |
| 1/3 positive | 45 | Consolidation / Mixed Signals |
| 0/3 positive | 20 | Bearish Pressure Across Timeframes |

**Deterministic Simulation Fallback:** When price history is unavailable (< 15 data points), generates a 30-day random walk seeded with `sum(ord(c) for c in ticker)` for repeatable metrics.

### `risk_engine.py` — Position Sizing & Stop-Loss (56 lines)
**Function:** `evaluate_risk(ticker, current_price, account_size=10000.0, risk_tolerance_pct=2.0, volatility_pct=5.0) -> Dict`

| Calculation | Formula |
|-------------|---------|
| Max Dollar Risk | `account_size * (risk_tolerance_pct / 100)` |
| Stop Loss Distance % | `clamp(volatility_pct / 100 * 1.5, 0.03, 0.12)` |
| Stop Loss Price | `round(price * (1.0 - SL_dist), 2)` |
| Risk Per Share | `price - stop_loss_price` |
| Recommended Shares | `floor(max_dollar_risk / risk_per_share)` (min: 1) |
| Take Profit Price | `round(price + risk_per_share * 2.5, 2)` — **2.5:1 Risk-Reward Ratio** |
| Overall Risk Score | `min(1.0, vol/10*0.5 + allocation/20*0.5)` |

**Beta Profiles:**
- `IBM` → β = 0.85 (Defensive Anchor)
- `NVDA`, `MSFT`, `GOOGL` → β = 1.45 (Growth Heavyweight)
- `IONQ`, `RGTI`, `QBTS`, `QUBT` → β = 2.35 (High-Beta Speculative)

### `upskill_engine.py` — Educational Progression (109 lines)
**Function:** `get_stock_upskill_tips(ticker, stock_info, quant_data, risk_data) -> Dict`

**4-Step Progressive Learning Path:**
1. **Step 1 — Baseline Foundation**: RSI awareness, capital risk caps, stop-loss discipline
2. **Step 2 — Technical Upgrade**: Beta scaling, RSI divergence recognition, ATR stop-loss sizing
3. **Step 3 — Portfolio Hedging**: Barbell strategy (70% anchors / 30% speculative), sector diversification
4. **Step 4 — Pre-Trade Checklist**: Interactive checklist (+50 XP per item), live mastery progress bar

### `quantum_prairie.py` — Midwest Quantum Ecosystem Knowledge Base (77 lines)
**Function:** `get_quantum_prairie_summary() -> Dict`
**Constant:** `QUANTUM_PRAIRIE_INFO: Dict`

**Infrastructure Anchors:**
- **IQMP** (Illinois Quantum & Microelectronics Park) — Chicago, IL
- **CQE** (Chicago Quantum Exchange) — UChicago, UIUC, Northwestern, Argonne, Fermilab, IBM
- **Quantum Corridor** — 400 Gbps quantum-safe optical fiber network (Chicago, IL ↔ Hammond, IN)
- **Argonne National Lab** — Q-NEXT Center
- **Fermilab** — SQMS Center

### `agents.py` — Multi-Agent Orchestration & LLM Integration (349 lines)

**Functions:**
- `load_env_keys() -> Dict[str, Optional[str]]` — Reads from `os.environ` and root `.env` file
- `generate_openai_thesis(ticker_info, quant_data, risk_data) -> Optional[Dict]`
- `generate_claude_thesis(ticker_info, quant_data, risk_data) -> Optional[Dict]`
- `run_trading_director(ticker_info, quant_data, risk_data) -> Dict`
- `run_sentiment_agent(ticker_info) -> Dict`
- `run_execution_agent(ticker, current_price, risk_data) -> Dict`
- `run_full_agent_analysis(ticker, account_size=10000.0, risk_tolerance=2.0) -> Dict`

**LLM API Integration Details:**

| Provider | Endpoint | Model | Key Parameters |
|----------|----------|-------|----------------|
| OpenAI | `POST https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` | `temperature: 0.7`, timeout: 10s |
| Anthropic | `POST https://api.anthropic.com/v1/messages` | `claude-3-5-sonnet-20241022` | `max_tokens: 400`, timeout: 10s |

**Auth Headers:**
- OpenAI: `Authorization: Bearer <OPENAI_API_KEY>`
- Anthropic: `x-api-key: <ANTHROPIC_API_KEY>`, `anthropic-version: 2023-06-01`

**HTTP Client:** Built-in `urllib.request.Request` (zero external dependencies)

**Cascading Fallback Tier:**
1. ✅ Attempt **OpenAI GPT-4o-mini**
2. ⬇️ If missing/quota-exhausted → **Anthropic Claude 3.5 Sonnet**
3. ⬇️ If also unavailable → **Deterministic Local Swarm Engine** (probability scores + ecosystem role)

**Expected LLM JSON Schema:** `{ recommendation, market_thesis, beginner_summary }`

### `app.py` — Zero-Dependency REST API Server (104 lines)
**Class:** `QuantumStockAPIHandler(BaseHTTPRequestHandler)`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stocks` | Returns quantum stock universe |
| GET | `/api/analyze/<ticker>` | Runs full 5-agent swarm pipeline |
| GET | `/api/quantum-prairie` | Returns Quantum Prairie ecosystem data |
| POST | `/api/simulate-trade` | Simulates paper trade execution |
| OPTIONS | `*` | CORS preflight (Access-Control-Allow-Origin: *) |

**Server:** `http.server.HTTPServer` on port `8000`

### Agent Pipeline Execution Order (Sequential)
```
GET /api/analyze/<ticker>
  → 1. Quant-Analyst    (analyze_quant_metrics)     → RSI, SMAs, Volatility, Key Levels, Trends
  → 2. Sentiment-Agent  (run_sentiment_agent)        → Sentiment Score 0-100
  → 3. Risk-Manager     (evaluate_risk)              → Shares, Stop-Loss, Take-Profit
  → 4. Trading-Director (run_trading_director)       → BUY/HOLD/SELL + Thesis (OpenAI → Claude → Local)
  → 5. Execution-Agent  (run_execution_agent)        → Paper Trade Limit Order Ticket
  → 6. Upskill-Engine   (get_stock_upskill_tips)     → 4-Step Education + Checklist
```

---

## 💎 Frontend Architecture (`Sovereign Code/frontend/`)

### Tech Stack
- **React** 19.2.8 (ES Modules)
- **Vite** 8.2.0 with `@vitejs/plugin-react` 6.0.4
- **Linter**: oxlint 1.75.0
- **Styling**: Vanilla CSS (glassmorphism design system)
- **No routing library** — tab-based SPA with `activeTab` state

### Component Tree & Props

| Component | Role | Key Props | State |
|-----------|------|-----------|-------|
| `App.jsx` | Root shell, API fetcher, tab router | — | `activeTab`, `selectedTicker`, `stocks`, `analysis`, `prairieData`, `loading`, `userXP` |
| `TickerBar.jsx` | Horizontal ticker feed ribbon | `stocks`, `selectedTicker`, `onSelectTicker` | Stateless |
| `StockPicker.jsx` | 5-Agent dashboard + upskill stepper | `analysis`, `loading`, `onRunAnalysis`, `userXP`, `userSkillLevel`, `onCompleteCheckitem` | `checkedItems: { [id]: bool }` |
| `QuantRiskManager.jsx` | Interactive risk calculator | `ticker`, `price` | `accountSize` (1K-100K), `riskTolerancePct` (0.5-5%), `volatility` (2-15%) |
| `QuantumPrairieHub.jsx` | Quantum Prairie spotlight | `prairieData` | Stateless |
| `TradeSimulator.jsx` | Paper trade order simulator | `executionOrder`, `onSimulateTrade` | `orders: []`, `loading: bool` |
| `TradingAcademy.jsx` | Educational lesson curriculum | — | `activeTab` ('beginner'/'intermediate'), `activeLesson` |

### Tab Navigation
`activeTab` values: `'picker'` | `'risk'` | `'prairie'` | `'simulator'` | `'academy'`

### API Endpoints Called (with Full Offline Fallback)
Every frontend component includes **100% client-side fallback data** for offline operation:
- `GET http://localhost:8000/api/stocks` → Fallback: `DEFAULT_STOCKS`
- `GET http://localhost:8000/api/quantum-prairie` → Fallback: IQMP, CQE, Quantum Corridor metadata
- `GET http://localhost:8000/api/analyze/{ticker}` → Fallback: Mock 5-agent payload with trends
- `POST http://localhost:8000/api/simulate-trade` → Fallback: Local order ticket `ORD-{ticker}-{timestamp}`

### CSS Design System Tokens (`:root` custom properties)

**Color Palette (Dark Theme):**
| Token | Value | Usage |
|-------|-------|-------|
| `--bg-dark` | `#0a0c16` | Deep space background |
| `--bg-card` | `rgba(18, 22, 41, 0.75)` | Glass card fill |
| `--bg-card-hover` | `rgba(28, 34, 61, 0.85)` | Card hover state |
| `--border-color` | `rgba(255, 255, 255, 0.1)` | Subtle glass borders |
| `--text-main` | `#f1f5f9` | Primary text |
| `--text-muted` | `#94a3b8` | Secondary text |

**Accent Colors:**
| Name | Value | Usage |
|------|-------|-------|
| Cyan | `#00f3ff` | Primary accent, active states |
| Purple | `#a855f7` | Secondary accent, gradients |
| Blue | `#3b82f6` | Info elements |
| Green | `#10b981` | Positive/success states |
| Amber | `#f59e0b` | Warning states |
| Red | `#ef4444` | Error/danger states |

**Key Visual Effects:**
- `--gradient-quantum`: `linear-gradient(135deg, #00f3ff 0%, #a855f7 100%)`
- `--shadow-glow`: `0 0 25px rgba(0, 243, 255, 0.15)`
- `.glass-card`: `backdrop-filter: blur(12px)`, `border-radius: 16px`, hover transform with `cubic-bezier(0.4, 0, 0.2, 1)`
- `.badge-*`: Pill badges (cyan, purple, green, amber) with 10% fill + 30% border opacity
- `.btn-primary`: Quantum gradient button, `translateY(-2px)` hover lift + cyan glow
- `.dashboard-grid`: `grid-template-columns: repeat(auto-fit, minmax(320px, 1fr))`
- `.xp-progress-bar`: Animated quantum gradient fill

### TradingAcademy Lesson Curriculum

**Beginner Track:** RSI Foundations, 1-2% Portfolio Risk Rule, Stop Loss vs. Take Profit, Quantum Prairie Ecosystem
**Intermediate Track:** Beta & Volatility Hedging (70/30 Barbell Portfolio), RSI Divergence & False Breakouts, ATR Dynamic Stop-Loss Sizing

---

## 🌾 Quantum Prairie Domain Knowledge

### Pure-Play Quantum Stocks
| Ticker | Company | Technology |
|--------|---------|------------|
| `IONQ` | IonQ Inc. | Trapped Ion Quantum Hardware |
| `RGTI` | Rigetti Computing | Superconducting Quantum Hardware |
| `QBTS` | D-Wave Quantum | Quantum Annealing & Optimization |
| `QUBT` | Quantum Computing Inc. | Photonic Quantum & Quantum Networks |

### Quantum Prairie Giants (Midwest Ecosystem)
| Ticker | Company | Quantum Role |
|--------|---------|--------------|
| `IBM` | IBM Corp. | CQE Founding Partner, Heron Processors |
| `NVDA` | NVIDIA Corp. | cuQuantum SDK, IQMP Partner |
| `MSFT` | Microsoft Corp. | Azure Quantum, Topological Qubit Research |
| `GOOGL` | Alphabet Inc. | Sycamore Processor, Google Quantum AI |

### Infrastructure Anchors
- **IQMP** — Illinois Quantum & Microelectronics Park (Chicago, IL)
- **CQE** — Chicago Quantum Exchange (UChicago, UIUC, Northwestern, Argonne, Fermilab, IBM)
- **Quantum Corridor** — 400 Gbps quantum-safe optical fiber network (Chicago, IL ↔ Hammond, IN)
- **Argonne National Lab** — Q-NEXT Center
- **Fermilab** — SQMS Center

### Ecosystem Companies (Private)
- PsiQuantum, Infleqtion (featured in QuantumPrairieHub)

---

## ⚙️ Legacy Reference: `assets/` Prompt Templates

The `assets/` directory contains the **original swarms-based prototypes** that informed the active `Sovereign Code/` implementation. They are NOT executed at runtime but serve as design reference.

### `assets/prompts.py` — 5 System Prompts + 6 Dynamic Templates
| Constant | Agent | Purpose |
|----------|-------|---------|
| `DIRECTOR_PROMPT` | Trading Director | Orchestrates thesis, entry/exit, sizing |
| `QUANT_PROMPT` | Quant Analyst | SMA, RSI, Bollinger, VaR, ES, Greeks |
| `SENTIMENT_PROMPT` | Sentiment Agent | News/social/institutional sentiment (0-1) |
| `RISK_PROMPT` | Risk Manager | Position sizing, drawdown, correlation risk |
| `EXECUTION_PROMPT` | Execution Agent | Order type, quantity, entry, stop-loss, time-in-force |

**Dynamic Templates:** `RISK_ASSESSMENT_PROMPT`, `EXECUTION_ORDER_PROMPT`, `DIRECTOR_THESIS_PROMPT`, `QUANT_ANALYSIS_PROMPT`, `DIRECTOR_DECISION_PROMPT`, `DIRECTOR_TICKER_DISCOVERY_PROMPT`

### `assets/workers.py` — Original swarms Agent Declarations
| Agent | Model | Context |
|-------|-------|---------|
| `sentiment_agent` | `gpt-4o-mini` | `max_loops=1` |
| `risk_agent` | `gpt-4.1` | `context_length=16000` |
| `execution_agent` | `gpt-4.1` | `context_length=16000` |
| `quant_agent` | `gpt-4.1` | `context_length=16000` |
| `director_agent` | `gpt-4.1` | Handoffs to all agents |

Appends `_SYSTEM_SUFFIX` with live formatted date/time to all system prompts.

---

## 🛠️ Development Rules & Conventions

### Coding Conventions
1. **Output Scoping**: ALL generated codebase modules MUST be written strictly inside `Sovereign Code/`.
2. **Zero-Dependency Backend**: Python backend uses ONLY standard library (`http.server`, `urllib.request`, `json`, `os`, `math`, `random`). No pip installs required.
3. **Dual Import Resolution**: Every backend module uses `try: from .module import ... except ImportError: from module import ...` for both package and direct script execution.
4. **Offline-First Frontend**: Every API call includes complete client-side fallback data structures so the UI works without the backend.
5. **Division-by-Zero Protection**: All math engines guard against zero denominators (RSI returns 100.0, risk engine floors shares to 1).

### Error Handling Patterns
1. **LLM API Quota Graceful Fallback**: `urllib.error.HTTPError` caught for 429/400, logged, returns `None` → cascades to next provider.
2. **Deterministic Simulation**: Missing price history → seeded random walk (`seed = sum(ord(c) for c in ticker)`) for repeatable metrics.
3. **REST API Errors**: Bad JSON → HTTP 400 `{"error": str(e)}`, unknown routes → HTTP 404, all endpoints attach CORS headers.

### Development Workflow
1. **Planning Mode First**: Research codebase and domain before outputting `implementation_plan.md` with feedback requested.
2. **Log-Driven Debugging**: Fix runtime crashes by fetching and inspecting un-truncated task logs.
3. **Clean Server Shutdown**: Always manage background tasks using `manage_task` tool before session end.

### Quickstart Commands
```powershell
# Backend (Port 8000)
python "Sovereign Code/backend/app.py"

# Frontend (Port 5173)
cd "Sovereign Code/frontend"
npm install
npm run dev
```

### Environment Variables (`.env` at project root)
```env
OPENAI_API_KEY="sk-proj-..."
# ANTHROPIC_API_KEY=""
WORKSPACE_DIR="agent_workspace"
WALLET_PRIVATE_KEY=""
```

---

## 🐛 Known Bug History & Fixes

| Issue | Root Cause | Resolution | Commit |
|-------|-----------|------------|--------|
| `ReferenceError: None is not defined` in StockPicker.jsx | Python `None` literal used in JavaScript context | Replaced with JavaScript `null` | — |
| Multi-horizon trends not rendering | Missing 1D/7D/30D trend data in analyze endpoint | Added trend calculations to `quant_engine.py`, wired through `agents.py` pipeline | `c0a2d0a` |
