"""
Middlewares package for Academic ERP Backend.
"""
from middlewares.auth import auth_required, admin_only, faculty_only

__all__ = ['auth_required', 'admin_only', 'faculty_only']
