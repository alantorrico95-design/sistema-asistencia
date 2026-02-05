import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Administrador, Empleado, Persona

app = create_app()

def fix_everything():
    with app.app_context():
        print("Iniciando corrección global de contraseñas...")
        
        # 1. Corregir todos los Administradores
        admins = Administrador.query.all()
        for a in admins:
            # Si empieza con pbkdf2, es un hash. Lo reseteamos a una clave simple.
            if a.contraseña.startswith('pbkdf2:'):
                a.contraseña = 'admin123'
            print(f"Admin: {a.correo} -> OK")
        
        # 2. Corregir todos los Empleados
        empleados = Empleado.query.all()
        for e in empleados:
            # Forzamos 12345 a todos para que no haya dudas
            e.contraseña = '12345'
            print(f"Empleado DNI: {e.persona.dni} -> OK (Pass: 12345)")
            
        db.session.commit()
        print("\n--- ¡ÉXITO! ---")
        print("Todos los administradores tienen sus claves en el formato correcto.")
        print("TODOS los empleados ahora tienen la contraseña: 12345")

if __name__ == "__main__":
    fix_everything()
