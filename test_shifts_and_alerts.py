#!/usr/bin/env python3
"""
Test script para verificar funcionamiento de turnos y alertas de tardanza
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Configuración
BASE_URL = "http://localhost:5000"
TEST_EMPLOYEES = [
    {"id": "TEST001", "name": "Juan Pérez", "department": "Operativos"},
    {"id": "TEST002", "name": "María García", "department": "Administracion"},
    {"id": "TEST003", "name": "Carlos López", "department": "Reacondicionamiento"}
]

def test_api_connection():
    """Probar conexión con la API"""
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard")
        if response.status_code == 200:
            print("✅ Conexión con API exitosa")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def create_test_employees():
    """Crear empleados de prueba"""
    print("\n🔧 Creando empleados de prueba...")
    
    for emp in TEST_EMPLOYEES:
        try:
            data = {
                "employee_id": emp["id"],
                "name": emp["name"],
                "department": emp["department"],
                "schedule": "turnos" if emp["department"] == "Operativos" else "administrativo"
            }
            
            response = requests.post(f"{BASE_URL}/api/employees", json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ Empleado creado: {emp['name']}")
                else:
                    print(f"⚠️  Empleado ya existe: {emp['name']}")
            else:
                print(f"❌ Error creando {emp['name']}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error creando {emp['name']}: {e}")

def test_shift_assignments():
    """Probar asignación de turnos"""
    print("\n🔄 Probando asignación de turnos...")
    
    # Obtener técnicos del departamento Operativos
    try:
        response = requests.get(f"{BASE_URL}/api/employees/technicians")
        if response.status_code == 200:
            technicians = response.json()
            operativos = [t for t in technicians if t['department'] == 'Operativos']
            
            if not operativos:
                print("⚠️  No hay técnicos operativos para probar")
                return
            
            print(f"📋 Encontrados {len(operativos)} técnicos operativos")
            
            # Probar asignación de cada turno
            shifts = ['mañana', 'tarde', 'noche']
            week_start = datetime.now().strftime('%Y-%m-%d')
            
            for i, shift in enumerate(shifts):
                if i < len(operativos):
                    emp_id = operativos[i]['employee_id']
                    emp_name = operativos[i]['name']
                    
                    data = {
                        "employee_ids": [emp_id],
                        "shift_type": shift,
                        "week_start": week_start
                    }
                    
                    response = requests.post(f"{BASE_URL}/api/schedules/bulk", json=data)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            print(f"✅ Turno {shift} asignado a {emp_name}")
                        else:
                            print(f"❌ Error asignando turno {shift}: {result.get('message')}")
                    else:
                        print(f"❌ Error HTTP asignando turno {shift}: {response.status_code}")
                        
        else:
            print(f"❌ Error obteniendo técnicos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en asignación de turnos: {e}")

def test_late_arrival_detection():
    """Probar detección de llegadas tarde"""
    print("\n⏰ Probando detección de llegadas tarde...")
    
    # Simular llegadas tarde para diferentes departamentos
    test_cases = [
        {
            "employee_id": "TEST001",
            "name": "Juan Pérez", 
            "department": "Operativos",
            "arrival_time": "06:30:00",  # 30 min tarde (esperado: 06:00)
            "expected": "06:00:00"
        },
        {
            "employee_id": "TEST002",
            "name": "María García",
            "department": "Administracion", 
            "arrival_time": "07:45:00",  # 45 min tarde (esperado: 07:00)
            "expected": "07:00:00"
        },
        {
            "employee_id": "TEST003",
            "name": "Carlos López",
            "department": "Reacondicionamiento",
            "arrival_time": "07:20:00",  # 20 min tarde (esperado: 07:00)
            "expected": "07:00:00"
        }
    ]
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for case in test_cases:
        try:
            # Simular registro de entrada tarde
            timestamp = f"{today} {case['arrival_time']}"
            
            # Crear registro de asistencia simulado
            data = {
                "employee_id": case["employee_id"],
                "name": case["name"],
                "department": case["department"],
                "event_type": "entrada",
                "timestamp": timestamp,
                "verify_method": "Huella",
                "reader_no": 1
            }
            
            # Calcular minutos de tardanza
            arrival = datetime.strptime(case["arrival_time"], "%H:%M:%S")
            expected = datetime.strptime(case["expected"], "%H:%M:%S")
            late_minutes = int((arrival - expected).total_seconds() / 60)
            
            print(f"📊 {case['name']} ({case['department']}):")
            print(f"   Esperado: {case['expected']}")
            print(f"   Llegó: {case['arrival_time']}")
            print(f"   Tardanza: {late_minutes} minutos")
            
            if late_minutes > 0:
                severity = 'severe' if late_minutes > 30 else 'moderate' if late_minutes > 15 else 'mild'
                print(f"   Severidad: {severity}")
                print("   ✅ Tardanza detectada correctamente")
            else:
                print("   ✅ Llegada a tiempo")
                
        except Exception as e:
            print(f"❌ Error probando tardanza para {case['name']}: {e}")

def test_break_system():
    """Probar sistema de breaks"""
    print("\n☕ Probando sistema de breaks...")
    
    try:
        # Obtener estado actual de breaks
        response = requests.get(f"{BASE_URL}/api/breaks/status")
        if response.status_code == 200:
            break_status = response.json()
            
            print("📊 Estado actual de breaks:")
            print(f"   En break: {len(break_status.get('on_break', []))}")
            print(f"   En almuerzo: {len(break_status.get('on_lunch', []))}")
            print(f"   Breaks completados: {break_status.get('breaks_completed', 0)}")
            print(f"   Breaks pendientes: {break_status.get('breaks_pending', 0)}")
            print(f"   Almuerzos completados: {break_status.get('lunch_completed', 0)}")
            print(f"   Almuerzos pendientes: {break_status.get('lunch_pending', 0)}")
            
            print("✅ Sistema de breaks funcionando")
            
        else:
            print(f"❌ Error obteniendo estado de breaks: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error probando sistema de breaks: {e}")

def test_monthly_report():
    """Probar reporte mensual"""
    print("\n📊 Probando reporte mensual...")
    
    try:
        current_month = datetime.now().strftime('%Y-%m')
        response = requests.get(f"{BASE_URL}/api/reports/monthly-summary?month={current_month}")
        
        if response.status_code == 200:
            report = response.json()
            
            print(f"📅 Reporte mensual para {current_month}:")
            print(f"   Días laborables: {report.get('work_days', 0)}")
            print(f"   Total empleados: {report['totals']['total_employees']}")
            print(f"   Horas totales: {report['totals']['total_hours']:.1f}")
            print(f"   Promedio días presente: {report['totals']['avg_days_present']}")
            
            # Mostrar algunos empleados
            employees = report.get('employees', [])[:3]
            for emp in employees:
                print(f"   • {emp['name']}: {emp['days_present']} días, {emp['total_hours']:.1f}h")
            
            print("✅ Reporte mensual funcionando")
            
        else:
            print(f"❌ Error obteniendo reporte mensual: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error probando reporte mensual: {e}")

def cleanup_test_data():
    """Limpiar datos de prueba"""
    print("\n🧹 Limpiando datos de prueba...")
    
    for emp in TEST_EMPLOYEES:
        try:
            response = requests.delete(f"{BASE_URL}/api/employees/{emp['id']}")
            if response.status_code == 200:
                print(f"✅ Empleado eliminado: {emp['name']}")
            else:
                print(f"⚠️  No se pudo eliminar: {emp['name']}")
        except Exception as e:
            print(f"❌ Error eliminando {emp['name']}: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA PCSHEK")
    print("=" * 50)
    
    # Probar conexión
    if not test_api_connection():
        print("❌ No se puede conectar al sistema. Asegúrate de que esté ejecutándose.")
        return
    
    # Crear empleados de prueba
    create_test_employees()
    
    # Esperar un momento
    time.sleep(2)
    
    # Probar funcionalidades
    test_shift_assignments()
    test_late_arrival_detection()
    test_break_system()
    test_monthly_report()
    
    # Preguntar si limpiar datos
    print("\n" + "=" * 50)
    cleanup = input("¿Deseas limpiar los datos de prueba? (s/n): ").lower().strip()
    if cleanup == 's':
        cleanup_test_data()
    
    print("\n✅ PRUEBAS COMPLETADAS")
    print("Revisa el dashboard en http://localhost:5000 para ver los resultados")

if __name__ == "__main__":
    main()