# app/models/recording.py
from datetime import datetime
import os

from app import db


class Recording(db.Model):
    """Speech recording model"""
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=True)  # Original text field
    transcription = db.Column(db.Text, nullable=True)  # New transcription field
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Added for compatibility
    duration = db.Column(db.Float, nullable=True)  # Duration in seconds
    file_size = db.Column(db.Integer, nullable=True)  # Size in bytes
    original_filename = db.Column(db.String(255), nullable=True)  # Added for compatibility
    display_name = db.Column(db.String(255), nullable=True)  # Custom name field

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, filename, text=None, user_id=None, duration=None, file_size=None, original_filename=None, transcription=None, display_name=None):
        self.filename = filename
        self.text = text
        self.transcription = transcription  # Can be set directly
        self.user_id = user_id
        self.duration = duration
        self.file_size = file_size
        self.original_filename = original_filename or filename
        self.display_name = display_name or original_filename
        
        # For backward compatibility, set both text and transcription
        if text and not transcription:
            self.transcription = text
        elif transcription and not text:
            self.text = transcription

    @property
    def file_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOAD_FOLDER'], self.filename)
    
    def to_dict(self):
        """Convert recording to dictionary."""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'text': self.text,
            'transcription': self.transcription,
            'timestamp': self.timestamp.isoformat(),
            'created_at': self.created_at.isoformat() if self.created_at else self.timestamp.isoformat(),
            'duration': self.duration,
            'file_size': self.file_size,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f'<Recording {self.filename}>'