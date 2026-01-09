"""
Instalador de dependencias para Sistema de Asistencia
Instala todo lo necesario para PostgreSQL y producción
"""
import subprocess
import sys
import os

def install_package(package):
    """Instalar paquete con pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("📦 INSTALADOR DE DEPENDENCIAS")
    print("Sistema de Asistencia Hikvision")
    print("=" * 40)
    
    # Lista de paquetes necesarios
    packages = [
        "psycopg2-binary",  # PostgreSQL driver
        "python-dotenv",    # Variables de entorno
        "flask",           # Framework web
        "flask-socketio",  # WebSocket
        "flask-cors",      # CORS
        "requests",        # HTTP requests
        "gunicorn",        # Servidor producción
        "eventlet",        # Async support
    ]
    
    print("Instalando paquetes necesarios...")
    print()
    
    success_count = 0
    for package in packages:
        print(f"📦 Instalando {package}...", end=" ")
        
        if install_package(package):
            print("✅")
            success_count += 1
        else:
            print("❌")
    
    print()
    print(f"📊 Resultado: {success_count}/{len(packages)} paquetes instalados")
    
    if success_count == len(packages):
        print("✅ Todas las dependencias instaladas correctamente")
        print("\n📋 PRÓXIMO PASO:")
        print("Ejecutar: python setup_supabase.py")
    else:
        print("⚠️  Algunas dependencias fallaron")
        print("💡 Intenta instalar manualmente:")
        print("pip install psycopg2-binary python-dotenv flask flask-socketio")

if __name__ == "__main__":
    main()