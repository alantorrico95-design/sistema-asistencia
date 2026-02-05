import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Persona, Administrador, Empleado

app = create_app()

def check_dni(dni_to_check):
    with app.app_context():
        print(f"Buscando DNI: {dni_to_check}")
        
        # Check Persona
        persona = Persona.query.filter_by(dni=dni_to_check).first()
        if not persona:
            print("Resultado: La persona no existe en la base de datos.")
            return

        print(f"Resultado: Persona encontrada - {persona.nombre} {persona.apellido}")
        
        # Check Empleado
        if persona.empleado:
            print(f"Rol: Empleado")
            print(f"Contraseña guardada: '{persona.empleado.contraseña}'")
        else:
            print("Rol: No es empleado.")
            
        # Check Administrador (using DNI as email just in case)
        admin = Administrador.query.filter_by(correo=dni_to_check).first()
        if admin:
            print(f"Rol: Administrador (encontrado por 'correo'={dni_to_check})")
            print(f"Contraseña guardada: '{admin.contraseña}'")
        else:
            # Also check if the person has an admin record
            admin_by_id = Administrador.query.get(persona.id)
            if admin_by_id:
                print(f"Rol: Administrador (encontrado por ID)")
                print(f"Correo: {admin_by_id.correo}")
                print(f"Contraseña guardada: '{admin_by_id.contraseña}'")

if __name__ == "__main__":
    check_dni("74304056")
