"""
Generated Question model for Academic ERP.
"""
from datetime import datetime
from models import db


class GeneratedQuestion(db.Model):
    """Mapping of questions to generated papers."""
    
    __tablename__ = 'generated_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('generated_papers.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    
    section = db.Column(db.String(10), nullable=False)  # A, B, C
    question_number = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    is_compulsory = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_gq_paper', 'paper_id'),
        db.UniqueConstraint('paper_id', 'section', 'question_number', name='uq_paper_section_qnum'),
    )
    
    # Relationships
    paper = db.relationship('GeneratedPaper', back_populates='questions')
    question = db.relationship('Question', back_populates='generated_mappings')
    
    def to_dict(self, include_question=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'paper_id': self.paper_id,
            'question_id': self.question_id,
            'section': self.section,
            'question_number': self.question_number,
            'marks': self.marks,
            'is_compulsory': self.is_compulsory,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_question and self.question:
            data['question'] = self.question.to_dict(include_relations=True)
        
        return data
    
    def __repr__(self):
        return f'<GeneratedQuestion Paper:{self.paper_id} Q:{self.question_number}>'
