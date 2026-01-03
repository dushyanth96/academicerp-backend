"""
Unit model for Academic ERP.
"""
from datetime import datetime
from models import db


class Unit(db.Model):
    """Course unit/module."""
    
    __tablename__ = 'units'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    unit_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    topics = db.Column(db.Text)  # Comma-separated topics
    hours = db.Column(db.Integer, default=10)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('course_id', 'unit_number', name='uq_course_unit'),
    )
    
    # Relationships
    course = db.relationship('Course', back_populates='units')
    questions = db.relationship('Question', back_populates='unit', lazy='dynamic')
    
    def to_dict(self, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'unit_number': self.unit_number,
            'unit_label': f'Unit {self.unit_number}',
            'name': self.name,
            'description': self.description,
            'topics': self.topics.split(',') if self.topics else [],
            'hours': self.hours,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations and self.course:
            data['course'] = {'id': self.course.id, 'name': self.course.name, 'code': self.course.code}
        
        return data
    
    def __repr__(self):
        return f'<Unit {self.unit_number}: {self.name}>'
