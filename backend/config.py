"""
Configuration settings for the Flask backend.

Defines base, development, production, and testing configuration classes.
Provides a helper to initialize the app and ensure upload paths exist.
"""

import os
from pathlib import Path

class Config:
    """Base configuration."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = Path('uploads')
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    
    # Wordset settings
    WORDSET_FILE = os.environ.get('WORDSET_FILE', 'wordset.txt')
    
    # Solver settings
    MAX_MOVES_RETURNED = int(os.environ.get('MAX_MOVES_RETURNED', '10'))
    SOLVER_TIMEOUT_SECONDS = int(os.environ.get('SOLVER_TIMEOUT_SECONDS', '30'))
    
    # Photo processing settings
    ENABLE_PHOTO_PROCESSING = os.environ.get('ENABLE_PHOTO_PROCESSING', 'False').lower() == 'true'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration (create upload path, etc.)."""
        # Create upload folder if it doesn't exist
        upload_path = Path(Config.UPLOAD_FOLDER)
        upload_path.mkdir(exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
