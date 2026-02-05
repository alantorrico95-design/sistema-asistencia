from backend.app import create_app
import os

app = create_app()

@app.route('/test')
def test():
    return "Conexión Exitosa - API Activa", 200

if __name__ == "__main__":
    app.run()
