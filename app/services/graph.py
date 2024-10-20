import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
from app import db
from app.models import Portfolio
import sqlalchemy as sa
from datetime import datetime, timezone


def download(tickers, last_date):
    try:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        start = min(last_date).strftime("%Y-%m-%d")
        data  =  yf.download(tickers, start=start, end=today)
        print(data)
        if data.empty:
            raise ValueError("Not data found for the tickers")
        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

def visualize(portfolio_id):
    
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    if not portfolio or not portfolio.stocks:
        return 
    
    tickers = [ ticker.symbol for ticker in portfolio.stocks]
    last_date = [ticker.last_position_date for ticker in portfolio.stocks]
    
    
    
    if not tickers:
        return
    
    data = download(tickers, last_date)
    
    if data is None:
        return
    
    
    adj_close_data = data['Adj Close']
    
    adj_close_data = adj_close_data.reset_index()
    
    melted_data = pd.melt(adj_close_data, id_vars='Date', var_name='Ticker', value_name='Adj Close')
    
    # Plot the data using seaborn and matplotlib
    plt.figure(figsize=(16, 8))
    sns.lineplot(data=melted_data, x='Date', y='Adj Close', hue='Ticker')
    plt.title(f"Price History (Adj Close) for Portfolio {portfolio.name}")
    plt.xlabel("Date")
    plt.ylabel("Adjusted Close Price")
    plt.legend(tickers)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
    
    
