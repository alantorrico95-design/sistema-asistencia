import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-asistencia'
    # Usa DATABASE_URL de la nube si existe, sino usa la local de MySQL
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = db_url or 'mysql+pymysql://root:@localhost/gestion_asistencia_restaurante'
    # Si estamos en Render (DATABASE_URL existe), usaremos el driver de Postgres
    if db_url:
        SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración del sistema
    GRACE_PERIOD_MINUTES = 10
