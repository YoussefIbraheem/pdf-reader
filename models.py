from datetime import datetime
from app import db  # SQLAlchemy instance

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    pdf_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship("Message", backref="conversation", lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversation.id"), nullable=False)
    sender = db.Column(db.String(10))  # 'user' or 'bot'
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
