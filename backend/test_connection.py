import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from sqlalchemy import text

app = create_app()

def test_connection():
    with app.app_context():
        try:
            # Intentar una consulta simple
            db.session.execute(text("SELECT 1"))
            print("SUCCESS: La conexion a MySQL funciona correctamente.")
            print(f"Base de Datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Verificar si las tablas existen
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tablas encontradas: {tables}")
            
        except Exception as e:
            print("ERROR: No se pudo conectar a la base de datos.")
            print(f"Motivo: {e}")

if __name__ == "__main__":
    test_connection()
