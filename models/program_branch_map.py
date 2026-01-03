"""
Program-Branch mapping model for Academic ERP.
"""
from datetime import datetime
from models import db


class ProgramBranchMap(db.Model):
    """Many-to-many mapping between programs and branches."""
    
    __tablename__ = 'program_branch_map'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    intake_capacity = db.Column(db.Integer, default=60)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('program_id', 'branch_id', name='uq_program_branch'),
    )
    
    # Relationships
    program = db.relationship('Program', back_populates='branches')
    branch = db.relationship('Branch', back_populates='programs')
    
    def to_dict(self, include_relations=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'program_id': self.program_id,
            'branch_id': self.branch_id,
            'intake_capacity': self.intake_capacity,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.program:
                data['program'] = {'id': self.program.id, 'name': self.program.name, 'code': self.program.code}
            if self.branch:
                data['branch'] = {'id': self.branch.id, 'name': self.branch.name, 'code': self.branch.code}
        
        return data
    
    def __repr__(self):
        return f'<ProgramBranchMap {self.program_id} -> {self.branch_id}>'
