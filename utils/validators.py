"""
Input validation utilities for Academic ERP Backend.
"""
import re
from typing import Any, List, Dict, Optional, Tuple


def validate_required(data: dict, fields: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that required fields are present and not empty.
    
    Args:
        data: Request data dictionary
        fields: List of required field names
        
    Returns:
        Tuple of (is_valid, list of missing fields)
    """
    missing = []
    
    for field in fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    
    return len(missing) == 0, missing


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_positive_int(value: Any, allow_zero: bool = False) -> bool:
    """
    Validate that value is a positive integer.
    
    Args:
        value: Value to validate
        allow_zero: Whether to allow zero
        
    Returns:
        True if valid, False otherwise
    """
    try:
        int_value = int(value)
        if allow_zero:
            return int_value >= 0
        return int_value > 0
    except (TypeError, ValueError):
        return False


def validate_in_list(value: Any, allowed_values: List[Any]) -> bool:
    """
    Validate that value is in allowed list.
    
    Args:
        value: Value to validate
        allowed_values: List of allowed values
        
    Returns:
        True if valid, False otherwise
    """
    return value in allowed_values


def validate_string_length(value: str, min_length: int = 0, max_length: int = None) -> bool:
    """
    Validate string length.
    
    Args:
        value: String to validate
        min_length: Minimum length (default 0)
        max_length: Maximum length (default None = no limit)
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    length = len(value)
    
    if length < min_length:
        return False
    
    if max_length is not None and length > max_length:
        return False
    
    return True


def validate_status(status: str) -> bool:
    """Validate status field value."""
    return validate_in_list(status, ['active', 'inactive'])


def sanitize_string(value: str) -> str:
    """
    Sanitize string input to prevent XSS.
    
    Args:
        value: String to sanitize
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return value
    
    # Basic HTML entity encoding
    return (
        value
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#x27;')
    )


def validate_pagination_params(page: Any, per_page: Any, max_per_page: int = 100) -> Dict:
    """
    Validate and normalize pagination parameters.
    
    Args:
        page: Page number
        per_page: Items per page
        max_per_page: Maximum allowed items per page
        
    Returns:
        Dict with validated page and per_page values
    """
    try:
        page = max(1, int(page))
    except (TypeError, ValueError):
        page = 1
    
    try:
        per_page = min(max(1, int(per_page)), max_per_page)
    except (TypeError, ValueError):
        per_page = 20
    
    return {'page': page, 'per_page': per_page}


def validate_question_data(data: dict) -> Tuple[bool, List[str]]:
    """
    Validate question creation/update data.
    
    Args:
        data: Question data dictionary
        
    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors = []
    
    # Required fields
    required_fields = ['course_id', 'unit_id', 'co_id', 'bloom_level_id', 
                       'difficulty_id', 'question_text', 'marks']
    is_valid, missing = validate_required(data, required_fields)
    
    if not is_valid:
        errors.extend([f'{field} is required' for field in missing])
    
    # Validate marks
    if 'marks' in data and not validate_positive_int(data['marks']):
        errors.append('marks must be a positive integer')
    
    # Validate question type
    if 'question_type' in data:
        valid_types = ['mcq', 'descriptive', 'numerical', 'short_answer']
        if not validate_in_list(data['question_type'], valid_types):
            errors.append(f'question_type must be one of: {", ".join(valid_types)}')
    
    # Validate MCQ options if question type is MCQ
    if data.get('question_type') == 'mcq':
        if not data.get('options') or not isinstance(data['options'], list):
            errors.append('MCQ questions require options array')
        if not data.get('correct_answer'):
            errors.append('MCQ questions require correct_answer')
    
    return len(errors) == 0, errors


def validate_paper_generation_params(data: dict) -> Tuple[bool, List[str]]:
    """
    Validate question paper generation parameters for AI-driven engine.
    """
    errors = []
    
    # Required Base Fields
    required_fields = ['course_id', 'total_marks', 'program', 'branch', 
                       'course', 'course_code', 'regulation', 'semester', 
                       'assessment_type']
    
    is_valid, missing = validate_required(data, required_fields)
    if not is_valid:
        errors.extend([f'{field} is required' for field in missing])
    
    # Validate numeric fields
    if 'total_marks' in data and not validate_positive_int(data['total_marks']):
        errors.append('total_marks must be a positive integer')
    
    # Distribution mappings (if provided)
    distributions = ['co_coverage', 'bloom_distribution', 'difficulty_distribution', 'unit_coverage']
    for dist in distributions:
        if dist in data and not isinstance(data[dist], dict):
            errors.append(f'{dist} must be a valid JSON object/dictionary')
    
    # Validate sections if provided
    sections = data.get('sections', [])
    if sections:
        for i, section in enumerate(sections):
            if not section.get('name'):
                errors.append(f'Section {i+1}: name is required')
            if not validate_positive_int(section.get('marks_per_question', 0)):
                errors.append(f'Section {i+1}: marks_per_question must be positive')
            if not validate_positive_int(section.get('total_questions', 0)):
                errors.append(f'Section {i+1}: total_questions must be positive')
    
    return len(errors) == 0, errors
