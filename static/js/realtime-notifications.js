// Script para mejorar notificaciones en tiempo real
console.log('Iniciando notificaciones en tiempo real...');

// Conectar WebSocket con reconexión automática
const socket = io({
    transports: ['websocket', 'polling'],
    upgrade: true,
    rememberUpgrade: true
});

// Escuchar nuevos registros
socket.on('new_record', function(data) {
    console.log('Nuevo registro:', data);
    
    // Mostrar notificación visual
    showNotification(`${data.name} - ${data.event_type.toUpperCase()}`, 'success');
    
    // Actualizar dashboard inmediatamente
    setTimeout(() => {
        location.reload();
    }, 1000);
});

// Escuchar actualizaciones del dashboard
socket.on('dashboard_refresh', function(data) {
    console.log('Dashboard actualizado');
    updateDashboardUI(data);
});

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-popup`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        padding: 15px;
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        color: #155724;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    notification.innerHTML = `
        <strong>🔔 Nuevo Registro:</strong> ${message}
        <button type="button" style="float: right; background: none; border: none; font-size: 18px; cursor: pointer;" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Forzar actualización cada 5 segundos
setInterval(() => {
    fetch('/api/force_update', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ Dashboard actualizado automáticamente');
            }
        })
        .catch(error => console.error('Error en actualización:', error));
}, 5000);