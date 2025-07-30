# 🗺️ CB_Trader Roadmap

This document outlines the development plan for **CB_Trader**. It is organized into phases, tracking completed features and future goals.

---

## ✅ Phase 1: Core Engine & Signal Generation (Complete)

- [x] **Project Setup**: Initialize the project with a clear structure, documentation, and environment configuration (`.env`).
- [x] **Continuous Monitoring**: Implement a 24/7 loop to run checks at set intervals.
- [x] **Multi-Asset Support**: Monitor a predefined list of top cryptocurrencies (`BTC`, `ETH`, `SOL`, etc.).
- [x] **API Connector**: Reliably fetch OHLCV data from exchanges.
- [x] **Database Logging**: Store price history and detected signals in separate SQLite databases.
- [x] **Signal Analysis**: Implement core indicators (RSI, 50/200 EMA Cross) and candlestick patterns (Engulfing).
- [x] **Confidence Scoring**: Develop a weighted engine to score signals based on indicator confluence.
- [x] **Command-Line Interface**: Implement a CLI for user-defined parameters (`--exchange`, `--interval`).

## ⏳ Phase 2: User Interaction & Feedback (Up Next)

- [x] **User Decision Logger**: Implement the `--record_decision` flag to allow users to log their actions (buy, sell, hold) and track the outcome/profitability of signals.
- [x] **Signal Filtering**: Allow users to filter signals based on confidence scores or other criteria.
- [x] **Visual Dashboard**: Create an optional terminal-based dashboard (e.g., using `rich`) to visualize signals and price history.
- [x] **Mythic Flair**: Enhance signals with "mythic" tags for poetic clarity.

## 🚀 Phase 3: Analysis & Lore Expansion (Future)

- [ ] **Expanded Indicators**:
  - [x] Add MACD calculation and signals.
  - [x] Add Bollinger Bands.
  - [x] Add more candlestick patterns (Hammer, Hanging Man).
- [x] **Advanced Confidence Scoring**: Refine the scoring engine to use confluence bonuses for stronger signal combinations.
- [x] **Backtesting Module**: Implement a backtesting framework with stop-loss, take-profit, and fee simulation to evaluate strategy performance.
- [ ] **Mythic Module Subscriptions**: Fulfill the lore by allowing users to filter signals based on custom rules (e.g., only show signals with >70 confidence).
- [ ] **Security Enhancements**: Integrate a secure key vaulting solution like EmbedID for API key management.
