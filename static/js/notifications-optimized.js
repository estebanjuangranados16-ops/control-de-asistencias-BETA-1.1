// Sistema de Notificaciones Optimizado
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
