"""
Standardized API response formatters for Academic ERP Backend.
"""
from flask import jsonify


def success_response(data=None, message=None, status_code=200):
    """
    Create a standardized success response.
    
    Args:
        data: Response data (dict, list, or None)
        message: Optional success message
        status_code: HTTP status code (default 200)
        
    Returns:
        Flask Response object
    """
    response = {
        'success': True
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(message, error_type='Error', status_code=400, details=None):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        error_type: Type of error (e.g., 'Validation Error', 'Not Found')
        status_code: HTTP status code (default 400)
        details: Optional additional error details
        
    Returns:
        Flask Response object
    """
    response = {
        'success': False,
        'error': error_type,
        'message': message
    }
    
    if details:
        response['details'] = details
    
    return jsonify(response), status_code


def paginated_response(items, page, per_page, total, message=None):
    """
    Create a standardized paginated response.
    
    Args:
        items: List of items for current page
        page: Current page number
        per_page: Items per page
        total: Total number of items
        message: Optional message
        
    Returns:
        Flask Response object
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
    
    response = {
        'success': True,
        'data': items,
        'meta': {
            'page': page,
            'limit': per_page,
            'total': total,
            'total_pages': total_pages
        }
    }
    
    if message:
        response['message'] = message
    
    return jsonify(response), 200


def created_response(data, message='Resource created successfully'):
    """Create response for successful resource creation."""
    return success_response(data, message, status_code=201)


def deleted_response(message='Resource deleted successfully'):
    """Create response for successful resource deletion."""
    return success_response(message=message)


def not_found_response(resource='Resource'):
    """Create response for resource not found."""
    return error_response(
        f'{resource} not found',
        error_type='Not Found',
        status_code=404
    )


def validation_error_response(errors):
    """
    Create response for validation errors.
    
    Args:
        errors: Dict or list of validation errors
    """
    return error_response(
        'Validation failed',
        error_type='Validation Error',
        status_code=400,
        details=errors
    )


def unauthorized_response(message='Authentication required'):
    """Create response for unauthorized access."""
    return error_response(message, error_type='Unauthorized', status_code=401)


def forbidden_response(message='Access denied'):
    """Create response for forbidden access."""
    return error_response(message, error_type='Forbidden', status_code=403)
