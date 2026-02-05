import requests

base_url = "http://192.168.140.10:5000/api/login"
users_to_test = ["74304056", "admin@asistencia.com"] # Testing both a DNI and an admin email if possible
password = "12345"

for user in users_to_test:
    print(f"Probando login para: {user}...")
    try:
        response = requests.post(base_url, json={"dni": user, "correo": user, "password": password})
        print(f"Respuesta ({response.status_code}): {response.json()}")
    except Exception as e:
        print(f"Error conectando: {e}")
