"""
Question model for Academic ERP.
"""
from datetime import datetime
from models import db


class Question(db.Model):
    """Question bank entry."""
    
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    co_id = db.Column(db.Integer, db.ForeignKey('course_outcomes.id'), nullable=False)
    bloom_level_id = db.Column(db.Integer, db.ForeignKey('bloom_levels.id'), nullable=False)
    difficulty_id = db.Column(db.Integer, db.ForeignKey('difficulty_levels.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_users.id'), nullable=False)
    
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default='descriptive')  # mcq, descriptive, numerical
    marks = db.Column(db.Integer, nullable=False, default=2)
    expected_time_minutes = db.Column(db.Integer)
    
    # For MCQ questions
    options = db.Column(db.JSON)  # List of options
    correct_answer = db.Column(db.Text)
    
    # Metadata
    image_url = db.Column(db.String(500))
    tags = db.Column(db.Text)  # Comma-separated tags
    usage_count = db.Column(db.Integer, default=0)  # Track how many times used
    last_used_at = db.Column(db.DateTime)
    
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for efficient filtering
    __table_args__ = (
        db.Index('idx_question_course', 'course_id'),
        db.Index('idx_question_unit', 'unit_id'),
        db.Index('idx_question_co', 'co_id'),
        db.Index('idx_question_bloom', 'bloom_level_id'),
        db.Index('idx_question_difficulty', 'difficulty_id'),
        db.Index('idx_question_marks', 'marks'),
        db.Index('idx_question_status', 'status'),
    )
    
    # Relationships
    course = db.relationship('Course', back_populates='questions')
    unit = db.relationship('Unit', back_populates='questions')
    course_outcome = db.relationship('CourseOutcome', back_populates='questions')
    bloom_level = db.relationship('BloomLevel', back_populates='questions')
    difficulty = db.relationship('DifficultyLevel', back_populates='questions')
    faculty = db.relationship('FacultyUser', back_populates='questions')
    generated_mappings = db.relationship('GeneratedQuestion', back_populates='question', lazy='dynamic')
    
    def to_dict(self, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'unit_id': self.unit_id,
            'co_id': self.co_id,
            'bloom_level_id': self.bloom_level_id,
            'difficulty_id': self.difficulty_id,
            'faculty_id': self.faculty_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'marks': self.marks,
            'expected_time_minutes': self.expected_time_minutes,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'image_url': self.image_url,
            'tags': self.tags.split(',') if self.tags else [],
            'usage_count': self.usage_count,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.course:
                data['course'] = {'id': self.course.id, 'name': self.course.name, 'code': self.course.code}
            if self.unit:
                data['unit'] = {'id': self.unit.id, 'unit_number': self.unit.unit_number, 'name': self.unit.name}
            if self.course_outcome:
                data['course_outcome'] = {'id': self.course_outcome.id, 'co_number': self.course_outcome.co_number}
            if self.bloom_level:
                data['bloom_level'] = {'id': self.bloom_level.id, 'level': self.bloom_level.level, 'name': self.bloom_level.name}
            if self.difficulty:
                data['difficulty'] = {'id': self.difficulty.id, 'level': self.difficulty.level, 'name': self.difficulty.name}
            if self.faculty:
                data['faculty'] = {'id': self.faculty.id, 'name': self.faculty.name}
        
        return data
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'
