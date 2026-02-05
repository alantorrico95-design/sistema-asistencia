import psycopg2

CLOUD_URL = "postgresql://asistencia_db_shwz_user:aiuQ8Yd5HO0APU8XAWSwc1S5TAVru09R@dpg-d62eru94tr6s73bm4u40-a.oregon-postgres.render.com/asistencia_db_shwz"

def debug_db():
    try:
        conn = psycopg2.connect(CLOUD_URL)
        cur = conn.cursor()
        
        print("--- Listado de tablas en la nube ---")
        cur.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        """)
        tables = cur.fetchall()
        for t in tables:
            print(f"Schema: {t[0]}, Table: {t[1]}")
            
        if not tables:
            print("No se encontró ninguna tabla.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    debug_db()
