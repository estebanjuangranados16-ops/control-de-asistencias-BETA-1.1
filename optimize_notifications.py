#!/usr/bin/env python3
"""
Script para optimizar notificaciones en tiempo real
"""
import os
import sys

def optimize_system():
    # Leer el archivo actual
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Optimización 1: Mejorar emisión WebSocket
    old_emit = """            # Emitir evento WebSocket
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
    
    new_emit = """            # Emitir evento WebSocket inmediatamente
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
    
    content = content.replace(old_emit, new_emit)
    
    # Optimización 2: Mejorar consulta de estado
    old_query = """                # Estado de empleados
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
    
    new_query = """                # Estado de empleados optimizado - solo último evento no-break
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
    
    # Solo reemplazar la primera ocurrencia
    content = content.replace(old_query, new_query, 1)
    
    # Optimización 3: Mejorar procesamiento de estado
    old_process = """            for emp in employees_status:
                name, emp_id, last_event, timestamp = emp
                if last_event == 'entrada':
                    inside.append({'name': name, 'id': emp_id, 'time': timestamp})
                else:
                    outside.append({'name': name, 'id': emp_id, 'time': timestamp})"""
    
    new_process = """            for emp in employees_status:
                name, emp_id, last_event, timestamp = emp
                if last_event == 'entrada':
                    inside.append({'name': name, 'id': emp_id, 'time': timestamp})
                elif last_event == 'salida':
                    outside.append({'name': name, 'id': emp_id, 'time': timestamp})
                else:
                    # Sin registros hoy = fuera
                    outside.append({'name': name, 'id': emp_id, 'time': None})"""
    
    content = content.replace(old_process, new_process, 1)
    
    # Escribir archivo optimizado
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Sistema optimizado para notificaciones en tiempo real")
    print("🔄 Reinicia el sistema: python system_optimized_v2.py")

if __name__ == '__main__':
    optimize_system()