# Academic ERP Backend

Flask-based REST API for Academic ERP system with Supabase integration and AI-powered question paper generation.

## Features

- 🔐 **Supabase Authentication** - JWT-based auth with role-based access control (Admin/Faculty)
- 🗃️ **Supabase REST API** - Complete CRUD operations via Supabase client (network-optimized)
- 🤖 **AI Paper Generation** - Google Gemini integration for intelligent question paper creation
- 📊 **Comprehensive Admin Panel** - Manage programs, branches, courses, faculty, and questions
- 📝 **Question Bank Management** - Multi-dimensional filtering (CO, Bloom's, Difficulty)
- 🎯 **Smart Paper Generation** - CO coverage, Bloom distribution, difficulty balancing

## Tech Stack

- **Backend**: Flask, Python 3.9+
- **Database**: Supabase (PostgreSQL)
- **AI**: Google Gemini Pro
- **Auth**: Supabase Auth (JWT)
- **Deployment**: Render

## Quick Start

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd academicerp-backend
pip install -r requirements.txt
```

### 2. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_JWT_SECRET=your_jwt_secret
GEMINI_API_KEY=your_gemini_key
DATABASE_URL=your_supabase_db_url
```

### 3. Database Setup

1. Run `migrations/001_initial_schema.sql` in Supabase Dashboard SQL Editor
2. Seed initial data: `python seeds_supabase.py`
3. Create auth users: `python create_auth_users.py`

### 4. Run Locally

```bash
python app.py
# Server runs on http://localhost:5000
```

## API Documentation

Access Swagger UI at: `http://localhost:5000/api/docs`

## Test Credentials

- **Admin**: `admin@academicerp.com` / `admin123`
- **Faculty**: `faculty@academicerp.com` / `faculty123`

## Deployment to Render

This repository includes `render.yaml` for automated deployment:

1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables in Render Dashboard
4. Deploy automatically

## Project Structure

```
academicerp-backend/
├── controllers/       # Request handlers
├── services/         # Business logic
├── models/           # Database models (deprecated, using Supabase)
├── middlewares/      # Auth & CORS
├── routes/          # API endpoints
├── utils/           # Helpers & Supabase client
├── migrations/      # Database schema
└── app.py          # Application entry point
```

## License

MIT

---

Built with ❤️ using Flask & Supabase
