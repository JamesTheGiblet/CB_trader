import argparse
from api_connector import fetch_candles
from date_logger import init_databases, log_candle
from signal_analyzer import analyze_signals
import sqlite3

def log_signals(signals, exchange, symbol, interval):
    con = sqlite3.connect("potential_trades.db")
    cur = con.cursor()
    for s in signals:
        cur.execute("""
        INSERT INTO TradeSignals (timestamp, exchange, symbol, timeframe, signal_type,
            pattern_detected, rsi, macd, ema_cross, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["timestamp"], exchange, symbol, interval,
            s["signal_type"], s["pattern_detected"], s["rsi"],
            s.get("macd"), s["ema_cross"], s["reason"]
        ))
    con.commit()
    con.close()

# --- Initialize and Parse ---
init_databases()

parser = argparse.ArgumentParser()
parser.add_argument("--exchange", required=True)
parser.add_argument("--symbol", required=True)
parser.add_argument("--interval", default="1h")
args = parser.parse_args()

# --- Fetch + Log Candles ---
candles = fetch_candles(args.exchange, args.symbol, args.interval)
if candles:
    log_candle(candles, args.exchange, args.symbol, args.interval)
    print(f"[CB_Trader] Logged {len(candles)} candles for {args.symbol} ({args.interval})")

    # --- Analyze + Log Signals ---
    signals = analyze_signals(candles)
    if signals:
        log_signals(signals, args.exchange, args.symbol, args.interval)
        print(f"[CB_Trader] Found {len(signals)} potential trade signals")
        for s in signals:
            print(f"  → {s['timestamp']} | {s['pattern_detected']} | RSI: {s['rsi']} | {s['reason']}")
    else:
        print("[CB_Trader] No actionable patterns detected.")
else:
    print("[CB_Trader] Failed to fetch data.")