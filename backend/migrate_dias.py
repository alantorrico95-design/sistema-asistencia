from backend.app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE horario ADD COLUMN dias VARCHAR(100) DEFAULT 'No definido'"))
        db.session.commit()
        print("Columna 'dias' añadida exitosamente.")
    except Exception as e:
        print(f"Error o ya existe: {e}")
