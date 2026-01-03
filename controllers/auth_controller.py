"""
Auth controller for Academic ERP Backend.
"""
from flask import g
from middlewares.auth import auth_required
from utils.responses import success_response

class AuthController:
    """Controller for authentication related endpoints."""
    
    @staticmethod
    @auth_required
    def verify_token():
        """Verify the JWT token and return user info."""
        user = g.user
        role = g.user_role
        
        return success_response({
            'user': user.to_dict(),
            'role': role
        }, message='Token verified successfully')
