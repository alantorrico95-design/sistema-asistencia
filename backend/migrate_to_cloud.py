import os
import pymysql
import psycopg2
from psycopg2.extras import execute_values

# CONFIGURACIÓN
# 1. Local (MySQL)
LOCAL_DB = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'gestion_asistencia_restaurante'
}

# 2. Cloud (External URL)
CLOUD_URL = "postgresql://asistencia_db_shwz_user:aiuQ8Yd5HO0APU8XAWSwc1S5TAVru09R@dpg-d62eru94tr6s73bm4u40-a.oregon-postgres.render.com/asistencia_db_shwz"

def migrate():
    try:
        print("--- Iniciando Migración Completa ---")
        
        local_conn = pymysql.connect(**LOCAL_DB)
        local_cursor = local_conn.cursor(pymysql.cursors.DictCursor)
        
        cloud_conn = psycopg2.connect(CLOUD_URL)
        cloud_cursor = cloud_conn.cursor()
        
        # EL ORDEN ES VITAL por las llaves foráneas
        tablas = ['persona', 'administrador', 'horario', 'empleado', 'asistencia', 'permiso']
        
        for tabla in tablas:
            print(f"Migrando tabla: {tabla}...")
            
            # Leer MySQL
            local_cursor.execute(f"SELECT * FROM `{tabla}`")
            rows = local_cursor.fetchall()
            
            if not rows:
                print(f"  Tabla {tabla} vacía.")
                continue
            
            # Limpiar Postgres
            cloud_cursor.execute(f'TRUNCATE TABLE "{tabla}" RESTART IDENTITY CASCADE')
            
            # Insertar en Postgres
            columnas = list(rows[0].keys())
            # Escapar nombres de columnas para Postgres
            cols_str = ', '.join([f'"{c}"' for c in columnas])
            query = f'INSERT INTO "{tabla}" ({cols_str}) VALUES %s'
            
            valores = [tuple(row[c] for c in columnas) for row in rows]
            
            execute_values(cloud_cursor, query, valores)
            print(f"  {len(rows)} registros migrados.")

        cloud_conn.commit()
        print("--- MIGRACIÓN EXITOSA ---")
        
    except Exception as e:
        print(f"ERROR: {e}")
        if 'cloud_conn' in locals(): cloud_conn.rollback()
    finally:
        if 'local_conn' in locals(): local_conn.close()
        if 'cloud_conn' in locals(): cloud_conn.close()

if __name__ == "__main__":
    migrate()
