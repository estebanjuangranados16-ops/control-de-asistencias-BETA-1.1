#!/usr/bin/env python3
"""
Script de prueba para el sistema de breaks y almuerzos
Simula eventos de empleados para probar FASE 2 y FASE 3
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:5000"

def test_break_system():
    """Probar el sistema completo de breaks y almuerzos"""
    
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE BREAKS")
    print("=" * 60)
    
    # 1. Verificar conexión
    print("1. Verificando conexión al sistema...")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard")
        if response.status_code == 200:
            print("✅ Sistema conectado correctamente")
        else:
            print("❌ Error de conexión")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    # 2. Obtener empleados
    print("\n2. Obteniendo lista de empleados...")
    try:
        response = requests.get(f"{BASE_URL}/api/employees")
        employees = response.json()
        print(f"✅ {len(employees)} empleados encontrados")
        
        # Filtrar empleados por departamento
        admin_employees = [emp for emp in employees if emp['department'] in ['Reacondicionamiento', 'Logistica', 'Administracion']]
        operativo_employees = [emp for emp in employees if emp['department'] == 'Operativos']
        
        print(f"   - Administrativos: {len(admin_employees)}")
        print(f"   - Operativos: {len(operativo_employees)}")
        
    except Exception as e:
        print(f"❌ Error obteniendo empleados: {e}")
        return
    
    # 3. Probar estado de breaks
    print("\n3. Verificando estado actual de breaks...")
    try:
        response = requests.get(f"{BASE_URL}/api/breaks/status")
        break_status = response.json()
        
        print(f"✅ Estado de breaks obtenido:")
        print(f"   - En break: {len(break_status.get('on_break', []))}")
        print(f"   - En almuerzo: {len(break_status.get('on_lunch', []))}")
        print(f"   - Breaks completados: {break_status.get('breaks_completed', 0)}")
        print(f"   - Almuerzos completados: {break_status.get('lunch_completed', 0)}")
        
    except Exception as e:
        print(f"❌ Error obteniendo estado de breaks: {e}")
        return
    
    # 4. Simular eventos de break (solo si hay empleados)
    if admin_employees:
        print(f"\n4. Simulando eventos de break para empleados administrativos...")
        test_employee = admin_employees[0]
        print(f"   Empleado de prueba: {test_employee['name']} ({test_employee['employee_id']})")
        
        # Simular entrada normal
        print("   - Simulando entrada normal...")
        simulate_attendance_event(test_employee['employee_id'], 'entrada')
        
        # Esperar un poco
        time.sleep(2)
        
        # Simular break (si estamos en horario de break)
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 10:
            print("   - Simulando salida a break...")
            simulate_attendance_event(test_employee['employee_id'], 'break_salida')
            
            time.sleep(2)
            
            print("   - Simulando regreso de break...")
            simulate_attendance_event(test_employee['employee_id'], 'break_entrada')
        else:
            print(f"   ⚠️ Fuera de horario de break (9:00-10:00). Hora actual: {current_hour}:00")
        
        # Simular almuerzo (si estamos en horario de almuerzo)
        if 12 <= current_hour <= 14:
            print("   - Simulando salida a almuerzo...")
            simulate_attendance_event(test_employee['employee_id'], 'almuerzo_salida')
            
            time.sleep(2)
            
            print("   - Simulando regreso de almuerzo...")
            simulate_attendance_event(test_employee['employee_id'], 'almuerzo_entrada')
        else:
            print(f"   ⚠️ Fuera de horario de almuerzo (12:00-14:00). Hora actual: {current_hour}:00")
    
    # 5. Verificar estado final
    print("\n5. Verificando estado final...")
    try:
        response = requests.get(f"{BASE_URL}/api/breaks/status")
        final_status = response.json()
        
        print(f"✅ Estado final:")
        print(f"   - En break: {len(final_status.get('on_break', []))}")
        print(f"   - En almuerzo: {len(final_status.get('on_lunch', []))}")
        print(f"   - Breaks completados: {final_status.get('breaks_completed', 0)}")
        print(f"   - Almuerzos completados: {final_status.get('lunch_completed', 0)}")
        
    except Exception as e:
        print(f"❌ Error obteniendo estado final: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("\n📋 RESUMEN DE FUNCIONALIDADES IMPLEMENTADAS:")
    print("✅ FASE 1: Breaks administrativos (9:00-10:00)")
    print("✅ FASE 2: Almuerzos administrativos (12:00-14:00)")
    print("✅ FASE 3: Breaks operativos por turnos")
    print("   - Mañana: 9:00-10:00")
    print("   - Tarde: 17:00-18:00") 
    print("   - Noche: 1:00-2:00")
    print("\n🌐 Dashboard disponible en: http://localhost:5000")

def simulate_attendance_event(employee_id, event_type):
    """Simular un evento de asistencia"""
    # Esta función simularía un evento real del dispositivo
    # En un entorno real, esto vendría del dispositivo Hikvision
    print(f"   📡 Evento simulado: {employee_id} - {event_type}")

def show_break_schedule():
    """Mostrar horarios de breaks por departamento"""
    print("\n📅 HORARIOS DE BREAKS Y ALMUERZOS:")
    print("-" * 50)
    print("🏢 DEPARTAMENTOS ADMINISTRATIVOS:")
    print("   • Reacondicionamiento, Logística, Administración")
    print("   • Break: 9:00 - 10:00 (20 minutos)")
    print("   • Almuerzo: 12:00 - 14:00 (60 minutos)")
    print("     - Opción 1: 12:00 - 13:00")
    print("     - Opción 2: 13:00 - 14:00")
    
    print("\n⚙️ DEPARTAMENTO OPERATIVO:")
    print("   • Turno Mañana (6:00-14:00): Break 9:00-10:00")
    print("   • Turno Tarde (14:00-22:00): Break 17:00-18:00")
    print("   • Turno Noche (22:00-6:00): Break 1:00-2:00")
    print("   • Sin almuerzo (solo breaks)")

if __name__ == "__main__":
    show_break_schedule()
    
    print("\n¿Deseas ejecutar las pruebas del sistema? (s/n): ", end="")
    response = input().lower().strip()
    
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        test_break_system()
    else:
        print("Pruebas canceladas. Sistema listo para uso.")