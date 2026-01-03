"""
Routes package for Academic ERP Backend.
Handles blueprint registration.
"""
from flask import Blueprint

def register_blueprints(app):
    """Register all blueprints with the Flask application."""
    
    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.faculty_routes import faculty_bp
    from routes.question_routes import question_bp
    from routes.paper_routes import paper_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(question_bp, url_prefix='/questions')
    app.register_blueprint(paper_bp, url_prefix='/question-paper')
    
    app.logger.info('All blueprints registered successfully')
