import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Persona, Empleado
from flask import json

app = create_app()

def simulate_login(identificador, password):
    with app.test_client() as client:
        response = client.post('/api/login', 
                                data=json.dumps({'dni': identificador, 'password': password}),
                                content_type='application/json')
        print(f"Login Test ({identificador}): {response.status_code} - {response.get_json()}")

if __name__ == "__main__":
    # Probar con el DNI fallido del usuario
    simulate_login('74304056', '12345')
    # Probar con admin
    simulate_login('admin@restaurante.com', 'admin123')
