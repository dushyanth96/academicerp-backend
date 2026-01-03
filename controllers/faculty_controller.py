"""
Faculty controller for Academic ERP Backend.
"""
from flask import request
from services.faculty_service import FacultyService
from middlewares.auth import auth_required, faculty_only
from utils.responses import (
    success_response, created_response, deleted_response,
    not_found_response
)
from utils.validators import validate_required

class FacultyController:
    """Controller for faculty management endpoints."""
    
    # ==================== Course Outcomes ====================
    
    @staticmethod
    @auth_required
    @faculty_only
    def get_course_outcomes():
        course_id = request.args.get('course_id', type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        result = FacultyService.get_course_outcomes(course_id, status, search)
        return success_response(result)

    @staticmethod
    @auth_required
    @faculty_only
    def create_course_outcome():
        data = request.get_json()
        is_valid, missing = validate_required(data, ['course_id', 'co_number', 'description'])
        if not is_valid:
            return {'success': False, 'message': f'Missing fields: {", ".join(missing)}'}, 400
        co = FacultyService.create_course_outcome(data)
        return created_response(co.to_dict())

    @staticmethod
    @auth_required
    @faculty_only
    def update_course_outcome(id):
        data = request.get_json()
        co = FacultyService.update_course_outcome(id, data)
        if not co:
            return not_found_response('Course Outcome')
        return success_response(co.to_dict(), 'Course Outcome updated successfully')

    @staticmethod
    @auth_required
    @faculty_only
    def delete_course_outcome(id):
        success = FacultyService.delete_course_outcome(id)
        if not success:
            return not_found_response('Course Outcome')
        return deleted_response('Course Outcome deleted successfully')

    # ==================== Units ====================
    
    @staticmethod
    @auth_required
    @faculty_only
    def get_units():
        course_id = request.args.get('course_id', type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        result = FacultyService.get_units(course_id, status, search)
        return success_response(result)

    @staticmethod
    @auth_required
    @faculty_only
    def create_unit():
        data = request.get_json()
        is_valid, missing = validate_required(data, ['course_id', 'unit_number', 'name'])
        if not is_valid:
            return {'success': False, 'message': f'Missing fields: {", ".join(missing)}'}, 400
        unit = FacultyService.create_unit(data)
        return created_response(unit.to_dict())

    @staticmethod
    @auth_required
    @faculty_only
    def update_unit(id):
        data = request.get_json()
        unit = FacultyService.update_unit(id, data)
        if not unit:
            return not_found_response('Unit')
        return success_response(unit.to_dict(), 'Unit updated successfully')

    @staticmethod
    @auth_required
    @faculty_only
    def delete_unit(id):
        success = FacultyService.delete_unit(id)
        if not success:
            return not_found_response('Unit')
        return deleted_response('Unit deleted successfully')

    # ==================== Bloom Levels ====================
    
    @staticmethod
    @auth_required
    def get_bloom_levels():
        result = FacultyService.get_bloom_levels()
        return success_response(result)

    # ==================== Difficulty Levels ====================
    
    @staticmethod
    @auth_required
    def get_difficulty_levels():
        result = FacultyService.get_difficulty_levels()
        return success_response(result)
