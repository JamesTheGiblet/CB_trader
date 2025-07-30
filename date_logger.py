import sqlite3

def init_databases():
    # Price History
    con1 = sqlite3.connect("price_history.db")
    cur1 = con1.cursor()
    cur1.execute("""
    CREATE TABLE IF NOT EXISTS CandlestickData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        exchange TEXT,
        symbol TEXT,
        interval TEXT,
        open REAL, high REAL, low REAL, close REAL, volume REAL
    )
    """)
    con1.commit()
    con1.close()

    # Potential Trades
    con2 = sqlite3.connect("potential_trades.db")
    cur2 = con2.cursor()
    cur2.execute("""
    CREATE TABLE IF NOT EXISTS TradeSignals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        exchange TEXT,
        symbol TEXT,
        timeframe TEXT,
        signal_type TEXT,
        pattern_detected TEXT,
        rsi REAL,
        macd REAL,
        ema_cross TEXT,
        reason TEXT
    )
    """)
    con2.commit()
    con2.close()

def log_candle(data, exchange, symbol, interval):
    con = sqlite3.connect("price_history.db")
    cur = con.cursor()
    for candle in data:
        timestamp, low, high, open_, close, volume = candle
        cur.execute("""
        INSERT INTO CandlestickData (timestamp, exchange, symbol, interval, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, exchange, symbol, interval, open_, high, low, close, volume))
    con.commit()
    con.close()