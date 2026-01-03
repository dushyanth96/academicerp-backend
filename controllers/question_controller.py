"""
Question controller for Academic ERP Backend.
"""
from flask import request, g
from services.question_service import QuestionService
from middlewares.auth import auth_required, faculty_only
from utils.responses import (
    success_response, created_response, deleted_response,
    paginated_response, not_found_response
)
from utils.validators import validate_question_data

class QuestionController:
    """Controller for question bank management endpoints."""
    
    @staticmethod
    @auth_required
    def get_questions():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        course_id = request.args.get('course_id', type=int)
        unit_id = request.args.get('unit_id', type=int)
        search_query = request.args.get('search')
        
        result = QuestionService.get_questions(
            page=page, per_page=per_page, 
            course_id=course_id, unit_id=unit_id,
            search_query=search_query
        )
        return paginated_response(
            result['items'], result['page'], result['per_page'], result['total']
        )

    @staticmethod
    @auth_required
    def get_question(id):
        question = QuestionService.get_question(id)
        if not question:
            return not_found_response('Question')
        return success_response(question.to_dict(include_relations=True))

    @staticmethod
    @auth_required
    @faculty_only
    def create_question():
        data = request.get_json()
        is_valid, errors = validate_question_data(data)
        if not is_valid:
            return {'success': False, 'errors': errors}, 400
            
        question = QuestionService.create_question(data, g.user.id)
        return created_response(question.to_dict())

    @staticmethod
    @auth_required
    @faculty_only
    def update_question(id):
        data = request.get_json()
        question = QuestionService.update_question(id, data)
        if not question:
            return not_found_response('Question')
        return success_response(question.to_dict(), 'Question updated successfully')

    @staticmethod
    @auth_required
    @faculty_only
    def delete_question(id):
        success = QuestionService.delete_question(id)
        if not success:
            return not_found_response('Question')
        return deleted_response('Question deleted successfully')

    @staticmethod
    @auth_required
    @faculty_only
    def bulk_upload():
        data = request.get_json()
        if not isinstance(data, list):
            return {'success': False, 'message': 'Data must be a list of questions'}, 400
            
        success, result = QuestionService.bulk_upload(data, g.user.id)
        if not success:
            return {'success': False, 'errors': result}, 400
            
        return success_response({'ids': result}, message=f'Successfully uploaded {len(result)} questions')
