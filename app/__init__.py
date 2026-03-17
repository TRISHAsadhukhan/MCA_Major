
from flask import Flask
from config import Config
from .extensions import db,migrate,bcrypt,jwt

def create_app():
    
    app=Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)


    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
  
  
    # register blueprints
    from app.routes.auth import auth
    app.register_blueprint(auth, url_prefix="/api/auth")
 
    return app