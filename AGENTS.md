# AGENTS.md — RJ-Stock Universal AI Agent Onboarding & Architecture Reference

> **Purpose**: This file is the **universal onboarding document** for any AI coding assistant (Claude, GPT, Gemini, Copilot, Cursor, etc.) starting work on the **RJ-Stock** (`Quantum-Stock-Mentor`) project. Read this file completely before making any changes.

---

## 🏷️ Project Identity

| Field | Value |
|-------|-------|
| **Name** | RJ-Stock (Quantum-Stock-Mentor) |
| **Type** | Educational multi-agent AI stock picking, risk management, and portfolio upskilling platform |
| **License** | MIT — Copyright (c) 2026 Jim Schweizer |
| **Domain** | Quantum Computing stocks + Midwest "Quantum Prairie" technology corridor |
| **Audience** | Beginner → Intermediate stock traders |
| **Status** | v0.1-beta |

---

## 🧠 Knowledge Graph — Required Visual Reference

**Read [`Sovereign Code/KNOWLEDGE_GRAPH.md`](Sovereign%20Code/KNOWLEDGE_GRAPH.md) alongside this file.** It contains Mermaid diagrams and visual architecture maps that supplement the text below:

| Diagram | What It Shows |
|---------|---------------|
| **System Architecture & Data Flow** | End-to-end flow from user interaction → React UI → REST API → 5-Agent Swarm → LLM providers → math engines → knowledge base |
| **Portfolio Upskilling Path** | 4-step progression: Stock Pick → Baseline Foundation → Technical Upgrade → Portfolio Hedging → Pre-Trade Checklist → Level Up |
| **Quantum Prairie Ecosystem** | Relationship map of research anchors (IQMP, CQE, Argonne, Fermilab), traded securities (8 tickers), and fiber networks (Quantum Corridor) |
| **Technical Analysis & Risk Logic** | Decision tree from price data → RSI/Trends/Volatility → risk rules → position sizing → take-profit targets |
| **Entity Relationship Matrix** | 10 core entity relationships defining how agents, UI components, risk rules, upskill engines, and ticker data interact |
| **Code Module Dependency Graph** | Import hierarchy for all backend and frontend modules |

> **Why this matters**: The Knowledge Graph provides spatial understanding of how components connect. Consult it before making cross-module changes, adding new agents to the pipeline, or modifying data flow between backend and frontend.

---

## ⚠️ Critical Rules — Read Before Writing Any Code

1. **Output Directory**: ALL generated/modified code MUST go inside `Sovereign Code/`. Never write application code to the project root, `assets/`, `logs/`, or temp directories.
2. **Zero-Dependency Backend**: The Python backend uses **ONLY** the standard library (`http.server`, `urllib.request`, `json`, `os`, `math`, `random`). Do NOT add pip dependencies.
3. **Dual Import Pattern**: Every backend module MUST use `try: from .module import ... except ImportError: from module import ...` so it works both as a package and as a direct script.
4. **Offline-First Frontend**: Every frontend API call MUST include complete client-side fallback data. The UI must function without the backend running.
5. **Division-by-Zero Guards**: All math engines must protect against zero denominators. RSI returns `100.0` when `avg_loss == 0`, risk engine floors shares to `1`.
6. **No Python `None` in JavaScript**: Never use `None` in `.jsx` files — use `null`. This was a previous production bug.
7. **CORS on All Endpoints**: Every REST response must include `Access-Control-Allow-Origin: *` headers.

---

## 📁 Repository Structure

