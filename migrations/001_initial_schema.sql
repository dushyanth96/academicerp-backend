-- Initial SQL Schema for Academic ERP Backend
-- Compatible with Supabase PostgreSQL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Programs Table
CREATE TABLE programs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    duration_years INTEGER DEFAULT 4,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Branches Table
CREATE TABLE branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Regulations Table
CREATE TABLE regulations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Courses Table
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) NOT NULL,
    credits INTEGER DEFAULT 3,
    lecture_hours INTEGER DEFAULT 3,
    tutorial_hours INTEGER DEFAULT 1,
    practical_hours INTEGER DEFAULT 0,
    regulation_id INTEGER REFERENCES regulations(id) ON DELETE CASCADE,
    semester INTEGER,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_course_code_regulation UNIQUE (code, regulation_id)
);

-- 5. Program-Branch Map Table
CREATE TABLE program_branch_map (
    id SERIAL PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id) ON DELETE CASCADE,
    branch_id INTEGER REFERENCES branches(id) ON DELETE CASCADE,
    intake_capacity INTEGER DEFAULT 60,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_program_branch UNIQUE (program_id, branch_id)
);

-- 6. Branch-Course Map Table
CREATE TABLE branch_course_map (
    id SERIAL PRIMARY KEY,
    branch_id INTEGER REFERENCES branches(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    semester INTEGER NOT NULL,
    is_elective BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_branch_course UNIQUE (branch_id, course_id)
);

-- 7. Faculty Users Table
CREATE TABLE faculty_users (
    id SERIAL PRIMARY KEY,
    supabase_user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    employee_id VARCHAR(50) UNIQUE,
    department VARCHAR(100),
    designation VARCHAR(100),
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'faculty', -- admin, faculty
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_faculty_supabase_id ON faculty_users(supabase_user_id);

-- 8. Faculty-Course Map Table
CREATE TABLE faculty_course_map (
    id SERIAL PRIMARY KEY,
    faculty_id INTEGER REFERENCES faculty_users(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    academic_year VARCHAR(20) NOT NULL,
    semester INTEGER NOT NULL,
    section VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_faculty_course_assignment UNIQUE (faculty_id, course_id, academic_year, semester, section)
);

-- 9. Bloom Levels Table
CREATE TABLE bloom_levels (
    id SERIAL PRIMARY KEY,
    level INTEGER UNIQUE NOT NULL, -- 1-6
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    keywords TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. Difficulty Levels Table
CREATE TABLE difficulty_levels (
    id SERIAL PRIMARY KEY,
    level INTEGER UNIQUE NOT NULL, -- 1-5
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    weight FLOAT DEFAULT 1.0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Course Outcomes Table
CREATE TABLE course_outcomes (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    co_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    bloom_level_id INTEGER REFERENCES bloom_levels(id),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_course_co UNIQUE (course_id, co_number)
);

-- 12. Units Table
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    unit_number INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    topics TEXT,
    hours INTEGER DEFAULT 10,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_course_unit UNIQUE (course_id, unit_number)
);

-- 13. Questions Table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    unit_id INTEGER REFERENCES units(id) ON DELETE CASCADE,
    co_id INTEGER REFERENCES course_outcomes(id) ON DELETE CASCADE,
    bloom_level_id INTEGER REFERENCES bloom_levels(id),
    difficulty_id INTEGER REFERENCES difficulty_levels(id),
    faculty_id INTEGER REFERENCES faculty_users(id),
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) DEFAULT 'descriptive',
    marks INTEGER NOT NULL DEFAULT 2,
    expected_time_minutes INTEGER,
    options JSONB,
    correct_answer TEXT,
    image_url VARCHAR(500),
    tags TEXT,
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_question_course ON questions(course_id);
CREATE INDEX idx_question_unit ON questions(unit_id);
CREATE INDEX idx_question_co ON questions(co_id);

-- 14. Generated Papers Table
CREATE TABLE generated_papers (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    faculty_id INTEGER REFERENCES faculty_users(id),
    title VARCHAR(300),
    exam_type VARCHAR(50),
    academic_year VARCHAR(20),
    semester INTEGER,
    duration_minutes INTEGER DEFAULT 180,
    total_marks INTEGER NOT NULL,
    generation_params JSONB,
    question_count INTEGER,
    unit_coverage JSONB,
    bloom_distribution JSONB,
    difficulty_distribution JSONB,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 15. Generated Questions Mapping Table
CREATE TABLE generated_questions (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER REFERENCES generated_papers(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(id),
    section VARCHAR(10) NOT NULL,
    question_number INTEGER NOT NULL,
    marks INTEGER NOT NULL,
    is_compulsory BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_paper_section_qnum UNIQUE (paper_id, section, question_number)
);

-- Seed Initial Data
INSERT INTO bloom_levels (level, name, status) VALUES 
(1, 'Remembering', 'active'),
(2, 'Understanding', 'active'),
(3, 'Applying', 'active'),
(4, 'Analyzing', 'active'),
(5, 'Evaluating', 'active'),
(6, 'Creating', 'active');

INSERT INTO difficulty_levels (level, name, weight, status) VALUES 
(1, 'Easy', 0.8, 'active'),
(2, 'Medium', 1.0, 'active'),
(3, 'Hard', 1.2, 'active'),
(4, 'Very Hard', 1.5, 'active');
