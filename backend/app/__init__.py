from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import sys

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Asegurar que el directorio raíz esté en el path para los imports
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if base_dir not in sys.path:
        sys.path.append(base_dir)
    
    from backend.config import Config
    app.config.from_object(Config)
    
    CORS(app) # CORS liberado
    db.init_app(app)

    @app.route('/')
    def index():
        return "Servidor de Asistencia Activo", 200

    # Importar y registrar rutas
    from backend.app.rutas import bp as api_bp
    app.register_blueprint(api_bp)
        
    return app
