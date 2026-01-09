"""
Diagnóstico de conectividad Supabase
"""
import socket
import requests

def test_dns():
    """Probar resolución DNS"""
    print("🔍 PROBANDO DNS...")
    
    hosts = [
        "db.gyoxiqcnkaimovbuyaas.supabase.co",
        "gyoxiqcnkaimovbuyaas.supabase.co",
        "supabase.co"
    ]
    
    for host in hosts:
        try:
            ip = socket.gethostbyname(host)
            print(f"✅ {host} → {ip}")
        except Exception as e:
            print(f"❌ {host} → {e}")

def test_http():
    """Probar conexión HTTP"""
    print("\n🌐 PROBANDO HTTP...")
    
    try:
        response = requests.get("https://gyoxiqcnkaimovbuyaas.supabase.co", timeout=10)
        print(f"✅ HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"❌ HTTP Error: {e}")

def test_ping():
    """Probar ping básico"""
    print("\n📡 PROBANDO PING...")
    
    import subprocess
    import platform
    
    # Comando ping según OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    try:
        result = subprocess.run(
            ["ping", param, "1", "gyoxiqcnkaimovbuyaas.supabase.co"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Ping exitoso")
        else:
            print("❌ Ping falló")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error ping: {e}")

def suggest_solutions():
    """Sugerir soluciones"""
    print("\n💡 POSIBLES SOLUCIONES:")
    print("1. Verificar conexión a internet")
    print("2. Desactivar VPN temporalmente")
    print("3. Cambiar DNS a 8.8.8.8 o 1.1.1.1")
    print("4. Desactivar firewall/antivirus temporalmente")
    print("5. Usar hotspot móvil para probar")
    print("6. Verificar URL en proyecto Supabase")

if __name__ == "__main__":
    print("🚨 DIAGNÓSTICO DE CONECTIVIDAD")
    print("=" * 40)
    
    test_dns()
    test_http()
    test_ping()
    suggest_solutions()