# Data Engineer Stock Task

This project fetches stock history from Yahoo Finance, stores the OHLCV data in SQLite, and prints the latest rows in the terminal.

## Project structure

- `stock_task/` — application code
- `.env` — local configuration
- `data/` — database files

## Running

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```

3. Fetch stock data, initialize the database, and print the latest rows:
   ```bash
   py -m stock_task --reset-db --ticker AAPL --period 5d --interval 1d --limit 5
   ```

## CLI usage

Fetch Apple stock data and save it to the default SQLite database:

```bash
py -m stock_task --ticker AAPL --period 1mo --interval 1d
```

Fetch multiple symbols:

```bash
py -m stock_task --ticker AAPL MSFT NVDA --period 1mo --interval 1d --limit 5
```

Fetch data without outputting:

```bash
py -m stock_task --fetch-only
```

All parameters:

```bash
py -m stock_task --h
```

## Database schema

The database file is `./data/stock.db` and the table is `stock_history`. 
This structure was chosen as it stores all relevant stock data for potentially multiple stock tickers within a single table.
Each row represents a single ticker, on a single date, with constraints added to reduce risk of duplication.


It stores:

   id INTEGER PRIMARY KEY,  
   ticker text NOT NULL,  
   date DATE NOT NULL,  
   open FLOAT,  
   high FLOAT,  
   low FLOAT,  
   close FLOAT,  
   volume INTEGER,  
   UNIQUE (ticker, date)  


## Improvements with more time
With more time on the task, or if it was a task with stake holder interaction, I would have tried to get hold of more detailed requirements e.g. What data to retrieve from the stock API, if there is a preferred schema, what the data is being used for, the desired granularity.  

There was also scope for additional tables to be introduced within the database, containing other stock data that is retrievable by the API, as I have just limited it to the data from a single call. Company information, quarterly financial statements, analyst price targets etc. For a more complex task, metadata may be useful in the data table, storing ingestion timestamps to track when data is inserted, if records can be updated - a timestamp to retain when it was changed. Historical data may also be important to maintain for certain record updates.  

Program wise, additional error handling would be an important addition, I've tried to cover some easy to run into areas I am aware that it probably is quite an easy program to break. End to end and unit tests would be a useful way to find if there are process issues that are possible to run into, indicating where error handling may be of use. There is also no user input sanitisation, allowing a malicious user to cause any problem they desire with sql injection.  

The UI is very basic, just using the CLI and user prompts, with more time a dedicated GUI could be created, making the user experience more pleasing, while potentially reducing errors that can be run into with the use of buttons rather than free text fields.  

I did attempt to use Docker to containerise the program but could not get it working on my personal machine, having never used Docker before I thought this was a good opportunity to learn how it works so that was unfortunate! With more time I hopefully would have been able to solve the issue that I was running into.
