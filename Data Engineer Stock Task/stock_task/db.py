import sqlite3

delete_table_sql = "DROP TABLE IF EXISTS stock_history;"
create_table_sql = """
    CREATE TABLE IF NOT EXISTS stock_history (
    id INTEGER PRIMARY KEY, 
    ticker text NOT NULL,
    date DATE NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume INTEGER,
    UNIQUE (ticker, date)
    );"""

def connection_test(database_url):
    try:
        with sqlite3.connect(database_url) as conn:
            cursor = conn.cursor()
            return True
    except sqlite3.OperationalError as e:
        print(e)
        return False

def init_db(database_url):
    try:
        with sqlite3.connect(database_url) as conn:
            cursor = conn.cursor()
            cursor.execute(delete_table_sql)
            cursor.execute(create_table_sql)  
            conn.commit()
            return True

    except sqlite3.OperationalError as e:
        print(e)
        return False

def drop_table(database_url):
    try:
        with sqlite3.connect(database_url) as conn:
            cursor = conn.cursor()
            cursor.execute(delete_table_sql)
            conn.commit()
            return True

    except sqlite3.OperationalError as e:
        print(e)
        return False

def create_table(database_url):
    try:
        with sqlite3.connect(database_url) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
            return True

    except sqlite3.OperationalError as e:
        print(e)
        return False
