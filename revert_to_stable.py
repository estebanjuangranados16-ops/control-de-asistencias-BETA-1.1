#!/usr/bin/env python3
"""
Script para revertir cambios y restaurar versión estable
"""

def revert_to_stable():
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Revertir 1: Eliminar notificaciones forzadas
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
    
    new_notification = ""
    
    content = content.replace(old_notification, new_notification)
    
    # Revertir 2: Restaurar endpoint simple del dashboard
    old_endpoint = """@app.route('/api/dashboard')
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
    
    new_endpoint = """@app.route('/api/dashboard')
def api_dashboard():
    return jsonify(system.get_dashboard_data())"""
    
    content = content.replace(old_endpoint, new_endpoint)
    
    # Revertir 3: Eliminar endpoint force_update
    force_update_endpoint = """@app.route('/api/force_update', methods=['POST'])
def api_force_update():
    try:
        dashboard_data = system.get_dashboard_data()
        socketio.emit('dashboard_refresh', dashboard_data, broadcast=True)
        return jsonify({'success': True, 'message': 'Dashboard actualizado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

"""
    
    content = content.replace(force_update_endpoint, "")
    
    # Revertir 4: Restaurar emisión WebSocket original
    old_emit = """            # Emitir evento WebSocket inmediatamente
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
            
            # Emitir actualización del dashboard inmediatamente
            socketio.emit('dashboard_update', self.get_dashboard_data())"""
    
    new_emit = """            # Emitir evento WebSocket
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
            })"""
    
    content = content.replace(old_emit, new_emit)
    
    # Revertir 5: Simplificar consulta del dashboard
    old_query = """                # Estado de empleados optimizado - solo último evento no-break
                cursor.execute('''
                    WITH last_non_break_events AS (
                        SELECT DISTINCT ON (employee_id) 
                               employee_id, event_type, timestamp
                        FROM attendance_records
                        WHERE DATE(timestamp) = CURRENT_DATE 
                              AND event_type IN ('entrada', 'salida')
                              AND (is_break_record = false OR is_break_record IS NULL)
                        ORDER BY employee_id, timestamp DESC
                    )
                    SELECT e.name, e.employee_id, lnbe.event_type, lnbe.timestamp
                    FROM employees e
                    LEFT JOIN last_non_break_events lnbe ON e.employee_id = lnbe.employee_id
                    WHERE e.active = true
                    ORDER BY e.name
                ''')"""
    
    new_query = """                # Estado de empleados
                cursor.execute('''
                    SELECT e.name, e.employee_id, ar.event_type, ar.timestamp
                    FROM employees e
                    LEFT JOIN (
                        SELECT DISTINCT ON (employee_id) employee_id, event_type, timestamp
                        FROM attendance_records
                        WHERE DATE(timestamp) = CURRENT_DATE
                        ORDER BY employee_id, timestamp DESC
                    ) ar ON e.employee_id = ar.employee_id
                    WHERE e.active = true
                ''')"""
    
    content = content.replace(old_query, new_query)
    
    # Revertir 6: Restaurar procesamiento de estado original
    old_process = """            for emp in employees_status:
                name, emp_id, last_event, timestamp = emp
                if last_event == 'entrada':
                    inside.append({'name': name, 'id': emp_id, 'time': timestamp})
                elif last_event == 'salida':
                    outside.append({'name': name, 'id': emp_id, 'time': timestamp})
                else:
                    # Sin registros hoy = fuera
                    outside.append({'name': name, 'id': emp_id, 'time': None})"""
    
    new_process = """            for emp in employees_status:
                name, emp_id, last_event, timestamp = emp
                if last_event == 'entrada':
                    inside.append({'name': name, 'id': emp_id, 'time': timestamp})
                else:
                    outside.append({'name': name, 'id': emp_id, 'time': timestamp})"""
    
    content = content.replace(old_process, new_process)
    
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Sistema revertido a versión estable")
    print("🔄 Reinicia el sistema: python system_optimized_v2.py")

if __name__ == '__main__':
    revert_to_stable()