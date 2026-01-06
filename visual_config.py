# Configuración Visual del Sistema de Control de Asistencia

# Iconos y Emojis
ICONS = {
    'building': '🏢',
    'user': '👤',
    'users': '👥',
    'clock': '⏰',
    'calendar': '📅',
    'chart': '📊',
    'report': '📈',
    'database': '🗄️',
    'network': '🌐',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'loading': '🔄',
    'rocket': '🚀',
    'gear': '⚙️',
    'tool': '🔧',
    'entry': '🟢',
    'exit': '🔴',
    'fingerprint': '👆',
    'door': '🚪',
    'monitor': '📺',
    'phone': '📱',
    'email': '📧',
    'department': '🏬',
    'schedule': '📋',
    'reacondicionamiento': '🔧'
}

# Colores ANSI para terminal
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'underline': '\033[4m',
    'blink': '\033[5m',
    'reverse': '\033[7m',
    'strikethrough': '\033[9m',
    
    # Colores de texto
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright_black': '\033[90m',
    'bright_red': '\033[91m',
    'bright_green': '\033[92m',
    'bright_yellow': '\033[93m',
    'bright_blue': '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan': '\033[96m',
    'bright_white': '\033[97m',
    
    # Colores de fondo
    'bg_black': '\033[40m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
    'bg_magenta': '\033[45m',
    'bg_cyan': '\033[46m',
    'bg_white': '\033[47m'
}

# Caracteres para bordes y cajas
BOX_CHARS = {
    'horizontal': '─',
    'vertical': '│',
    'top_left': '┌',
    'top_right': '┐',
    'bottom_left': '└',
    'bottom_right': '┘',
    'cross': '┼',
    'tee_down': '┬',
    'tee_up': '┴',
    'tee_right': '├',
    'tee_left': '┤',
    
    # Doble línea
    'double_horizontal': '═',
    'double_vertical': '║',
    'double_top_left': '╔',
    'double_top_right': '╗',
    'double_bottom_left': '╚',
    'double_bottom_right': '╝',
    'double_cross': '╬',
    'double_tee_down': '╦',
    'double_tee_up': '╩',
    'double_tee_right': '╠',
    'double_tee_left': '╣'
}

# Configuración de mensajes
MESSAGES = {
    'startup': {
        'title': 'SISTEMA DE CONTROL DE ASISTENCIA',
        'subtitle': 'Versión Optimizada 2024',
        'loading': 'Inicializando componentes...',
        'ready': 'Sistema listo para usar',
        'port': 'Puerto: 5000'
    },
    'connection': {
        'testing': 'Probando conexión con dispositivo...',
        'connected': 'DISPOSITIVO CONECTADO',
        'disconnected': 'DISPOSITIVO NO DISPONIBLE',
        'monitoring_active': 'Monitoreo de eventos activo',
        'monitoring_inactive': 'Sistema en modo sin monitoreo'
    },
    'database': {
        'healthy': 'Base de datos saludable',
        'error': 'Error en base de datos',
        'repair_needed': 'Ejecutar fix_database.py para reparar'
    },
    'events': {
        'entry': 'ENTRADA',
        'exit': 'SALIDA',
        'authorized': 'Acceso autorizado',
        'denied': 'Acceso denegado'
    }
}

# Configuración de departamentos
DEPARTMENTS = {
    'General': {
        'icon': '🏢',
        'color': 'blue',
        'schedule': 'estandar'
    },
    'Reacondicionamiento': {
        'icon': '🔧',
        'color': 'yellow',
        'schedule': 'reacondicionamiento',
        'times': ['07:00', '09:30', '09:50', '12:40', '13:40', '17:00']
    },
    'Administración': {
        'icon': '💼',
        'color': 'green',
        'schedule': 'estandar'
    },
    'Seguridad': {
        'icon': '🛡️',
        'color': 'red',
        'schedule': '24h'
    }
}

