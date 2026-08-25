import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_database_url():
    return os.getenv("DATABASE_URL", "./data/stock.db")
