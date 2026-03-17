
from ..extensions import db


class User(db.Model):
    
    __tablename__ = "users"

    Uid = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    password=db.Column(db.String(100),nullable=True)
    
    # role = db.Column(db.String(50),nullable=False)
    
    google_id = db.Column(db.String(255), nullable=True)
    
    
    def to_dict(self):
        return {
            "id": self.Uid,
            "name": self.username,
            "email": self.email
        }
   
   
