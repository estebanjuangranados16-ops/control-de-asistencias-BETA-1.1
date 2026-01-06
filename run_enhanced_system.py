#!/usr/bin/env python3
"""
Sistema de Control de Asistencia - Versión con Diseño Mejorado
Integra todas las mejoras visuales y de interfaz
"""

import os
import sys
import time
from datetime import datetime

# Importar configuración visual
try:
    from visual_config import ICONS, COLORS, BOX_CHARS, MESSAGES, colorize, create_box, format_event
except ImportError:
    # Fallback si no existe el archivo de configuración
    ICONS = {'building': '🏢', 'rocket': '🚀', 'success': '✅', 'error': '❌'}
    COLORS = {'reset': '\033[0m', 'blue': '\033[94m', 'green': '\033[92m'}
    def colorize(text, color='white', bg=None, style=None):
        return text

def clear_screen():
    """Limpiar pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_enhanced_banner():
    """Banner mejorado con colores y animación"""
    clear_screen()
    
    banner_text = f"""
{ICONS.get('building', '🏢')} SISTEMA DE CONTROL DE ASISTENCIA {ICONS.get('building', '🏢')}
                    Versión Optimizada 2024
                    
{ICONS.get('rocket', '🚀')} Iniciando sistema con diseño mejorado...
"""
    
    try:
        print(colorize(banner_text, 'bright_blue', style='bold'))
    except:
        print(banner_text)
    
    # Animación de carga
    loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    print("\n" + colorize("Cargando componentes:", 'bright_yellow'))
    
    components = [
        "Interfaz de consola mejorada",
        "Sistema de colores y iconos", 
        "Banners y mensajes profesionales",
        "Configuración visual personalizable",
        "Formato de eventos mejorado",
        "Sistema de notificaciones visuales"
    ]
    
    for component in components:
        for i in range(3):
            char = loading_chars[i % len(loading_chars)]
            print(f"\r{char} {component}...", end="", flush=True)
            time.sleep(0.1)
        print(f"\r{ICONS.get('success', '✅')} {component} - LISTO")
    
    print(f"\n{ICONS.get('success', '✅')} Todas las mejoras visuales cargadas exitosamente!")

def show_feature_summary():
    """Mostrar resumen de características mejoradas"""
    features = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           🎨 MEJORAS DE DISEÑO APLICADAS                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ✨ Interfaz de consola profesional con banners y colores                   ║
║  🎯 Mensajes de eventos formateados con iconos y colores                    ║
║  📊 Estado del sistema con información detallada y visual                   ║
║  🔄 Animaciones de carga y transiciones suaves                              ║
║  🎨 Sistema de colores ANSI para terminales compatibles                     ║
║  📱 Dashboard web moderno con efectos glass y gradientes                    ║
║  ⚙️  Configuración visual personalizable                                     ║
║  🚀 Secuencia de inicio mejorada con información completa                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(features)

def show_usage_instructions():
    """Mostrar instrucciones de uso mejoradas"""
    instructions = f"""
{colorize('📋 INSTRUCCIONES DE USO:', 'bright_cyan', style='bold')}

{colorize('🖥️  CONSOLA:', 'bright_green')}
  • Esta ventana mostrará eventos en tiempo real con formato mejorado
  • Los mensajes incluyen iconos, colores y información detallada
  • Mantén esta ventana abierta durante el uso del sistema

{colorize('🌐 WEB DASHBOARD:', 'bright_blue')}
  • Accede a http://localhost:5000 para la interfaz web moderna
  • Dashboard con diseño profesional y efectos visuales
  • Actualización automática cada 30 segundos

{colorize('⚡ CONTROLES:', 'bright_yellow')}
  • Ctrl+C: Detener sistema de forma segura
  • F5: Actualizar dashboard web
  • Los eventos se muestran automáticamente

{colorize('🔧 PERSONALIZACIÓN:', 'bright_magenta')}
  • Edita visual_config.py para cambiar colores e iconos
  • Modifica design_config.py para temas del dashboard web
  • Ejecuta apply_modern_design.py para aplicar cambios
"""
    print(instructions)

def show_system_ready():
    """Mostrar mensaje de sistema listo"""
    ready_msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                            {ICONS.get('rocket', '🚀')} SISTEMA INICIADO                                ║
║                                                                              ║
║  {colorize('El sistema está ejecutándose con todas las mejoras visuales', 'bright_green')}      ║
║  {colorize('Disfruta de la nueva experiencia mejorada!', 'bright_blue')}                        ║
║                                                                              ║
║  {colorize('Presiona Ctrl+C para detener el servidor', 'bright_yellow')}                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(ready_msg)

def run_enhanced_system():
    """Ejecutar sistema con mejoras visuales"""
    try:
        # Mostrar secuencia de inicio mejorada
        show_enhanced_banner()
        time.sleep(1)
        
        show_feature_summary()
        time.sleep(1)
        
        show_usage_instructions()
        time.sleep(1)
        
        show_system_ready()
        
        # Importar y ejecutar el sistema principal
        print(f"\n{colorize('Iniciando sistema principal...', 'bright_cyan')}")
        
        # Intentar importar el sistema optimizado
        try:
            import system_optimized
            print(f"{ICONS.get('success', '✅')} Sistema principal cargado exitosamente")
        except ImportError as e:
            print(f"{ICONS.get('error', '❌')} Error al cargar sistema principal: {e}")
            print("Asegúrate de que system_optimized.py esté en el directorio actual")
            return False
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n\n{colorize('🛑 DETENIENDO SISTEMA...', 'bright_red', style='bold')}")
        print(f"{ICONS.get('success', '✅')} Sistema detenido correctamente")
        print(f"{colorize('👋 ¡Hasta luego!', 'bright_green')}")
        return True
    except Exception as e:
        print(f"\n{ICONS.get('error', '❌')} Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print(f"{colorize('Iniciando Sistema de Control de Asistencia...', 'bright_blue', style='bold')}")
    
    if run_enhanced_system():
        print(f"\n{colorize('Sistema finalizado correctamente', 'bright_green')}")
    else:
        print(f"\n{colorize('Sistema finalizado con errores', 'bright_red')}")
        sys.exit(1)

if __name__ == "__main__":
    main()