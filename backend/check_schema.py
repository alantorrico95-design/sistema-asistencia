import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from sqlalchemy import text

app = create_app()

def check():
    with app.app_context():
        print("--- SCHEMA: empleado ---")
        rows = db.session.execute(text("DESCRIBE empleado")).fetchall()
        for row in rows:
            print(row)
            
        print("\n--- SCHEMA: administrador ---")
        rows = db.session.execute(text("DESCRIBE administrador")).fetchall()
        for row in rows:
            print(row)

        print("\n--- DATA LENGTHS: empleado ---")
        rows = db.session.execute(text("SELECT dni, LENGTH(contraseña), contraseña FROM empleado JOIN persona ON empleado.id = persona.id")).fetchall()
        for row in rows:
            print(f"DNI: {row[0]} | Length: {row[1]} | Hash: {row[2]}")

if __name__ == "__main__":
    check()
