"""
Paper controller for Academic ERP Backend.
"""
from flask import request, g, current_app
from services.paper_generation_service import PaperGenerationService
from middlewares.auth import auth_required, faculty_only
from utils.responses import (
    success_response, created_response, not_found_response, paginated_response
)
from utils.validators import validate_paper_generation_params

class PaperController:
    """Controller for question paper generation endpoints."""
    
    @staticmethod
    @auth_required
    @faculty_only
    def generate_paper():
        data = request.get_json()
        current_app.logger.info(f"Received paper generation request for course_id: {data.get('course_id')}")
        
        is_valid, errors = validate_paper_generation_params(data)
        if not is_valid:
            current_app.logger.warning(f"Validation failed for paper generation: {errors}")
            return {'success': False, 'errors': errors}, 400
            
        paper, error = PaperGenerationService.generate_paper(data, g.user.id)
        if error:
            current_app.logger.error(f"Paper generation failed: {error}")
            return {'success': False, 'message': error}, 400
            
        current_app.logger.info(f"Paper generated successfully: ID {paper.id}")
        return created_response(paper.to_dict(include_questions=True), message='Paper generated successfully')

    @staticmethod
    @auth_required
    def get_history():
        course_id = request.args.get('course_id', type=int)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # Admins can see all, faculty see their own (or course specific)
        faculty_id = None if g.user_role == 'admin' else g.user.id
        
        result = PaperGenerationService.get_history(course_id, faculty_id, page, limit)
        return paginated_response(
            result['items'], result['page'], result['per_page'], result['total']
        )

    @staticmethod
    @auth_required
    def get_paper(paper_id):
        result = PaperGenerationService.get_paper_details(paper_id)
        if not result:
            return not_found_response('Question Paper')
        return success_response(result)
