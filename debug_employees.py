#!/usr/bin/env python3
"""
Script para verificar y corregir empleados en la base de datos
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def check_employees():
    """Verificar empleados en la base de datos"""
    try:
        response = requests.get(f"{BASE_URL}/api/employees")
        if response.status_code == 200:
            employees = response.json()
            
            print("EMPLEADOS EN LA BASE DE DATOS:")
            print("=" * 50)
            
            operativos = []
            for emp in employees:
                print(f"ID: {emp['employee_id']}")
                print(f"Nombre: {emp['name']}")
                print(f"Departamento: {emp['department']}")
                print(f"Activo: {emp['active']}")
                print("-" * 30)
                
                if emp['department'] == 'Operativos' and emp['active']:
                    operativos.append(emp)
            
            print(f"\nEMPLEADOS OPERATIVOS ACTIVOS: {len(operativos)}")
            for op in operativos:
                print(f"- {op['name']} ({op['employee_id']})")
            
            return operativos
            
        else:
            print(f"Error obteniendo empleados: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

def check_technicians_api():
    """Verificar API de técnicos"""
    try:
        response = requests.get(f"{BASE_URL}/api/employees/technicians")
        if response.status_code == 200:
            technicians = response.json()
            
            print(f"\nAPI TÉCNICOS DEVUELVE: {len(technicians)} técnicos")
            for tech in technicians:
                print(f"- {tech['name']} ({tech['employee_id']}) - {tech['department']}")
            
            return technicians
            
        else:
            print(f"Error en API técnicos: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

def test_shift_assignment_direct():
    """Probar asignación directa de turnos"""
    operativos = check_employees()
    
    if len(operativos) >= 3:
        print(f"\nPROBANDO ASIGNACIÓN DIRECTA DE TURNOS...")
        
        shifts = ['mañana', 'tarde', 'noche']
        week_start = "2026-01-06"  # Lunes
        
        for i, shift in enumerate(shifts):
            emp = operativos[i]
            
            data = {
                "employee_ids": [emp['employee_id']],
                "shift_type": shift,
                "week_start": week_start
            }
            
            print(f"Asignando turno {shift} a {emp['name']}...")
            
            try:
                response = requests.post(f"{BASE_URL}/api/schedules/bulk", json=data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"OK - Turno {shift} asignado a {emp['name']}")
                    else:
                        print(f"ERROR - {result.get('message')}")
                else:
                    print(f"ERROR HTTP - {response.status_code}")
                    print(f"Response: {response.text}")
                    
            except Exception as e:
                print(f"ERROR - {e}")
    else:
        print(f"Solo hay {len(operativos)} empleados operativos, se necesitan al menos 3")

if __name__ == "__main__":
    print("VERIFICANDO EMPLEADOS Y TURNOS")
    print("=" * 50)
    
    operativos = check_employees()
    technicians = check_technicians_api()
    
    if operativos and not technicians:
        print("\nPROBLEMA: Hay empleados operativos pero la API de técnicos no los devuelve")
        print("Esto indica un problema en el filtro de la API")
    
    test_shift_assignment_direct()