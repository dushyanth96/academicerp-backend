import sys
import os
from flask import Flask
from config import get_config
from services.admin_service import AdminService
from services.faculty_service import FacultyService
from services.question_service import QuestionService
from services.paper_generation_service import PaperGenerationService

def verify_services():
    app = Flask(__name__)
    app.config.from_object(get_config())
    
    with app.app_context():
        print("=== Verifying AdminService ===")
        try:
            programs = AdminService.get_programs(page=1, per_page=5)
            print(f"Success! Found {programs['total']} programs.")
            if programs['items']:
                print(f"Sample Program: {programs['items'][0]['name']}")
        except Exception as e:
            print(f"FAILED: {e}")
            import traceback
            traceback.print_exc()

        print("\n=== Verifying FacultyService ===")
        try:
            blooms = FacultyService.get_bloom_levels()
            print(f"Success! Found {len(blooms)} bloom levels.")
            if blooms:
                print(f"Sample Bloom: {blooms[0]['name']}")
        except Exception as e:
            print(f"FAILED: {e}")
            import traceback
            traceback.print_exc()

        print("\n=== Verifying QuestionService ===")
        try:
            questions = QuestionService.get_questions(page=1, per_page=5)
            print(f"Success! Found {questions['total']} questions.")
            if questions['items']:
                print(f"Sample Question: {questions['items'][0]['question_text']}")
        except Exception as e:
            print(f"FAILED: {e}")
            import traceback
            traceback.print_exc()
            
        print("\n=== Verifying PaperGenerationService ===")
        try:
            history = PaperGenerationService.get_history(page=1, limit=5)
            print(f"Success! Found {history['total']} generated papers.")
        except Exception as e:
            print(f"FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    verify_services()
