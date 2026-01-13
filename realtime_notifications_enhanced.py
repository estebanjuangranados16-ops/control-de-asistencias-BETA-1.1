#!/usr/bin/env python3
"""
Sistema de Notificaciones en Tiempo Real Mejorado
Optimizado para máxima velocidad y confiabilidad
"""

def enhance_realtime_notifications():
    """Mejorar el sistema de notificaciones en tiempo real"""
    
    # Leer archivo principal
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. MEJORAR EL MÉTODO record_attendance para notificaciones instantáneas
    old_notification = """            # NOTIFICACIÓN SIMPLE
            try:
                socketio.emit('new_record', {
                    'name': employee[0],
                    'event_type': event_type,
                    'timestamp': local_timestamp,
                    'department': employee[1] or 'General'
                }, broadcast=True)
                print(f"✅ Notificación: {employee[0]} - {event_type}")
            except Exception as e:
                print(f"❌ Error notificación: {e}")"""
    
    new_notification = """            # 🚀 NOTIFICACIONES INSTANTÁNEAS MEJORADAS
            try:
                # Notificación principal con todos los datos
                notification_data = {
                    'employee_id': employee_id,
                    'name': employee[0],
                    'event_type': event_type,
                    'timestamp': local_timestamp,
                    'department': employee[1] or 'General',
                    'is_break': is_break,
                    'is_lunch': is_lunch,
                    'break_type': break_type,
                    'real_time': True
                }
                
                # Emitir múltiples eventos para diferentes componentes
                socketio.emit('instant_notification', notification_data, broadcast=True)
                socketio.emit('new_record', notification_data, broadcast=True)
                socketio.emit('attendance_update', notification_data, broadcast=True)
                
                # Actualización rápida de contadores
                socketio.emit('counter_update', {
                    'type': 'increment',
                    'employee_name': employee[0],
                    'timestamp': local_timestamp
                }, broadcast=True)
                
                print(f"🔔 NOTIFICACIÓN INSTANTÁNEA: {employee[0]} - {event_type.upper()}")
                
            except Exception as e:
                print(f"❌ Error notificación: {e}")"""
    
    content = content.replace(old_notification, new_notification)
    
    # 2. AGREGAR ENDPOINTS ULTRA RÁPIDOS
    api_endpoints = """@app.route('/api/quick_dashboard')
def api_quick_dashboard():
    \"\"\"Dashboard ultra rápido - solo datos esenciales\"\"\"
    try:
        conn = system.get_connection()
        cursor = conn.cursor()
        
        if system.db_type == 'postgresql':
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
            total_records = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
            unique_employees = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE date(timestamp) = date('now')")
            total_records = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE date(timestamp) = date('now')")
            unique_employees = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_records': total_records,
            'unique_employees': unique_employees,
            'connected': system.connected,
            'monitoring': system.monitoring,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'total_records': 0,
            'unique_employees': 0,
            'connected': False,
            'monitoring': False,
            'error': str(e)
        })

@app.route('/api/instant_status')
def api_instant_status():
    \"\"\"Estado instantáneo del sistema\"\"\"
    return jsonify({
        'connected': system.connected,
        'monitoring': system.monitoring,
        'timestamp': datetime.now().isoformat(),
        'status': 'active' if system.monitoring else 'inactive',
        'device_ip': system.device_ip
    })

@app.route('/api/live_feed')
def api_live_feed():
    \"\"\"Feed en vivo de los últimos 5 registros\"\"\"
    try:
        conn = system.get_connection()
        cursor = conn.cursor()
        
        if system.db_type == 'postgresql':
            cursor.execute('''
                SELECT e.name, ar.event_type, ar.timestamp, e.department
                FROM attendance_records ar
                JOIN employees e ON ar.employee_id = e.employee_id
                WHERE e.active = true
                ORDER BY ar.timestamp DESC LIMIT 5
            ''')
        else:
            cursor.execute('''
                SELECT e.name, ar.event_type, ar.timestamp, e.department
                FROM attendance_records ar
                JOIN employees e ON ar.employee_id = e.employee_id
                WHERE e.active = 1
                ORDER BY ar.timestamp DESC LIMIT 5
            ''')
        
        records = cursor.fetchall()
        conn.close()
        
        return jsonify([{
            'name': record[0],
            'event_type': record[1],
            'timestamp': record[2],
            'department': record[3]
        } for record in records])
        
    except Exception as e:
        return jsonify([])

@app.route('/api/dashboard')"""
    
    content = content.replace("@app.route('/api/dashboard')", api_endpoints)
    
    # 3. MEJORAR EL PROCESAMIENTO DE EVENTOS
    old_process = """    def _process_event(self, event):
        \"\"\"Procesar eventos del dispositivo\"\"\"
        if 'AccessControllerEvent' in event:
            acs_event = event['AccessControllerEvent']
            sub_type = acs_event.get('subEventType')
            
            if sub_type == 38:  # Acceso autorizado
                employee_id = acs_event.get('employeeNoString')
                timestamp = event.get('dateTime', datetime.now().isoformat())
                reader_no = acs_event.get('cardReaderNo', 1)
                verify_method = 'huella'  # Simplificado
                
                if employee_id:
                    self.record_attendance(employee_id, timestamp, reader_no, verify_method)"""
    
    new_process = """    def _process_event(self, event):
        \"\"\"Procesar eventos del dispositivo de forma ultra rápida\"\"\"
        try:
            if 'AccessControllerEvent' in event:
                acs_event = event['AccessControllerEvent']
                sub_type = acs_event.get('subEventType')
                
                if sub_type == 38:  # Acceso autorizado
                    employee_id = acs_event.get('employeeNoString')
                    
                    if employee_id:
                        # Procesar inmediatamente en hilo separado
                        import threading
                        
                        def process_attendance():
                            try:
                                timestamp = datetime.now().isoformat()
                                self.record_attendance(employee_id, timestamp, 1, 'huella')
                                
                                # Emitir evento de procesamiento exitoso
                                socketio.emit('event_processed', {
                                    'employee_id': employee_id,
                                    'timestamp': timestamp,
                                    'success': True
                                }, broadcast=True)
                                
                            except Exception as e:
                                print(f"❌ Error procesando asistencia: {e}")
                                socketio.emit('event_processed', {
                                    'employee_id': employee_id,
                                    'success': False,
                                    'error': str(e)
                                }, broadcast=True)
                        
                        # Ejecutar en hilo separado para no bloquear
                        thread = threading.Thread(target=process_attendance, daemon=True)
                        thread.start()
                        
                        print(f"⚡ EVENTO RECIBIDO: {employee_id}")
                        
        except Exception as e:
            print(f"❌ Error procesando evento: {e}")"""
    
    content = content.replace(old_process, new_process)
    
    # 4. AGREGAR WEBSOCKET EVENTS MEJORADOS
    websocket_events = """
# 🚀 WEBSOCKET EVENTS MEJORADOS
@socketio.on('connect')
def handle_connect():
    print('🔌 Cliente conectado')
    emit('connection_status', {
        'connected': system.connected,
        'monitoring': system.monitoring,
        'timestamp': datetime.now().isoformat(),
        'message': 'Conectado al sistema PCSHEK'
    })

@socketio.on('disconnect')
def handle_disconnect():
    print('🔌 Cliente desconectado')

@socketio.on('request_update')
def handle_request_update():
    \"\"\"Cliente solicita actualización inmediata\"\"\"
    try:
        dashboard_data = system.get_dashboard_data()
        emit('dashboard_update', dashboard_data)
        emit('update_complete', {'success': True, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        emit('update_complete', {'success': False, 'error': str(e)})

@socketio.on('ping')
def handle_ping():
    \"\"\"Mantener conexión activa\"\"\"
    emit('pong', {'timestamp': datetime.now().isoformat()})

# WebSocket events originales"""
    
    # Insertar antes de los eventos WebSocket existentes
    content = content.replace("# WebSocket events\n@socketio.on('connect')", websocket_events + "\n@socketio.on('connect')")
    
    # 5. OPTIMIZAR EL MONITOREO
    old_monitor = """    def _monitor_events(self):
        \"\"\"Monitoreo de eventos del dispositivo\"\"\"
        url = f\"http://{self.device_ip}/ISAPI/Event/notification/alertStream\""""
    
    new_monitor = """    def _monitor_events(self):
        \"\"\"Monitoreo optimizado de eventos del dispositivo\"\"\"
        url = f\"http://{self.device_ip}/ISAPI/Event/notification/alertStream\"
        
        # Configurar timeout más agresivo
        self.session.timeout = 30"""
    
    content = content.replace(old_monitor, new_monitor)
    
    # Guardar archivo modificado
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Sistema de notificaciones en tiempo real mejorado")

