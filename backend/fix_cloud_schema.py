import psycopg2

CLOUD_URL = "postgresql://asistencia_db_shwz_user:aiuQ8Yd5HO0APU8XAWSwc1S5TAVru09R@dpg-d62eru94tr6s73bm4u40-a.oregon-postgres.render.com/asistencia_db_shwz"

SQL_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS persona (
        id SERIAL PRIMARY KEY,
        dni VARCHAR(15) NOT NULL UNIQUE,
        nombre VARCHAR(50) NOT NULL,
        apellido VARCHAR(50) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS administrador (
        id INTEGER PRIMARY KEY REFERENCES persona(id),
        correo VARCHAR(100) NOT NULL UNIQUE,
        contraseña VARCHAR(100) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS horario (
        id SERIAL PRIMARY KEY,
        turno VARCHAR(30) NOT NULL,
        horario_inicio TIME NOT NULL,
        horario_fin TIME NOT NULL,
        dias VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY REFERENCES persona(id),
        "idHorario" INTEGER NOT NULL REFERENCES horario(id),
        estado VARCHAR(20) NOT NULL,
        contraseña VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS asistencia (
        id SERIAL PRIMARY KEY,
        fecha DATE NOT NULL,
        hora_entrada TIME NOT NULL,
        hora_salida TIME,
        "idEmpleado" INTEGER NOT NULL REFERENCES empleado(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS permiso (
        "idAsistencia" INTEGER PRIMARY KEY REFERENCES asistencia(id),
        fecha DATE NOT NULL,
        nombre VARCHAR(50) NOT NULL,
        descripcion TEXT,
        "idAdministrador" INTEGER NOT NULL REFERENCES administrador(id)
    )
    """
]

def fix_schema():
    try:
        conn = psycopg2.connect(CLOUD_URL)
        cur = conn.cursor()
        print("--- Creando tablas manualmente en la nube ---")
        for query in SQL_QUERIES:
            cur.execute(query)
        conn.commit()
        print("--- Tablas creadas/verificadas con éxito ---")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    fix_schema()
