"""
Paper routes for Academic ERP Backend.
"""
from flask import Blueprint
from controllers.paper_controller import PaperController

paper_bp = Blueprint('paper', __name__)

paper_bp.route('/generate', methods=['POST'])(PaperController.generate_paper)
paper_bp.route('/history', methods=['GET'])(PaperController.get_history)
paper_bp.route('/<int:paper_id>', methods=['GET'])(PaperController.get_paper)
