"""
Script para migrar datos de Supabase a Railway PostgreSQL
Ejecutar cuando Supabase esté disponible
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# URLs de conexión
SUPABASE_URL = "postgresql://postgres.gyoxiqcnkaimovbuyaas:Control2024Hikvision!@aws-1-us-east-1.pooler.supabase.com:5432/postgres"
RAILWAY_URL = "TU_RAILWAY_DATABASE_URL_AQUI"

def migrate_data():
    try:
        # Conectar a Supabase
        supabase_conn = psycopg2.connect(SUPABASE_URL)
        supabase_cursor = supabase_conn.cursor()
        
        # Conectar a Railway
        railway_conn = psycopg2.connect(RAILWAY_URL)
        railway_cursor = railway_conn.cursor()
        
        # Migrar empleados
        supabase_cursor.execute("SELECT * FROM employees")
        employees = supabase_cursor.fetchall()
        
        for emp in employees:
            railway_cursor.execute("""
                INSERT INTO employees (employee_id, name, department, schedule, phone, email, active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (employee_id) DO NOTHING
            """, emp[1:])
        
        # Migrar registros
        supabase_cursor.execute("SELECT * FROM attendance_records")
        records = supabase_cursor.fetchall()
        
        for record in records:
            railway_cursor.execute("""
                INSERT INTO attendance_records (employee_id, event_type, timestamp, reader_no, verify_method, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, record[1:])
        
        railway_conn.commit()
        print("✅ Migración completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'supabase_conn' in locals():
            supabase_conn.close()
        if 'railway_conn' in locals():
            railway_conn.close()

if __name__ == "__main__":
    migrate_data()