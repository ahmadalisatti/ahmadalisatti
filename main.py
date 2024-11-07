from app import create_app
from flask import jsonify, request
from app.models import ExchangeRate
from app.utils import fetch_exchange_rates
from app.config import Config  
from datetime import datetime, timedelta

app = create_app()

@app.before_first_request
def update_rates():
    with app.app_context():  
        last_update = app.session.query(ExchangeRate).order_by(ExchangeRate.timestamp.desc()).first()
        if not last_update or datetime.utcnow() - last_update.timestamp > timedelta(seconds=Config.UPDATE_INTERVAL):
            fetch_exchange_rates()

@app.route("/convert")
def convert_currency():
    base = request.args.get("from")
    target = request.args.get("to")
    amount = request.args.get("amount", type=float)

    with app.app_context():  
        rate = app.session.query(ExchangeRate).filter_by(currency_from=base, currency_to=target).first()
        if rate:
            converted_amount = amount * rate.rate
            return jsonify({"converted_amount": converted_amount}), 200
        return jsonify({"error": "Conversion rate not available"}), 400

@app.route("/rates")
def get_rates():
    with app.app_context():  
        rates = {f"{rate.currency_from}_{rate.currency_to}": rate.rate for rate in app.session.query(ExchangeRate).all()}
        return jsonify(rates), 200

@app.route("/rate")
def get_rate():
    base = request.args.get("from")
    target = request.args.get("to")

    with app.app_context(): 
        rate = app.session.query(ExchangeRate).filter_by(currency_from=base, currency_to=target).first()
        if rate:
            return jsonify({"rate": rate.rate}), 200
        return jsonify({"error": "Rate not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