```
RJ-Stock/
├── .env                              # API keys (never commit real values)
├── .gitignore                        # Standard exclusions
├── GEMINI.md                         # Gemini/Antigravity-specific session history
├── AGENTS.md                         # THIS FILE — universal AI agent onboarding
├── README.md                         # GitHub-facing documentation
├── RELEASE_NOTES.md                  # v0.1-beta release notes
├── LICENSE                           # MIT License
│
├── assets/                           # ⛔ LEGACY ONLY — reference prototypes, NOT active code
│   ├── prompts.py                    # Original 5 system prompts + 6 dynamic templates (swarms-based)
│   └── workers.py                    # Original swarms Agent declarations (gpt-4.1, gpt-4o-mini)
│
├── Sovereign Code/                   # ★ ACTIVE CODEBASE — all work happens here
│   ├── KNOWLEDGE_GRAPH.md            # Architecture diagrams, ER matrix, domain graph
│   ├── backend/                      # Python REST API & Multi-Agent Swarm Core
│   │   ├── app.py                    # HTTP server (http.server, port 8000)
│   │   ├── agents.py                 # 5-Agent pipeline + OpenAI/Anthropic/Local fallback
│   │   ├── config.py                 # Stock universe definitions & ticker metadata
│   │   ├── data_fetcher.py           # Universe & ticker lookup functions
│   │   ├── quant_engine.py           # RSI, SMA, Volatility, Key Levels, Multi-Horizon Trends
│   │   ├── risk_engine.py            # Position sizing, stop-loss, take-profit (1-2% rule)
│   │   ├── upskill_engine.py         # 4-Step progressive trader education + checklist
│   │   ├── quantum_prairie.py        # Midwest Quantum ecosystem knowledge base
│   │   └── test_backend.py           # Pipeline verification script
│   └── frontend/                     # Vite + React Glassmorphic UI Dashboard
│       ├── package.json              # React 19.2.8, Vite 8.2.0, oxlint 1.75.0
│       ├── vite.config.js            # @vitejs/plugin-react 6.0.4
│       └── src/
│           ├── App.jsx               # Root shell, state orchestrator, tab router
│           ├── index.css             # Dark-mode glassmorphism design system
│           └── components/
│               ├── TickerBar.jsx         # Horizontal ticker feed ribbon
│               ├── StockPicker.jsx       # 5-Agent dashboard + upskill stepper + trend grid
│               ├── QuantRiskManager.jsx  # Interactive risk & position sizing calculator
│               ├── QuantumPrairieHub.jsx # Midwest Quantum Prairie spotlight
│               ├── TradeSimulator.jsx    # Paper trade order ticket simulator
│               └── TradingAcademy.jsx    # Beginner & Intermediate lesson curriculum
│
└── logs/                             # Runtime logs (gitignored)
```

---

## 🏗️ Backend Architecture

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

### REST API Endpoints (`app.py`, port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/stocks` | Returns full quantum stock universe (pure-play + prairie giants) |
| `GET` | `/api/analyze/<ticker>` | Runs the complete 5-agent swarm pipeline for a ticker |
| `GET` | `/api/quantum-prairie` | Returns Quantum Prairie ecosystem metadata |
| `POST` | `/api/simulate-trade` | Simulates paper trade execution (body: `{ ticker, action, quantity, entry_price }`) |
| `OPTIONS` | `*` | CORS preflight handler |

### Agent Pipeline — Exact Sequential Execution Order

When `/api/analyze/<ticker>` is called, `run_full_agent_analysis()` runs these steps **in order**:

```
Step 1: Quant-Analyst    → analyze_quant_metrics()     → RSI, SMAs, Volatility, Key Levels, Trends
Step 2: Sentiment-Agent  → run_sentiment_agent()        → Sentiment Score 0-100
Step 3: Risk-Manager     → evaluate_risk()              → Shares, Stop-Loss, Take-Profit
Step 4: Trading-Director → run_trading_director()       → BUY/HOLD/SELL + Thesis
Step 5: Execution-Agent  → run_execution_agent()        → Paper Trade Limit Order Ticket
Step 6: Upskill-Engine   → get_stock_upskill_tips()     → 4-Step Education + Checklist
```

### LLM Cascading Fallback

The Trading Director (Step 4) attempts LLM providers in this order:
1. **OpenAI GPT-4o-mini** (`POST https://api.openai.com/v1/chat/completions`, temp: 0.7, timeout: 10s)
2. **Anthropic Claude 3.5 Sonnet** (`POST https://api.anthropic.com/v1/messages`, max_tokens: 400, timeout: 10s)
3. **Deterministic Local Swarm Engine** (probability scores + ecosystem role — always available)

Expected LLM JSON response schema: `{ "recommendation": str, "market_thesis": str, "beginner_summary": str }`

### Key Algorithms & Formulas

