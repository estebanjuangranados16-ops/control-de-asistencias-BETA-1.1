"""
Script para verificar el estado de la base de datos PostgreSQL
"""
import os
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno
load_dotenv()

def check_database_status():
    """Verificar el estado de la base de datos"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("DATABASE_URL no encontrada en .env")
            return False
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("Verificando estado de la base de datos...")
        
        # Verificar columnas de attendance_records
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name='attendance_records' 
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print("\nColumnas en attendance_records:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        # Verificar restricciones
        cursor.execute("""
            SELECT constraint_name, check_clause 
            FROM information_schema.check_constraints 
            WHERE constraint_name LIKE '%attendance_records%'
        """)
        
        constraints = cursor.fetchall()
        print("\nRestricciones de verificación:")
        for constraint in constraints:
            print(f"  - {constraint[0]}: {constraint[1]}")
        
        # Probar inserción de tipos de eventos
        test_types = ['entrada', 'salida', 'break_salida', 'break_entrada', 'almuerzo_salida', 'almuerzo_entrada']
        print("\nTipos de eventos permitidos:")
        for event_type in test_types:
            try:
                cursor.execute("""
                    SELECT 1 WHERE %s IN ('entrada', 'salida', 'break_salida', 'break_entrada', 'almuerzo_salida', 'almuerzo_entrada')
                """, (event_type,))
                result = cursor.fetchone()
                status = "✓" if result else "✗"
                print(f"  {status} {event_type}")
            except Exception as e:
                print(f"  ✗ {event_type} - Error: {e}")
        
        conn.close()
        
        print("\nVerificación completada")
        return True
        
    except Exception as e:
        print(f"Error verificando base de datos: {e}")
        return False

if __name__ == "__main__":
    check_database_status()