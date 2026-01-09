#!/usr/bin/env python3
"""
Script para probar conexión a Supabase
"""
import os
from dotenv import load_dotenv
import psycopg2

def test_supabase_connection():
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL no encontrada en .env")
        return False
    
    try:
        print("🔄 Probando conexión a Supabase...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Probar consulta simple
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance_records")
        records_count = cursor.fetchone()[0]
        
        conn.close()
        
        print("✅ Conexión exitosa a Supabase!")
        print(f"📊 Empleados en BD: {count}")
        print(f"📊 Registros de asistencia: {records_count}")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == '__main__':
    test_supabase_connection()