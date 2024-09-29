from flask import Blueprint, render_template

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/')
def portfolios():
    return render_template('portfolios.html', title='Portfolios')