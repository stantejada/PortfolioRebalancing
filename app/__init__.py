from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app.config.from_object(DevelopmentConfig)
    
    #Initialize extensions
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    
    
    from . import routes
    
    return app
