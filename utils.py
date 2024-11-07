import requests
from .models import db, ExchangeRate
from datetime import datetime
from flask import current_app as app

def fetch_exchange_rates():
    url = f"https://api.example.com/rates?apikey={app.config['API_KEY']}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for rate in data['rates']:
            exchange_rate = ExchangeRate(
                base_currency=rate['base'],
                target_currency=rate['target'],
                rate=rate['rate'],
                timestamp=datetime.utcnow()
            )
            db.session.merge(exchange_rate)  
        db.session.commit()
    else:
        print("Failed to fetch exchange rates.")
