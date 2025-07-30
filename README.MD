# CB_Trader 🔱

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

> _“The market speaks. CB_Trader listens.”_

**CB_Trader** is a terminal-native crypto signal bot that continuously watches market tides for top cryptocurrencies, detects candlestick patterns, and logs its findings with technical rigor and a touch of mythic flair. It is not an auto-trader—it’s a vigilant signal oracle that empowers you to act based on insight, not automation.

## ✨ Features

- ✅ **Continuous Monitoring**: Runs 24/7, checking for signals at user-defined intervals.
- ✅ **Multi-Asset Watcher**: Monitors the top 5 cryptocurrencies (BTC, ETH, SOL, XRP, ADA) in a single session.
- ✅ **Pattern Recognition**: Detects key candlestick patterns like **Bullish & Bearish Engulfing**.
- ✅ **Technical Indicators**:
  - Identifies **RSI** (14-period) threshold crossings for overbought/oversold conditions.
  - Spots **Golden Cross** and **Death Cross** EMA events (50/200 period).
- ✅ **Confidence Scoring**: A weighted engine scores signals (0-100) based on the confluence of patterns, EMA crosses, and RSI.
- ✅ **Dual Database Logging**:
  - `price_history.db`: Stores raw OHLCV candles for analysis.
  - `potential_trades.db`: Logs every detected signal for review.
- 🎴 **Mythic Flair**: Enriches signals with "mythic" tags for poetic clarity.

## 🧱 Tech Stack

- Python 3.x
- SQLite
- `requests`, `numpy`, `python-dotenv`
- `rich` (for terminal UI)

## 🛠️ Installation & Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/cb_trader.git
    cd cb_trader
    ```

2. **Install dependencies:**
    _(It's recommended to use a virtual environment)_

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file** in the root directory and add your API keys:

    ```env
    COINBASE_KEY=xxx
    COINBASE_SECRET=xxx
    GEMINI_KEY=yyy
    GEMINI_SECRET=yyy
    ```

## 📜 Usage

Run the bot from your terminal. It will automatically monitor the top 5 symbols.

```bash
# Example: Run the bot with a 4-hour interval and enable confidence scoring
python cb_trader.py --exchange coinbase --interval 4h --evaluate_confidence
```

### Command-Line Arguments

| Flag                  | Description                                      | Status         |
| --------------------- | ------------------------------------------------ | -------------- |
| `--exchange`          | The exchange to use (`coinbase` or `gemini`).    | ✅ Required    |
| `--interval`          | The candle interval (e.g., `1h`, `4h`, `1d`).    | ✅ Required    |
| `--evaluate_confidence` | Enable the confidence scoring engine.            | ✅ Implemented |
| `--min_confidence`    | Filter signals below a confidence score.         | ✅ Implemented |
| `--include-reasons`   | Only show signals matching these reasons.        | ✅ Implemented |
| `--exclude-reasons`   | Do not show signals matching these reasons.      | ✅ Implemented |
| `--record_decision`   | Prompt user to confirm and log a trade action.   | ✅ Implemented |

## 📊 Example Output

```plaintext
[2023-10-27 14:00:00] Running check cycle...
  -> Checking BTC-USD...
    > Logged 350 candles for BTC-USD
    > Found 1 potential trade signals for BTC-USD!
      → Signal: Buy | Reason: Golden Cross (EMA 50/200) | RSI: 58.5 | Confidence: 60/100
```

## 🗺️ Roadmap

The project's development plan is tracked in our Roadmap. Key upcoming features include a user decision logger and expanded technical indicators.

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

📜 License
This project is licensed under the MIT License - see the LICENSE.md file for details.

---

Made with care, code, and cryptic rhythm by [James the Giblet]
