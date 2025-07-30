import argparse
import time
from datetime import datetime
from api_connector import fetch_candles
from date_logger import init_databases, log_candle, log_user_decision
from signal_analyzer import analyze_signals
from mythic_flair import get_mythic_tag
import sqlite3
from rich.console import Console
from rich.table import Table

def log_signals(signals, exchange, symbol, interval):
    con = sqlite3.connect("potential_trades.db")
    cur = con.cursor()
    inserted_ids = []
    for s in signals:
        cur.execute("""
        INSERT INTO TradeSignals (timestamp, exchange, symbol, timeframe, signal_type,
            pattern_detected, rsi, macd, ema_cross, reason, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["timestamp"], exchange, symbol, interval,
            s["signal_type"], s["pattern_detected"], s["rsi"],
            s.get("macd"), s["ema_cross"], s["reason"],
            s.get("confidence") # Will insert NULL if not present
        ))
        inserted_ids.append(cur.lastrowid)
    con.commit()
    con.close()
    return inserted_ids

def get_interval_in_seconds(interval_str):
    """Converts interval string like '1h', '4h' to seconds for the sleep timer."""
    mapping = {
        '1m': 60,
        '5m': 300,
        '15m': 900,
        '1h': 3600,
        '4h': 14400,
        '1d': 86400
    }
    # Default to 1 hour if interval is not in the mapping
    return mapping.get(interval_str, 3600)

def main():
    """Main function to run the trader bot continuously."""
    console = Console()
    # --- Initialize and Parse ---
    init_databases()

    parser = argparse.ArgumentParser(description="CB_Trader: A crypto signal bot.")
    parser.add_argument("--exchange", required=True, help="Exchange to use (e.g., coinbase)")
    parser.add_argument("--evaluate_confidence", action="store_true", help="Enable confidence scoring engine.")
    parser.add_argument("--min_confidence", type=int, default=0, help="Minimum confidence score (0-100) for a signal to be shown. Requires --evaluate_confidence.")
    parser.add_argument("--record_decision", action="store_true", help="Prompt to record a decision for each new signal.")
    parser.add_argument("--mythic", action="store_true", help="Enrich signals with mythic tags for poetic clarity.")
    parser.add_argument("--interval", default="1h", help="Candle interval (e.g., 1h, 4h, 1d)")
    args = parser.parse_args()

    # --- Configuration ---
    top_symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'XRP-USD', 'ADA-USD']
    API_CALL_DELAY_SECONDS = 2 # Delay between checking each symbol to avoid rate limits

    if args.min_confidence > 0 and not args.evaluate_confidence:
        console.print("[bold red][CB_Trader] Error: --min_confidence requires --evaluate_confidence to be enabled. Exiting.[/bold red]")
        return

    wait_time_seconds = get_interval_in_seconds(args.interval)
    console.print(f"[CB_Trader] Starting continuous monitoring for {len(top_symbols)} symbols on {args.exchange} with {args.interval} interval.")
    console.print(f"Symbols: {', '.join(top_symbols)}")
    console.print(f"Press Ctrl+C to stop.")

    while True:
        try:
            console.print(f"\n[dim][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}][/dim] [bold]Running check cycle...[/bold]")

            for symbol in top_symbols:
                console.print(f"  -> Checking {symbol}...")
                # --- Fetch + Log Candles ---
                candles = fetch_candles(args.exchange, symbol, args.interval)
                if candles:
                    log_candle(candles, args.exchange, symbol, args.interval)
                    console.print(f"    > Logged {len(candles)} candles for {symbol}")

                    # --- Analyze + Log Signals ---
                    signals = analyze_signals(candles, evaluate_confidence=args.evaluate_confidence)

                    # --- Filter signals based on confidence ---
                    if args.evaluate_confidence and args.min_confidence > 0:
                        original_signal_count = len(signals)
                        signals = [s for s in signals if s.get('confidence', 0) >= args.min_confidence]
                        if len(signals) < original_signal_count:
                            console.print(f"    > Filtered {original_signal_count - len(signals)} signals below {args.min_confidence} confidence.")

                    if signals:
                        inserted_ids = log_signals(signals, args.exchange, symbol, args.interval)
                        console.print(f"    > Found [bold yellow]{len(signals)}[/bold yellow] potential trade signals for {symbol}!")

                        # --- Display signals in a table ---
                        table = Table(show_header=True, header_style="bold magenta")
                        table.add_column("Timestamp", style="dim", width=20)
                        table.add_column("Signal", justify="center")
                        table.add_column("Reason")
                        table.add_column("RSI", justify="right")
                        table.add_column("MACD Hist", justify="right")
                        if args.evaluate_confidence:
                            table.add_column("Confidence", justify="right")
                        if args.mythic:
                            table.add_column("Oracle's Whisper", style="cyan", justify="left")

                        for s in signals:
                            signal_style = "green" if s['signal_type'] == 'Buy' else "red" if s['signal_type'] == 'Sell' else "yellow"
                            
                            # Convert timestamp to a readable string to avoid render errors
                            ts = s['timestamp']
                            # Gemini uses milliseconds, Coinbase uses seconds. A simple check for magnitude can differentiate.
                            if ts > 1_000_000_000_000: # Heuristic for milliseconds
                                dt_object = datetime.fromtimestamp(ts / 1000)
                            else: # Assumed seconds
                                dt_object = datetime.fromtimestamp(ts)

                            row_data = [
                                dt_object.strftime('%Y-%m-%d %H:%M:%S'),
                                f"[{signal_style}]{s['signal_type']}[/{signal_style}]",
                                s['reason'],
                                str(s['rsi'])
                            ]
                            row_data.append(str(s.get('macd', 'N/A')))
                            if args.evaluate_confidence:
                                confidence = s.get('confidence', 0)
                                conf_style = "bold green" if confidence >= 75 else "bold yellow" if confidence >= 50 else ""
                                row_data.append(f"[{conf_style}]{confidence}/100[/{conf_style}]")
                            
                            if args.mythic:
                                mythic_tag = get_mythic_tag(s['signal_type'], s.get('confidence', 0), s['reason'])
                                row_data.append(mythic_tag)
                            
                            table.add_row(*row_data)
                        
                        console.print(table)

                        if args.record_decision:
                            console.print(f"    > Recording decisions for {len(signals)} new signal(s)...")
                            for i, signal in enumerate(signals):
                                signal_id = inserted_ids[i]

                                # Also format timestamp for this output
                                ts = signal['timestamp']
                                if ts > 1_000_000_000_000:
                                    dt_object = datetime.fromtimestamp(ts / 1000)
                                else:
                                    dt_object = datetime.fromtimestamp(ts)

                                confidence_str = f"| Confidence: {signal.get('confidence', 'N/A')}/100" if args.evaluate_confidence else ""
                                console.print(f"\n      [bold]Signal ID: {signal_id}[/bold] | {dt_object.strftime('%Y-%m-%d %H:%M:%S')}")
                                console.print(f"      → {signal['signal_type']} | {signal['reason']} | RSI: {signal['rsi']} {confidence_str}")
                                
                                action = input("      Enter action (B)uy, (S)ell, (I)gnore [default: I]: ").upper()
                                
                                decision = 'IGNORE'
                                if action == 'B': decision = 'BUY'
                                elif action == 'S': decision = 'SELL'
                                if decision != 'IGNORE':
                                    price_at_decision = float(candles[-1][4]) # Use last close price as proxy
                                    notes = input("      Enter optional notes: ")
                                    log_user_decision(signal_id, decision, price_at_decision, notes)
                                    console.print(f"      [green]✓ Logged decision '{decision}' for signal {signal_id}.[/green]")
                    else:
                        console.print(f"    > No new actionable signals detected for {symbol}.")
                else:
                    console.print(f"    > [red]Failed to fetch data from API for {symbol}.[/red]")

                # Wait a moment before the next API call in the loop
                time.sleep(API_CALL_DELAY_SECONDS)
            console.print(f"--- Cycle complete. Waiting for {wait_time_seconds} seconds ({args.interval}) ---")
            time.sleep(wait_time_seconds)

        except KeyboardInterrupt:
            console.print("\n[bold yellow][CB_Trader] Shutdown signal received. Exiting gracefully.[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red][CB_Trader] An unexpected error occurred: {e}. Retrying in 60 seconds...[/bold red]")
            time.sleep(60)

if __name__ == "__main__":
    main()