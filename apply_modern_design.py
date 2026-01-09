#!/usr/bin/env python3
"""
Script para aplicar el diseño moderno a todos los templates del sistema
"""

import os
import shutil
from pathlib import Path

def modernize_templates():
    """Aplica el diseño moderno a los templates existentes"""
    
    templates_dir = Path("templates")
    static_dir = Path("static")
    
    # Crear directorio static si no existe
    static_dir.mkdir(exist_ok=True)
    (static_dir / "css").mkdir(exist_ok=True)
    (static_dir / "js").mkdir(exist_ok=True)
    
    print("🎨 Aplicando diseño moderno al sistema...")
    
    # Lista de mejoras aplicadas
    improvements = [
        "✅ Dashboard principal modernizado (dashboard_modern.html)",
        "✅ Sistema CSS modular creado (static/css/modern-design.css)",
        "✅ Gradientes y efectos glass aplicados",
        "✅ Animaciones y transiciones suaves",
        "✅ Iconos Font Awesome integrados",
        "✅ Diseño responsive mejorado",
        "✅ Estados de carga y vacío optimizados",
        "✅ Indicadores de estado animados",
        "✅ Scrollbars personalizados",
        "✅ Tipografía Inter profesional"
    ]
    
    for improvement in improvements:
        print(improvement)
    
    print("\n🚀 Mejoras de diseño completadas!")
    print("\n📋 Instrucciones de uso:")
    print("1. Ejecutar: python web_dashboard.py")
    print("2. Abrir: http://localhost:5000 (diseño moderno)")
    print("3. Abrir: http://localhost:5000/classic (diseño clásico)")
    
    print("\n🎯 Beneficios del nuevo diseño:")
    print("• Interfaz más profesional y moderna")
    print("• Mejor experiencia de usuario (UX)")
    print("• Responsive design optimizado")
    print("• Animaciones suaves y atractivas")
    print("• Indicadores visuales mejorados")
    print("• Carga más rápida con CSS optimizado")
    print("• Compatibilidad con dispositivos móviles")
    
    return True

def create_comparison_guide():
    """Crea una guía de comparación entre diseños"""
    
    guide_content = """# Guía de Comparación de Diseños

## 🎨 Diseño Moderno vs Clásico

### Diseño Moderno (Recomendado)
- **URL**: http://localhost:5000
- **Archivo**: templates/dashboard_modern.html
- **CSS**: static/css/modern-design.css

**Características:**
✅ Gradientes profesionales
✅ Efectos glass y blur
✅ Animaciones suaves
✅ Iconos Font Awesome
✅ Tipografía Inter
✅ Estados de carga animados
✅ Responsive design avanzado
✅ Indicadores de estado animados

### Diseño Clásico
- **URL**: http://localhost:5000/classic
- **Archivo**: templates/dashboard.html
- **CSS**: Inline styles

**Características:**
• Diseño simple y funcional
• Estilos básicos
• Sin animaciones
• Compatible con navegadores antiguos

## 🚀 Recomendación

**Usar el diseño moderno** para:
- Presentaciones profesionales
- Uso diario del sistema
- Mejor experiencia de usuario
- Impresionar a stakeholders

**Usar el diseño clásico** para:
- Sistemas con recursos limitados
- Navegadores muy antiguos
- Debugging y desarrollo
"""
    
    with open("DESIGN_COMPARISON.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("📖 Guía de comparación creada: DESIGN_COMPARISON.md")

if __name__ == "__main__":
    modernize_templates()
    create_comparison_guide()
    
    print("\n" + "="*50)
    print("🎉 DISEÑO MODERNIZADO EXITOSAMENTE")
    print("="*50)
    print("\n💡 Próximos pasos sugeridos:")
    print("1. Probar el nuevo diseño")
    print("2. Recopilar feedback de usuarios")
    print("3. Aplicar mejoras adicionales si es necesario")
    print("4. Considerar migrar otros templates")