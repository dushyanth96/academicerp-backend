"""
Admin controller for Academic ERP Backend.
"""
from flask import request
from services.admin_service import AdminService
from middlewares.auth import auth_required, admin_only
from utils.responses import (
    success_response, created_response, deleted_response, 
    not_found_response, paginated_response
)
from utils.validators import validate_required

class AdminController:
    """Controller for admin management endpoints."""
    
    # ==================== Programs ====================
    
    @staticmethod
    @auth_required
    @admin_only
    def get_programs():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        
        result = AdminService.get_programs(page, per_page, status, search)
        return paginated_response(
            result['items'], result['page'], result['per_page'], result['total']
        )
    
    @staticmethod
    @auth_required
    @admin_only
    def create_program():
        data = request.get_json()
        is_valid, missing = validate_required(data, ['name', 'code'])
        if not is_valid:
            return {'success': False, 'message': f'Missing: {", ".join(missing)}'}, 400
            
        program = AdminService.create_program(data)
        return created_response(program.to_dict())

    @staticmethod
    @auth_required
    @admin_only
    def update_program(id):
        data = request.get_json()
        program = AdminService.update_program(id, data)
        if not program:
            return not_found_response('Program')
        return success_response(program.to_dict(), 'Program updated successfully')

    @staticmethod
    @auth_required
    @admin_only
    def delete_program(id):
        success = AdminService.delete_program(id)
        if not success:
            return not_found_response('Program')
        return deleted_response('Program deleted successfully')

    # ==================== Branches ====================
    
    @staticmethod
    @auth_required
    @admin_only
    def get_branches():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        
        result = AdminService.get_branches(page, per_page, status, search)
        return paginated_response(result['items'], result['page'], result['per_page'], result['total'])

    @staticmethod
    @auth_required
    @admin_only
    def create_branch():
        data = request.get_json()
        is_valid, missing = validate_required(data, ['name', 'code'])
        if not is_valid:
            return {'success': False, 'message': f'Missing: {", ".join(missing)}'}, 400
        branch = AdminService.create_branch(data)
        return created_response(branch.to_dict())

    @staticmethod
    @auth_required
    @admin_only
    def update_branch(id):
        data = request.get_json()
        branch = AdminService.update_branch(id, data)
        if not branch:
            return not_found_response('Branch')
        return success_response(branch.to_dict(), 'Branch updated successfully')

    @staticmethod
    @auth_required
    @admin_only
    def delete_branch(id):
        success = AdminService.delete_branch(id)
        if not success:
            return not_found_response('Branch')
        return deleted_response('Branch deleted successfully')

    # ==================== Regulations ====================

    @staticmethod
    @auth_required
    @admin_only
    def get_regulations():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        
        result = AdminService.get_regulations(page, per_page, status)
        return paginated_response(result['items'], result['page'], result['per_page'], result['total'])

    @staticmethod
    @auth_required
    @admin_only
    def create_regulation():
        data = request.get_json()
        is_valid, missing = validate_required(data, ['name', 'code', 'year'])
        if not is_valid:
            return {'success': False, 'message': f'Missing: {", ".join(missing)}'}, 400
        regulation = AdminService.create_regulation(data)
        return created_response(regulation.to_dict())

    @staticmethod
    @auth_required
    @admin_only
    def update_regulation(id):
        data = request.get_json()
        regulation = AdminService.update_regulation(id, data)
        if not regulation:
            return not_found_response('Regulation')
        return success_response(regulation.to_dict(), 'Regulation updated successfully')

    @staticmethod
    @auth_required
    @admin_only
    def delete_regulation(id):
        success = AdminService.delete_regulation(id)
        if not success:
            return not_found_response('Regulation')
        return deleted_response('Regulation deleted successfully')

    # ==================== Courses ====================

    @staticmethod
    @auth_required
    @admin_only
    def get_courses():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        regulation_id = request.args.get('regulation_id')
        search = request.args.get('search')
        
        result = AdminService.get_courses(page, per_page, status, regulation_id, search)
        return paginated_response(result['items'], result['page'], result['per_page'], result['total'])

    @staticmethod
    @auth_required
    @admin_only
    def create_course():
        data = request.get_json()
        is_valid, missing = validate_required(data, ['name', 'code', 'regulation_id'])
        if not is_valid:
            return {'success': False, 'message': f'Missing: {", ".join(missing)}'}, 400
        course = AdminService.create_course(data)
        return created_response(course.to_dict())

    @staticmethod
    @auth_required
    @admin_only
    def update_course(id):
        data = request.get_json()
        course = AdminService.update_course(id, data)
        if not course:
            return not_found_response('Course')
        return success_response(course.to_dict(), 'Course updated successfully')

    @staticmethod
    @auth_required
    @admin_only
    def delete_course(id):
        success = AdminService.delete_course(id)
        if not success:
            return not_found_response('Course')
        return deleted_response('Course deleted successfully')

    # ==================== Faculty ====================
    
    @staticmethod
    @auth_required
    @admin_only
    def get_faculty():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        department = request.args.get('department')
        search = request.args.get('search')
        
        result = AdminService.get_faculty_users(page, per_page, status, department, search)
        return paginated_response(result['items'], result['page'], result['per_page'], result['total'])

    @staticmethod
    @auth_required
    @admin_only
    def create_faculty():
        data = request.get_json()
        required = ['email', 'name', 'supabase_user_id']
        is_valid, missing = validate_required(data, required)
        if not is_valid:
            return {'success': False, 'message': f'Missing: {", ".join(missing)}'}, 400
        faculty = AdminService.create_faculty_user(data)
        return created_response(faculty.to_dict())

    @staticmethod
    @auth_required
    @admin_only
    def update_faculty(id):
        data = request.get_json()
        faculty = AdminService.update_faculty_user(id, data)
        if not faculty:
            return not_found_response('Faculty')
        return success_response(faculty.to_dict(), 'Faculty updated successfully')

    @staticmethod
    @auth_required
    @admin_only
    def delete_faculty(id):
        success = AdminService.delete_faculty_user(id)
        if not success:
            return not_found_response('Faculty')
        return deleted_response('Faculty deleted successfully')

    @staticmethod
    @auth_required
    @admin_only
    def bulk_upload_faculty():
        data = request.get_json()  # Expecting list of faculty objects
        if not isinstance(data, list):
             return {'success': False, 'message': 'Expected list of faculty objects'}, 400
        
        created = []
        errors = []
        
        for index, item in enumerate(data):
            # Simplistic bulk logic - real world needs transaction or smart error reporting
            try:
                required = ['email', 'name', 'supabase_user_id']
                is_valid, missing = validate_required(item, required)
                if not is_valid:
                    errors.append(f"Row {index+1}: Missing {', '.join(missing)}")
                    continue
                    
                fac = AdminService.create_faculty_user(item)
                created.append(fac.to_dict())
            except Exception as e:
                errors.append(f"Row {index+1}: {str(e)}")
        
        return success_response({
            'created_count': len(created),
            'error_count': len(errors),
            'errors': errors
        }, 'Bulk upload processed')
