import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from sqlalchemy import text

app = create_app()

def migrate():
    with app.app_context():
        print("Migrating database schema...")
        try:
            # MySQL syntax for modifying column
            db.session.execute(text("ALTER TABLE empleado MODIFY contraseña VARCHAR(255)"))
            db.session.execute(text("ALTER TABLE administrador MODIFY contraseña VARCHAR(255)"))
            db.session.commit()
            print("Successfully increased 'contraseña' column length to 255.")
        except Exception as e:
            db.session.rollback()
            print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()
