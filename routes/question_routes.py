"""
Question routes for Academic ERP Backend.
"""
from flask import Blueprint
from controllers.question_controller import QuestionController

question_bp = Blueprint('questions', __name__)

question_bp.route('/', methods=['GET'])(QuestionController.get_questions)
question_bp.route('/', methods=['POST'])(QuestionController.create_question)
question_bp.route('/<int:id>', methods=['GET'])(QuestionController.get_question)
question_bp.route('/<int:id>', methods=['PUT'])(QuestionController.update_question)
question_bp.route('/<int:id>', methods=['DELETE'])(QuestionController.delete_question)
question_bp.route('/bulk-upload', methods=['POST'])(QuestionController.bulk_upload)