def create_enhanced_js():
    """Crear JavaScript mejorado para notificaciones"""
    
    js_content = """// 🚀 SISTEMA DE NOTIFICACIONES INSTANTÁNEAS MEJORADO
console.log('🚀 Iniciando sistema de notificaciones mejorado...');

// Configuración WebSocket optimizada
const socket = io({
    transports: ['websocket', 'polling'],
    upgrade: true,
    rememberUpgrade: true,
    timeout: 3000,
    forceNew: false,
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1000
});

// Variables globales
let lastNotificationTime = 0;
let notificationQueue = [];
let isConnected = false;
let pingInterval;

// 🔌 EVENTOS DE CONEXIÓN
socket.on('connect', function() {
    console.log('✅ Conectado al servidor PCSHEK');
    isConnected = true;
    showSystemNotification('✅ Sistema conectado', 'success');
    
    // Iniciar ping para mantener conexión
    pingInterval = setInterval(() => {
        socket.emit('ping');
    }, 30000);
    
    // Solicitar actualización inicial
    socket.emit('request_update');
});

socket.on('disconnect', function() {
    console.log('❌ Desconectado del servidor');
    isConnected = false;
    showSystemNotification('❌ Conexión perdida - Reintentando...', 'error');
    
    if (pingInterval) {
        clearInterval(pingInterval);
    }
});

socket.on('connection_status', function(data) {
    console.log('📡 Estado de conexión:', data);
    updateConnectionStatus(data);
});

// 🔔 NOTIFICACIONES INSTANTÁNEAS
socket.on('instant_notification', function(data) {
    console.log('🔔 Notificación instantánea:', data);
    
    // Evitar duplicados
    const now = Date.now();
    if (now - lastNotificationTime < 500) {
        return;
    }
    lastNotificationTime = now;
    
    // Mostrar notificación inmediatamente
    showInstantNotification(data);
    
    // Actualizar contadores
    updateCountersInstantly(data);
    
    // Reproducir sonido
    playNotificationSound(data.event_type);
});

socket.on('counter_update', function(data) {
    console.log('📊 Actualización de contador:', data);
    updateQuickStats(data);
});

socket.on('attendance_update', function(data) {
    console.log('👥 Actualización de asistencia:', data);
    updateEmployeeStatus(data);
});

socket.on('event_processed', function(data) {
    console.log('⚡ Evento procesado:', data);
    if (!data.success) {
        showSystemNotification(`❌ Error procesando evento: ${data.error}`, 'error');
    }
});

// 📊 ACTUALIZACIONES DEL DASHBOARD
socket.on('dashboard_update', function(data) {
    console.log('📊 Actualización del dashboard:', data);
    updateDashboardData(data);
});

socket.on('update_complete', function(data) {
    if (data.success) {
        console.log('✅ Actualización completada');
    } else {
        console.error('❌ Error en actualización:', data.error);
    }
});

// 🎨 FUNCIÓN PARA MOSTRAR NOTIFICACIONES INSTANTÁNEAS
function showInstantNotification(data) {
    // Crear notificación visual
    const notification = document.createElement('div');
    notification.className = 'instant-notification';
    
    // Determinar estilo según tipo de evento
    let bgColor, icon, title;
    
    if (data.event_type === 'entrada') {
        bgColor = '#28a745';
        icon = '🟢';
        title = 'ENTRADA';
    } else if (data.event_type === 'salida') {
        bgColor = '#dc3545';
        icon = '🔴';
        title = 'SALIDA';
    } else if (data.is_break) {
        bgColor = '#ffc107';
        icon = '☕';
        title = data.event_type.includes('salida') ? 'BREAK INICIADO' : 'REGRESO DE BREAK';
    } else if (data.is_lunch) {
        bgColor = '#17a2b8';
        icon = '🍽️';
        title = data.event_type.includes('salida') ? 'ALMUERZO INICIADO' : 'REGRESO DE ALMUERZO';
    } else {
        bgColor = '#6c757d';
        icon = '📋';
        title = data.event_type.toUpperCase();
    }
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${bgColor};
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: bold;
        font-size: 16px;
        min-width: 320px;
        max-width: 400px;
        animation: slideInBounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        cursor: pointer;
        border-left: 5px solid rgba(255,255,255,0.3);
    `;
    
    const timeStr = new Date(data.timestamp).toLocaleTimeString('es-CO', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 28px;">${icon}</span>
            <div style="flex: 1;">
                <div style="font-size: 18px; margin-bottom: 4px;">${data.name}</div>
                <div style="font-size: 14px; opacity: 0.9; margin-bottom: 2px;">
                    ${title} - ${data.department}
                </div>
                <div style="font-size: 12px; opacity: 0.8;">
                    ${timeStr}
                </div>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; opacity: 0.7; padding: 0; margin-left: 8px;">×</button>
        </div>
    `;
    
    // Agregar efecto hover
    notification.addEventListener('mouseenter', () => {
        notification.style.transform = 'scale(1.02)';
        notification.style.transition = 'transform 0.2s ease';
    });
    
    notification.addEventListener('mouseleave', () => {
        notification.style.transform = 'scale(1)';
    });
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 6 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutBounce 0.4s ease-in';
            setTimeout(() => notification.remove(), 400);
        }
    }, 6000);
}

// 🔊 FUNCIÓN PARA REPRODUCIR SONIDOS
function playNotificationSound(eventType) {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Diferentes tonos según el evento
        if (eventType === 'entrada') {
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.1);
        } else if (eventType === 'salida') {
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(400, audioContext.currentTime + 0.1);
        } else {
            oscillator.frequency.setValueAtTime(700, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(700, audioContext.currentTime + 0.1);
        }
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (error) {
        console.log('No se pudo reproducir sonido:', error);
    }
}

// 📊 ACTUALIZAR CONTADORES INSTANTÁNEAMENTE
function updateCountersInstantly(data) {
    const totalRecords = document.getElementById('total-records');
    if (totalRecords) {
        const current = parseInt(totalRecords.textContent) || 0;
        totalRecords.textContent = current + 1;
        totalRecords.style.animation = 'pulse 0.6s ease-in-out';
        
        // Agregar efecto de brillo
        totalRecords.style.color = '#28a745';
        setTimeout(() => {
            totalRecords.style.color = '';
        }, 1000);
    }
}

// 👥 ACTUALIZAR ESTADO DE EMPLEADOS
function updateEmployeeStatus(data) {
    // Buscar y actualizar el estado del empleado en la lista
    const employeeElements = document.querySelectorAll('[data-employee-id]');
    employeeElements.forEach(element => {
        if (element.dataset.employeeId === data.employee_id) {
            // Actualizar estado visual
            element.classList.remove('employee-inside', 'employee-outside');
            if (data.event_type === 'entrada') {
                element.classList.add('employee-inside');
            } else {
                element.classList.add('employee-outside');
            }
            
            // Agregar efecto de actualización
            element.style.animation = 'highlight 1s ease-in-out';
        }
    });
}

// 🔄 ACTUALIZAR DATOS DEL DASHBOARD
function updateDashboardData(data) {
    // Actualizar contadores
    const elements = {
        'total-records': data.total_records,
        'unique-employees': data.unique_employees
    };
    
    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element && element.textContent !== String(value)) {
            element.textContent = value;
            element.style.animation = 'pulse 0.5s ease-in-out';
        }
    });
    
    // Actualizar estado de conexión
    updateConnectionStatus({
        connected: data.connected,
        monitoring: data.monitoring
    });
}

// 📡 ACTUALIZAR ESTADO DE CONEXIÓN
function updateConnectionStatus(status) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        if (status.connected && status.monitoring) {
            statusElement.innerHTML = '🟢 Conectado';
            statusElement.className = 'status-connected';
        } else if (status.connected) {
            statusElement.innerHTML = '🟡 Conectado (Sin monitoreo)';
            statusElement.className = 'status-warning';
        } else {
            statusElement.innerHTML = '🔴 Desconectado';
            statusElement.className = 'status-disconnected';
        }
    }
}

// 🔔 NOTIFICACIONES DEL SISTEMA
function showSystemNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'system-notification';
    
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        info: '#17a2b8',
        warning: '#ffc107'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        z-index: 9999;
        font-size: 14px;
        max-width: 300px;
        animation: fadeInOut 4s ease-in-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 4000);
}

// 🎨 ESTILOS CSS MEJORADOS
const enhancedStyles = document.createElement('style');
enhancedStyles.textContent = `
    @keyframes slideInBounce {
        0% { 
            transform: translateX(100%) scale(0.8); 
            opacity: 0; 
        }
        60% { 
            transform: translateX(-10px) scale(1.05); 
            opacity: 1; 
        }
        100% { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
        }
    }
    
    @keyframes slideOutBounce {
        0% { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
        }
        100% { 
            transform: translateX(100%) scale(0.8); 
            opacity: 0; 
        }
    }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 0; transform: translateY(-10px); }
        10%, 90% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); color: #28a745; }
        100% { transform: scale(1); }
    }
    
    @keyframes highlight {
        0% { background-color: transparent; }
        50% { background-color: rgba(40, 167, 69, 0.2); }
        100% { background-color: transparent; }
    }
    
    .instant-notification:hover {
        transform: scale(1.02) !important;
        transition: transform 0.2s ease;
    }
    
    .status-connected { color: #28a745; font-weight: bold; }
    .status-warning { color: #ffc107; font-weight: bold; }
    .status-disconnected { color: #dc3545; font-weight: bold; }
    
    .employee-inside { border-left: 4px solid #28a745; }
    .employee-outside { border-left: 4px solid #dc3545; }
`;
document.head.appendChild(enhancedStyles);

// 🚀 INICIALIZACIÓN
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Sistema de notificaciones mejorado listo');
    
    // Verificar estado cada 30 segundos
    setInterval(() => {
        if (isConnected) {
            fetch('/api/instant_status')
                .then(response => response.json())
                .then(data => {
                    updateConnectionStatus(data);
                    if (!data.monitoring) {
                        showSystemNotification('⚠️ Monitoreo inactivo', 'warning');
                    }
                })
                .catch(error => {
                    console.error('Error verificando estado:', error);
                    showSystemNotification('❌ Error de comunicación', 'error');
                });
        }
    }, 30000);
    
    // Actualización periódica del dashboard
    setInterval(() => {
        if (isConnected) {
            socket.emit('request_update');
        }
    }, 60000); // Cada minuto
});

console.log('✅ Sistema de notificaciones mejorado cargado');
"""
    
    with open('static/js/instant-notifications.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("JavaScript de notificaciones mejorado creado")

if __name__ == '__main__':
    print("MEJORANDO SISTEMA DE NOTIFICACIONES EN TIEMPO REAL")
    print("=" * 60)
    
    enhance_realtime_notifications()
    create_enhanced_js()
    
    print("=" * 60)
    print("SISTEMA MEJORADO COMPLETAMENTE")
    print("Notificaciones instantaneas activadas")
    print("Procesamiento ultra rapido habilitado")
    print("Interfaz mejorada con animaciones")
    print("Sonidos diferenciados por evento")
    print("Reconexion automatica configurada")