#!/usr/bin/env python3
"""
Script para agregar empleados operativos de prueba
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# Empleados operativos de prueba
OPERATIVOS_TEST = [
    {"id": "OP001", "name": "Carlos Técnico", "department": "Operativos"},
    {"id": "OP002", "name": "Ana Operativa", "department": "Operativos"},
    {"id": "OP003", "name": "Luis Desarme", "department": "Operativos"},
    {"id": "OP004", "name": "Sofia Técnica", "department": "Operativos"}
]

def add_operativos():
    """Agregar empleados operativos"""
    print("Agregando empleados operativos de prueba...")
    
    for emp in OPERATIVOS_TEST:
        try:
            data = {
                "employee_id": emp["id"],
                "name": emp["name"],
                "department": emp["department"],
                "schedule": "turnos"
            }
            
            response = requests.post(f"{BASE_URL}/api/employees", json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"OK - Empleado creado: {emp['name']}")
                else:
                    print(f"AVISO - Empleado ya existe: {emp['name']}")
            else:
                print(f"ERROR - Error creando {emp['name']}: {response.status_code}")
                
        except Exception as e:
            print(f"ERROR - Error creando {emp['name']}: {e}")

def test_shift_assignment():
    """Probar asignación de turnos"""
    print("\nProbando asignación de turnos...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/employees/technicians")
        if response.status_code == 200:
            technicians = response.json()
            operativos = [t for t in technicians if t['department'] == 'Operativos']
            
            print(f"Técnicos operativos encontrados: {len(operativos)}")
            
            if len(operativos) >= 3:
                shifts = ['mañana', 'tarde', 'noche']
                week_start = "2026-01-06"  # Lunes
                
                for i, shift in enumerate(shifts):
                    emp = operativos[i]
                    
                    data = {
                        "employee_ids": [emp['employee_id']],
                        "shift_type": shift,
                        "week_start": week_start
                    }
                    
                    response = requests.post(f"{BASE_URL}/api/schedules/bulk", json=data)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            print(f"OK - Turno {shift} asignado a {emp['name']}")
                        else:
                            print(f"ERROR - {result.get('message')}")
                    else:
                        print(f"ERROR - HTTP {response.status_code}")
            else:
                print("ERROR - Se necesitan al menos 3 técnicos operativos")
                
        else:
            print(f"ERROR - No se pudieron obtener técnicos: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - Error en asignación: {e}")

if __name__ == "__main__":
    add_operativos()
    test_shift_assignment()
    print("\nCompletado. Revisa el dashboard en http://localhost:5000")