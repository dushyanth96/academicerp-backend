"""
Database models package for Academic ERP Backend.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models for easy access
from models.program import Program
from models.branch import Branch
from models.regulation import Regulation
from models.course import Course
from models.program_branch_map import ProgramBranchMap
from models.branch_course_map import BranchCourseMap
from models.faculty import FacultyUser
from models.faculty_course_map import FacultyCourseMap
from models.course_outcome import CourseOutcome
from models.bloom_level import BloomLevel
from models.difficulty_level import DifficultyLevel
from models.unit import Unit
from models.question import Question
from models.generated_paper import GeneratedPaper
from models.generated_question import GeneratedQuestion

__all__ = [
    'db',
    'Program',
    'Branch',
    'Regulation',
    'Course',
    'ProgramBranchMap',
    'BranchCourseMap',
    'FacultyUser',
    'FacultyCourseMap',
    'CourseOutcome',
    'BloomLevel',
    'DifficultyLevel',
    'Unit',
    'Question',
    'GeneratedPaper',
    'GeneratedQuestion'
]
