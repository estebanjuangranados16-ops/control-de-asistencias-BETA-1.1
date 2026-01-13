// JavaScript optimizado para notificaciones instantáneas
console.log('🚀 Iniciando sistema de notificaciones instantáneas...');

// Configurar WebSocket con reconexión automática
const socket = io({
    transports: ['websocket', 'polling'],
    upgrade: true,
    rememberUpgrade: true,
    timeout: 5000,
    forceNew: true
});

// Variables globales
let lastNotificationTime = 0;
let notificationQueue = [];

// Conectar WebSocket
socket.on('connect', function() {
    console.log('✅ Conectado al servidor PCSHEK');
    showSystemNotification('✅ Sistema conectado', 'success');
});

socket.on('disconnect', function() {
    console.log('❌ Desconectado del servidor');
    showSystemNotification('❌ Conexión perdida', 'error');
});

// Escuchar notificaciones instantáneas
socket.on('instant_notification', function(data) {
    console.log('🔔 Notificación instantánea:', data);
    
    // Evitar duplicados
    const now = Date.now();
    if (now - lastNotificationTime < 1000) {
        return; // Ignorar si es muy reciente
    }
    lastNotificationTime = now;
    
    // Mostrar notificación inmediatamente
    showInstantNotification(data);
    
    // Actualizar dashboard después de 500ms
    setTimeout(() => {
        updateDashboardQuick();
    }, 500);
});

// Escuchar actualizaciones rápidas
socket.on('quick_update', function(data) {
    console.log('⚡ Actualización rápida:', data);
    updateQuickStats();
});

// Función para mostrar notificaciones instantáneas
function showInstantNotification(data) {
    // Crear notificación visual
    const notification = document.createElement('div');
    notification.className = 'instant-notification';
    
    // Determinar color según tipo de evento
    let bgColor = '#28a745'; // Verde por defecto
    let icon = '🏢';
    
    if (data.event_type === 'entrada') {
        bgColor = '#28a745';
        icon = '🟢';
    } else if (data.event_type === 'salida') {
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
        top: 20px;
        right: 20px;
        background: ${bgColor};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: bold;
        font-size: 16px;
        min-width: 300px;
        animation: slideInBounce 0.5s ease-out;
        cursor: pointer;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 24px;">${icon}</span>
            <div>
                <div style="font-size: 18px;">${data.name}</div>
                <div style="font-size: 14px; opacity: 0.9;">
                    ${data.event_type.toUpperCase()} - ${data.department}
                </div>
                <div style="font-size: 12px; opacity: 0.8;">
                    ${new Date(data.timestamp).toLocaleTimeString()}
                </div>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: none; border: none; color: white; font-size: 20px; cursor: pointer; margin-left: auto;">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Reproducir sonido (opcional)
    playNotificationSound();
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutBounce 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Función para mostrar notificaciones del sistema
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
        top: 80px;
        right: 20px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        z-index: 9999;
        font-size: 14px;
        animation: fadeInOut 3s ease-in-out;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 3000);
}

// Función para actualizar dashboard rápidamente
function updateDashboardQuick() {
    fetch('/api/quick_dashboard')
        .then(response => response.json())
        .then(data => {
            // Actualizar solo estadísticas básicas
            const totalRecords = document.getElementById('total-records');
            const uniqueEmployees = document.getElementById('unique-employees');
            
            if (totalRecords) totalRecords.textContent = data.total_records || 0;
            if (uniqueEmployees) uniqueEmployees.textContent = data.unique_employees || 0;
            
            console.log('📊 Dashboard actualizado rápidamente');
        })
        .catch(error => console.error('Error actualizando dashboard:', error));
}

// Función para actualizar estadísticas rápidas
function updateQuickStats() {
    // Incrementar contador visual inmediatamente
    const totalRecords = document.getElementById('total-records');
    if (totalRecords) {
        const current = parseInt(totalRecords.textContent) || 0;
        totalRecords.textContent = current + 1;
        totalRecords.style.animation = 'pulse 0.5s ease-in-out';
    }
}

// Función para reproducir sonido de notificación
function playNotificationSound() {
    try {
        // Crear sonido simple usando Web Audio API
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
        console.log('No se pudo reproducir sonido:', error);
    }
}

// Agregar estilos CSS para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInBounce {
        0% { transform: translateX(100%) scale(0.8); opacity: 0; }
        50% { transform: translateX(-10px) scale(1.05); opacity: 1; }
        100% { transform: translateX(0) scale(1); opacity: 1; }
    }
    
    @keyframes slideOutBounce {
        0% { transform: translateX(0) scale(1); opacity: 1; }
        100% { transform: translateX(100%) scale(0.8); opacity: 0; }
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
    
    .instant-notification:hover {
        transform: scale(1.02);
        transition: transform 0.2s ease;
    }
`;
document.head.appendChild(style);

// Inicializar sistema
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Sistema de notificaciones instantáneas listo');
    
    // Verificar estado cada 30 segundos
    setInterval(() => {
        fetch('/api/instant_status')
            .then(response => response.json())
            .then(data => {
                if (!data.monitoring) {
                    showSystemNotification('⚠️ Monitoreo inactivo', 'warning');
                }
            })
            .catch(error => console.error('Error verificando estado:', error));
    }, 30000);
});