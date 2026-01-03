"""
Auth routes for Academic ERP Backend.
"""
from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/verify-token', methods=['GET'])(AuthController.verify_token)
