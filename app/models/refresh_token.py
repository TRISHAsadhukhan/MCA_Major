
from ..extensions import db
from datetime import datetime

class RefreshToken(db.Model):

    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    token = db.Column(db.String(500), unique=True, nullable=False)

    is_revoked = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)