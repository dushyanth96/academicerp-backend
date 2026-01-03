"""
Branch-Course mapping model for Academic ERP.
"""
from datetime import datetime
from models import db


class BranchCourseMap(db.Model):
    """Many-to-many mapping between branches and courses."""
    
    __tablename__ = 'branch_course_map'
    
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    is_elective = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('branch_id', 'course_id', name='uq_branch_course'),
    )
    
    # Relationships
    branch = db.relationship('Branch', back_populates='courses')
    course = db.relationship('Course', back_populates='branches')
    
    def to_dict(self, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'branch_id': self.branch_id,
            'course_id': self.course_id,
            'semester': self.semester,
            'is_elective': self.is_elective,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.branch:
                data['branch'] = {'id': self.branch.id, 'name': self.branch.name, 'code': self.branch.code}
            if self.course:
                data['course'] = {'id': self.course.id, 'name': self.course.name, 'code': self.course.code}
        
        return data
    
    def __repr__(self):
        return f'<BranchCourseMap {self.branch_id} -> {self.course_id}>'
