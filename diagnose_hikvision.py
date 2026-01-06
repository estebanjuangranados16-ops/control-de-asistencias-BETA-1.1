"""
Diagnóstico del dispositivo Hikvision
Verificar IP, conectividad y configuración
"""
import requests
from requests.auth import HTTPDigestAuth
import socket
import subprocess
import platform

def ping_device(ip):
    """Hacer ping al dispositivo"""
    print(f"📡 Haciendo ping a {ip}...")
    
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    try:
        result = subprocess.run(
            ["ping", param, "1", ip],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Ping exitoso - Dispositivo responde")
            return True
        else:
            print("❌ Ping falló - Dispositivo no responde")
            return False
            
    except Exception as e:
        print(f"❌ Error en ping: {e}")
        return False

def scan_network():
    """Escanear red local para encontrar dispositivos"""
    print("\n🔍 ESCANEANDO RED LOCAL...")
    print("Buscando dispositivos Hikvision...")
    
    # Obtener IP local
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        network = ".".join(local_ip.split(".")[:-1])
        print(f"Red local: {network}.x")
        
        # Escanear IPs comunes para Hikvision
        common_ips = [
            f"{network}.64",
            f"{network}.66", 
            f"{network}.100",
            f"{network}.200",
            "192.168.1.64",
            "192.168.1.66",
            "192.168.0.64", 
            "192.168.0.66",
            "172.10.0.66",
            "172.10.1.62"  # IP actual
        ]
        
        found_devices = []
        
        for ip in common_ips:
            print(f"  Probando {ip}...", end=" ")
            
            try:
                # Ping rápido
                result = subprocess.run(
                    ["ping", "-n" if platform.system().lower() == "windows" else "-c", "1", ip],
                    capture_output=True,
                    timeout=2
                )
                
                if result.returncode == 0:
                    print("✅ Responde")
                    found_devices.append(ip)
                else:
                    print("❌")
                    
            except:
                print("❌")
        
        return found_devices
        
    except Exception as e:
        print(f"❌ Error escaneando red: {e}")
        return []

def test_hikvision_connection(ip, username="admin", password="PC2024*+"):
    """Probar conexión específica a Hikvision"""
    print(f"\n🔐 PROBANDO CONEXIÓN HIKVISION: {ip}")
    
    endpoints = [
        f"http://{ip}/ISAPI/System/deviceInfo",
        f"http://{ip}/ISAPI/System/status", 
        f"http://{ip}",
        f"http://{ip}/doc/page/login.asp"
    ]
    
    session = requests.Session()
    session.auth = HTTPDigestAuth(username, password)
    
    for endpoint in endpoints:
        try:
            print(f"  Probando: {endpoint}...", end=" ")
            response = session.get(endpoint, timeout=5)
            
            if response.status_code in [200, 401]:
                print(f"✅ Status: {response.status_code}")
                
                # Si es 200, intentar leer info del dispositivo
                if response.status_code == 200 and "deviceInfo" in endpoint:
                    print(f"    📊 Respuesta: {response.text[:100]}...")
                
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("⏱️ Timeout")
        except requests.exceptions.ConnectionError:
            print("❌ No conecta")
        except Exception as e:
            print(f"❌ Error: {str(e)[:30]}...")
    
    return False

def suggest_solutions():
    """Sugerir soluciones"""
    print("\n💡 POSIBLES SOLUCIONES:")
    print("1. Verificar que el dispositivo esté encendido")
    print("2. Verificar cables de red")
    print("3. Comprobar si cambió la IP del dispositivo")
    print("4. Verificar usuario/contraseña (admin/PC2024*+)")
    print("5. Acceder a la interfaz web del dispositivo")
    print("6. Verificar configuración ISAPI en el dispositivo")
    print("7. Reiniciar el dispositivo")

def main():
    print("🔍 DIAGNÓSTICO DISPOSITIVO HIKVISION")
    print("=" * 50)
    
    current_ip = "172.10.1.62"
    
    # 1. Ping al dispositivo actual
    if ping_device(current_ip):
        # 2. Probar conexión Hikvision
        if test_hikvision_connection(current_ip):
            print("\n✅ DISPOSITIVO FUNCIONANDO CORRECTAMENTE")
            print("💡 El problema puede ser temporal o de configuración")
        else:
            print("\n⚠️ DISPOSITIVO RESPONDE PERO NO HIKVISION")
            print("💡 Verificar credenciales o configuración ISAPI")
    else:
        print(f"\n❌ DISPOSITIVO {current_ip} NO RESPONDE")
        
        # 3. Escanear red para encontrar dispositivos
        found = scan_network()
        
        if found:
            print(f"\n📍 DISPOSITIVOS ENCONTRADOS: {found}")
            
            for ip in found:
                if test_hikvision_connection(ip):
                    print(f"\n🎯 DISPOSITIVO HIKVISION ENCONTRADO: {ip}")
                    print(f"💡 Actualizar DEVICE_IP en .env a: {ip}")
                    break
        else:
            print("\n❌ NO SE ENCONTRARON DISPOSITIVOS")
    
    suggest_solutions()

if __name__ == "__main__":
    main()