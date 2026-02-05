import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Empleado
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    print("Iniciando reseteo global de contraseñas...")
    empleados = Empleado.query.all()
    count = 0
    default_hash = generate_password_hash("12345")
    for e in empleados:
        e.contraseña = default_hash
        count += 1
    db.session.commit()
    print(f"ÉXITO: Se actualizaron {count} empleados con la contraseña '12345'")
