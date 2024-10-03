from typing import Optional, List
import sqlalchemy as sa 
import sqlalchemy.orm as so
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app import login
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    
    #user Data
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False, unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, index=True, unique=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    remember_me: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False)
   
    #Relationship to portfolio One-to-Many
    portfolios: so.Mapped[List[Optional['Portfolio']]] = so.relationship('Portfolio', back_populates='user')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_json(self):
        return {
            'username' : self.username,
            'email' : self.email
        }
    
class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False, index=True)
    
    #relationship back to user
    user: so.Mapped["User"] = so.relationship("User", back_populates='portfolios')
    
    #One-to-Many relationship: A portfolio can have multiples stocks
    stocks: so.Mapped[List[Optional["Stock"]]] = so.relationship("Stock", back_populates='portfolios')
    
class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    portfolio_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('portfolios.id'), nullable=False)
    
    #Relationship back to portfolio
    portfolios: so.Mapped["Portfolio"] = so.relationship('Portfolio', back_populates='stocks')
    
    #Stock Details
    company: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    symbol: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=False)
    last_price: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    currency: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=False)
    price_change: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    percent_change: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    shares: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    market_value: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    daily_gain_value: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    daily_gain_percent: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    
    total_cost: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    total_gain_value: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)  # Calculated field
    total_gain_percent: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)  # Calculated field
    
    avg_cost_per_share: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)  # Total cost / shares
    last_position_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    
    def calculate_total_gain(self):
        """
        Calculate total gain in value and percentage based on the last price and total cost.
        """
        self.total_gain_value = (self.last_price * self.shares) - self.total_cost
        self.total_gain_percent = (self.total_gain_value / self.total_cost) * 100 if self.total_cost != 0 else 0
        
    def calculate_market_value(self):
        """
        Calculate the market value based on the last price and number of shares.
        """
        self.market_value = self.last_price * self.shares
    
    def calculate_avg_cost_per_share(self):
        """
        Calculate the average cost per share based on total cost and number of shares.
        """
        self.avg_cost_per_share = self.total_cost / self.shares if self.shares != 0 else 0
    


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))