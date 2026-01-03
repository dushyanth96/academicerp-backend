"""
Authentication middleware for Academic ERP Backend.
Validates Supabase JWT tokens and enforces role-based access control.
"""
import jwt
from functools import wraps
from flask import request, jsonify, g, current_app
from utils.supabase_client import get_supabase_client


def get_token_from_header():
    """Extract JWT token from Authorization header."""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    # Support both "Bearer <token>" and just "<token>"
    parts = auth_header.split()
    
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2 and parts[0].lower() == 'bearer':
        return parts[1]
    
    return None


def decode_supabase_jwt(token):
    """
    Decode and validate Supabase JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload or None if invalid
    """
    jwt_secret = current_app.config.get('SUPABASE_JWT_SECRET')
    
    if not jwt_secret:
        current_app.logger.error('SUPABASE_JWT_SECRET not configured')
        return None
    
    try:
        # Supabase uses HS256 algorithm
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=['HS256'],
            audience='authenticated'
        )
        return payload
    except jwt.ExpiredSignatureError:
        current_app.logger.warning('JWT token expired')
        return None
    except jwt.InvalidTokenError as e:
        current_app.logger.warning(f'Invalid JWT token: {e}')
        return None


def get_user_from_token(payload):
    """
    Get or create user from JWT payload.
    
    Args:
        payload: Decoded JWT payload
        
    Returns:
        User dictionary or None
    """
    supabase_user_id = payload.get('sub')
    email = payload.get('email')
    
    if not supabase_user_id:
        return None
    
    supabase = get_supabase_client()
    
    # Try to find existing user by supabase_user_id
    response = supabase.table('faculty_users').select("*").eq('supabase_user_id', supabase_user_id).execute()
    
    if response.data:
        return response.data[0]
    
    # Check if user exists by email (for linking)
    response = supabase.table('faculty_users').select("*").eq('email', email).execute()
    if response.data:
        user = response.data[0]
        # Link existing user to Supabase
        supabase.table('faculty_users').update({'supabase_user_id': supabase_user_id}).eq('id', user['id']).execute()
        # Return updated user
        updated_response = supabase.table('faculty_users').select("*").eq('id', user['id']).execute()
        return updated_response.data[0] if updated_response.data else None
    
    return None


def get_role_from_token(payload, user=None):
    """
    Extract role from JWT payload or user record.
    
    Supabase stores custom claims in:
    - user_metadata (set during signup)
    - app_metadata (set via Supabase admin API)
    
    Args:
        payload: Decoded JWT payload
        user: Optional FacultyUser instance
        
    Returns:
        Role string ('admin', 'faculty', or None)
    """
    # Check app_metadata first (admin-set, more trusted)
    app_metadata = payload.get('app_metadata', {})
    role = app_metadata.get('role')
    
    if not role:
        # Fall back to user_metadata
        user_metadata = payload.get('user_metadata', {})
        role = user_metadata.get('role')
    
    if not role and user:
        # Fall back to database role
        role = user.get('role')
    
    return role


def auth_required(f):
    """
    Decorator to require authentication.
    Validates JWT and populates g.user and g.token_payload.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_header()
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'Authentication token is required'
            }), 401
        
        payload = decode_supabase_jwt(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'Invalid or expired token'
            }), 401
        
        # Get user from database
        user = get_user_from_token(payload)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'User not found in system. Please contact administrator.'
            }), 401
        
        if user.get('status') != 'active':
            return jsonify({
                'success': False,
                'error': 'Forbidden',
                'message': 'User account is inactive'
            }), 403
        
        # Get role
        role = get_role_from_token(payload, user)
        
        # Store in Flask global context
        g.user = user
        g.token_payload = payload
        g.user_role = role
        
        return f(*args, **kwargs)
    
    return decorated


def admin_only(f):
    """
    Decorator to require admin role.
    Must be used after @auth_required.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Ensure auth_required has been called
        if not hasattr(g, 'user') or not g.user:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401
        
        role = getattr(g, 'user_role', None)
        
        if role != 'admin':
            current_app.logger.warning(
                f"Admin access denied for user {g.user.get('email')} with role {role}"
            )
            return jsonify({
                'success': False,
                'error': 'Forbidden',
                'message': 'Admin access required'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated


def faculty_only(f):
    """
    Decorator to require faculty role (includes admin).
    Must be used after @auth_required.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Ensure auth_required has been called
        if not hasattr(g, 'user') or not g.user:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401
        
        role = getattr(g, 'user_role', None)
        
        # Admin can access faculty routes too
        if role not in ['admin', 'faculty']:
            current_app.logger.warning(
                f"Faculty access denied for user {g.user.get('email')} with role {role}"
            )
            return jsonify({
                'success': False,
                'error': 'Forbidden',
                'message': 'Faculty access required'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated


def get_current_user():
    """Helper function to get current authenticated user."""
    return getattr(g, 'user', None)


def get_current_user_role():
    """Helper function to get current user's role."""
    return getattr(g, 'user_role', None)


def is_admin():
    """Check if current user is admin."""
    return get_current_user_role() == 'admin'


def is_faculty():
    """Check if current user is faculty (or admin)."""
    return get_current_user_role() in ['admin', 'faculty']
