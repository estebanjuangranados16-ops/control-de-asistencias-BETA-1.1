#!/usr/bin/env python3
"""
Script de diagnóstico de conectividad
"""
import socket
import requests
import os
from dotenv import load_dotenv

def test_connectivity():
    load_dotenv()
    
    host = "db.gyoxiqcnkaimovbuyaas.supabase.co"
    port = 5432
    
    print("🔍 Diagnóstico de conectividad...")
    
    # Test 1: DNS Resolution
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS OK: {host} → {ip}")
    except socket.gaierror as e:
        print(f"❌ Error DNS: {e}")
        print("💡 Solución: Cambiar a conexión pooled")
        return False
    
    # Test 2: Port connectivity
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Puerto {port} accesible")
        else:
            print(f"❌ Puerto {port} no accesible")
            return False
    except Exception as e:
        print(f"❌ Error conectividad: {e}")
        return False
    
    # Test 3: Internet connectivity
    try:
        response = requests.get("https://www.google.com", timeout=5)
        print("✅ Conectividad a internet OK")
    except:
        print("❌ Sin conectividad a internet")
        return False
    
    return True

if __name__ == '__main__':
    test_connectivity()