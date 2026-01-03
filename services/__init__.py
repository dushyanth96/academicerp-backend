"""
Services package for Academic ERP Backend.
"""
from services.admin_service import AdminService
from services.faculty_service import FacultyService
from services.question_service import QuestionService
from services.paper_generation_service import PaperGenerationService

__all__ = [
    'AdminService',
    'FacultyService', 
    'QuestionService',
    'PaperGenerationService'
]
