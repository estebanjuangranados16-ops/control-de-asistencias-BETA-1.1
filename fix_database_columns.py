"""
Script para agregar columnas faltantes a la base de datos PostgreSQL
"""
import os
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno
load_dotenv()

def fix_database_columns():
    """Agregar columnas faltantes a la tabla attendance_records"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("DATABASE_URL no encontrada en .env")
            return False
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("Agregando columnas faltantes...")
        
        # Agregar columnas si no existen
        columns_to_add = [
            ("is_break_record", "BOOLEAN DEFAULT FALSE"),
            ("break_type", "VARCHAR(50)"),
            ("break_duration_minutes", "INTEGER")
        ]
        
        for column_name, column_definition in columns_to_add:
            try:
                # Verificar si la columna existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='attendance_records' AND column_name=%s
                """, (column_name,))
                
                if not cursor.fetchone():
                    # La columna no existe, agregarla
                    cursor.execute(f"ALTER TABLE attendance_records ADD COLUMN {column_name} {column_definition}")
                    print(f"Columna '{column_name}' agregada")
                else:
                    print(f"Columna '{column_name}' ya existe")
                    
            except Exception as e:
                print(f"Error agregando columna '{column_name}': {e}")
        
        conn.commit()
        conn.close()
        
        print("Base de datos actualizada correctamente")
        return True
        
    except Exception as e:
        print(f"Error actualizando base de datos: {e}")
        return False

if __name__ == "__main__":
    fix_database_columns()