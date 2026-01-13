#!/usr/bin/env python3
"""
Optimización de Notificaciones en Tiempo Real
Corrige errores de SocketIO y mejora el rendimiento
"""

def fix_socketio_notifications():
    """Corregir las notificaciones SocketIO"""
    
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar todas las emisiones con broadcast=True
    content = content.replace(", broadcast=True)", ")")
    content = content.replace("broadcast=True, ", "")
    content = content.replace("broadcast=True)", ")")
    
    # Mejorar el método de emisión de eventos
    old_emit = "            # Emitir evento WebSocket inmediatamente"
    new_emit = """            # Emitir eventos WebSocket optimizados
            try:
                # Evento principal de asistencia
                socketio.emit('attendance_record', {
                    'employee_id': employee_id,
                    'name': employee[0],
                    'event_type': event_type,
                    'timestamp': local_timestamp,
                    'verify_method': verify_method,
                    'department': employee[1] or 'General',
                    'schedule': employee[2] or 'estandar',
                    'real_time': True,
                    'is_break': is_break,
                    'is_lunch': is_lunch,
                    'break_type': break_type
                })
                
                # Evento de actualización rápida
                socketio.emit('quick_update', {
                    'type': 'new_record',
                    'employee_name': employee[0],
                    'event_type': event_type,
                    'timestamp': local_timestamp
                })
                
                print(f"📡 Eventos WebSocket enviados para {employee[0]}")
                
            except Exception as e:
                print(f"❌ Error enviando eventos WebSocket: {e}")
            
            # Emitir evento WebSocket inmediatamente"""
    
    content = content.replace(old_emit, new_emit)
    
    # Agregar método para notificaciones push
    push_method = '''
    def send_push_notification(self, employee_name, event_type, timestamp, department):
        """Enviar notificación push optimizada"""
        try:
            notification_data = {
                'title': f'{employee_name} - {event_type.upper()}',
                'message': f'{department} - {timestamp}',
                'timestamp': timestamp,
                'type': event_type,
                'employee': employee_name,
                'department': department
            }
            
            # Emitir notificación
            socketio.emit('push_notification', notification_data)
            
            return True
        except Exception as e:
            print(f"Error enviando push notification: {e}")
            return False
'''
    
    # Insertar el método antes de start_monitoring
    content = content.replace("    def start_monitoring(self):", push_method + "    def start_monitoring(self):")
    
    # Usar el nuevo método en record_attendance
    old_call = "                print(f\"🔔 NOTIFICACIÓN INSTANTÁNEA: {employee[0]} - {event_type.upper()}\")"
    new_call = """                print(f"🔔 NOTIFICACIÓN INSTANTÁNEA: {employee[0]} - {event_type.upper()}")
                
                # Enviar notificación push
                self.send_push_notification(employee[0], event_type, local_timestamp, employee[1] or 'General')"""
    
    content = content.replace(old_call, new_call)
    
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Notificaciones SocketIO corregidas")

