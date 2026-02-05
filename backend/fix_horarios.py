import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Horario

app = create_app()

def inspect_and_fix_horarios():
    with app.app_context():
        print("--- HORARIOS ACTUALES ---")
        horarios = Horario.query.all()
        for h in horarios:
            print(f"ID: {h.id} | Turno: {h.turno} | Días: {h.dias}")
        
        print("\nActualizando horarios según requerimientos...")
        
        # Turno Mañana: Lun a Sáb
        h_manana = Horario.query.filter(Horario.turno.ilike('%mañana%')).all()
        for h in h_manana:
            h.dias = "Lun, Mar, Mié, Jue, Vie, Sáb"
            
        # Turno Noche: Lun a Dom
        h_noche = Horario.query.filter(Horario.turno.ilike('%noche%')).all()
        for h in h_noche:
            h.dias = "Lun, Mar, Mié, Jue, Vie, Sáb, Dom"
            
        # Turno Tarde: Lun a Sáb (Asumiendo)
        h_tarde = Horario.query.filter(Horario.turno.ilike('%tarde%')).all()
        for h in h_tarde:
            h.dias = "Lun, Mar, Mié, Jue, Vie, Sáb"
            
        db.session.commit()
        print("Horarios actualizados correctamente.")

if __name__ == "__main__":
    inspect_and_fix_horarios()