| Algorithm | Formula |
|-----------|---------|
| **RSI (Wilder's)** | `avg_gain[i] = (avg_gain[i-1] * 13 + gain[i]) / 14`; `RSI = 100 - 100/(1+RS)` |
| **SMA-N** | `mean(prices[-N:])` for N ∈ {7, 20, 30} |
| **Volatility %** | `(stdev(prices) / mean(prices)) * 100` |
| **Pivot Point** | `P = (High + Low + Close) / 3` |
| **Support S1** | `S1 = (2 * P) - High` |
| **Resistance R1** | `R1 = (2 * P) - Low` |
| **RSI Score** | `clamp(1.0 - abs(RSI - 55) / 50.0, 0.1, 1.0)` |
| **Technical Score** | `RSI_Score * 0.5 + SMA_Bias * 0.5` |
| **Probability Score** | `Technical * 0.4 + Volume * 0.3 + Trend * 0.3` |
| **Max Dollar Risk** | `account_size * (risk_tolerance_pct / 100)` |
| **Stop Loss Distance** | `clamp(volatility / 100 * 1.5, 0.03, 0.12)` |
| **Take Profit** | `price + (risk_per_share * 2.5)` — **2.5:1 risk-reward ratio** |

### Multi-Horizon Trend Confluence Scoring (1D, 7D, 30D)

| Positive Trends | Score | Label |
|-----------------|-------|-------|
| 3/3 | 95 | Strong Bullish Confluence |
| 2/3 | 70 | Moderate Bullish Bias |
| 1/3 | 45 | Consolidation / Mixed Signals |
| 0/3 | 20 | Bearish Pressure Across Timeframes |

### Beta Profiles

| Ticker(s) | Beta (β) | Classification |
|-----------|----------|----------------|
| `IBM` | 0.85 | Defensive Anchor |
| `NVDA`, `MSFT`, `GOOGL` | 1.45 | Growth Heavyweight |
| `IONQ`, `RGTI`, `QBTS`, `QUBT` | 2.35 | High-Beta Speculative |

### Deterministic Simulation Fallback

When price history has fewer than 15 data points, the quant engine generates a **30-day random walk** seeded with `sum(ord(c) for c in ticker)`. This ensures identical, repeatable metrics across sessions for testing and debugging.

---

## 💎 Frontend Architecture

### Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | React (ES Modules) | 19.2.8 |
| Bundler | Vite | 8.2.0 |
| Styling | Vanilla CSS (glassmorphism) | — |
| Linter | oxlint | 1.75.0 |
| Routing | Tab-based SPA (`activeTab` state) | No library |

### Component Map

| Component | Role | Props | Local State |
|-----------|------|-------|-------------|
| `App.jsx` | Root shell, API fetcher, tab router | — | `activeTab`, `selectedTicker`, `stocks`, `analysis`, `prairieData`, `loading`, `userXP` |
| `TickerBar.jsx` | Horizontal ticker feed | `stocks`, `selectedTicker`, `onSelectTicker` | Stateless |
| `StockPicker.jsx` | 5-Agent dashboard + upskill stepper | `analysis`, `loading`, `onRunAnalysis`, `userXP`, `userSkillLevel`, `onCompleteCheckitem` | `checkedItems: { [id]: bool }` |
| `QuantRiskManager.jsx` | Interactive risk calculator | `ticker`, `price` | `accountSize`, `riskTolerancePct`, `volatility` |
| `QuantumPrairieHub.jsx` | Midwest Quantum spotlight | `prairieData` | Stateless |
| `TradeSimulator.jsx` | Paper trade simulator | `executionOrder`, `onSimulateTrade` | `orders: []`, `loading: bool` |
| `TradingAcademy.jsx` | Lesson curriculum | — | `activeTab`, `activeLesson` |

### Tab Navigation Values
`'picker'` · `'risk'` · `'prairie'` · `'simulator'` · `'academy'`

### Design System (CSS Custom Properties)

**Dark Theme Palette:**
| Token | Value | Purpose |
|-------|-------|---------|
| `--bg-dark` | `#0a0c16` | Page background |
| `--bg-card` | `rgba(18, 22, 41, 0.75)` | Glass card fill |
| `--bg-card-hover` | `rgba(28, 34, 61, 0.85)` | Card hover fill |
| `--border-color` | `rgba(255, 255, 255, 0.1)` | Glass borders |
| `--text-main` | `#f1f5f9` | Primary text |
| `--text-muted` | `#94a3b8` | Secondary text |

**Accents:** Cyan (`#00f3ff`), Purple (`#a855f7`), Blue (`#3b82f6`), Green (`#10b981`), Amber (`#f59e0b`), Red (`#ef4444`)

**Signature Effects:**
- `--gradient-quantum`: `linear-gradient(135deg, #00f3ff 0%, #a855f7 100%)`
- `.glass-card`: `backdrop-filter: blur(12px)`, 16px radius, hover glow
- `.btn-primary`: Quantum gradient, `translateY(-2px)` hover lift
- `.dashboard-grid`: `repeat(auto-fit, minmax(320px, 1fr))`
- `.xp-progress-bar`: Animated gradient fill for gamification

---

## 🌾 Domain Knowledge — Quantum Prairie Ecosystem

### Tracked Stock Universe

**Pure-Play Quantum (High-Beta Speculative):**
| Ticker | Company | Technology | Price |
|--------|---------|------------|-------|
| `IONQ` | IonQ Inc. | Trapped Ion Quantum Hardware | $14.85 |
| `RGTI` | Rigetti Computing | Superconducting Quantum Hardware | $2.15 |
| `QBTS` | D-Wave Quantum | Quantum Annealing & Optimization | $1.95 |
| `QUBT` | Quantum Computing Inc. | Photonic Quantum & Networks | $4.10 |

**Quantum Prairie Giants (Midwest Ecosystem Anchors):**
| Ticker | Company | Quantum Role | Price |
|--------|---------|--------------|-------|
| `IBM` | IBM Corp. | CQE Founding Partner, Heron Processors | $204.50 |
| `NVDA` | NVIDIA Corp. | cuQuantum SDK, IQMP Partner | $128.40 |
| `MSFT` | Microsoft Corp. | Azure Quantum, Topological Qubit Research | $448.20 |
| `GOOGL` | Alphabet Inc. | Sycamore Processor, Google Quantum AI | $178.60 |

### Midwest Infrastructure Anchors
- **IQMP** — Illinois Quantum & Microelectronics Park (Chicago, IL)
- **CQE** — Chicago Quantum Exchange (UChicago, UIUC, Northwestern, Argonne, Fermilab, IBM)
- **Quantum Corridor** — 400 Gbps quantum-safe optical fiber (Chicago, IL ↔ Hammond, IN)
- **Argonne National Lab** — Q-NEXT Center
- **Fermilab** — SQMS Center
- **Ecosystem Private Cos** — PsiQuantum, Infleqtion

---

## 📐 Error Handling Patterns

| Pattern | Implementation |
|---------|---------------|
| **LLM quota exhaustion** | `urllib.error.HTTPError` caught for 429/400 → returns `None` → cascades to next LLM provider |
| **Missing price history** | Generates seeded random walk for deterministic simulation |
| **Bad POST body** | Returns HTTP 400 `{"error": str(e)}` |
| **Unknown route** | Returns HTTP 404 `{"error": "Endpoint not found"}` |
| **Zero-division** | RSI → 100.0; risk engine → min 1 share |
| **Import resolution** | `try/except ImportError` dual-path on every module |

---

## 🧪 Testing & Verification

```powershell
# Run backend pipeline test
python "Sovereign Code/backend/test_backend.py"

# Start backend server (port 8000)
python "Sovereign Code/backend/app.py"

# Start frontend dev server (port 5173)
cd "Sovereign Code/frontend"
npm install
npm run dev

# Lint frontend
cd "Sovereign Code/frontend"
npm run lint
```

### Environment Variables (`.env` at project root)
```env
OPENAI_API_KEY="sk-proj-..."       # Required for GPT-4o-mini thesis generation
ANTHROPIC_API_KEY=""                # Optional fallback for Claude 3.5 Sonnet
WORKSPACE_DIR="agent_workspace"    # Agent workspace directory
WALLET_PRIVATE_KEY=""              # Reserved for future use
```

---

## 🐛 Known Issues & Historical Fixes

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| `ReferenceError: None is not defined` in StockPicker.jsx | Python `None` literal used in JavaScript | Replace with `null` in all `.jsx` files |
| Multi-horizon trends not rendering | Missing 1D/7D/30D data in analyze endpoint | Added trend calculations to `quant_engine.py`, wired through `agents.py` |

---

## 📚 Legacy Reference (`assets/`)

The `assets/` directory holds the **original swarms-based prototypes** that inspired the active implementation. They are **NOT executed at runtime**.

- `prompts.py`: 5 system prompts (`DIRECTOR_PROMPT`, `QUANT_PROMPT`, `SENTIMENT_PROMPT`, `RISK_PROMPT`, `EXECUTION_PROMPT`) + 6 dynamic `.format()` templates
- `workers.py`: 5 swarms `Agent` declarations using `gpt-4.1` / `gpt-4o-mini` with `_SYSTEM_SUFFIX` date injection

---

*This document should be updated whenever significant architectural changes are made to the project.*
