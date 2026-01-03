"""
Faculty-Course mapping model for Academic ERP.
"""
from datetime import datetime
from models import db


class FacultyCourseMap(db.Model):
    """Faculty-to-course assignment mapping."""
    
    __tablename__ = 'faculty_course_map'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)  # e.g., "2024-25"
    semester = db.Column(db.Integer, nullable=False)  # 1 or 2 (odd/even)
    section = db.Column(db.String(10))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint(
            'faculty_id', 'course_id', 'academic_year', 'semester', 'section',
            name='uq_faculty_course_assignment'
        ),
    )
    
    # Relationships
    faculty = db.relationship('FacultyUser', back_populates='course_assignments')
    course = db.relationship('Course', back_populates='faculty_assignments')
    
    def to_dict(self, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'faculty_id': self.faculty_id,
            'course_id': self.course_id,
            'academic_year': self.academic_year,
            'semester': self.semester,
            'section': self.section,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.faculty:
                data['faculty'] = {'id': self.faculty.id, 'name': self.faculty.name, 'email': self.faculty.email}
            if self.course:
                data['course'] = {'id': self.course.id, 'name': self.course.name, 'code': self.course.code}
        
        return data
    
    def __repr__(self):
        return f'<FacultyCourseMap {self.faculty_id} -> {self.course_id}>'
