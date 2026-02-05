from backend.app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE empleado ADD COLUMN contraseña VARCHAR(100) DEFAULT '12345'"))
        db.session.commit()
        print("Columna 'contraseña' añadida exitosamente a la tabla empleado.")
    except Exception as e:
        print(f"Error o ya existe: {e}")
