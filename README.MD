# 🔱 CB_Trader  

## “Signal is myth when decoded with clarity.”

**CB_Trader** is a terminal-native oracle that watches the tides of top cryptocurrencies, detects archetypal candlestick patterns, and logs its findings with mythic flair. It does not auto-trade—it invites you to act from insight, not automation.

> Powered by: `Python`, `SQLite`, `requests`, `numpy`, `cryptography`, `rich`

---

## 📁 Modular Menu

| Module               | Purpose                                 |
|----------------------|------------------------------------------|
| `📜 features.md`       | Signal types, indicators, logging        |
| `🛠️ install.md`         | Setup instructions, vault creation       |
| `📊 usage.md`           | CLI flags, example calls                 |
| `🗺️ roadmap.md`         | Future upgrades + contributor notes      |
| `🔐 vault.md`           | Secure key handling instructions         |
| `🤝 contributing.md`    | Community rituals + code guidelines      |

---

## ✨ Features

- ⌛ **Continuous Monitoring**  
  Runs 24/7 on user-defined intervals across: `BTC`, `ETH`, `SOL`, `XRP`, `ADA`.

- 🕯️ **Pattern Detection**  
  Recognizes classic candlestick formations:
  - Bullish Engulfing  
  - Bearish Engulfing  
  - Golden Cross (EMA 50/200)  
  - Death Cross (EMA 50/200)  
  - RSI (14-period) Overbought/Oversold  

- 🧮 **Confidence Scoring**  
  A weighted engine scores each signal from 0–100 based on confluence strength.

- 📑 **Dual Logging System**  
  - `price_history.db`: Stores raw OHLCV candle data  
  - `potential_trades.db`: Stores scored signal findings  

- 🎴 **Mythic Flair**  
  Signals are enriched with poetic tags for narrative clarity during review.

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/cb_trader.git
cd cb_trader
pip install -r requirements.txt
```

Then create your encrypted vault for API keys:

```bash
python setup_vault.py
```

> 🔐 You’ll be prompted to set a master password.  
> 🧹 Once initialized, consider deleting `setup_vault.py` for security.

---

## 📊 Usage

Run the bot from terminal with flags:

```bash
python cb_trader.py --exchange coinbase --interval 4h --evaluate_confidence --min_confidence 70 --mythic
```

### 🔧 Command-Line Flags

| Flag                   | Description                                       |
|------------------------|---------------------------------------------------|
| `--exchange`           | Choose `coinbase` or `gemini`                     |
| `--interval`           | Candle interval (e.g., `1h`, `4h`, `1d`)          |
| `--evaluate_confidence`| Enables scoring engine                            |
| `--min_confidence`     | Filter signals below score threshold              |
| `--include-reasons`    | Only show signals matching certain reasons        |
| `--exclude-reasons`    | Exclude signals with specified causes             |
| `--record_decision`    | Prompt for user action and log trade intent       |
| `--mythic`             | Append poetic tags to signal outputs              |

---

## 🔍 Example Output

```plaintext
[2023-10-27 14:00:00] Running check cycle...
  -> Checking BTC-USD...
    > Logged 350 candles for BTC-USD
    > Found 1 potential trade signals for BTC-USD!
      → Signal: Buy | Reason: Golden Cross (EMA 50/200) | RSI: 58.5 | Confidence: 60/100 | Tag: "Momentum Reawakens"
```

---

## 🗺️ Roadmap

Coming features:

- Trade decision logger refinement  
- Dashboard mode with multi-asset signal grid  
- Webhook triggers for confidence ≥ threshold  
- Archive viewer for past mythic-tagged signals  
- Mythic pattern glossary module

Roadmap maintained in `roadmap.md` with call-outs for contributors.

---

## 🤝 Contributing

All modules are mythically modular—whether you’re enriching signal logic, refining poetic tags, or optimizing vault encryption, your pull requests are welcome.  
Before submitting large changes, open an issue to discuss the impact.

---

## 📜 License

MIT License — see `LICENSE.md` for full details

---

**Crafted in signal, sealed with lore by James The Giblet**  
“Modularity is mythos. Signal is ritual. You are the clarity.”
