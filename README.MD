# CB_Trader �

> _“The market speaks. CB_Trader listens.”_

**CB_Trader** is a terminal-native crypto signal bot that watches market tides, detects candlestick patterns, and logs its findings with technical rigor and a touch of mythic flair. It is not an auto-trader—it’s a vigilant signal oracle that empowers you to act based on insight, not automation.

## ✨ Features

- Monitor top coins across Coinbase & Gemini
- Detects **Bullish & Bearish Engulfing** patterns.
- Identifies **RSI** threshold crossings (overbought/oversold).
- Spots **Golden Cross** and **Death Cross** EMA events (5/20 period).
- Stores raw price history and trade signals in dual **SQLite** databases.
- Enriches signals with "mythic" tags for poetic clarity.

## 🧱 Tech Stack

- Python 3.x
- SQLite
- `requests` & `numpy`

## 📁 SQLite Databases

### `candle_data.db`

Stores raw OHLCV (Open, High, Low, Close, Volume) candles for all monitored assets, creating a permanent archive for backtesting and analysis.

### `potential_trades.db`

Logs every detected signal—including patterns, EMA crosses, and RSI events—for review.

## 📜 CLI Usage

```bash
# Example: Fetch 1-hour candles for BTC-USD from Coinbase
python cb_trader.py --exchange coinbase --symbol BTC-USD --interval 1h
```

Optional flags (in development):

- `--evaluate_confidence true`: trigger Gemini scoring engine
- `--save_signal true`: log pattern detections to DB
- `--record_decision`: prompt user to confirm and log a trade action

## 🧠 Signal Analysis

Includes:

- RSI calculation (14-period)
- EMA crossover detection (5 vs 20)
- Pattern recognition engine (engulfing, hammer, etc.)
- Optional mythic tags for poetic clarity

Example Output:

Signal: BUY | Pattern: Bullish Engulfing
RSI: 29.8 | EMA: Golden Cross
Confidence: 75/100 → ⚠️ Risk Level: Moderate
User Action Required.

## 🔐 Security Notes

- API keys loaded via `.env` file
- EmbedID integration planned for key vaulting, manifest logging, and user-bound access rituals

## 🎴 Mythic Lore

CB_Trader channels modular wisdom from Coddy and the Codex of EmbedID. Each signal is a glyph; each decision, a chapter in the user’s trading saga.

## 🛠️ Setup

1. Clone repo
2. Create `.env` file with API keys:

   COINBASE_KEY=xxx
   GEMINI_KEY=yyy

3. Run `cb_trader.py` with desired flags

## 🧪 Dev Notes

Next enhancements:

- Confidence scoring engine
- User decision logger with outcome tracking
- Visual dashboard (optional)
- Mythic module subscriptions

---

Made with care, code, and cryptic rhythm by [James the Giblet]
