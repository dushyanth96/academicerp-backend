import logging
import time
from dotenv import load_dotenv
from utils.supabase_client import get_supabase_client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """Seed the Supabase database with initial demo data."""
    supabase = get_supabase_client()
    
    logger.info("Starting database seeding via REST API...")
    
    # 1. Bloom Levels
    bloom_levels = [
        {"level": 1, "name": "Remember", "description": "Recall facts and basic concepts", "keywords": "define, duplicate, list, memorize, repeat, state"},
        {"level": 2, "name": "Understand", "description": "Explain ideas or concepts", "keywords": "classify, describe, discuss, explain, identify, locate, recognize, report, select, translate"},
        {"level": 3, "name": "Apply", "description": "Use information in new situations", "keywords": "execute, implement, solve, use, demonstrate, interpret, operate, schedule, sketch"},
        {"level": 4, "name": "Analyze", "description": "Draw connections among ideas", "keywords": "differentiate, organize, relate, compare, contrast, distinguish, examine, experiment, question, test"},
        {"level": 5, "name": "Evaluate", "description": "Justify a stand or decision", "keywords": "appraise, argue, defend, judge, select, support, value, critique, weigh"},
        {"level": 6, "name": "Create", "description": "Produce new or original work", "keywords": "design, assemble, construct, conjecture, develop, formulate, author, investigate"}
    ]
    
    logger.info("Seeding Bloom Levels...")
    for bl in bloom_levels:
        existing = supabase.table('bloom_levels').select('id').eq('level', bl['level']).execute()
        if not existing.data:
            supabase.table('bloom_levels').insert(bl).execute()
    
    # 2. Difficulty Levels
    difficulty_levels = [
        {"level": 1, "name": "Easy", "weight": 1.0},
        {"level": 2, "name": "Medium", "weight": 1.5},
        {"level": 3, "name": "Hard", "weight": 2.0}
    ]
    
    logger.info("Seeding Difficulty Levels...")
    for dl in difficulty_levels:
        existing = supabase.table('difficulty_levels').select('id').eq('level', dl['level']).execute()
        if not existing.data:
            supabase.table('difficulty_levels').insert(dl).execute()

    # 3. Programs
    logger.info("Seeding Programs...")
    program_payload = {"name": "Bachelor of Technology", "code": "B.Tech", "duration_years": 4, "status": "active"}
    prog_res = supabase.table('programs').select('id').eq('code', 'B.Tech').execute()
    
    if prog_res.data:
        program_id = prog_res.data[0]['id']
    else:
        res = supabase.table('programs').insert(program_payload).execute()
        program_id = res.data[0]['id']
        
    # 4. Branches
    logger.info("Seeding Branches...")
    branch_payload = {"name": "Computer Science and Engineering", "code": "CSE", "status": "active"}
    branch_res = supabase.table('branches').select('id').eq('code', 'CSE').execute()
    
    if branch_res.data:
        branch_id = branch_res.data[0]['id']
    else:
        res = supabase.table('branches').insert(branch_payload).execute()
        branch_id = res.data[0]['id']
        
    # 5. Program-Branch Map
    logger.info("Mapping Program to Branch...")
    map_res = supabase.table('program_branch_map').select('id').eq('program_id', program_id).eq('branch_id', branch_id).execute()
    if not map_res.data:
        supabase.table('program_branch_map').insert({
            "program_id": program_id, "branch_id": branch_id, "intake_capacity": 120
        }).execute()

    # 6. Regulations
    logger.info("Seeding Regulations...")
    reg_payload = {"name": "Regulation 2024", "code": "R24", "year": 2024, "status": "active"}
    reg_res = supabase.table('regulations').select('id').eq('code', 'R24').execute()
    
    if reg_res.data:
        regulation_id = reg_res.data[0]['id']
    else:
        res = supabase.table('regulations').insert(reg_payload).execute()
        regulation_id = res.data[0]['id']

    # 7. Courses
    logger.info("Seeding Courses...")
    courses = [
        {"name": "Data Structures", "code": "CS201", "credits": 4, "semester": 3, "regulation_id": regulation_id},
        {"name": "Database Management Systems", "code": "CS202", "credits": 3, "semester": 4, "regulation_id": regulation_id},
        {"name": "Artificial Intelligence", "code": "CS301", "credits": 3, "semester": 5, "regulation_id": regulation_id}
    ]
    
    course_ids = {}
    for c in courses:
        existing = supabase.table('courses').select('id').eq('code', c['code']).execute()
        if existing.data:
            course_ids[c['code']] = existing.data[0]['id']
        else:
            res = supabase.table('courses').insert(c).execute()
            course_ids[c['code']] = res.data[0]['id']
            
    # Map Courses to Branch
    for code, cid in course_ids.items():
        existing = supabase.table('branch_course_map').select('id').eq('course_id', cid).eq('branch_id', branch_id).execute()
        if not existing.data:
            supabase.table('branch_course_map').insert({
                "branch_id": branch_id, "course_id": cid, "semester": 3 if code=='CS201' else 4
            }).execute()

    # 8. Faculty Users
    logger.info("Seeding Faculty Users...")
    users = [
        {
            "email": "admin@academicerp.com",
            "name": "Admin User",
            "role": "admin",
            "supabase_user_id": "temp-admin-id",  # Placeholder, will be updated by auth middleware on first login
            "department": "Administration"
        },
        {
            "email": "faculty@academicerp.com",
            "name": "Dr. Smith",
            "role": "faculty",
            "supabase_user_id": "temp-faculty-id",
            "department": "CSE"
        }
    ]
    
    faculty_ids = {}
    for u in users:
        existing = supabase.table('faculty_users').select('id').eq('email', u['email']).execute()
        if existing.data:
            faculty_ids[u['role']] = existing.data[0]['id']
        else:
            res = supabase.table('faculty_users').insert(u).execute()
            faculty_ids[u['role']] = res.data[0]['id']

    # 9. Faculty-Course Map
    logger.info("Mapping Faculty to Courses...")
    if 'faculty' in faculty_ids and 'CS201' in course_ids:
        f_id = faculty_ids['faculty']
        c_id = course_ids['CS201']
        
        map_res = supabase.table('faculty_course_map').select('id').eq('faculty_id', f_id).eq('course_id', c_id).execute()
        if not map_res.data:
            supabase.table('faculty_course_map').insert({
                "faculty_id": f_id, 
                "course_id": c_id, 
                "section": "A", 
                "academic_year": "2023-2024",
                "semester": 3
            }).execute()

    logger.info("Seeding complete! You can now log in and generate papers.")
    logger.info("Login with email: admin@academicerp.com (Admin) or faculty@academicerp.com (Faculty)")

if __name__ == "__main__":
    seed_database()
