"""
Generated Paper model for Academic ERP.
"""
from datetime import datetime
from models import db


class GeneratedPaper(db.Model):
    """Generated question paper."""
    
    __tablename__ = 'generated_papers'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_users.id'), nullable=False)
    
    # Paper metadata
    title = db.Column(db.String(300))
    exam_type = db.Column(db.String(50))  # midterm, semester, quiz
    academic_year = db.Column(db.String(20))
    semester = db.Column(db.Integer)
    duration_minutes = db.Column(db.Integer, default=180)
    total_marks = db.Column(db.Integer, nullable=False)
    
    # Generation parameters (stored for reference)
    generation_params = db.Column(db.JSON)
    """
    Example generation_params:
    {
        "total_marks": 100,
        "sections": [
            {"name": "A", "marks_per_question": 2, "total_questions": 10, "total_marks": 20},
            {"name": "B", "marks_per_question": 5, "total_questions": 5, "select": 4, "total_marks": 20},
            {"name": "C", "marks_per_question": 10, "total_questions": 5, "select": 4, "total_marks": 40}
        ],
        "unit_coverage": {"1": 20, "2": 20, "3": 20, "4": 20, "5": 20},
        "bloom_distribution": {"1-2": 30, "3-4": 50, "5-6": 20},
        "difficulty_distribution": {"easy": 30, "medium": 50, "hard": 20}
    }
    """
    
    # Analytics
    question_count = db.Column(db.Integer)
    unit_coverage = db.Column(db.JSON)  # Actual coverage achieved
    bloom_distribution = db.Column(db.JSON)  # Actual distribution
    difficulty_distribution = db.Column(db.JSON)  # Actual distribution
    
    status = db.Column(db.String(20), default='draft')  # draft, finalized, used
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_paper_course', 'course_id'),
        db.Index('idx_paper_faculty', 'faculty_id'),
        db.Index('idx_paper_created', 'created_at'),
    )
    
    # Relationships
    course = db.relationship('Course', back_populates='generated_papers')
    faculty = db.relationship('FacultyUser', back_populates='generated_papers')
    questions = db.relationship('GeneratedQuestion', back_populates='paper', lazy='dynamic',
                               cascade='all, delete-orphan')
    
    def to_dict(self, include_questions=False, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'faculty_id': self.faculty_id,
            'title': self.title,
            'exam_type': self.exam_type,
            'academic_year': self.academic_year,
            'semester': self.semester,
            'duration_minutes': self.duration_minutes,
            'total_marks': self.total_marks,
            'generation_params': self.generation_params,
            'question_count': self.question_count,
            'unit_coverage': self.unit_coverage,
            'bloom_distribution': self.bloom_distribution,
            'difficulty_distribution': self.difficulty_distribution,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.course:
                data['course'] = {'id': self.course.id, 'name': self.course.name, 'code': self.course.code}
            if self.faculty:
                data['faculty'] = {'id': self.faculty.id, 'name': self.faculty.name}
        
        if include_questions:
            data['questions'] = [
                gq.to_dict(include_question=True) 
                for gq in self.questions.order_by('section', 'question_number').all()
            ]
        
        return data
    
    def __repr__(self):
        return f'<GeneratedPaper {self.id}: {self.title}>'
