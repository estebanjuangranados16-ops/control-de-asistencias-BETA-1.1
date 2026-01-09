#!/usr/bin/env python3
"""
Script para corregir esquema de base de datos
"""
import sqlite3
import os

def fix_database():
    db_path = 'attendance.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar columnas existentes
        cursor.execute("PRAGMA table_info(attendance_records)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Agregar columnas faltantes
        if 'is_break_record' not in columns:
            cursor.execute('ALTER TABLE attendance_records ADD COLUMN is_break_record BOOLEAN DEFAULT 0')
            print("✅ Agregada columna is_break_record")
        
        if 'break_type' not in columns:
            cursor.execute('ALTER TABLE attendance_records ADD COLUMN break_type TEXT DEFAULT NULL')
            print("✅ Agregada columna break_type")
        
        if 'break_duration_minutes' not in columns:
            cursor.execute('ALTER TABLE attendance_records ADD COLUMN break_duration_minutes INTEGER DEFAULT NULL')
            print("✅ Agregada columna break_duration_minutes")
        
        # Agregar empleado faltante
        cursor.execute('INSERT OR IGNORE INTO employees (employee_id, name, department) VALUES (?, ?, ?)', 
                      ('1069643075', 'Empleado Temporal', 'General'))
        
        conn.commit()
        print("✅ Base de datos corregida exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    fix_database()