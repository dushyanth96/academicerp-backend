"""
Course model for Academic ERP.
"""
from datetime import datetime
from models import db


class Course(db.Model):
    """Academic course."""
    
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=3)
    lecture_hours = db.Column(db.Integer, default=3)
    tutorial_hours = db.Column(db.Integer, default=1)
    practical_hours = db.Column(db.Integer, default=0)
    regulation_id = db.Column(db.Integer, db.ForeignKey('regulations.id'), nullable=False)
    semester = db.Column(db.Integer)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint for code within a regulation
    __table_args__ = (
        db.UniqueConstraint('code', 'regulation_id', name='uq_course_code_regulation'),
    )
    
    # Relationships
    regulation = db.relationship('Regulation', back_populates='courses')
    branches = db.relationship('BranchCourseMap', back_populates='course', lazy='dynamic')
    faculty_assignments = db.relationship('FacultyCourseMap', back_populates='course', lazy='dynamic')
    outcomes = db.relationship('CourseOutcome', back_populates='course', lazy='dynamic')
    units = db.relationship('Unit', back_populates='course', lazy='dynamic')
    questions = db.relationship('Question', back_populates='course', lazy='dynamic')
    generated_papers = db.relationship('GeneratedPaper', back_populates='course', lazy='dynamic')
    
    def to_dict(self, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'credits': self.credits,
            'lecture_hours': self.lecture_hours,
            'tutorial_hours': self.tutorial_hours,
            'practical_hours': self.practical_hours,
            'regulation_id': self.regulation_id,
            'semester': self.semester,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations and self.regulation:
            data['regulation'] = {
                'id': self.regulation.id,
                'name': self.regulation.name,
                'code': self.regulation.code
            }
        
        return data
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'
