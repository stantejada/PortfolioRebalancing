from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app as app
from app import db
import yfinance as yf
from datetime import datetime
from app.models import Stock

def update_stock_prices(app):
    # Use the app context for database access
    with app.app_context():
        stocks = Stock.query.all()

        for stock in stocks:
            ticker = yf.Ticker(stock.symbol)
            stock_data = ticker.history(period='1d')
            
            if not stock_data.empty:
                last_price = stock_data['Close'].iloc[-1]
                stock.last_price = last_price
                stock.market_value = stock.shares * last_price
                stock.total_gain_value = (last_price * stock.shares) - stock.total_cost
                stock.total_gain_percent = (stock.total_gain_value / stock.total_cost) * 100

                db.session.commit()


# Scheduler setup function
def start_scheduler(app):
    scheduler = BackgroundScheduler()
    # Pass app to the update_stock_prices job
    scheduler.add_job(func=update_stock_prices, trigger="interval", minutes=1, args=[app])
    scheduler.start()

