from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig
from flask_login import LoginManager
import logging
from flasgger import Swagger

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view='auth.login'
logging.basicConfig(level=logging.INFO)
swagger=Swagger()


def create_app():
    app.config.from_object(DevelopmentConfig)
    
    #Initialize extensions
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    login.init_app(app=app)
    swagger.init_app(app=app)
    
    #extensions
    from .scheduler import start_scheduler
    start_scheduler(app)
    
    
    #import models
    # Import models
    with app.app_context():
        from app import models
    
    #Import Blueprints routes
    from .routes.index import main
    from .routes.auth import auth
    from .routes.portfolio import portfolio_bp
    
    #Import Blueprints API
    from .api.user import api as user_api
    
    #Register Blueprints
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolios')
    
    #Register Blueprints API
    app.register_blueprint(user_api, url_prefix='/api')
    
    return app
