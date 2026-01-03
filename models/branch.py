"""
Branch model for Academic ERP.
"""
from datetime import datetime
from models import db


class Branch(db.Model):
    """Academic branch/department (e.g., CSE, ECE, ME)."""
    
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    programs = db.relationship('ProgramBranchMap', back_populates='branch', lazy='dynamic')
    courses = db.relationship('BranchCourseMap', back_populates='branch', lazy='dynamic')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Branch {self.code}: {self.name}>'
