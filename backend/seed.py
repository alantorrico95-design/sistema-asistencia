from backend.app import create_app, db
from backend.app.modelos import Persona, Administrador, Empleado, Horario
from werkzeug.security import generate_password_hash
from datetime import time

app = create_app()

def seed():
    with app.app_context():
        # Crear tablas (si no existen)
        db.create_all()
        
        # 1. Crear Persona para Admin
        if not Persona.query.filter_by(dni='ADMIN01').first():
            p_admin = Persona(dni='ADMIN01', nombre='Admin', apellido='Sistema')
            db.session.add(p_admin)
            db.session.flush() # Para obtener el ID
            
            admin = Administrador(
                id=p_admin.id,
                correo='admin@restaurante.com',
                contraseña=generate_password_hash('admin123')
            )
            db.session.add(admin)
            print("Administrador creado: admin@restaurante.com / admin123")
            
        # 2. Crear Horario
        if not Horario.query.first():
            h_manana = Horario(
                turno='Mañana',
                horario_inicio=time(8, 0),
                horario_fin=time(16, 0)
            )
            db.session.add(h_manana)
            db.session.flush()
            print("Horario de mañana creado")
            
            # 3. Crear Persona y Empleado de prueba
            p_empleado = Persona(dni='12345678', nombre='Juan', apellido='Perez')
            db.session.add(p_empleado)
            db.session.flush()
            
            empleado = Empleado(
                id=p_empleado.id,
                idHorario=h_manana.id,
                estado='Activo',
                contraseña=generate_password_hash('12345')
            )
            db.session.add(empleado)
            print("Empleado de prueba creado: Juan Perez (DNI: 12345678)")
            
        db.session.commit()
        print("Base de datos sincronizada y poblada.")

if __name__ == '__main__':
    seed()
