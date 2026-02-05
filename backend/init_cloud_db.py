import os
import sys

# Asegurar que el directorio raíz del backend esté en el path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from backend.app import create_app, db
from backend.app.modelos import * # Asegurar que los modelos se carguen

# URL EXTERNA de Render
CLOUD_URL = "postgresql://asistencia_db_shwz_user:aiuQ8Yd5HO0APU8XAWSwc1S5TAVru09R@dpg-d62eru94tr6s73bm4u40-a.oregon-postgres.render.com/asistencia_db_shwz"

def init_db():
    try:
        app = create_app()
        # Forzar la URL externa para inicialización local
        app.config['SQLALCHEMY_DATABASE_URI'] = CLOUD_URL
        
        with app.app_context():
            print("--- Creando tablas en la nube (Postgres) ---")
            db.create_all()
            print("--- Tablas creadas con éxito ---")
            
    except Exception as e:
        print(f"Error al inicializar DB: {e}")

if __name__ == "__main__":
    init_db()
