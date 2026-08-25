import sqlite3
from types import SimpleNamespace
import yfinance as yf
import pandas as pd

def fetch_stock_data(
    tickers = ["AAPL"],
    period = "1mo",
    interval = "1d",
    auto_adjust = False,
    progress = False
    ):
    tickers = [tickers] if isinstance(tickers, str) else list(tickers)
    tickers = [tick.strip().upper() for tick in tickers]
    if not tickers:
        return []

    df = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        auto_adjust=auto_adjust,
        progress=progress,
        actions=False,
        threads=True,
    )

    # Move date index into a column
    df = df.reset_index()
    date_column = "Date" if "Date" in df.columns else "Datetime"
    df = df.rename(columns={date_column: "date"})
    if isinstance(df.columns, pd.MultiIndex):
        if len(tickers) == 1:
            df.columns = df.columns.get_level_values(0)
            df["ticker"] = tickers[0]
        else:
            df = df.set_index("date")
            df = df.stack(level=1, future_stack=True).reset_index()
            df = df.rename(columns={"Ticker": "ticker"})
    else:
        df["ticker"] = tickers[0]
    # Match column names
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    })
    df["date"] = pd.to_datetime(df["date"], utc=True)

    required_columns = ["ticker", "date", "open", "high", "low", "close", "volume"]
    df = df[required_columns]
    return df

def store_stock_data(df, database_url, table_name="stock_history"):
    try:
        with sqlite3.connect(database_url) as conn:
            df.to_sql(table_name, conn, if_exists="append", index=False)
            return True
    except sqlite3.OperationalError as e:
        print(e)
        return False
    except sqlite3.IntegrityError as e:
        print(e)
        return False

def fetch_store_stock_data(database_url, ticker, period, interval):
    df = fetch_stock_data(ticker, period, interval)
    return store_stock_data(df, database_url, table_name="stock_history")

def read_stock_rows(ticker, database_url, limit, table_name="stock_history"):
    try:
        tickers = [ticker] if isinstance(ticker, str) else list(ticker)
        tickers = [tick.strip().upper() for tick in tickers]

        if not tickers:
            return []

        placeholders = ", ".join("?" for _ in tickers)
        query = (
            f"SELECT * FROM {table_name} "
            f"WHERE ticker IN ({placeholders}) "
            "ORDER BY date DESC LIMIT ?"
        )

        with sqlite3.connect(database_url) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*tickers, limit))
            rows = [
                SimpleNamespace(
                    id=row[0],
                    ticker=row[1],
                    date=pd.to_datetime(row[2], utc=True).to_pydatetime(),
                    open=row[3],
                    high=row[4],
                    low=row[5],
                    close=row[6],
                    volume=row[7],
                )
                for row in cursor.fetchall()
            ]
            return sorted(rows, key=lambda item: item.date)
    except sqlite3.OperationalError as e:
        print(e)
        return []

def render_stock_table(rows):
    if not rows:
        return "No stock data available."

    data = [
        {
            "Ticker": row.ticker,
            "Datetime": row.date.strftime("%Y-%m-%d %H:%M:%S"),
            "Open": round(row.open, 2),
            "High": round(row.high, 2),
            "Low": round(row.low, 2),
            "Close": round(row.close, 2),
            "Volume": row.volume,
        }
        for row in rows
    ]

    frame = pd.DataFrame(data)
    return frame.to_string()

def print_stock_table(ticker, database_url, limit):
    rows = read_stock_rows(ticker, database_url, limit)
    print(render_stock_table(rows))