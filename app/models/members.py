from app.extensions import db
from datetime import datetime

class Members(db.Model):
    __tablename__ = "classroom_members"

    id = db.Column(db.Integer, primary_key=True)

    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("users.Uid"), nullable=False)   # renamed

    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_creator = db.Column(db.Boolean, default=False)   # NEW COLUMN
    
    def to_dict(self):
        return {
            "id": self.id,
            "classroom_id": self.classroom_id,
            "user_id": self.member_id,
            "joined_at": self.joined_at
        }