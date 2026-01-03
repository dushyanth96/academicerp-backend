"""
Faculty user model for Academic ERP.
"""
from datetime import datetime
from models import db


class FacultyUser(db.Model):
    """Faculty user linked to Supabase Auth."""
    
    __tablename__ = 'faculty_users'
    
    id = db.Column(db.Integer, primary_key=True)
    supabase_user_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    employee_id = db.Column(db.String(50), unique=True)
    department = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='faculty')  # admin, faculty
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course_assignments = db.relationship('FacultyCourseMap', back_populates='faculty', lazy='dynamic')
    questions = db.relationship('Question', back_populates='faculty', lazy='dynamic')
    generated_papers = db.relationship('GeneratedPaper', back_populates='faculty', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_faculty_supabase_id', 'supabase_user_id'),
        db.Index('idx_faculty_email', 'email'),
    )
    
    def to_dict(self, include_assignments=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'supabase_user_id': self.supabase_user_id,
            'email': self.email,
            'name': self.name,
            'employee_id': self.employee_id,
            'department': self.department,
            'designation': self.designation,
            'phone': self.phone,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_assignments:
            data['course_assignments'] = [
                assignment.to_dict(include_relations=True) 
                for assignment in self.course_assignments.all()
            ]
        
        return data
    
    def __repr__(self):
        return f'<FacultyUser {self.email}>'
