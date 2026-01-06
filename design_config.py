# Configuración de Diseño - Sistema de Control de Asistencia

## Paleta de Colores Personalizable

### Colores Principales
PRIMARY_BLUE = "#3b82f6"
PRIMARY_PURPLE = "#8b5cf6" 
PRIMARY_GREEN = "#10b981"
PRIMARY_ORANGE = "#f59e0b"
PRIMARY_RED = "#ef4444"

### Gradientes
GRADIENT_PRIMARY = "linear-gradient(135deg, #3b82f6, #8b5cf6)"
GRADIENT_SUCCESS = "linear-gradient(135deg, #10b981, #059669)"
GRADIENT_WARNING = "linear-gradient(135deg, #f59e0b, #d97706)"
GRADIENT_BACKGROUND = "linear-gradient(135deg, #f8fafc 0%, #e0f2fe 50%, #e8eaf6 100%)"

### Configuración de Tema
THEME_CONFIG = {
    "company_name": "Sistema de Control de Asistencia",
    "logo_icon": "fas fa-building",
    "primary_color": PRIMARY_BLUE,
    "accent_color": PRIMARY_PURPLE,
    "success_color": PRIMARY_GREEN,
    "warning_color": PRIMARY_ORANGE,
    "danger_color": PRIMARY_RED,
    "font_family": "Inter",
    "border_radius": "1.5rem",
    "animation_duration": "0.3s",
    "glass_opacity": 0.9,
    "blur_strength": "10px"
}

### Opciones de Personalización Rápida

# Para cambiar a tema oscuro, usar estos colores:
DARK_THEME = {
    "background": "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)",
    "card_bg": "rgba(30, 41, 59, 0.9)",
    "text_primary": "#f1f5f9",
    "text_secondary": "#cbd5e1"
}

# Para tema corporativo azul:
CORPORATE_BLUE = {
    "primary": "#1e40af",
    "secondary": "#3b82f6", 
    "accent": "#60a5fa",
    "background": "linear-gradient(135deg, #eff6ff 0%, #dbeafe 50%, #bfdbfe 100%)"
}

# Para tema verde eco:
ECO_GREEN = {
    "primary": "#059669",
    "secondary": "#10b981",
    "accent": "#34d399", 
    "background": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%)"
}

### Instrucciones de Uso

"""
Para aplicar un tema personalizado:

1. Editar las variables en este archivo
2. Ejecutar: python apply_custom_theme.py
3. Reiniciar el servidor web

Para crear un tema completamente nuevo:

1. Copiar una de las configuraciones existentes
2. Modificar los colores según preferencias
3. Aplicar usando el script de temas
"""

### Configuración Responsive

BREAKPOINTS = {
    "mobile": "480px",
    "tablet": "768px", 
    "desktop": "1024px",
    "large": "1400px"
}

### Configuración de Animaciones

ANIMATIONS = {
    "fade_in": "fadeIn 0.5s ease-out",
    "slide_up": "slideUp 0.6s ease-out", 
    "hover_lift": "translateY(-8px)",
    "button_hover": "translateY(-2px)",
    "pulse_duration": "2s",
    "spin_duration": "1s"
}