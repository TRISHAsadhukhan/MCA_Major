
import os
from datetime import timedelta

class Config:
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}/"
        f"{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')