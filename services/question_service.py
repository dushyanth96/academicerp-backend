"""
Question service for Academic ERP Backend.
Handles business logic for question bank management.
"""
from utils.supabase_client import get_supabase_client


class QuestionService:
    """Service class for question bank operations."""
    
    @staticmethod
    def get_questions(page=1, per_page=20, course_id=None, unit_id=None, 
                      co_id=None, bloom_level_id=None, difficulty_id=None, 
                      search_query=None, status='active'):
        """Get paginated and filtered questions."""
        supabase = get_supabase_client()
        query = supabase.table('questions').select(
            "*, course_outcomes(description, co_number), bloom_levels(name), difficulty_levels(name), units(name, unit_number), courses(name, code)",
            count='exact'
        )
        
        if status:
            query = query.eq('status', status)
        if course_id:
            query = query.eq('course_id', course_id)
        if unit_id:
            query = query.eq('unit_id', unit_id)
        if co_id:
            query = query.eq('co_id', co_id)
        if bloom_level_id:
            query = query.eq('bloom_level_id', bloom_level_id)
        if difficulty_id:
            query = query.eq('difficulty_id', difficulty_id)
            
        if search_query:
            query = query.ilike('question_text', f"%{search_query}%")
            
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.order('created_at', desc=True).range(start, end).execute()
        
        items = []
        for item in response.data:
            # Flatten or format relations if needed for frontend consistency
            if item.get('course_outcomes'):
                item['co_description'] = item['course_outcomes']['description']
                item['co_number'] = item['course_outcomes']['co_number']
            if item.get('bloom_levels'):
                item['bloom_level_name'] = item['bloom_levels']['name']
            if item.get('difficulty_levels'):
                item['difficulty_level_name'] = item['difficulty_levels']['name']
            if item.get('units'):
                item['unit_name'] = item['units']['name']
                item['unit_number'] = item['units']['unit_number']
            if item.get('courses'):
                item['course_name'] = item['courses']['name']
                item['course_code'] = item['courses']['code']
            items.append(item)
        
        return {
            'items': items,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_question(question_id):
        """Get a single question by ID."""
        supabase = get_supabase_client()
        query = supabase.table('questions').select(
            "*, course_outcomes(description, co_number), bloom_levels(name), difficulty_levels(name), units(name, unit_number), courses(name, code)"
        ).eq('id', question_id)
        
        response = query.execute()
        
        if response.data:
            item = response.data[0]
            # Consistency formatting
            if item.get('course_outcomes'):
                item['co_description'] = item['course_outcomes']['description']
                item['co_number'] = item['course_outcomes']['co_number']
            if item.get('bloom_levels'):
                item['bloom_level_name'] = item['bloom_levels']['name']
            if item.get('difficulty_levels'):
                item['difficulty_level_name'] = item['difficulty_levels']['name']
            if item.get('units'):
                item['unit_name'] = item['units']['name']
                item['unit_number'] = item['units']['unit_number']
            if item.get('courses'):
                item['course_name'] = item['courses']['name']
                item['course_code'] = item['courses']['code']
            return item
            
        return None
    
    @staticmethod
    def create_question(data, faculty_id):
        """Create a new question."""
        supabase = get_supabase_client()
        payload = {
            'course_id': data['course_id'],
            'unit_id': data['unit_id'],
            'co_id': data['co_id'],
            'bloom_level_id': data['bloom_level_id'],
            'difficulty_id': data['difficulty_id'],
            'faculty_id': faculty_id,
            'question_text': data['question_text'],
            'question_type': data.get('question_type', 'descriptive'),
            'marks': data['marks'],
            'expected_time_minutes': data.get('expected_time_minutes'),
            'options': data.get('options'),
            'correct_answer': data.get('correct_answer'),
            'image_url': data.get('image_url'),
            'tags': ','.join(data.get('tags', [])),
            'status': data.get('status', 'active')
        }
        response = supabase.table('questions').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_question(question_id, data):
        """Update an existing question."""
        supabase = get_supabase_client()
        
        # Prepare payload from data, only including fields that are present
        payload = {}
        for field in ['course_id', 'unit_id', 'co_id', 'bloom_level_id', 
                      'difficulty_id', 'question_text', 'question_type', 
                      'marks', 'expected_time_minutes', 'options', 
                      'correct_answer', 'image_url', 'status']:
            if field in data:
                payload[field] = data[field]
        
        if 'tags' in data:
            payload['tags'] = ','.join(data['tags'])
            
        if not payload:
            return None
            
        response = supabase.table('questions').update(payload).eq('id', question_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_question(question_id):
        """Delete a question."""
        supabase = get_supabase_client()
        response = supabase.table('questions').delete().eq('id', question_id).execute()
        return len(response.data) > 0
    
    @staticmethod
    def bulk_upload(questions_data, faculty_id):
        """
        Bulk upload questions using Supabase batch insert.
        Supabase/PostgREST performs atomic inserts for batch requests, usually.
        If one fails, all might fail depending on configuraiton, but here we construct payload.
        """
        supabase = get_supabase_client()
        payloads = []
        
        for q_data in questions_data:
            payloads.append({
                'course_id': q_data['course_id'],
                'unit_id': q_data['unit_id'],
                'co_id': q_data['co_id'],
                'bloom_level_id': q_data['bloom_level_id'],
                'difficulty_id': q_data['difficulty_id'],
                'faculty_id': faculty_id,
                'question_text': q_data['question_text'],
                'marks': q_data['marks'],
                'question_type': q_data.get('question_type', 'descriptive'),
                'status': 'active'
                # Add default other fields if needed or let DB default handle them
            })
            
        if not payloads:
            return False, ["No data provided"]

        try:
            response = supabase.table('questions').insert(payloads).execute()
            if response.data:
                return True, [q['id'] for q in response.data]
            return False, ["Upload failed silently"]
        except Exception as e:
            return False, [str(e)]
