# 📜 CB_TRADER DEVELOPMENT ROADMAP  
>
> _“We build not just a bot, but a shrine to signal.”_

This sacred roadmap documents the evolving architecture of **CB_trader**, from its early foundation to future signal[ ]wielding mastery. Each phase is a passage in the pilgrimage—debugged, persistent, and terminal[ ]bound.

---

## ⚔️ Phase 1 — The Foundation Rites _(MVP Ascension)_

**Goal**: Build a stable, reliable signal oracle within the terminal.  
**Duration**: 2–4 Weeks  
**Key Rites**:

- ✅ 🔧 **Sanctify the Project Realm**  
  ✅ Initialize Git & Visual Studio Code workspace  
  ✅ Cast the requirements.txt, config.py, and define `logs/`, `db/` (with `.gitignore wards)

- ✅ 🧿 **Bind to the Coinbase Spirits (API Integration)**  
  - ✅ Secure API key using `cdp_api_key.json` (JWT)
  - ✅ Build `coinbase_api.py` for fetching live & historical data  
  - ✅ Layer error wards: catch connection bans, rate-limit curses, trace invalid auth rituals

- ✅ 🪶 **Inscribe the Data Scrolls (SQLite Persistence)**  
  - ✅ Define candlestick_data schema inside `db/price_data.db`  
  - ✅ Log each crypto whisper with timestamp, pair, and candlestick values
  - ✅ Ensure graceful opening/closing of sacred connections

- ✅ 🧙 **Invoke the Signal Spirits (Technical Analysis)**  
  - ✅ Use `pandas` and `pandas-ta` for SMA, RSI  
  - ✅ Generate simple signal incantations based on crossover and overbought/oversold visions

- ✅ 🔥 **Illuminate the Path (Logging & Feedback)**  
  - ✅ Configure logging rituals: rotating files, terminal echoes  
  - ✅ Log every event with clarity—from bot awakenings to cryptic calculation errors  
  - ✅ Chronicle all signal revelations with full context

- ✅ 🛡️ **Reveal the Terminal Truth (Output Layer)**  
  - ✅ Format crypto price table with clarity  
  - ✅ Announce buy/sell omens directly to the console  
  - ✅ Ensure the bot whispers status updates (“Fetching… Analyzing…”)

- ✅ 📖 **Codify the User Will (config.py)**  
  - ✅ User-defined tracked pairs  
  - ✅ Polling interval adjustments  
  - ✅ Indicator parameters (SMA periods, RSI thresholds)

---

## 🌀 Phase 2 — The Rites of Refinement _(Signal Maturity)_

**Goal**: Expand signal wisdom, enhance user control, and deepen data resilience.  
**Duration**: 3–5 Weeks  
**Augmented Rites**:

[ ] 🌊 **Widen the Signal Scope**  
  [ ] Introduce EMA, MACD, Bollinger Bands  
  [ ] Enable hybrid signal logic & implement risk awareness parameters (e.g., symbolic stop[ ]loss)

[ ] 🎚️ **Empower the Seer (Dynamic Config)**  
  [ ] Hot[ ]reload `config.py` for seamless mid[ ]ritual adjustments  
  [ ] Support CLI flags (`[ ][ ]debug`, `[ ][ ]pairs`) for rapid invocation style changes

[ ] 📂 **Query the Scrolls (SQLite Retrieval)**  
  [ ] Allow timeframe[ ]based queries  
  [ ] Implement indexed access for speed  
  [ ] Design database cleaning rituals for long[ ]term sustainability

[ ] 🧱 **Strengthen the Ward System (Resilient Error Handling)**  
  [ ] Retry logic for transient curses  
  [ ] Log analysis failures with empathy  
  [ ] Catch unhandled exceptions and document them with final words

[ ] 💓 **Monitor the Pulse (Terminal Heartbeat)**  
  [ ] Periodic heartbeat messages (e.g., every 5 minutes: “CB_Trader still listens…”)  
  [ ] Log runtime metrics for future optimization quests

---

## 🌟 Phase 3 — Ascension & Future Lore _(Analytical Enlightenment)_

**Goal**: Enable deep analysis, reflective reporting, and cross[ ]timeframe divination.  
**Duration**: Ongoing (as omens allow)  
**Divine Rites**:

[ ] 🧪 **Backtest the Past (Historical Trials)**  
  [ ] Use SQLite archives to simulate past trades  
  [ ] Generate terminal scrolls of win rate, signal efficacy, ritual accuracy

[ ] 📊 **Summon Daily Scrolls (Reporting)**  
  [ ] Offer summaries of signals at chosen intervals  
  [ ] Include performance indicators and symbolic “current position states”

[ ] ⏳ **View the Many Times (Multi[ ]Timeframe Analysis)**  
  [ ] Fetch and compare candlesticks across dimensions  
  [ ] Combine signals from multiple perspectives for strength of divination

[ ] 🔔 **Customize the Chant (Notification Control)**  
  [ ] Let users configure verbosity: whisper[ ]mode, full oracle mode, or mythic verbosity

[ ] 🛠️ **Optimize the Shrine (Database & Performance)**  
  [ ] Monitor scale thresholds  
  [ ] Explore alternative embedded databases if SQLite meets its limits

[ ] 🧬 **Signal Prophesy Engine (Long[ ]Term Research)**  
  [ ] Investigate machine learning rituals: regression[ ]based oracle models  
  [ ] Compare traditional indicators vs. emergent patterns  
  [ ] Build but never blindly trust the data gods.
