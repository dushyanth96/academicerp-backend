"""
Admin routes for Academic ERP Backend.
"""
from flask import Blueprint
from controllers.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__)

# Programs
admin_bp.route('/programs', methods=['GET'])(AdminController.get_programs)
admin_bp.route('/programs', methods=['POST'])(AdminController.create_program)
admin_bp.route('/programs/<int:id>', methods=['PUT'])(AdminController.update_program)
admin_bp.route('/programs/<int:id>', methods=['DELETE'])(AdminController.delete_program)

# Branches
admin_bp.route('/branches', methods=['GET'])(AdminController.get_branches)
admin_bp.route('/branches', methods=['POST'])(AdminController.create_branch)
admin_bp.route('/branches/<int:id>', methods=['PUT'])(AdminController.update_branch)
admin_bp.route('/branches/<int:id>', methods=['DELETE'])(AdminController.delete_branch)

# Regulations
admin_bp.route('/regulations', methods=['GET'])(AdminController.get_regulations)
admin_bp.route('/regulations', methods=['POST'])(AdminController.create_regulation)
admin_bp.route('/regulations/<int:id>', methods=['PUT'])(AdminController.update_regulation)
admin_bp.route('/regulations/<int:id>', methods=['DELETE'])(AdminController.delete_regulation)

# Courses
admin_bp.route('/courses', methods=['GET'])(AdminController.get_courses)
admin_bp.route('/courses', methods=['POST'])(AdminController.create_course)
admin_bp.route('/courses/<int:id>', methods=['PUT'])(AdminController.update_course)
admin_bp.route('/courses/<int:id>', methods=['DELETE'])(AdminController.delete_course)

# Faculty Management
admin_bp.route('/faculty', methods=['GET'])(AdminController.get_faculty)
admin_bp.route('/faculty', methods=['POST'])(AdminController.create_faculty)
admin_bp.route('/faculty/<int:id>', methods=['PUT'])(AdminController.update_faculty)
admin_bp.route('/faculty/<int:id>', methods=['DELETE'])(AdminController.delete_faculty)
admin_bp.route('/faculty/upload', methods=['POST'])(AdminController.bulk_upload_faculty)
