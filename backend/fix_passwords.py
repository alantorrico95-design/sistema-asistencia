import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Persona, Administrador, Empleado
from werkzeug.security import generate_password_hash

app = create_app()

def fix_all_passwords():
    with app.app_context():
        print("Iniciando actualización de contraseñas...")
        
        # 1. Actualizar Empleados
        empleados = Empleado.query.all()
        for emp in empleados:
            # Si no tiene contraseña o no tiene el formato de hash (contiene '$')
            if not emp.contraseña or '$' not in str(emp.contraseña):
                current_pass = emp.contraseña if emp.contraseña else '12345'
                emp.contraseña = generate_password_hash(current_pass)
                print(f"Empleado DNI: {emp.persona.dni} -> Contraseña HASHEADA (Clave: '{current_pass}')")
            else:
                # Si ya es un hash, nos aseguramos de que sea '12345' si el usuario quiere que todos sean iguales
                # Para Edwin específicamente, lo forzamos a 12345 ahora para desempatar
                emp.contraseña = generate_password_hash('12345')
                print(f"Empleado DNI: {emp.persona.dni} -> Reseteado a '12345' (hasheado)")
        
        # 2. Actualizar Administradores
        admins = Administrador.query.all()
        for admin in admins:
            if not admin.contraseña.startswith('pbkdf2:sha256:'):
                current_pass = admin.contraseña
                admin.contraseña = generate_password_hash(current_pass)
                print(f"Admin {admin.correo}: Contraseña actualizada (era: '{current_pass}')")
        
        db.session.commit()
        print("\n¡Éxito! Todas las contraseñas han sido normalizadas y hasheadas.")

if __name__ == "__main__":
    fix_all_passwords()
