from app import create_app
from app import db

if __name__ == "__main__":
    
    main = create_app()
    
    with main.app_context():
        db.create_all()
        
    main.run()