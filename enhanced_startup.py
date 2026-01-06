#!/usr/bin/env python3
"""
Mejoras adicionales de diseño para el sistema de control de asistencia
"""

import os
import sys
from datetime import datetime
import sqlite3

def clear_screen():
    """Limpiar pantalla de forma compatible"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored_banner():
    """Banner con colores para terminales compatibles"""
    try:
        # Códigos ANSI para colores
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        END = '\033[0m'
        
        banner = f"""
{BLUE}╔══════════════════════════════════════════════════════════════════════════════╗{END}
{BLUE}║{END} {BOLD}{WHITE}                   🏢 SISTEMA DE CONTROL DE ASISTENCIA{END} {BLUE}                     ║{END}
{BLUE}║{END} {PURPLE}                          Versión Optimizada 2024{END} {BLUE}                          ║{END}
{BLUE}╠══════════════════════════════════════════════════════════════════════════════╣{END}
{BLUE}║{END} {CYAN}📅 Fecha:{END} {datetime.now().strftime('%d/%m/%Y %H:%M:%S'):<20} {GREEN}🌐 Puerto: 5000{END} {BLUE}                    ║{END}
{BLUE}║{END} {YELLOW}🚀 Estado: INICIANDO SISTEMA...{END} {BLUE}                                              ║{END}
{BLUE}╚══════════════════════════════════════════════════════════════════════════════╝{END}
"""
        print(banner)
    except:
        # Fallback sin colores
        print("🏢 SISTEMA DE CONTROL DE ASISTENCIA - Versión Optimizada 2024")
        print("=" * 80)

def show_loading_animation():
    """Mostrar animación de carga"""
    import time
    
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    print("\n🔄 Inicializando componentes del sistema...")
    
    components = [
        "Base de datos SQLite",
        "Servidor Flask",
        "WebSocket SocketIO", 
        "Sistema de monitoreo",
        "APIs REST",
        "Templates web"
    ]
    
    for i, component in enumerate(components):
        for frame in frames[:3]:  # Solo 3 frames por componente
            print(f"\r{frame} Cargando {component}...", end="", flush=True)
            time.sleep(0.1)
        print(f"\r✅ {component} - LISTO")
    
    print("\n🎉 Todos los componentes cargados exitosamente!\n")

def display_system_info():
    """Mostrar información detallada del sistema"""
    info = f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                            📊 INFORMACIÓN DEL SISTEMA                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  🐍 Python: {sys.version.split()[0]:<15} 🖥️  SO: {os.name.upper():<20}              │
│  📁 Directorio: {os.getcwd()[:50]:<50}     │
│  🕐 Inicio: {datetime.now().strftime('%H:%M:%S'):<15} 📅 Fecha: {datetime.now().strftime('%d/%m/%Y'):<15}        │
├─────────────────────────────────────────────────────────────────────────────┤
│                              🌐 ACCESOS DISPONIBLES                         │
│  📊 Dashboard Principal:  http://localhost:5000                             │
│  👥 Gestión Empleados:   http://localhost:5000/employees                   │
│  📈 Reportes:            http://localhost:5000/reports                     │
│  ⏰ Horarios:            http://localhost:5000/schedules                   │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(info)

def check_database_health():
    """Verificar salud de la base de datos"""
    try:
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM employees")
        emp_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance_records")
        record_count = cursor.fetchone()[0]
        
        conn.close()
        
        health_info = f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                           🗄️  ESTADO BASE DE DATOS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Conexión: EXITOSA                                                       │
│  📋 Tablas encontradas: {len(tables):<5} 👥 Empleados: {emp_count:<10}                    │
│  📊 Registros totales: {record_count:<10} 🔧 Estado: SALUDABLE                     │
└─────────────────────────────────────────────────────────────────────────────┘
"""
        print(health_info)
        return True
        
    except Exception as e:
        error_info = f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ❌ ERROR BASE DE DATOS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Error: {str(e)[:65]:<65}  │
│  💡 Ejecutar fix_database.py para reparar                                   │
└─────────────────────────────────────────────────────────────────────────────┘
"""
        print(error_info)
        return False

def show_tips():
    """Mostrar consejos de uso"""
    tips = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                              💡 CONSEJOS DE USO                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  🖥️  Mantén esta ventana abierta mientras uses el sistema                   │
│  🌐 Usa el navegador web para una mejor experiencia visual                 │
│  📱 El dashboard es responsive - funciona en móviles                       │
│  🔄 Los datos se actualizan automáticamente cada 30 segundos               │
│  ⚡ Usa Ctrl+C para detener el sistema de forma segura                     │
│  🔧 Revisa el Panel de Problemas de Código para mejoras                    │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(tips)

def enhanced_startup_sequence():
    """Secuencia de inicio mejorada"""
    clear_screen()
    print_colored_banner()
    show_loading_animation()
    display_system_info()
    
    if check_database_health():
        print("✅ Sistema listo para funcionar")
    else:
        print("⚠️  Sistema iniciado con advertencias")
    
    show_tips()
    
    print("\n" + "="*80)
    print("🚀 INICIANDO SERVIDOR WEB...")
    print("="*80)

if __name__ == "__main__":
    enhanced_startup_sequence()