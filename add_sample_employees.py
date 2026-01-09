#!/usr/bin/env python3
"""
Script para agregar empleados de prueba
"""
import os
from dotenv import load_dotenv
import psycopg2

def add_sample_employees():
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    employees = [
        ('1069643075', 'Juan Pérez', 'Reacondicionamiento'),
        ('1234567890', 'María García', 'Logistica'),
        ('0987654321', 'Carlos López', 'Operativos'),
        ('1111111111', 'Ana Martínez', 'Administracion'),
    ]
    
    try:
        for emp_id, name, dept in employees:
            cursor.execute('''
                INSERT INTO employees (employee_id, name, department, active) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employee_id) DO NOTHING
            ''', (emp_id, name, dept, True))
        
        conn.commit()
        print("✅ Empleados de prueba agregados")
        
        # Mostrar empleados
        cursor.execute("SELECT employee_id, name, department FROM employees ORDER BY name")
        employees = cursor.fetchall()
        
        print("\n📋 Empleados en la base de datos:")
        for emp in employees:
            print(f"  • {emp[1]} ({emp[0]}) - {emp[2]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_sample_employees()