"""
The Archivist — stores whispers into SQLite stone.
"""
import logging
import sqlite3
import numpy as np
import pandas as pd

# --- Constants ---
DB_FILE = "db/price_data.db"
TABLE_NAME = "candlestick_data"


def get_db_connection() -> sqlite3.Connection:
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    # This allows accessing columns by name, though not used in this module yet
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database and creates the candlestick_data table
    if it doesn't already exist. This rite is performed once.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # The schema for the sacred scrolls of price data
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                low REAL NOT NULL,
                high REAL NOT NULL,
                open REAL NOT NULL,
                close REAL NOT NULL,
                volume REAL NOT NULL,
                UNIQUE(pair, timestamp)
            );
        """)
        conn.commit()
        logging.info("Database sanctified. The scrolls are ready.")


def save_candlestick_data(pair: str, df: pd.DataFrame):
    """
    Inscribes candlestick data into the SQLite scrolls.
    It handles duplicate whispers by ignoring them.

    Args:
        pair (str): The trading pair to inscribe (e.g., "BTC-USD").
        df (pd.DataFrame): DataFrame containing candlestick data.
                           Must have a DatetimeIndex.
    """
    if df is None or df.empty:
        return

    with get_db_connection() as conn:
        # Prepare the DataFrame for SQL insertion
        df_to_save = df.copy()
        df_to_save["pair"] = pair
        # Convert DatetimeIndex to Unix timestamp for storage
        df_to_save["timestamp"] = (df_to_save.index.astype(np.int64) // 10**9)
        df_to_save.reset_index(drop=True, inplace=True)

        # Reorder columns to match the table schema for clarity
        cols = ["pair", "timestamp", "low", "high", "open", "close", "volume"]
        df_to_save = df_to_save[cols]

        # Convert DataFrame to list of tuples for executemany
        data_tuples = [tuple(x) for x in df_to_save.to_numpy()]

        # Use 'INSERT OR IGNORE' to handle duplicates gracefully
        sql = f"""
            INSERT OR IGNORE INTO {TABLE_NAME} (pair, timestamp, low, high, open, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = conn.cursor()
        cursor.executemany(sql, data_tuples)
        conn.commit()