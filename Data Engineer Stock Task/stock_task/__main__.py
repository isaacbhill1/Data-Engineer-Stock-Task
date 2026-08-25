import argparse

from .config import get_database_url
from .db import init_db, connection_test
from .stock_data import print_stock_table, fetch_store_stock_data


def main():
    parser = argparse.ArgumentParser(description="Fetch stock data from Yahoo Finance and display it in the terminal")
    parser.add_argument("--ticker", nargs="+", dest="ticker", default=["AAPL"], help="List of stock symbols to fetch and display, such as AAPL")
    parser.add_argument("--database-url", default=None, help="Override DATABASE_URL for this run")
    parser.add_argument("--period", default="1mo", help="Yahoo Finance period to fetch, e.g. 1d, 5d, 1mo, 1y")
    parser.add_argument("--interval", default="1d", help="Yahoo Finance interval, for example 1d or 1h")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of most recent rows to display in the terminal")
    parser.add_argument("--reset-db", action="store_true", help="Reset the database by dropping and recreating the table")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--fetch-only", action="store_true", help="Fetch and save data without printing it")
    group.add_argument("--print-only", action="store_true", help="Print data without fetching it")
    args = parser.parse_args()

    database_url = get_database_url()
    print(f"Database URL: {database_url}")
    if args.reset_db:
        print("Resetting database...")
        init_db(database_url)
    else:
        connection_test(database_url)
    print(f"Database ready: {database_url}")

    try:
        if args.fetch_only:
            fetch_store_stock_data(database_url, args.ticker, args.period, args.interval)
        elif args.print_only:
            print_stock_table(args.ticker, database_url, args.limit)
        else:
            fetch_store_stock_data(database_url, args.ticker, args.period, args.interval)
            print_stock_table(args.ticker, database_url, args.limit)
    except Exception as e:
        print(f"Error: {e}")

    while True:
        try:
            user_input = input("Enter command (fetch, print, reset, exit): ").strip().lower()
            if user_input == "fetch":
                user_input_ticker = input("Enter ticker(s) to fetch (comma-separated, default AAPL): ").strip().upper().split(",") or "AAPL"
                user_input_ticker = [tick.strip() for tick in user_input_ticker if tick.strip()] or ["AAPL"]
                if not user_input_ticker:
                    print("No valid tickers entered. Please try again.")
                    continue
                user_input_period = input("Enter period (default 1mo): ").strip() or "1mo"
                user_input_interval = input("Enter interval (default 1d): ").strip() or "1d"
                if fetch_store_stock_data(database_url, user_input_ticker, user_input_period, user_input_interval):
                    print_stock_table(user_input_ticker, database_url, args.limit)
                else:
                    print("Failed to fetch and store stock data.")
            elif user_input == "print":
                user_input_ticker = input("Enter ticker(s) to print (comma-separated, default AAPL): ").strip().upper().split(",") or "AAPL"
                user_input_ticker = [tick.strip() for tick in user_input_ticker if tick.strip()] or ["AAPL"]
                if not user_input_ticker:
                    print("No valid tickers entered. Please try again.")
                    continue
                user_input_limit = input("Enter limit (default 10): ").strip() or "10"
                print_stock_table(user_input_ticker, database_url, user_input_limit)
            elif user_input == "reset":
                init_db(database_url)
                print("Database reset.")
            elif user_input == "exit":
                print("Exiting...")
                break
            else:
                print("Invalid command. Please enter 'fetch', 'print', 'reset', or 'exit'.")
        except Exception as e:
            print(f"Error: {e}")

    

if __name__ == "__main__":
    main()
