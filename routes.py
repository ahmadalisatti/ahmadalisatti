from flask import Blueprint, jsonify, request
from .models import ExchangeRate
from app import app  # Import app for accessing the session

bp = Blueprint('main', __name__)

@bp.route('/convert')
def convert_currency():
    base = request.args.get("from")
    target = request.args.get("to")
    amount = request.args.get("amount", type=float)

    # Access the session from the app
    rate = app.session.query(ExchangeRate).filter_by(currency_from=base, currency_to=target).first()
    if rate:
        converted_amount = amount * rate.rate
        return jsonify({"converted_amount": converted_amount}), 200
    return jsonify({"error": "Conversion rate not available"}), 400

@bp.route("/rates")
def get_rates():
    rates = {f"{rate.currency_from}_{rate.currency_to}": rate.rate for rate in app.session.query(ExchangeRate).all()}
    return jsonify(rates), 200

@bp.route("/rate")
def get_rate():
    base = request.args.get("from")
    target = request.args.get("to")
    rate = app.session.query(ExchangeRate).filter_by(currency_from=base, currency_to=target).first()
    if rate:
        return jsonify({"rate": rate.rate}), 200
    return jsonify({"error": "Rate not found"}), 404
