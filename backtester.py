import sqlite3
import argparse
import pandas as pd
from rich.console import Console
from rich.table import Table
from date_logger import init_databases
from signal_analyzer import analyze_signals

def run_backtest(symbol, interval, min_confidence, stop_loss_pct, take_profit_pct, fee_pct):
    """
    Runs a backtest for a given symbol and parameters.
    """
    console = Console()
    console.print(f"\n[Backtester] Running for [bold]{symbol}[/bold] on [bold]{interval}[/bold] interval...")

    # Ensure the database and tables exist before trying to read from them.
    init_databases()

    sl_str = f"{stop_loss_pct}%" if stop_loss_pct else "N/A"
    tp_str = f"{take_profit_pct}%" if take_profit_pct else "N/A"
    fee_str = f"{fee_pct}%" if fee_pct else "0.0%"
    console.print(f"Parameters: Min Confidence: [bold]{min_confidence}[/bold], Stop-Loss: [bold]{sl_str}[/bold], Take-Profit: [bold]{tp_str}[/bold], Fees: [bold]{fee_str}[/bold]")

    # 1. Load data from SQLite
    con = sqlite3.connect("price_history.db")
    df = pd.read_sql_query(
        f"SELECT timestamp, open, high, low, close, volume FROM CandlestickData WHERE symbol = '{symbol}' AND interval = '{interval}' ORDER BY timestamp ASC",
        con
    )
    con.close()

    if df.empty:
        console.print(f"[red]No historical data found for {symbol} on {interval}.[/red]")
        return

    # Convert timestamp column to numeric before applying logic
    df['timestamp'] = pd.to_numeric(df['timestamp'])

    # Normalize timestamps to seconds for consistency
    df['timestamp'] = df['timestamp'].apply(lambda ts: ts / 1000 if ts > 1_000_000_000_000 else ts)
    candles = df.to_numpy().tolist()

    # 2. Generate all signals (not just the last 5)
    all_signals = analyze_signals(candles, evaluate_confidence=True, return_all=True)

    # --- Filter signals based on custom rules (Mythic Module) ---
    if include_reasons:
        reasons_to_include = [r.strip() for r in include_reasons.split(',')]
        all_signals = [s for s in all_signals if any(reason in s['reason'] for reason in reasons_to_include)]

    if exclude_reasons:
        reasons_to_exclude = [r.strip() for r in exclude_reasons.split(',')]
        all_signals = [s for s in all_signals if not any(reason in s['reason'] for reason in reasons_to_exclude)]

    # 3. Filter signals by confidence
    signals = [s for s in all_signals if s.get('confidence', 0) >= min_confidence]
    console.print(f"Found {len(signals)} signals passing the confidence threshold.")

    # 4. Simulate trades
    trades = []
    position = None  # Can be 'LONG' or None
    entry_price = 0
    entry_time = 0

    for _, row in df.iterrows():
        current_time = row['timestamp']
        current_low = row['low']
        current_high = row['high']
        current_close = row['close']
        
        # Check for exit conditions if a position is open
        if position == 'LONG':
            exit_price = 0
            exit_reason = None

            # Priority 1: Stop-Loss (checks the candle's low)
            if stop_loss_pct and current_low <= entry_price * (1 - stop_loss_pct / 100):
                exit_price = entry_price * (1 - stop_loss_pct / 100)
                exit_reason = f"Stop-Loss ({stop_loss_pct}%)"
            
            # Priority 2: Take-Profit (checks the candle's high)
            elif take_profit_pct and current_high >= entry_price * (1 + take_profit_pct / 100):
                exit_price = entry_price * (1 + take_profit_pct / 100)
                exit_reason = f"Take-Profit ({take_profit_pct}%)"

            # Priority 3: Sell Signal
            else:
                sell_signals_today = [s for s in signals if s['timestamp'] == current_time and s['signal_type'] == 'Sell']
                if sell_signals_today:
                    exit_price = current_close
                    exit_reason = "Signal"

            if exit_reason:
                # Factor in trading fees for a more realistic PnL
                if fee_pct:
                    entry_cost = entry_price * (1 + fee_pct / 100)
                    exit_value = exit_price * (1 - fee_pct / 100)
                    pnl = ((exit_value - entry_cost) / entry_cost) * 100
                else:
                    pnl = (exit_price - entry_price) / entry_price * 100

                trades.append({
                    "entry_time": entry_time, "exit_time": current_time,
                    "entry_price": entry_price, "exit_price": exit_price, 
                    "pnl_percent": pnl, "exit_reason": exit_reason
                })
                position = None
        # Only check for an entry if we are not in a position (and didn't just exit)
        elif position is None:
            buy_signals_today = [s for s in signals if s['timestamp'] == current_time and s['signal_type'] == 'Buy']
            if buy_signals_today:
                position = 'LONG'
                entry_price = current_close
                entry_time = current_time

    # 5. Report results
    if not trades:
        console.print("[yellow]No trades were executed in this backtest.[/yellow]")
        return

    # Calculate net PnL by compounding returns
    initial_capital = 100
    end_capital = initial_capital
    for t in trades:
        end_capital = end_capital * (1 + t['pnl_percent'] / 100)
    total_pnl = ((end_capital - initial_capital) / initial_capital) * 100
    wins = [t for t in trades if t['pnl_percent'] > 0]
    win_rate = (len(wins) / len(trades)) * 100 if trades else 0

    console.print("\n--- Backtest Results ---")
    console.print(f"Total Trades: {len(trades)}")
    console.print(f"Win Rate: {win_rate:.2f}%")
    console.print(f"Total PnL: [green]{total_pnl:.2f}%[/green]" if total_pnl > 0 else f"[red]{total_pnl:.2f}%[/red]")

    table = Table(title="Trade Log")
    table.add_column("Entry Time"), table.add_column("Exit Time"), table.add_column("Entry Price", justify="right")
    table.add_column("Exit Price", justify="right"), table.add_column("Exit Reason"), table.add_column("PnL %", justify="right")
    for trade in trades:
        pnl_str = f"[green]{trade['pnl_percent']:.2f}[/green]" if trade['pnl_percent'] > 0 else f"[red]{trade['pnl_percent']:.2f}[/red]"
        table.add_row(
            pd.to_datetime(trade['entry_time'], unit='s').strftime('%Y-%m-%d %H:%M'), 
            pd.to_datetime(trade['exit_time'], unit='s').strftime('%Y-%m-%d %H:%M'), 
            f"{trade['entry_price']:.2f}", f"{trade['exit_price']:.2f}", 
            trade['exit_reason'], pnl_str
        )
    console.print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CB_Trader Backtester")
    parser.add_argument("--symbol", required=True, help="Symbol to backtest (e.g., BTC-USD)")
    parser.add_argument("--interval", default="1h", help="Candle interval (e.g., 1h, 4h)")
    parser.add_argument("--min_confidence", type=int, default=70, help="Minimum confidence score for signals")
    parser.add_argument("--stop_loss", type=float, help="Stop-loss percentage (e.g., 2.5 for 2.5%)")
    parser.add_argument("--take_profit", type=float, help="Take-profit percentage (e.g., 5.0 for 5.0%)")
    parser.add_argument("--fees", type=float, default=0.1, help="Trading fee percentage per trade (e.g., 0.1 for 0.1%)")
    args = parser.parse_args()
    run_backtest(args.symbol, args.interval, args.min_confidence, args.stop_loss, args.take_profit, args.fees)