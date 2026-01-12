from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '1') == '1'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
    
    # Registrar blueprints
    from app.routes import main_bp, algorithms_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(algorithms_bp)
    
    return app
