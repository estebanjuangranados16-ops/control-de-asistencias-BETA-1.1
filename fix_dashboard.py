#!/usr/bin/env python3
"""
Fix para error de datos undefined
"""

def fix_dashboard_error():
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Asegurar que get_dashboard_data siempre retorne datos válidos
    old_return = """            return {
                'total_records': 0,
                'unique_employees': 0,
                'employees_inside': [],
                'employees_outside': [],
                'recent_records': [],
                'connected': self.connected,
                'monitoring': self.monitoring
            }"""
    
    new_return = """            return {
                'total_records': 0,
                'unique_employees': 0,
                'employees_inside': [],
                'employees_outside': [],
                'recent_records': [],
                'connected': self.connected,
                'monitoring': self.monitoring,
                'status': 'error',
                'message': str(e)
            }"""
    
    content = content.replace(old_return, new_return)
    
    # Fix 2: Simplificar el endpoint del dashboard
    old_endpoint = """@app.route('/api/dashboard')
def api_dashboard():
    try:
        data = system.get_dashboard_data()
        # Emitir también por WebSocket
        socketio.emit('dashboard_data', data, broadcast=True)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})"""
    
    new_endpoint = """@app.route('/api/dashboard')
def api_dashboard():
    try:
        data = system.get_dashboard_data()
        # Validar datos antes de enviar
        if not isinstance(data, dict):
            data = {
                'total_records': 0,
                'unique_employees': 0,
                'employees_inside': [],
                'employees_outside': [],
                'recent_records': [],
                'connected': system.connected,
                'monitoring': system.monitoring
            }
        
        # Asegurar que las listas existan
        data['employees_inside'] = data.get('employees_inside', [])
        data['employees_outside'] = data.get('employees_outside', [])
        data['recent_records'] = data.get('recent_records', [])
        
        return jsonify(data)
    except Exception as e:
        print(f"Error en api_dashboard: {e}")
        return jsonify({
            'total_records': 0,
            'unique_employees': 0,
            'employees_inside': [],
            'employees_outside': [],
            'recent_records': [],
            'connected': False,
            'monitoring': False,
            'error': str(e)
        })"""
    
    content = content.replace(old_endpoint, new_endpoint)
    
    # Fix 3: Simplificar las notificaciones
    old_notification = """            # FORZAR NOTIFICACIONES INMEDIATAS
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
    
    new_notification = """            # NOTIFICACIÓN SIMPLE
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
    
    content = content.replace(old_notification, new_notification)
    
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fix aplicado para errores de dashboard")

if __name__ == '__main__':
    fix_dashboard_error()