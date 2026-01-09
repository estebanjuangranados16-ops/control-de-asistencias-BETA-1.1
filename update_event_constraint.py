"""
Script para actualizar la restricción de tipos de eventos en PostgreSQL
"""
import os
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno
load_dotenv()

def update_event_type_constraint():
    """Actualizar la restricción de tipos de eventos"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("DATABASE_URL no encontrada en .env")
            return False
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("Actualizando restricción de tipos de eventos...")
        
        # Primero, eliminar la restricción existente si existe
        try:
            cursor.execute("""
                ALTER TABLE attendance_records 
                DROP CONSTRAINT IF EXISTS attendance_records_event_type_check
            """)
            print("Restricción anterior eliminada")
        except Exception as e:
            print(f"Info: {e}")
        
        # Agregar nueva restricción que incluye los tipos de almuerzo y break
        cursor.execute("""
            ALTER TABLE attendance_records 
            ADD CONSTRAINT attendance_records_event_type_check 
            CHECK (event_type IN (
                'entrada', 'salida', 
                'break_salida', 'break_entrada',
                'almuerzo_salida', 'almuerzo_entrada'
            ))
        """)
        
        conn.commit()
        conn.close()
        
        print("Restricción de tipos de eventos actualizada correctamente")
        print("Tipos permitidos: entrada, salida, break_salida, break_entrada, almuerzo_salida, almuerzo_entrada")
        return True
        
    except Exception as e:
        print(f"Error actualizando restricción: {e}")
        return False

if __name__ == "__main__":
    update_event_type_constraint()