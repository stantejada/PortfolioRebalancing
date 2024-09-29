from dotenv import load_dotenv
import os


basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    PORT = os.environ.get('PORT') or 5000
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'test.db')
    
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'site.db')