import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Administrador, Empleado, Persona
from sqlalchemy import text

app = create_app()

def check_creds():
    with app.app_context():
        print("--- ADMINS ---")
        admins = Administrador.query.all()
        for a in admins:
            print(f"Correo: {a.correo} | Pass (Stored): {a.contraseña}")
        
        print("\n--- EMPLEADOS ---")
        empleados = Empleado.query.all()
        for e in empleados:
            print(f"DNI: {e.persona.dni} | Pass (Stored): {e.contraseña}")

if __name__ == "__main__":
    check_creds()