# Configuración de horarios
SCHEDULES = {
    'estandar': {
        'name': 'Horario Estándar',
        'entry': '08:00',
        'exit': '17:00',
        'lunch_start': '12:00',
        'lunch_end': '13:00'
    },
    'reacondicionamiento': {
        'name': 'Reacondicionamiento',
        'times': {
            'entry_1': '07:00',
            'break_out': '09:30',
            'break_in': '09:50',
            'lunch_out': '12:40',
            'lunch_in': '13:40',
            'exit_normal': '17:00',
            'exit_friday': '16:00'
        }
    },
    '24h': {
        'name': 'Turno 24 Horas',
        'flexible': True
    }
}

# Configuración de la interfaz web
WEB_CONFIG = {
    'theme': {
        'primary_color': '#3b82f6',
        'secondary_color': '#8b5cf6',
        'success_color': '#10b981',
        'warning_color': '#f59e0b',
        'danger_color': '#ef4444',
        'background_gradient': 'linear-gradient(135deg, #f8fafc 0%, #e0f2fe 50%, #e8eaf6 100%)'
    },
    'animations': {
        'duration': '0.3s',
        'easing': 'ease-out',
        'hover_lift': '-8px',
        'button_hover': '-2px'
    },
    'layout': {
        'max_width': '1400px',
        'border_radius': '1.5rem',
        'card_padding': '2rem',
        'grid_gap': '1.5rem'
    }
}

# Funciones de utilidad para aplicar estilos
def colorize(text, color='white', bg=None, style=None):
    """Aplicar color y estilo a texto"""
    result = ""
    
    if style:
        if style in COLORS:
            result += COLORS[style]
    
    if color in COLORS:
        result += COLORS[color]
    
    if bg and f'bg_{bg}' in COLORS:
        result += COLORS[f'bg_{bg}']
    
    result += text + COLORS['reset']
    return result

def create_box(content, width=80, style='single'):
    """Crear caja con contenido"""
    if style == 'double':
        h = BOX_CHARS['double_horizontal']
        v = BOX_CHARS['double_vertical']
        tl = BOX_CHARS['double_top_left']
        tr = BOX_CHARS['double_top_right']
        bl = BOX_CHARS['double_bottom_left']
        br = BOX_CHARS['double_bottom_right']
    else:
        h = BOX_CHARS['horizontal']
        v = BOX_CHARS['vertical']
        tl = BOX_CHARS['top_left']
        tr = BOX_CHARS['top_right']
        bl = BOX_CHARS['bottom_left']
        br = BOX_CHARS['bottom_right']
    
    lines = content.split('\n')
    box = tl + h * (width - 2) + tr + '\n'
    
    for line in lines:
        padding = width - len(line) - 2
        box += v + line + ' ' * padding + v + '\n'
    
    box += bl + h * (width - 2) + br
    return box

def format_event(employee_name, event_type, timestamp, department='General'):
    """Formatear evento de asistencia"""
    dept_config = DEPARTMENTS.get(department, DEPARTMENTS['General'])
    dept_icon = dept_config['icon']
    event_icon = ICONS['entry'] if event_type == 'entrada' else ICONS['exit']
    
    return f"{event_icon} {dept_icon} {employee_name:<20} │ {event_type.upper():<7} │ {timestamp} │ {department}"

# Configuración de logging
LOG_CONFIG = {
    'format': '%(asctime)s │ %(levelname)s │ %(message)s',
    'date_format': '%H:%M:%S',
    'level': 'INFO',
    'file': 'attendance_system.log'
}

# Configuración de notificaciones
NOTIFICATIONS = {
    'sound_enabled': False,
    'desktop_enabled': True,
    'email_enabled': False,
    'webhook_enabled': False
}

# Configuración de exportación
EXPORT_CONFIG = {
    'formats': ['csv', 'excel', 'pdf'],
    'default_format': 'csv',
    'include_charts': True,
    'logo_path': 'static/images/logo.png'
}