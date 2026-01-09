#!/usr/bin/env python3
"""
Test script para verificar funcionamiento de turnos y alertas de tardanza
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Configuracion
BASE_URL = "http://localhost:5000"

def test_api_connection():
    """Probar conexion con la API"""
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard")
        if response.status_code == 200:
            print("OK - Conexion con API exitosa")
            return True
        else:
            print(f"ERROR - Error de conexion: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR - Error de conexion: {e}")
        return False

def test_shift_assignments():
    """Probar asignacion de turnos"""
    print("\nProbando asignacion de turnos...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/employees/technicians")
        if response.status_code == 200:
            technicians = response.json()
            operativos = [t for t in technicians if t['department'] == 'Operativos']
            
            print(f"Encontrados {len(operativos)} tecnicos operativos")
            print(f"Total tecnicos: {len(technicians)}")
            
            if operativos:
                # Probar asignacion de turno manana
                emp_id = operativos[0]['employee_id']
                emp_name = operativos[0]['name']
                
                data = {
                    "employee_ids": [emp_id],
                    "shift_type": "manana",
                    "week_start": datetime.now().strftime('%Y-%m-%d')
                }
                
                response = requests.post(f"{BASE_URL}/api/schedules/bulk", json=data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"OK - Turno manana asignado a {emp_name}")
                    else:
                        print(f"ERROR - {result.get('message')}")
                else:
                    print(f"ERROR - HTTP {response.status_code}")
            else:
                print("AVISO - No hay tecnicos operativos para probar")
                
        else:
            print(f"ERROR - No se pudieron obtener tecnicos: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - Error en asignacion de turnos: {e}")

def test_late_arrival_detection():
    """Probar deteccion de llegadas tarde"""
    print("\nProbando deteccion de llegadas tarde...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/alerts/late")
        if response.status_code == 200:
            alerts = response.json()
            print(f"Alertas de tardanza hoy: {len(alerts)}")
            
            for alert in alerts[:3]:  # Mostrar solo las primeras 3
                print(f"  - {alert['name']}: {alert['late_minutes']} min tarde")
                
            print("OK - Sistema de alertas funcionando")
        else:
            print(f"ERROR - No se pudieron obtener alertas: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - Error probando alertas: {e}")

def test_break_system():
    """Probar sistema de breaks"""
    print("\nProbando sistema de breaks...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/breaks/status")
        if response.status_code == 200:
            break_status = response.json()
            
            print("Estado actual de breaks:")
            print(f"  En break: {len(break_status.get('on_break', []))}")
            print(f"  En almuerzo: {len(break_status.get('on_lunch', []))}")
            print(f"  Breaks completados: {break_status.get('breaks_completed', 0)}")
            print(f"  Almuerzos completados: {break_status.get('lunch_completed', 0)}")
            
            print("OK - Sistema de breaks funcionando")
            
        else:
            print(f"ERROR - Error obteniendo breaks: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - Error probando breaks: {e}")

def test_monthly_report():
    """Probar reporte mensual"""
    print("\nProbando reporte mensual...")
    
    try:
        current_month = datetime.now().strftime('%Y-%m')
        response = requests.get(f"{BASE_URL}/api/reports/monthly-summary?month={current_month}")
        
        if response.status_code == 200:
            report = response.json()
            
            print(f"Reporte mensual para {current_month}:")
            print(f"  Dias laborables: {report.get('work_days', 0)}")
            print(f"  Total empleados: {report['totals']['total_employees']}")
            print(f"  Horas totales: {report['totals']['total_hours']:.1f}")
            
            employees = report.get('employees', [])[:3]
            for emp in employees:
                print(f"  - {emp['name']}: {emp['days_present']} dias, {emp['total_hours']:.1f}h")
            
            print("OK - Reporte mensual funcionando")
            
        else:
            print(f"ERROR - Error obteniendo reporte: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - Error probando reporte: {e}")

def test_dashboard_data():
    """Probar datos del dashboard"""
    print("\nProbando datos del dashboard...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard")
        if response.status_code == 200:
            data = response.json()
            
            print("Estado del dashboard:")
            print(f"  Empleados dentro: {len(data.get('employees_inside', []))}")
            print(f"  Empleados fuera: {len(data.get('employees_outside', []))}")
            print(f"  Conectado: {data.get('connected', False)}")
            
            print("OK - Dashboard funcionando")
            
        else:
            print(f"ERROR - Error obteniendo dashboard: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - Error probando dashboard: {e}")

def main():
    """Funcion principal de pruebas"""
    print("INICIANDO PRUEBAS DEL SISTEMA PCSHEK")
    print("=" * 50)
    
    # Probar conexion
    if not test_api_connection():
        print("ERROR - No se puede conectar al sistema")
        return
    
    # Probar funcionalidades
    test_dashboard_data()
    test_shift_assignments()
    test_late_arrival_detection()
    test_break_system()
    test_monthly_report()
    
    print("\n" + "=" * 50)
    print("PRUEBAS COMPLETADAS")
    print("Revisa el dashboard en http://localhost:5000")

if __name__ == "__main__":
    main()