"""
Bloom Level model for Academic ERP.
"""
from datetime import datetime
from models import db


class BloomLevel(db.Model):
    """Bloom's Taxonomy level for questions."""
    
    __tablename__ = 'bloom_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, unique=True, nullable=False)  # 1-6
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    keywords = db.Column(db.Text)  # Comma-separated keywords
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', back_populates='bloom_level', lazy='dynamic')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'level': self.level,
            'name': self.name,
            'description': self.description,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<BloomLevel {self.level}: {self.name}>'
