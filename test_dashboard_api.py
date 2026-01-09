#!/usr/bin/env python3
"""
Test simple del API dashboard
"""
import requests
import json

def test_dashboard_api():
    try:
        print("🔍 Probando API dashboard...")
        response = requests.get('http://localhost:5000/api/dashboard', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API responde correctamente")
            print(f"📊 Registros totales: {data.get('total_records', 'N/A')}")
            print(f"👥 Empleados únicos: {data.get('unique_employees', 'N/A')}")
            print(f"🏢 Dentro: {len(data.get('employees_inside', []))}")
            print(f"🚪 Fuera: {len(data.get('employees_outside', []))}")
            
            # Verificar estructura
            required_keys = ['employees_inside', 'employees_outside', 'recent_records']
            for key in required_keys:
                if key not in data:
                    print(f"❌ Falta clave: {key}")
                elif not isinstance(data[key], list):
                    print(f"❌ {key} no es lista: {type(data[key])}")
                else:
                    print(f"✅ {key}: OK ({len(data[key])} elementos)")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_dashboard_api()