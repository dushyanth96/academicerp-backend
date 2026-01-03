"""
Difficulty Level model for Academic ERP.
"""
from datetime import datetime
from models import db


class DifficultyLevel(db.Model):
    """Difficulty level for questions."""
    
    __tablename__ = 'difficulty_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, unique=True, nullable=False)  # 1-5
    name = db.Column(db.String(50), unique=True, nullable=False)  # Easy, Medium, Hard, etc.
    description = db.Column(db.Text)
    weight = db.Column(db.Float, default=1.0)  # For weighted selection
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', back_populates='difficulty', lazy='dynamic')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'level': self.level,
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<DifficultyLevel {self.level}: {self.name}>'
