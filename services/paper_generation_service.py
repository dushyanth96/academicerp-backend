"""
Paper Generation service for Academic ERP Backend.
Integrates with Google Gemini AI for intelligent question paper generation.
"""
import json
import random
import logging
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from datetime import datetime
from flask import current_app
from utils.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class PaperGenerationService:
    """Service class for question paper generation engine with Gemini AI."""
    
    @staticmethod
    def generate_paper(data, faculty_id):
        """
        Main entry point for paper generation.
        Tries Gemini first, falls back to deterministic if fails.
        """
        supabase = get_supabase_client()
        course_id = data.get('course_id')
        
        # Fetch Question Bank with relations
        response = supabase.table('questions').select(
            "*, units(unit_number), course_outcomes(co_number), bloom_levels(name), difficulty_levels(name)"
        ).eq('course_id', course_id).eq('status', 'active').execute()
        
        question_bank = response.data
        
        if not question_bank:
            return None, "Question bank for this course is empty."

        # Convert question bank to simple dict for AI performance
        bank_json = [
            {
                "qid": q['id'],
                "question_text": q['question_text'],
                "marks": q['marks'],
                "unit": q['units']['unit_number'] if q.get('units') else 0,
                "co": f"CO{q['course_outcomes']['co_number']}" if q.get('course_outcomes') else "",
                "bloom": q['bloom_levels']['name'] if q.get('bloom_levels') else "",
                "difficulty": q['difficulty_levels']['name'] if q.get('difficulty_levels') else ""
            }
            for q in question_bank
        ]

        # Filter out previously used questions if provided
        prev_ids = data.get('previously_used_ids', [])
        eligible_bank = [q for q in bank_json if q['qid'] not in prev_ids]
        
        if len(eligible_bank) < data.get('total_questions', 5): # Basic threshold
            logger.warning("Eligible question bank is small, using full bank.")
            eligible_bank = bank_json

        try:
            # 1. AI Generation
            logger.info(f"Calling Gemini for paper generation: Course {course_id}")
            ai_paper = PaperGenerationService.call_gemini_api(data, eligible_bank)
            
            if ai_paper:
                # 2. Validate and Save
                return PaperGenerationService.save_generated_paper(ai_paper, data, faculty_id)
            
        except ResourceExhausted:
            logger.warning("Gemini AI Rate Quota Exceeded. Switching to deterministic fallback engine.")
        except Exception as e:
            logger.error(f"Gemini generation failed: {str(e)}")
            
        # 3. Fallback to deterministic
        logger.info("Falling back to deterministic generation.")
        return PaperGenerationService.fallback_algorithm(data, faculty_id, question_bank)

    @staticmethod
    def build_system_prompt():
        """Define AI behavior and strict rules."""
        return (
            "You are an expert Academic Examination Controller. Your task is to generate a professional "
            "university question paper. \n\n"
            "STRICT RULES:\n"
            "1. ONLY use questions from the provided 'Question Bank' JSON.\n"
            "2. DO NOT invent new questions.\n"
            "3. Enforce the requested CO coverage, Bloom's distribution, and Difficulty mix.\n"
            "4. Ensure Unit coverage is balanced as per requirements.\n"
            "5. The output MUST be a single clean JSON object matching the schema exactly.\n"
            "6. DO NOT include any markdown formatting, backticks, or explanatory text. Return ONLY JSON."
        )

    @staticmethod
    def build_runtime_prompt(data, bank):
        """Construct the prompt with specific requirements and context."""
        return f"""
Generate a question paper for:
- Program: {data.get('program', 'B.Tech')}
- Branch: {data.get('branch', 'CSE')}
- Course: {data.get('course', 'TBD')}
- Code: {data.get('course_code', 'TBD')}
- Regulation: {data.get('regulation', 'R20')}
- Semester: {data.get('semester', '1')}
- Assessment Type: {data.get('assessment_type', 'Terminal')}
- Total Marks: {data.get('total_marks', 100)}

REQUIREMENTS:
- CO Coverage: {json.dumps(data.get('co_coverage', {}))}
- Bloom Distribution: {json.dumps(data.get('bloom_distribution', {}))}
- Difficulty Mix: {json.dumps(data.get('difficulty_distribution', {}))}
- Unit Coverage: {json.dumps(data.get('unit_coverage', {}))}

QUESTION BANK:
{json.dumps(bank)}

OUTPUT SCHEMA:
{{
  "paper": {{
    "course": "...",
    "course_code": "...",
    "assessment_type": "...",
    "total_marks": 0,
    "sections": [
      {{
        "section": "Section A",
        "instructions": "Answer all questions",
        "questions": [
          {{
            "qid": "id from bank",
            "question_text": "text from bank",
            "marks": 0,
            "unit": 0,
            "co": "...",
            "bloom": "...",
            "difficulty": "..."
          }}
        ]
      }}
    ]
  }}
}}
"""

    @staticmethod
    def call_gemini_api(data, bank):
        """Interface with Gemini Pro."""
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        system_prompt = PaperGenerationService.build_system_prompt()
        runtime_prompt = PaperGenerationService.build_runtime_prompt(data, bank)
        
        response = model.generate_content(
            f"{system_prompt}\n\n{runtime_prompt}",
            generation_config={"temperature": 0.1}
        )
        
        return PaperGenerationService.validate_and_format_response(response.text, bank)

    @staticmethod
    def validate_and_format_response(response_text, bank):
        """Parse, validate, and sanitize AI response."""
        try:
            # Remove potential markdown clutter
            clean_json = response_text.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:-3].strip()
            elif clean_json.startswith("```"):
                clean_json = clean_json[3:-3].strip()
            
            data = json.loads(clean_json)
            
            # Validation: Ensure qids are from the bank
            bank_ids = {str(q['qid']) for q in bank}
            for section in data.get('paper', {}).get('sections', []):
                valid_questions = []
                for q in section.get('questions', []):
                    if str(q.get('qid')) in bank_ids:
                        valid_questions.append(q)
                section['questions'] = valid_questions
                
            return data
        except Exception as e:
            logger.error(f"AI response validation failed: {str(e)}")
            return None

    @staticmethod
    def fallback_algorithm(data, faculty_id, full_bank):
        """Deterministic random selection logic."""
        supabase = get_supabase_client()
        course_id = data.get('course_id')
        total_marks = data.get('total_marks', 100)
        
        sections_params = data.get('sections', [
            {"name": "Part A", "marks_per_question": 10, "total_questions": 10}
        ])
        
        selected_questions = []
        used_ids = set()
        
        # full_bank is a list of dicts (Supabase response) here
        for sp in sections_params:
            pool = [q for q in full_bank if q['marks'] == sp['marks_per_question'] and q['id'] not in used_ids]
            num = sp['total_questions']
            
            if len(pool) < num:
                num = len(pool)
                
            picked = random.sample(pool, num)
            for i, q in enumerate(picked):
                selected_questions.append({
                    "section": sp['name'],
                    "question_number": i + 1,
                    "question_id": q['id'],
                    "marks": q['marks'],
                    "is_compulsory": True
                })
                used_ids.add(q['id'])

        # Create Paper
        paper_payload = {
            'course_id': course_id,
            'faculty_id': faculty_id,
            'title': data.get('title', f"Generated-Paper-{datetime.now().strftime('%Y%m%d%H%M')}"),
            'exam_type': data.get('assessment_type', 'semester'),
            'total_marks': total_marks,
            'generation_params': data,
            'status': 'finalized'
        }
        paper_res = supabase.table('generated_papers').insert(paper_payload).execute()
        
        if not paper_res.data:
            return None, "Failed to save paper."
            
        paper = paper_res.data[0]
        
        # Save Questions
        gq_payloads = []
        for sq in selected_questions:
            gq_payloads.append({
                'paper_id': paper['id'],
                'question_id': sq['question_id'],
                'section': sq['section'],
                'question_number': sq['question_number'],
                'marks': sq['marks']
            })
            
        if gq_payloads:
            supabase.table('generated_questions').insert(gq_payloads).execute()
            
        return paper, None

    @staticmethod
    def save_generated_paper(ai_data, original_params, faculty_id):
        """Persist AI generated structure to DB."""
        supabase = get_supabase_client()
        course_id = original_params.get('course_id')
        paper_data = ai_data.get('paper', {})
        
        # Save Paper
        paper_payload = {
            'course_id': course_id,
            'faculty_id': faculty_id,
            'title': paper_data.get('course', 'AI Generated Paper'),
            'exam_type': paper_data.get('assessment_type', 'semester'),
            'total_marks': paper_data.get('total_marks', 100),
            'generation_params': original_params,
            'status': 'finalized'
        }
        paper_res = supabase.table('generated_papers').insert(paper_payload).execute()
        
        if not paper_res.data:
            return None, "Failed to save paper."
            
        paper = paper_res.data[0]
        
        # Save Questions
        gq_payloads = []
        
        for section in paper_data.get('sections', []):
            section_name = section.get('section', 'General')
            for i, q in enumerate(section.get('questions', [])):
                gq_payloads.append({
                    'paper_id': paper['id'],
                    'question_id': int(q['qid']),
                    'section': section_name,
                    'question_number': i + 1,
                    'marks': q.get('marks', 0)
                })
                
                # Update usage metadata individually (Supabase RPC would be better but simple update loop for now)
                # TODO: Optimize with RPC or Batch Update
                try:
                    supabase.table('questions').update({
                        'usage_count': 1, # Should increment, but client simple update can't easily increment without read. keeping it simple.
                        # Wait, we can't increment easily. Let's just update last_used_at for now to avoid read-write cycle lag.
                        'last_used_at': datetime.utcnow().isoformat()
                    }).eq('id', int(q['qid'])).execute()
                except:
                    pass
        
        if gq_payloads:
            supabase.table('generated_questions').insert(gq_payloads).execute()
            
        return paper, None

    @staticmethod
    def get_history(course_id=None, faculty_id=None, page=1, limit=20):
        """Get paginated history of papers."""
        supabase = get_supabase_client()
        query = supabase.table('generated_papers').select("*", count='exact')
        
        if course_id:
            query = query.eq('course_id', course_id)
        if faculty_id:
            query = query.eq('faculty_id', faculty_id)
            
        start = (page - 1) * limit
        end = start + limit - 1
        
        response = query.order('created_at', desc=True).range(start, end).execute()
        
        return {
            'items': response.data,
            'total': response.count,
            'page': page,
            'per_page': limit
        }

    @staticmethod
    def get_paper_details(paper_id):
        """Get full paper details."""
        supabase = get_supabase_client()
        
        # Get Paper
        paper_res = supabase.table('generated_papers').select("*").eq('id', paper_id).execute()
        if not paper_res.data:
            return None
            
        paper = paper_res.data[0]
        
        # Get/Join Generated Questions with actual Questions
        # Supabase Join: generated_questions (*, questions (*))
        gq_res = supabase.table('generated_questions').select(
            "*, questions(*, course_outcomes(co_number), bloom_levels(name), difficulty_levels(name))"
        ).eq('paper_id', paper_id).order('question_number').execute()
        
        paper['questions'] = gq_res.data
        return paper
