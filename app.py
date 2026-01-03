"""
Academic ERP Backend - Flask Application Factory

Production-ready Flask backend with Supabase PostgreSQL and JWT authentication.
"""
import logging
from flask import Flask, jsonify
from flask_cors import CORS

from config import get_config
from routes import register_blueprints


def create_app(config_class=None):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_class: Configuration class to use. Defaults to environment-based config.
    
    Returns:
        Flask application instance.
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # Configure logging
    configure_logging(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'academic-erp-backend'}), 200
    
    app.logger.info('Academic ERP Backend initialized successfully')
    
    return app


def init_extensions(app):
    """Initialize Flask extensions."""
    # Database
    # db.init_app(app) # Deprecated: Switched to Supabase REST API
    
    # CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Swagger Documentation
    from flasgger import Swagger
    Swagger(app, config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    })
    
    # Create tables if they don't exist (development only)
    # if app.config.get('DEBUG'):
    #     with app.app_context():
    #         db.create_all()


def configure_logging(app):
    """Configure application logging."""
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Reduce SQLAlchemy noise
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


def register_error_handlers(app):
    """Register global error handlers."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': str(error.description) if hasattr(error, 'description') else 'Invalid request'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal Server Error: {error}')
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500


# Gunicorn entry point
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
