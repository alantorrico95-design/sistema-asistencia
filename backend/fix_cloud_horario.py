import psycopg2

CLOUD_URL = "postgresql://asistencia_db_shwz_user:aiuQ8Yd5HO0APU8XAWSwc1S5TAVru09R@dpg-d62eru94tr6s73bm4u40-a.oregon-postgres.render.com/asistencia_db_shwz"

def fix_horario_schema():
    try:
        conn = psycopg2.connect(CLOUD_URL)
        cur = conn.cursor()
        print("--- Corrigiendo columna en la tabla 'horario' ---")
        # Renombramos la columna 'dias' a 'dias_semana' para que coincida con lo que viene de MySQL
        cur.execute('ALTER TABLE horario RENAME COLUMN dias TO dias_semana')
        conn.commit()
        print("--- Columna renombrada con éxito ---")
    except Exception as e:
        print(f"Error o ya existe: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    fix_horario_schema()
