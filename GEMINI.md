# GEMINI.md - Pair Programming & System Architecture Log

## Overview
This document records the pair programming collaboration between the **USER** and **Antigravity** (Google DeepMind Agentic AI Coding Assistant) for project **RJ-Stock**.

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

## 🏗️ Technical Architecture (`Sovereign Code/`)

### Multi-Agent Swarm Logic (`Sovereign Code/backend/agents.py`)
- **Trading-Director**: Generates overall BUY/HOLD/SELL ratings & fundamental theses using OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, or local Swarm fallback.
- **Quant-Analyst**: Evaluates RSI (14-day), 20-day SMA, Volatility, Probability Scores, and Key Levels.
- **Sentiment-Agent**: Calculates quantitative market sentiment (0-100 scale).
- **Risk-Manager**: Enforces Wall Street's 1-2% Portfolio Risk Rule, maximum drawdown calculations, and stop-loss placement.
- **Execution-Agent**: Generates paper trading limit order execution tickets.

### Quantum Prairie Midwest Ecosystem (`Sovereign Code/backend/quantum_prairie.py`)
- **Pure-Play Quantum Stocks**: `IONQ`, `RGTI`, `QBTS`, `QUBT`.
- **Quantum Prairie Giants**: `IBM`, `NVDA`, `MSFT`, `GOOGL`.
- **Infrastructure Anchors**: Illinois Quantum & Microelectronics Park (IQMP), Chicago Quantum Exchange (CQE), Quantum Corridor optical fiber network (Chicago, IL to Hammond, IN), Argonne National Lab, Fermilab.

### Glassmorphic Web App (`Sovereign Code/frontend/`)
- Built with **React 19**, **Vite 8**, and **Vanilla CSS Design System**.
- Component Architecture: `TickerBar.jsx`, `StockPicker.jsx`, `QuantRiskManager.jsx`, `QuantumPrairieHub.jsx`, `TradeSimulator.jsx`, `TradingAcademy.jsx`.

---

## 🛠️ Verification & Development Rules Followed

1. **Planning Mode First**: Researched codebase and Quantum Prairie domain before outputting `implementation_plan.md` with feedback requested.
2. **Output Scoping**: All generated codebase modules written strictly inside `Sovereign Code/`.
3. **Log-Driven Debugging**: Fixed runtime crashes by fetching and inspecting un-truncated task logs (`task-91.log`).
4. **Zero-Dependency Fallbacks**: Python backend designed with standard library `http.server` and `urllib.request` to ensure 100% execution capability across any machine.
5. **Clean Server Shutdown**: Managed background tasks using `manage_task` tool.
