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
    
    CORS(app)
    db.init_app(app)

    with app.app_context():
        from backend.app import rutas
        app.register_blueprint(rutas.bp)
        
    return app
