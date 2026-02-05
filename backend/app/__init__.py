from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    import os
    import sys
    # Asegurar que el directorio raíz del backend esté en el path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    from backend.config import Config
    app.config.from_object(Config)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    @app.route('/')
    def health_check():
        return "Servidor de Asistencia Activo", 200

    from backend.app.rutas import bp as api_bp
    app.register_blueprint(api_bp)
        
    return app