def create_notification_js():
    """Crear JavaScript optimizado para notificaciones"""
    
    js_content = '''// Sistema de Notificaciones Optimizado
console.log('🚀 Iniciando notificaciones optimizadas...');

// Configuración WebSocket
const socket = io({
    transports: ['websocket', 'polling'],
    upgrade: true,
    timeout: 5000,
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 2000
});

let isConnected = false;
let notificationCount = 0;

// Eventos de conexión
socket.on('connect', function() {
    console.log('✅ Conectado al sistema');
    isConnected = true;
    showSystemMessage('Sistema conectado', 'success');
});

socket.on('disconnect', function() {
    console.log('❌ Desconectado');
    isConnected = false;
    showSystemMessage('Conexión perdida', 'error');
});

// Notificaciones principales
socket.on('attendance_record', function(data) {
    console.log('📋 Registro de asistencia:', data);
    showAttendanceNotification(data);
    updateDashboardCounters();
});

socket.on('push_notification', function(data) {
    console.log('🔔 Push notification:', data);
    showPushNotification(data);
});

socket.on('quick_update', function(data) {
    console.log('⚡ Actualización rápida:', data);
    updateQuickCounters(data);
});

// Función para mostrar notificaciones de asistencia
function showAttendanceNotification(data) {
    const notification = document.createElement('div');
    notification.className = 'attendance-notification';
    
    let bgColor = '#28a745';
    let icon = '🟢';
    
    if (data.event_type === 'salida') {
        bgColor = '#dc3545';
        icon = '🔴';
    } else if (data.is_break) {
        bgColor = '#ffc107';
        icon = '☕';
    } else if (data.is_lunch) {
        bgColor = '#17a2b8';
        icon = '🍽️';
    }
    
    notification.style.cssText = `
        position: fixed;
        top: ${20 + (notificationCount * 80)}px;
        right: 20px;
        background: ${bgColor};
        color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        min-width: 300px;
        animation: slideIn 0.5s ease-out;
        cursor: pointer;
    `;
    
    const timeStr = new Date(data.timestamp).toLocaleTimeString();
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 24px;">${icon}</span>
            <div>
                <div style="font-weight: bold; font-size: 16px;">${data.name}</div>
                <div style="font-size: 14px;">${data.event_type.toUpperCase()} - ${data.department}</div>
                <div style="font-size: 12px; opacity: 0.8;">${timeStr}</div>
            </div>
            <button onclick="removeNotification(this)" style="background: none; border: none; color: white; font-size: 18px; cursor: pointer;">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    notificationCount++;
    
    // Reproducir sonido
    playNotificationSound();
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        removeNotification(notification);
    }, 5000);
}

// Función para mostrar push notifications
function showPushNotification(data) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(data.title, {
            body: data.message,
            icon: '/static/images/logo-pcshek.jpg',
            tag: 'attendance-' + Date.now()
        });
    }
}

// Función para remover notificaciones
function removeNotification(element) {
    if (element.parentElement) {
        element.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            element.remove();
            notificationCount = Math.max(0, notificationCount - 1);
            repositionNotifications();
        }, 300);
    }
}

// Reposicionar notificaciones
function repositionNotifications() {
    const notifications = document.querySelectorAll('.attendance-notification');
    notifications.forEach((notification, index) => {
        notification.style.top = `${20 + (index * 80)}px`;
    });
}

// Actualizar contadores del dashboard
function updateDashboardCounters() {
    const totalRecords = document.getElementById('total-records');
    if (totalRecords) {
        const current = parseInt(totalRecords.textContent) || 0;
        totalRecords.textContent = current + 1;
        totalRecords.style.animation = 'pulse 0.5s ease-in-out';
    }
}

// Actualizar contadores rápidos
function updateQuickCounters(data) {
    if (data.type === 'new_record') {
        updateDashboardCounters();
    }
}

// Mostrar mensajes del sistema
function showSystemMessage(message, type) {
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        info: '#17a2b8',
        warning: '#ffc107'
    };
    
    const msg = document.createElement('div');
    msg.style.cssText = `
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        background: ${colors[type] || colors.info};
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        z-index: 10001;
        font-weight: bold;
        animation: fadeInOut 3s ease-in-out;
    `;
    msg.textContent = message;
    
    document.body.appendChild(msg);
    setTimeout(() => msg.remove(), 3000);
}

// Reproducir sonido de notificación
function playNotificationSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
    } catch (error) {
        console.log('No se pudo reproducir sonido');
    }
}

// Solicitar permisos de notificación
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Estilos CSS
const styles = document.createElement('style');
styles.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 0; }
        10%, 90% { opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); color: #28a745; }
        100% { transform: scale(1); }
    }
    
    .attendance-notification:hover {
        transform: scale(1.02);
        transition: transform 0.2s ease;
    }
`;
document.head.appendChild(styles);

console.log('✅ Sistema de notificaciones listo');
'''
    
    with open('static/js/notifications-optimized.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("JavaScript de notificaciones optimizado creado")

if __name__ == '__main__':
    print("OPTIMIZANDO NOTIFICACIONES EN TIEMPO REAL")
    print("=" * 50)
    
    fix_socketio_notifications()
    create_notification_js()
    
    print("=" * 50)
    print("NOTIFICACIONES OPTIMIZADAS")
    print("- Errores de SocketIO corregidos")
    print("- JavaScript optimizado creado")
    print("- Push notifications habilitadas")
    print("- Sonidos mejorados")