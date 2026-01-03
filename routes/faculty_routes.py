"""
Faculty routes for Academic ERP Backend.
"""
from flask import Blueprint
from controllers.faculty_controller import FacultyController

faculty_bp = Blueprint('faculty', __name__)

# Course Outcomes
faculty_bp.route('/course-outcomes', methods=['GET'])(FacultyController.get_course_outcomes)
faculty_bp.route('/course-outcomes', methods=['POST'])(FacultyController.create_course_outcome)
faculty_bp.route('/course-outcomes/<int:id>', methods=['PUT'])(FacultyController.update_course_outcome)
faculty_bp.route('/course-outcomes/<int:id>', methods=['DELETE'])(FacultyController.delete_course_outcome)

# Units
faculty_bp.route('/units', methods=['GET'])(FacultyController.get_units)
faculty_bp.route('/units', methods=['POST'])(FacultyController.create_unit)
faculty_bp.route('/units/<int:id>', methods=['PUT'])(FacultyController.update_unit)
faculty_bp.route('/units/<int:id>', methods=['DELETE'])(FacultyController.delete_unit)

# Levels
faculty_bp.route('/bloom-levels', methods=['GET'])(FacultyController.get_bloom_levels)
faculty_bp.route('/difficulty-levels', methods=['GET'])(FacultyController.get_difficulty_levels)
