"""
Course Outcome model for Academic ERP.
"""
from datetime import datetime
from models import db


class CourseOutcome(db.Model):
    """Course outcome (CO) for a course."""
    
    __tablename__ = 'course_outcomes'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    co_number = db.Column(db.Integer, nullable=False)  # CO1, CO2, etc.
    description = db.Column(db.Text, nullable=False)
    bloom_level_id = db.Column(db.Integer, db.ForeignKey('bloom_levels.id'))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('course_id', 'co_number', name='uq_course_co'),
    )
    
    # Relationships
    course = db.relationship('Course', back_populates='outcomes')
    bloom_level = db.relationship('BloomLevel')
    questions = db.relationship('Question', back_populates='course_outcome', lazy='dynamic')
    
    def to_dict(self, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'co_number': self.co_number,
            'co_label': f'CO{self.co_number}',
            'description': self.description,
            'bloom_level_id': self.bloom_level_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.bloom_level:
                data['bloom_level'] = self.bloom_level.to_dict()
            if self.course:
                data['course'] = {'id': self.course.id, 'name': self.course.name, 'code': self.course.code}
        
        return data
    
    def __repr__(self):
        return f'<CourseOutcome CO{self.co_number} for Course {self.course_id}>'
