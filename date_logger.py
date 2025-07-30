import sqlite3

def _add_confidence_column_if_missing(cursor):
    """Checks if the 'confidence' column exists in TradeSignals and adds it if not."""
    cursor.execute("PRAGMA table_info(TradeSignals)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'confidence' not in columns:
        print("[DB Logger] Schema update: Adding 'confidence' column to TradeSignals table.")
        cursor.execute("ALTER TABLE TradeSignals ADD COLUMN confidence INTEGER")

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
        open REAL, high REAL, low REAL, close REAL, volume REAL,
        UNIQUE(timestamp, exchange, symbol, interval)
    );
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
        reason TEXT,
        confidence INTEGER
    )
    """)
    cur2.execute("""
    CREATE TABLE IF NOT EXISTS UserDecisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        signal_id INTEGER,
        decision_timestamp TEXT,
        decision TEXT,
        price_at_decision REAL,
        notes TEXT,
        FOREIGN KEY(signal_id) REFERENCES TradeSignals(id)
    )
    """)

    # This handles existing DBs that are missing the column
    _add_confidence_column_if_missing(cur2)

    con2.commit()
    con2.close()

def log_candle(data, exchange, symbol, interval):
    con = sqlite3.connect("price_history.db")
    cur = con.cursor()
    for candle in data:
        timestamp, low, high, open_, close, volume = candle
        cur.execute("""
        INSERT OR IGNORE INTO CandlestickData (timestamp, exchange, symbol, interval, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, exchange, symbol, interval, open_, high, low, close, volume))
    con.commit()
    con.close()

def log_user_decision(signal_id, decision, price, notes):
    """Logs a user's decision against a specific signal."""
    con = sqlite3.connect("potential_trades.db")
    cur = con.cursor()
    cur.execute("""
    INSERT INTO UserDecisions (signal_id, decision_timestamp, decision, price_at_decision, notes)
    VALUES (?, datetime('now', 'utc'), ?, ?, ?)
    """, (signal_id, decision, price, notes))
    con.commit()
    con.close()