import subprocess
import os

def generate_requirements():
    try:
        # Obtener dependencias actuales
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
        deps = result.stdout.splitlines()
        
        # Filtrar o añadir dependencias críticas para la nube
        cloud_deps = [
            'gunicorn',             # Servidor para Linux (Render)
            'psycopg2-binary',      # Driver para PostgreSQL
            'pymysql',              # Driver para MySQL (por si acaso)
            'cryptography'          # Para hashing y seguridad
        ]
        
        final_deps = set(deps)
        for d in cloud_deps:
            if not any(d in existing for existing in deps):
                final_deps.add(d)
        
        with open('backend/requirements.txt', 'w', encoding='utf-8') as f:
            for dep in sorted(final_deps):
                f.write(dep + '\n')
        
        print("requirements.txt generado exitosamente en UTF-8")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_requirements()
