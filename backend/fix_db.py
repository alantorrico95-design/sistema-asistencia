import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.modelos import Administrador, Empleado, Persona

app = create_app()

def fix_creds():
    with app.app_context():
        # 1. Asegurar Admin principal
        admin = Administrador.query.filter_by(correo='admin@restaurante.com').first()
        if not admin:
            # Crear persona si no existe
            p = Persona.query.filter_by(dni='ADMIN01').first()
            if not p:
                p = Persona(dni='ADMIN01', nombre='Admin', apellido='Sistema')
                db.session.add(p)
                db.session.flush()
            
            admin = Administrador(id=p.id, correo='admin@restaurante.com', contraseña='admin123')
            db.session.add(admin)
        else:
            admin.contraseña = 'admin123'
        
        # 2. Asegurar Empleado de prueba
        p_emp = Persona.query.filter_by(dni='12345678').first()
        if not p_emp:
            p_emp = Persona(dni='12345678', nombre='Juan', apellido='Perez')
            db.session.add(p_emp)
            db.session.flush()
            
            # Necesitamos un horario
            from backend.app.modelos import Horario
            h = Horario.query.first()
            if not h:
                from datetime import time
                h = Horario(turno='Mañana', horario_inicio=time(8,0), horario_fin=time(16,0))
                db.session.add(h)
                db.session.flush()
            
            emp = Empleado(id=p_emp.id, idHorario=h.id, estado='Activo', contraseña='12345')
            db.session.add(emp)
        else:
            if not p_emp.empleado:
                from backend.app.modelos import Horario
                h = Horario.query.first()
                emp = Empleado(id=p_emp.id, idHorario=h.id, estado='Activo', contraseña='12345')
                db.session.add(emp)
            else:
                p_emp.empleado.contraseña = '12345'

        # 3. Poner password default a todos los demás empleados que no tengan
        todos_emp = Empleado.query.all()
        for e in todos_emp:
            if not e.contraseña:
                e.contraseña = '12345'

        db.session.commit()
        print("Credenciales corregidas exitosamente.")

if __name__ == "__main__":
    fix_creds()
