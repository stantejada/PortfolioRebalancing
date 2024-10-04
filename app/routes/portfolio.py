from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request
from app.forms import CreatePortfolioForm, AddStockForm
from flask_login import login_required, current_user
from app.models import Stock, Portfolio, User
from app import db
import sqlalchemy as sa
import yfinance as yf
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler

portfolio_bp = Blueprint('portfolio', __name__)



#GET ALL PORTFOLIOS
@portfolio_bp.route('/', methods=['GET','POST'])
@login_required
def portfolios():
    
    portfolios = Portfolio.query.filter(Portfolio.user_id == current_user.id).all()
    
    
    form = CreatePortfolioForm()
    
    if form.validate_on_submit():
        portfolio = Portfolio(user_id = current_user.id, name=form.name.data)
        db.session.add(portfolio)
        db.session.commit()
        flash(f'Portfolio has been created', 'success')
        return redirect(url_for('portfolio.portfolios'))
    
    
    return render_template('portfolios.html', title='Portfolios', form=form, portfolios=portfolios)


@portfolio_bp.route('/portfolio/<int:portfolio_id>', methods=['GET', 'POST'])
def portfolio_details(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    form = AddStockForm()
    if form.validate_on_submit():
        symbol = form.symbol.data
        shares = form.shares.data
        cost_per_share = form.cost.data
        date = form.date.data
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        #stock data
        ticker = yf.Ticker(symbol)
        
        history = ticker.history(start=date, end=today)
  
        if history.empty:
            flash(f'No stock data found for {symbol} on {date}', 'danger')
            return redirect(url_for('portfolio.portfolio_details', portfolio_id=portfolio_id))
        
        #extract stock closing
        
        try:
            last_price = history['Close'].iloc[-1]  # Closing price from history
        except IndexError:
            # Fallback to the latest price if no historical data for the date
            last_price = ticker.info.get('regularMarketPrice', cost_per_share)
        
        market_value = shares * last_price
        total_cost = shares * cost_per_share
        avg_cost_per_share = cost_per_share
        day_gain_value = (last_price - cost_per_share) * shares
        day_gain_percent = (last_price - cost_per_share)/cost_per_share * 100
        total_gain_value = (last_price * shares) - total_cost
        total_gain_percent = (total_gain_value / total_cost) * 100
        
        new_stock = Stock(
            portfolio_id = portfolio.id,
            company = ticker.info['longName'],
            industry = ticker.info['industry'],
            symbol = symbol,
            last_price = last_price,
            currency = ticker.info['currency'],
            price_change = last_price - cost_per_share,
            percent_change = day_gain_percent,
            shares = shares,
            market_value = market_value,
            daily_gain_value = day_gain_value,
            daily_gain_percent = day_gain_percent,
            total_cost = total_cost,
            total_gain_value = total_gain_value,
            total_gain_percent = total_gain_percent,
            avg_cost_per_share = avg_cost_per_share,
            last_position_date = date
        )
        db.session.add(new_stock)
        db.session.commit()
        flash('Stock has been added', 'success')
        return redirect(url_for('portfolio.portfolio_details', portfolio_id=portfolio_id))
        
    # Calculate statistics for the portfolio
    total_market_value = sum(stock.market_value for stock in portfolio.stocks)
    total_gain_value = sum(stock.total_gain_value for stock in portfolio.stocks)
    total_gain_percent = (total_gain_value / total_market_value) * 100 if total_market_value > 0 else 0
    total_cost = sum(stock.total_cost for stock in portfolio.stocks)
    
    # Optional: Risk or sector breakdown (if stock has sector info)
    sector_breakdown = {}
    for stock in portfolio.stocks:
        sector = stock.industry if hasattr(stock, 'sector') else 'Unknown'
        sector_breakdown[sector] = sector_breakdown.get(sector, 0) + stock.market_value
    
    return render_template('_portfolio.html', title='Portfolio Details', form=form, portfolio=portfolio,
                           total_market_value=total_market_value,
                           total_gain_value=total_gain_value,
                           total_gain_percent=total_gain_percent,
                           total_cost=total_cost,
                           sector_breakdown=sector_breakdown)
    
    

@portfolio_bp.route('/portfolio/<int:portfolio_id>/stock/<int:stock_id>')
def delete_stock(portfolio_id,stock_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    stock = Stock.query.get_or_404(stock_id)
    
    if stock in portfolio.stocks:
        portfolio.stocks.remove(stock)
        db.session.delete(stock)
        db.session.commit()
        return redirect(url_for('portfolio.portfolio_details', portfolio_id=portfolio_id))
    return render_template('portfolio.html')