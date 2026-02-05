from backend.app import db
from datetime import datetime

class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(15), nullable=False, unique=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, db.ForeignKey('persona.id'), primary_key=True)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(100), nullable=False) # En el SQL es varchar(100)
    persona = db.relationship('Persona', backref=db.backref('admin', uselist=False))

class Horario(db.Model):
    __tablename__ = 'horario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    turno = db.Column(db.String(30), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fin = db.Column(db.Time, nullable=False)
    dias = db.Column(db.String(100), nullable=True) # Ejemplo: "Lun,Mar,Mie,Jue,Vie"

class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, db.ForeignKey('persona.id'), primary_key=True)
    idHorario = db.Column(db.Integer, db.ForeignKey('horario.id'), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    contraseña = db.Column(db.String(100), nullable=True) # Para su login personal
    persona = db.relationship('Persona', backref=db.backref('empleado', uselist=False), foreign_keys=[id])
    horario = db.relationship('Horario', backref='empleados')

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False)
    hora_entrada = db.Column(db.Time, nullable=False)
    hora_salida = db.Column(db.Time, nullable=True)
    idEmpleado = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    empleado = db.relationship('Empleado', backref='asistencias')

class Permiso(db.Model):
    __tablename__ = 'permiso'
    idAsistencia = db.Column(db.Integer, db.ForeignKey('asistencia.id'), primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    idAdministrador = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=False)
    asistencia = db.relationship('Asistencia', backref=db.backref('permiso', uselist=False))
    administrador = db.relationship('Administrador', backref='permisos_otorgados')
