from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig
from flask_login import LoginManager
import logging

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view='auth.login'
logging.basicConfig(level=logging.INFO)


def create_app():
    app.config.from_object(DevelopmentConfig)
    
    #Initialize extensions
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    login.init_app(app=app)
    
    
    #import models
    # Import models
    with app.app_context():
        from app import models
    
    #Import Blueprints routes
    from .routes.index import main
    from .routes.auth import auth
    from .routes.portfolio import portfolio_bp
    
    #Register Blueprints
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolios')
    
    return app
