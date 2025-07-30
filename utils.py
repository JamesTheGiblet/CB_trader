"""
The Lantern — logging, formatting, guiding the path.
"""
import logging
import os
from typing import Optional

import pandas as pd
from logging.handlers import RotatingFileHandler

from rich.console import Console
from rich.table import Table

LOG_DIR = "logs"
LOG_FILE = "cb_trader.log"


def setup_logging():
    """
    Configures the logging for the application.

    This ritual sets up a rotating file handler and a stream handler to output
    logs to both a file and the console, ensuring every event is chronicled.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Rotating file handler to preserve the scrolls of knowledge
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE), maxBytes=1024 * 1024 * 5, backupCount=5
    )
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # Console handler to echo the whispers to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)


def display_oracle_verdict(
    pair: str, signal: str, df: Optional[pd.DataFrame] = None
):
    """
    Formats and displays the final signal and recent data in a rich table.

    Args:
        pair (str): The trading pair (e.g., "BTC-USD").
        signal (str): The generated signal ("BUY", "SELL", or "HOLD").
        df (pd.DataFrame, optional): DataFrame with data and indicators to display.
    """
    console = Console()

    # Determine signal style
    if signal == "BUY":
        style = "bold green"
    elif signal == "SELL":
        style = "bold red"
    else:
        style = "bold yellow"

    console.print(f"\n🔮 [bold]Oracle's Verdict for {pair}:[/bold] [{style}]{signal}[/{style}]")

    if df is not None and not df.empty:
        # Dynamically get indicator column names from config
        from config import (
            SMA_SHORT_PERIOD,
            SMA_LONG_PERIOD,
            RSI_PERIOD,
        )

        sma_short_col = f"SMA_{SMA_SHORT_PERIOD}"
        sma_long_col = f"SMA_{SMA_LONG_PERIOD}"
        rsi_col = f"RSI_{RSI_PERIOD}"

        table = Table(title="--- Recent Whispers ---", show_header=True, header_style="bold magenta")
        table.add_column("Time (UTC)", style="dim")
        table.add_column("Close", justify="right")
        table.add_column(f"SMA_{SMA_SHORT_PERIOD}", justify="right", style="cyan")
        table.add_column(f"SMA_{SMA_LONG_PERIOD}", justify="right", style="purple")
        table.add_column(f"RSI_{RSI_PERIOD}", justify="right", style="yellow")

        # Display the last 5 rows
        for index, row in df.tail(5).iterrows():
            table.add_row(
                str(index),
                f"{row['close']:.2f}",
                f"{row.get(sma_short_col, 'N/A'):.2f}",
                f"{row.get(sma_long_col, 'N/A'):.2f}",
                f"{row.get(rsi_col, 'N/A'):.2f}",
            )

        console.print(table)
    console.print("-" * 25 + "\n")