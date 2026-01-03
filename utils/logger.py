"""
Logging configuration for Academic ERP Backend.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    # Get log level from config
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # File handler (optional, for production)
    log_dir = os.getenv('LOG_DIR', 'logs')
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError:
            log_dir = None
    
    if log_dir:
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'app.log'),
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    
    # Add console handler
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Reduce noise from other libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    app.logger.info('Logger initialized')


def get_logger(name):
    """
    Get a named logger.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger


# Pre-configured loggers
auth_logger = get_logger('auth')
api_logger = get_logger('api')
db_logger = get_logger('database')
