# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_migrate import Migrate
import hashlib

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()


def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)

    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])

    # Ensure the upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.speech import speech_bp
    from app.routes.transcribe import transcribe_bp  # Import new blueprint

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(speech_bp)
    app.register_blueprint(transcribe_bp)  # Register new blueprint

    # Set up user loader for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Add template context processors
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.now()}
    
    # Add custom filters
    @app.template_filter('md5')
    def md5_filter(s):
        """Generate md5 hash of the string for Gravatar"""
        if s is None:
            return ''
        return hashlib.md5(s.encode('utf-8')).hexdigest()
    
    @app.template_filter('trim')
    def trim_filter(s):
        """Remove whitespace from string"""
        if s is None:
            return ''
        return s.strip()

    return app