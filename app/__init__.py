
from flask import Flask
from config import Config
from .extensions import db,migrate,bcrypt,jwt
from app.models.token_blacklist import TokenBlacklist

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
    
    from app.routes.classroom import classroom_bp
    app.register_blueprint(classroom_bp,url_prefix="/api/classroom")
 
    return app



@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):

    jti = jwt_payload["jti"]

    token = TokenBlacklist.query.filter_by(jti=jti).first()

    return token is not None