"""
Database Seeder for Academic ERP.
Populates the database with initial demo data.
"""
from app import create_app
from models import db
from models.program import Program
from models.branch import Branch
from models.program_branch_map import ProgramBranchMap
from models.course import Course
from models.branch_course_map import BranchCourseMap
from models.faculty import FacultyUser
from models.faculty_course_map import FacultyCourseMap
from models.unit import Unit
from models.course_outcome import CourseOutcome
from models.bloom_level import BloomLevel
from models.difficulty_level import DifficultyLevel
from models.question import Question

app = create_app()

def seed_database():
    with app.app_context():
        db.create_all()
        print("🌱 Seeding database...")
        
        # 1. Programs & Branches
        btech = Program(name="Bachelor of Technology", code="B.Tech", duration_years=4)
        cse = Branch(name="Computer Science", code="CSE")
        ece = Branch(name="Electronics", code="ECE")
        
        db.session.add_all([btech, cse, ece])
        db.session.flush()
        
        # Map Program-Branch
        db.session.add(ProgramBranchMap(program_id=btech.id, branch_id=cse.id))
        db.session.add(ProgramBranchMap(program_id=btech.id, branch_id=ece.id))
        
        # 2. Courses (R20 Regulation assumed from SQL default)
        # Note: Regulation needs to be created first if strictly enforcing FK, 
        # but our initial SQL schema migration might have missed creating a default regulation.
        # Let's check or assume R20 exists if seeded in migration? 
        # Actually the migration script didn't seed Regulations. We should add one.
        from models.regulation import Regulation
        r20 = Regulation(name="Regulation 2020", code="R20", year=2020)
        db.session.add(r20)
        db.session.flush()

        python = Course(name="Python Programming", code="CS101", credits=3, regulation_id=r20.id)
        dsa = Course(name="Data Structures", code="CS201", credits=4, regulation_id=r20.id)
        
        db.session.add_all([python, dsa])
        db.session.flush()
        
        # Map Branch-Course
        db.session.add(BranchCourseMap(branch_id=cse.id, course_id=python.id, semester=1))
        db.session.add(BranchCourseMap(branch_id=cse.id, course_id=dsa.id, semester=3))

        # 3. Attributes (COs, Units)
        # Python Units
        u1 = Unit(course_id=python.id, unit_number=1, name="Introduction", description="Basics")
        u2 = Unit(course_id=python.id, unit_number=2, name="Control Flow", description="Loops and Conditions")
        db.session.add_all([u1, u2])

        # Python COs
        co1 = CourseOutcome(course_id=python.id, co_number=1, description="Understand Python syntax")
        co2 = CourseOutcome(course_id=python.id, co_number=2, description="Apply control structures")
        db.session.add_all([co1, co2])
        db.session.flush()

        # 4. Faculty
        f1 = FacultyUser(
            supabase_user_id="demo-faculty-id",
            email="faculty@demo.com",
            name="Dr. Smith",
            department="CSE",
            role="faculty"
        )
        db.session.add(f1)
        db.session.flush()
        
        # Assign Faculty
        db.session.add(FacultyCourseMap(
            faculty_id=f1.id, course_id=python.id, academic_year="2023-24", semester=1, section="A"
        ))

        # 5. Questions (Demo Bank)
        # Seed Levels first as they might be missing in SQLite
        bloom_remember = BloomLevel.query.filter_by(level=1).first()
        if not bloom_remember:
            bloom_remember = BloomLevel(level=1, name="Remember", description="Recall facts")
            db.session.add(bloom_remember)
        
        diff_easy = DifficultyLevel.query.filter_by(level=1).first()
        if not diff_easy:
            diff_easy = DifficultyLevel(level=1, name="Easy", weight=1.0)
            db.session.add(diff_easy)
            
        db.session.flush()
        
        q1 = Question(
            course_id=python.id, unit_id=u1.id, co_id=co1.id, 
            bloom_level_id=bloom_remember.id, difficulty_id=diff_easy.id,
            faculty_id=f1.id,
            question_text="What is a variable in Python?",
            marks=2,
            question_type="descriptive"
        )
        q2 = Question(
            course_id=python.id, unit_id=u2.id, co_id=co2.id,
            bloom_level_id=bloom_remember.id, difficulty_id=diff_easy.id,
            faculty_id=f1.id,
            question_text="Explain the difference between list and tuple.",
            marks=5,
            question_type="descriptive"
        )
        
        db.session.add_all([q1, q2])
        
        try:
            db.session.commit()
            print("✅ Database seeded successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Seeding failed: {e}")

if __name__ == '__main__':
    seed_database()
