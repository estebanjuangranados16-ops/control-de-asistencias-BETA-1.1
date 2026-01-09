import sqlite3
import os

def fix_db_simple():
    """Reparar base de datos sin emojis"""
    db_path = "attendance.db"
    
    if not os.path.exists(db_path):
        print("Base de datos no encontrada")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar columnas actuales
        cursor.execute("PRAGMA table_info(employees)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Columnas actuales: {columns}")
        
        # Agregar columnas faltantes
        missing_columns = []
        
        if 'phone' not in columns:
            cursor.execute('ALTER TABLE employees ADD COLUMN phone TEXT DEFAULT ""')
            missing_columns.append('phone')
        
        if 'email' not in columns:
            cursor.execute('ALTER TABLE employees ADD COLUMN email TEXT DEFAULT ""')
            missing_columns.append('email')
        
        if 'synced_to_device' not in columns:
            cursor.execute('ALTER TABLE employees ADD COLUMN synced_to_device BOOLEAN DEFAULT 0')
            missing_columns.append('synced_to_device')
        
        if 'schedule' not in columns:
            cursor.execute('ALTER TABLE employees ADD COLUMN schedule TEXT DEFAULT "estandar"')
            missing_columns.append('schedule')
        
        conn.commit()
        
        if missing_columns:
            print(f"Columnas agregadas: {missing_columns}")
        else:
            print("Base de datos ya estaba completa")
        
        # Verificar estructura final
        cursor.execute("PRAGMA table_info(employees)")
        final_columns = [col[1] for col in cursor.fetchall()]
        print(f"Columnas finales: {final_columns}")
        
        print("Base de datos reparada exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_db_simple()