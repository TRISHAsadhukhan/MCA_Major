from app.extensions import db
from datetime import datetime

class Classroom(db.Model):
    __tablename__ = "classrooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    room_key = db.Column(db.String(8),nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey("users.Uid"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "room_key": self.room_key,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": self.created_at
        }