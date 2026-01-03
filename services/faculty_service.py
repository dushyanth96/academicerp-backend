"""
Faculty service for Academic ERP Backend.
Handles business logic for faculty operations on course outcomes, bloom levels, difficulty levels, and units.
"""
from utils.supabase_client import get_supabase_client


class FacultyService:
    """Service class for faculty operations."""
    
    # ==================== Course Outcomes ====================
    
    @staticmethod
    def get_course_outcomes(course_id=None, status=None, search=None):
        """Get list of course outcomes."""
        supabase = get_supabase_client()
        query = supabase.table('course_outcomes').select("*, bloom_levels(name, description)")
        
        if course_id:
            query = query.eq('course_id', course_id)
        if status:
            query = query.eq('status', status)
        if search:
            query = query.ilike('description', f"%{search}%")
            
        response = query.order('co_number').execute()
        
        items = []
        for item in response.data:
            if item.get('bloom_levels'):
                item['bloom_level_name'] = item['bloom_levels']['name']
            items.append(item)
            
        return items
    
    @staticmethod
    def get_course_outcome(co_id):
        """Get a single course outcome by ID."""
        supabase = get_supabase_client()
        response = supabase.table('course_outcomes').select("*, bloom_levels(name)").eq('id', co_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_course_outcome(data):
        """Create a new course outcome."""
        supabase = get_supabase_client()
        payload = {
            'course_id': data['course_id'],
            'co_number': data['co_number'],
            'description': data['description'],
            'bloom_level_id': data.get('bloom_level_id'),
            'status': data.get('status', 'active')
        }
        response = supabase.table('course_outcomes').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_course_outcome(co_id, data):
        """Update an existing course outcome."""
        supabase = get_supabase_client()
        response = supabase.table('course_outcomes').update(data).eq('id', co_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_course_outcome(co_id):
        """Delete a course outcome."""
        supabase = get_supabase_client()
        response = supabase.table('course_outcomes').delete().eq('id', co_id).execute()
        return len(response.data) > 0
    
    # ==================== Bloom Levels ====================
    
    @staticmethod
    def get_bloom_levels():
        """Get all bloom levels."""
        supabase = get_supabase_client()
        response = supabase.table('bloom_levels').select("*").order('level').execute()
        return response.data
        
    @staticmethod
    def create_bloom_level(data):
        """Create a new bloom level."""
        supabase = get_supabase_client()
        payload = {
            'level': data['level'],
            'name': data['name'],
            'description': data.get('description'),
            'keywords': data.get('keywords', ''),
            'status': data.get('status', 'active')
        }
        response = supabase.table('bloom_levels').insert(payload).execute()
        return response.data[0] if response.data else None
        
    # ==================== Difficulty Levels ====================
    
    @staticmethod
    def get_difficulty_levels():
        """Get all difficulty levels."""
        supabase = get_supabase_client()
        response = supabase.table('difficulty_levels').select("*").order('level').execute()
        return response.data
        
    @staticmethod
    def create_difficulty_level(data):
        """Create a new difficulty level."""
        supabase = get_supabase_client()
        payload = {
            'level': data['level'],
            'name': data['name'],
            'description': data.get('description'),
            'weight': data.get('weight', 1.0),
            'status': data.get('status', 'active')
        }
        response = supabase.table('difficulty_levels').insert(payload).execute()
        return response.data[0] if response.data else None
        
    # ==================== Units ====================
    
    @staticmethod
    def get_units(course_id=None, status=None, search=None):
        """Get list of units for a course."""
        supabase = get_supabase_client()
        query = supabase.table('units').select("*")
        
        if course_id:
            query = query.eq('course_id', course_id)
        if status:
            query = query.eq('status', status)
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(f"name.ilike.{search_pattern},description.ilike.{search_pattern}")
            
        response = query.order('unit_number').execute()
        return response.data
    
    @staticmethod
    def get_unit(unit_id):
        """Get a single unit by ID."""
        supabase = get_supabase_client()
        response = supabase.table('units').select("*").eq('id', unit_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_unit(data):
        """Create a new unit."""
        supabase = get_supabase_client()
        payload = {
            'course_id': data['course_id'],
            'unit_number': data['unit_number'],
            'name': data['name'],
            'description': data.get('description'),
            'topics': data.get('topics', ''),
            'hours': data.get('hours', 10),
            'status': data.get('status', 'active')
        }
        response = supabase.table('units').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_unit(unit_id, data):
        """Update an existing unit."""
        supabase = get_supabase_client()
        response = supabase.table('units').update(data).eq('id', unit_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_unit(unit_id):
        """Delete a unit."""
        supabase = get_supabase_client()
        response = supabase.table('units').delete().eq('id', unit_id).execute()
        return len(response.data) > 0
