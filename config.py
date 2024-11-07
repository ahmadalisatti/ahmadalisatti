import os

class Config:
    API_KEY = os.getenv("API_KEY", "cbe4b88bdfa2478300b13482")

    SQL_SERVER = {
        'DRIVER': 'ODBC Driver 17 for SQL Server',
        'SERVER': r'DESKTOP-SPCKMUD\SQLEXPRESS03',
        'DATABASE': 'CurrencyDB',
        'UID': 'ahmadalisatti',
        'PWD': 'knightfall0'
    }

    BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    UPDATE_INTERVAL = 86400  # in seconds
