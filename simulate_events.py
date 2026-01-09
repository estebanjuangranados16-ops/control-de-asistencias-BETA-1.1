#!/usr/bin/env python3
"""
Simulador de eventos de asistencia para probar breaks y almuerzos
Simula eventos reales del dispositivo Hikvision
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system_optimized_v2 import OptimizedAttendanceSystem
from datetime import datetime, time
import time as time_module

def simulate_real_events():
    """Simular eventos reales en el sistema"""
    
    print("SIMULADOR DE EVENTOS DE ASISTENCIA")
    print("=" * 50)
    
    # Inicializar sistema
    system = OptimizedAttendanceSystem()
    
    # Obtener empleados
    employees = system.get_employees()
    admin_employees = [emp for emp in employees if emp['department'] in ['Reacondicionamiento', 'Logistica', 'Administracion']]
    
    if not admin_employees:
        print("No hay empleados administrativos para simular")
        return
    
    test_employee = admin_employees[0]
    emp_id = test_employee['employee_id']
    emp_name = test_employee['name']
    
    print(f"Empleado de prueba: {emp_name} ({emp_id})")
    print(f"Departamento: {test_employee['department']}")
    
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    
    print(f"Hora actual: {current_hour:02d}:{current_minute:02d}")
    
    # Simular entrada normal
    print("\n1. Simulando ENTRADA normal...")
    result = system.record_attendance(emp_id, datetime.now().isoformat())
    if result:
        print("Entrada registrada exitosamente")
    else:
        print("Error registrando entrada")
    
    time_module.sleep(2)
    
    # Verificar estado después de entrada
    dashboard_data = system.get_dashboard_data()
    inside_count = len(dashboard_data['employees_inside'])
    print(f"Empleados dentro: {inside_count}")
    
    # Simular break si estamos en horario
    if 9 <= current_hour <= 10:
        print(f"\n2. Simulando BREAK (horario válido: {current_hour}:00)...")
        
        # Salida a break
        print("   Salida a break...")
        result = system.record_attendance(emp_id, datetime.now().isoformat())
        if result:
            print("   Salida a break registrada")
        else:
            print("   Error registrando salida a break")
        
        time_module.sleep(3)
        
        # Regreso de break
        print("   Regreso de break...")
        result = system.record_attendance(emp_id, datetime.now().isoformat())
        if result:
            print("   Regreso de break registrado")
        else:
            print("   Error registrando regreso de break")
            
    else:
        print(f"Fuera de horario de break (9:00-10:00). Hora: {current_hour}:00")
    
    time_module.sleep(2)
    
    # Simular almuerzo si estamos en horario
    if 12 <= current_hour <= 14:
        print(f"\n3. Simulando ALMUERZO (horario válido: {current_hour}:00)...")
        
        # Salida a almuerzo
        print("   Salida a almuerzo...")
        result = system.record_attendance(emp_id, datetime.now().isoformat())
        if result:
            print("   Salida a almuerzo registrada")
        else:
            print("   Error registrando salida a almuerzo")
        
        time_module.sleep(3)
        
        # Regreso de almuerzo
        print("   Regreso de almuerzo...")
        result = system.record_attendance(emp_id, datetime.now().isoformat())
        if result:
            print("   Regreso de almuerzo registrado")
        else:
            print("   Error registrando regreso de almuerzo")
            
    else:
        print(f"Fuera de horario de almuerzo (12:00-14:00). Hora: {current_hour}:00")
    
    time_module.sleep(2)
    
    # Verificar estado final
    print("ESTADO FINAL DEL SISTEMA:")
    try:
        import requests
        response = requests.get('http://localhost:5000/api/breaks/status')
        if response.status_code == 200:
            break_status = response.json()
            print(f"   En break: {len(break_status.get('on_break', []))}")
            print(f"   En almuerzo: {len(break_status.get('on_lunch', []))}")
            print(f"   Breaks completados: {break_status.get('breaks_completed', 0)}")
            print(f"   Almuerzos completados: {break_status.get('lunch_completed', 0)}")
        else:
            print("   Error obteniendo estado de breaks")
    except Exception as e:
        print(f"   Error conectando con API: {e}")
    
    # Mostrar registros recientes
    dashboard_data = system.get_dashboard_data()
    recent_records = dashboard_data.get('recent_records', [])
    
    print(f"REGISTROS RECIENTES ({len(recent_records)}):")
    for i, record in enumerate(recent_records[:5]):
        timestamp = str(record[2])[:19] if len(str(record[2])) > 19 else str(record[2])
        print(f"   {i+1}. {record[0]} - {record[1].upper()} - {timestamp}")
    
    print("\n" + "=" * 50)
    print("SIMULACIÓN COMPLETADA")
    print("\nPara ver los resultados en tiempo real:")
    print("   Dashboard: http://localhost:5000")
    print("   Sección: 'Estado de Breaks - Hoy'")

def show_current_time_info():
    """Mostrar información de horarios actuales"""
    now = datetime.now()
    current_time = now.time()
    
    print(f"\nINFORMACIÓN DE HORARIOS ACTUALES:")
    print(f"   Hora actual: {now.strftime('%H:%M:%S')}")
    print(f"   Fecha: {now.strftime('%Y-%m-%d')}")
    
    # Verificar en qué horarios estamos
    if time(9, 0) <= current_time <= time(10, 0):
        print("   HORARIO DE BREAK ADMINISTRATIVO (9:00-10:00)")
    else:
        print("   Fuera de horario de break administrativo")
    
    if time(12, 0) <= current_time <= time(14, 0):
        print("   HORARIO DE ALMUERZO (12:00-14:00)")
    else:
        print("   Fuera de horario de almuerzo")
    
    if time(17, 0) <= current_time <= time(18, 0):
        print("   HORARIO DE BREAK OPERATIVO TARDE (17:00-18:00)")
    else:
        print("   Fuera de horario de break operativo tarde")

if __name__ == "__main__":
    show_current_time_info()
    
    print("\n¿Deseas simular eventos reales en el sistema? (s/n): ", end="")
    response = input().lower().strip()
    
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        simulate_real_events()
    else:
        print("Simulación cancelada.")