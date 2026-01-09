#!/usr/bin/env python3
"""
Parche para notificaciones en tiempo real
"""

def patch_notifications():
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Agregar emisión inmediata después del registro
    old_emit = """            print(f"REGISTRO: {employee[0]} - {event_type.upper()} - {local_timestamp}")"""
    
    new_emit = """            print(f"REGISTRO: {employee[0]} - {event_type.upper()} - {local_timestamp}")
            
            # FORZAR NOTIFICACIONES INMEDIATAS
            try:
                # Emitir evento individual
                socketio.emit('new_record', {
                    'name': employee[0],
                    'event_type': event_type,
                    'timestamp': local_timestamp,
                    'department': employee[1]
                }, broadcast=True)
                
                # Emitir actualización completa del dashboard
                dashboard_data = self.get_dashboard_data()
                socketio.emit('dashboard_refresh', dashboard_data, broadcast=True)
                
                print(f"✅ Notificación enviada: {employee[0]} - {event_type}")
            except Exception as e:
                print(f"❌ Error enviando notificación: {e}")"""
    
    content = content.replace(old_emit, new_emit)
    
    # 2. Agregar endpoint para forzar actualización
    api_routes = """@app.route('/api/force_update', methods=['POST'])
def api_force_update():
    try:
        dashboard_data = system.get_dashboard_data()
        socketio.emit('dashboard_refresh', dashboard_data, broadcast=True)
        return jsonify({'success': True, 'message': 'Dashboard actualizado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/dashboard')"""
    
    content = content.replace("@app.route('/api/dashboard')", api_routes)
    
    # 3. Mejorar el endpoint del dashboard
    old_dashboard = """@app.route('/api/dashboard')
def api_dashboard():
    return jsonify(system.get_dashboard_data())"""
    
    new_dashboard = """@app.route('/api/dashboard')
def api_dashboard():
    try:
        data = system.get_dashboard_data()
        # Emitir también por WebSocket
        socketio.emit('dashboard_data', data, broadcast=True)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})"""
    
    content = content.replace(old_dashboard, new_dashboard)
    
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Parche de notificaciones aplicado")
    print("🔄 Reinicia el sistema")

if __name__ == '__main__':
    patch_notifications()