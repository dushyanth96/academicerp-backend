"""
Admin service for Academic ERP Backend.
Handles business logic for admin operations on programs, branches, regulations, courses, and mappings.
"""
from utils.supabase_client import get_supabase_client


class AdminService:
    """Service class for admin operations."""
    
    # ==================== Programs ====================
    
    @staticmethod
    def get_programs(page=1, per_page=20, status=None, search=None):
        """Get paginated list of programs."""
        supabase = get_supabase_client()
        query = supabase.table('programs').select("*", count='exact')
        
        if status:
            query = query.eq('status', status)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(f"name.ilike.{search_pattern},code.ilike.{search_pattern}")
        
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.order('name').range(start, end).execute()
        
        return {
            'items': response.data,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_program(program_id):
        """Get a single program by ID."""
        supabase = get_supabase_client()
        response = supabase.table('programs').select("*").eq('id', program_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_program(data):
        """Create a new program."""
        supabase = get_supabase_client()
        payload = {
            'name': data['name'],
            'code': data['code'],
            'description': data.get('description'),
            'duration_years': data.get('duration_years', 4),
            'status': data.get('status', 'active')
        }
        response = supabase.table('programs').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_program(program_id, data):
        """Update an existing program."""
        supabase = get_supabase_client()
        response = supabase.table('programs').update(data).eq('id', program_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_program(program_id):
        """Delete a program."""
        supabase = get_supabase_client()
        response = supabase.table('programs').delete().eq('id', program_id).execute()
        return len(response.data) > 0
    
    # ==================== Branches ====================
    
    @staticmethod
    def get_branches(page=1, per_page=20, status=None, search=None):
        """Get paginated list of branches."""
        supabase = get_supabase_client()
        query = supabase.table('branches').select("*", count='exact')
        
        if status:
            query = query.eq('status', status)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(f"name.ilike.{search_pattern},code.ilike.{search_pattern}")
        
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.order('name').range(start, end).execute()
        
        return {
            'items': response.data,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_branch(branch_id):
        """Get a single branch by ID."""
        supabase = get_supabase_client()
        response = supabase.table('branches').select("*").eq('id', branch_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_branch(data):
        """Create a new branch."""
        supabase = get_supabase_client()
        payload = {
            'name': data['name'],
            'code': data['code'],
            'description': data.get('description'),
            'status': data.get('status', 'active')
        }
        response = supabase.table('branches').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_branch(branch_id, data):
        """Update an existing branch."""
        supabase = get_supabase_client()
        response = supabase.table('branches').update(data).eq('id', branch_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_branch(branch_id):
        """Delete a branch."""
        supabase = get_supabase_client()
        response = supabase.table('branches').delete().eq('id', branch_id).execute()
        return len(response.data) > 0
    
    # ==================== Regulations ====================
    
    @staticmethod
    def get_regulations(page=1, per_page=20, status=None):
        """Get paginated list of regulations."""
        supabase = get_supabase_client()
        query = supabase.table('regulations').select("*", count='exact')
        
        if status:
            query = query.eq('status', status)
        
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.order('year', desc=True).range(start, end).execute()
        
        return {
            'items': response.data,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_regulation(regulation_id):
        """Get a single regulation by ID."""
        supabase = get_supabase_client()
        response = supabase.table('regulations').select("*").eq('id', regulation_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_regulation(data):
        """Create a new regulation."""
        supabase = get_supabase_client()
        payload = {
            'name': data['name'],
            'code': data['code'],
            'year': data['year'],
            'description': data.get('description'),
            'status': data.get('status', 'active')
        }
        response = supabase.table('regulations').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_regulation(regulation_id, data):
        """Update an existing regulation."""
        supabase = get_supabase_client()
        response = supabase.table('regulations').update(data).eq('id', regulation_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_regulation(regulation_id):
        """Delete a regulation."""
        supabase = get_supabase_client()
        response = supabase.table('regulations').delete().eq('id', regulation_id).execute()
        return len(response.data) > 0
    
    # ==================== Courses ====================
    
    @staticmethod
    def get_courses(page=1, per_page=20, status=None, regulation_id=None, search=None):
        """Get paginated list of courses."""
        supabase = get_supabase_client()
        query = supabase.table('courses').select("*, regulations(name, code)", count='exact')
        
        if status:
            query = query.eq('status', status)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(f"name.ilike.{search_pattern},code.ilike.{search_pattern}")
        if regulation_id:
            query = query.eq('regulation_id', regulation_id)
        
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.order('code').range(start, end).execute()
        
        # Flatten nested response if necessary to match old to_dict format
        # Or just return as is if frontend can handle it. 
        # But old to_dict probably flattened 'regulations': {'name': ...} to 'regulation_name': ...
        # For simplicity, let's keep the structure close to what Supabase returns, 
        # but we might need to adjust frontend later or process items here.
        # Let's process items to be safe if we want to match legacy structure exactly.
        items = []
        for item in response.data:
            if item.get('regulations'):
                item['regulation_name'] = item['regulations']['name']
                item['regulation_code'] = item['regulations']['code']
            items.append(item)
            
        return {
            'items': items,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_course(course_id):
        """Get a single course by ID."""
        supabase = get_supabase_client()
        response = supabase.table('courses').select("*, regulations(name, code)").eq('id', course_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_course(data):
        """Create a new course."""
        supabase = get_supabase_client()
        payload = {
            'name': data['name'],
            'code': data['code'],
            'credits': data.get('credits', 3),
            'lecture_hours': data.get('lecture_hours', 3),
            'tutorial_hours': data.get('tutorial_hours', 1),
            'practical_hours': data.get('practical_hours', 0),
            'regulation_id': data['regulation_id'],
            'semester': data.get('semester'),
            'description': data.get('description'),
            'status': data.get('status', 'active')
        }
        response = supabase.table('courses').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_course(course_id, data):
        """Update an existing course."""
        supabase = get_supabase_client()
        response = supabase.table('courses').update(data).eq('id', course_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_course(course_id):
        """Delete a course."""
        supabase = get_supabase_client()
        response = supabase.table('courses').delete().eq('id', course_id).execute()
        return len(response.data) > 0
    
    # ==================== Program-Branch Mapping ====================
    
    @staticmethod
    def get_program_branch_maps(page=1, per_page=20, program_id=None, branch_id=None):
        """Get paginated list of program-branch mappings."""
        supabase = get_supabase_client()
        query = supabase.table('program_branch_map').select("*, programs(name, code), branches(name, code)", count='exact')
        
        if program_id:
            query = query.eq('program_id', program_id)
        if branch_id:
            query = query.eq('branch_id', branch_id)
        
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.range(start, end).execute()
        
        items = []
        for item in response.data:
            if item.get('programs'):
                item['program_name'] = item['programs']['name']
            if item.get('branches'):
                item['branch_name'] = item['branches']['name']
            items.append(item)
            
        return {
            'items': items,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def create_program_branch_map(data):
        """Create a new program-branch mapping."""
        supabase = get_supabase_client()
        payload = {
            'program_id': data['program_id'],
            'branch_id': data['branch_id'],
            'intake_capacity': data.get('intake_capacity', 60),
            'status': data.get('status', 'active')
        }
        response = supabase.table('program_branch_map').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_program_branch_map(mapping_id):
        """Delete a program-branch mapping."""
        supabase = get_supabase_client()
        response = supabase.table('program_branch_map').delete().eq('id', mapping_id).execute()
        return len(response.data) > 0
    
    # ==================== Branch-Course Mapping ====================
    
    @staticmethod
    def get_branch_course_maps(page=1, per_page=20, branch_id=None, course_id=None):
        """Get paginated list of branch-course mappings."""
        supabase = get_supabase_client()
        query = supabase.table('branch_course_map').select("*, branches(name, code), courses(name, code)", count='exact')
        
        if branch_id:
            query = query.eq('branch_id', branch_id)
        if course_id:
            query = query.eq('course_id', course_id)
        
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.range(start, end).execute()
        
        items = []
        for item in response.data:
            if item.get('branches'):
                item['branch_name'] = item['branches']['name']
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
    def create_branch_course_map(data):
        """Create a new branch-course mapping."""
        supabase = get_supabase_client()
        payload = {
            'branch_id': data['branch_id'],
            'course_id': data['course_id'],
            'semester': data['semester'],
            'is_elective': data.get('is_elective', False),
            'status': data.get('status', 'active')
        }
        response = supabase.table('branch_course_map').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_branch_course_map(mapping_id):
        """Delete a branch-course mapping."""
        supabase = get_supabase_client()
        response = supabase.table('branch_course_map').delete().eq('id', mapping_id).execute()
        return len(response.data) > 0
    
    # ==================== Faculty Users ====================
    
    @staticmethod
    def get_faculty_users(page=1, per_page=20, status=None, department=None, search=None):
        """Get paginated list of faculty users."""
        supabase = get_supabase_client()
        query = supabase.table('faculty_users').select("*", count='exact')
        
        if status:
            query = query.eq('status', status)
        if department:
            query = query.eq('department', department)
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(f"name.ilike.{search_pattern},email.ilike.{search_pattern},employee_id.ilike.{search_pattern}")
        
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.order('name').range(start, end).execute()
        
        return {
            'items': response.data,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_faculty_user(faculty_id):
        """Get a single faculty user by ID."""
        supabase = get_supabase_client()
        response = supabase.table('faculty_users').select("*").eq('id', faculty_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_faculty_by_supabase_id(supabase_user_id):
        """Get faculty user by Supabase user ID."""
        supabase = get_supabase_client()
        response = supabase.table('faculty_users').select("*").eq('supabase_user_id', supabase_user_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_faculty_user(data):
        """Create a new faculty user."""
        supabase = get_supabase_client()
        payload = {
            'supabase_user_id': data['supabase_user_id'],
            'email': data['email'],
            'name': data['name'],
            'employee_id': data.get('employee_id'),
            'department': data.get('department'),
            'designation': data.get('designation'),
            'phone': data.get('phone'),
            'role': data.get('role', 'faculty'),
            'status': data.get('status', 'active')
        }
        response = supabase.table('faculty_users').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_faculty_user(faculty_id, data):
        """Update an existing faculty user."""
        supabase = get_supabase_client()
        response = supabase.table('faculty_users').update(data).eq('id', faculty_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_faculty_user(faculty_id):
        """Delete a faculty user."""
        supabase = get_supabase_client()
        response = supabase.table('faculty_users').delete().eq('id', faculty_id).execute()
        return len(response.data) > 0
    
    # ==================== Faculty-Course Mapping ====================
    
    @staticmethod
    def get_faculty_course_maps(page=1, per_page=20, faculty_id=None, course_id=None, 
                                academic_year=None):
        """Get paginated list of faculty-course mappings."""
        supabase = get_supabase_client()
        query = supabase.table('faculty_course_map').select("*, courses(name, code), faculty_users(name, email)", count='exact')
        
        if faculty_id:
            query = query.eq('faculty_id', faculty_id)
        if course_id:
            query = query.eq('course_id', course_id)
        if academic_year:
            query = query.eq('academic_year', academic_year)
            
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.range(start, end).execute()
        
        items = []
        for item in response.data:
            if item.get('courses'):
                item['course_name'] = item['courses']['name']
                item['course_code'] = item['courses']['code']
            if item.get('faculty_users'):
                item['faculty_name'] = item['faculty_users']['name']
                item['faculty_email'] = item['faculty_users']['email']
            items.append(item)
            
        return {
            'items': items,
            'total': response.count,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def create_faculty_course_map(data):
        """Create a new faculty-course mapping."""
        supabase = get_supabase_client()
        payload = {
            'faculty_id': data['faculty_id'],
            'course_id': data['course_id'],
            'academic_year': data['academic_year'],
            'semester': data['semester'],
            'section': data.get('section'),
            'status': data.get('status', 'active')
        }
        response = supabase.table('faculty_course_map').insert(payload).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_faculty_course_map(mapping_id):
        """Delete a faculty-course mapping."""
        supabase = get_supabase_client()
        response = supabase.table('faculty_course_map').delete().eq('id', mapping_id).execute()
        return len(response.data) > 0
