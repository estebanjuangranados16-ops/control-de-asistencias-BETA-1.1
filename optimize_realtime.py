#!/usr/bin/env python3
"""
Optimización para notificaciones instantáneas
"""

def optimize_realtime_system():
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Optimizar el método record_attendance para ser más rápido
    old_record = """            # Emitir evento WebSocket
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
    
    new_record = """            # NOTIFICACIÓN INSTANTÁNEA
            try:
                # Emitir inmediatamente sin esperar
                socketio.emit('instant_notification', {
                    'name': employee[0],
                    'event_type': event_type,
                    'timestamp': local_timestamp,
                    'department': employee[1] or 'General',
                    'is_break': is_break,
                    'is_lunch': is_lunch
                }, broadcast=True)
                
                # Emitir actualización rápida del dashboard
                socketio.emit('quick_update', {
                    'employee_name': employee[0],
                    'action': event_type,
                    'time': local_timestamp
                }, broadcast=True)
                
                print(f"🔔 NOTIFICACIÓN ENVIADA: {employee[0]} - {event_type.upper()}")
            except Exception as e:
                print(f"❌ Error notificación: {e}")"""
    
    content = content.replace(old_record, new_record)
    
    # 2. Agregar método de actualización rápida
    dashboard_method = """    def get_dashboard_data(self):"""
    
    quick_method = """    def get_quick_dashboard_data(self):
        \"\"\"Obtener datos básicos del dashboard de forma ultra rápida\"\"\"
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.db_type == 'postgresql':
                # Solo contar registros básicos
                cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
                total_records = cursor.fetchone()[0]
                
                # Empleados activos hoy
                cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
                unique_employees = cursor.fetchone()[0]
            else:
                cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE date(timestamp) = date('now')")
                total_records = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE date(timestamp) = date('now')")
                unique_employees = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_records': total_records,
                'unique_employees': unique_employees,
                'connected': self.connected,
                'monitoring': self.monitoring,
                'last_update': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'total_records': 0,
                'unique_employees': 0,
                'connected': self.connected,
                'monitoring': self.monitoring,
                'error': str(e)
            }
    
    def get_dashboard_data(self):"""
    
    content = content.replace(dashboard_method, quick_method)
    
    # 3. Agregar endpoints optimizados
    api_endpoints = """@app.route('/api/quick_dashboard')
def api_quick_dashboard():
    \"\"\"Dashboard ultra rápido\"\"\"
    return jsonify(system.get_quick_dashboard_data())

@app.route('/api/instant_status')
def api_instant_status():
    \"\"\"Estado instantáneo del sistema\"\"\"
    return jsonify({
        'connected': system.connected,
        'monitoring': system.monitoring,
        'timestamp': datetime.now().isoformat(),
        'status': 'active' if system.monitoring else 'inactive'
    })

@app.route('/api/dashboard')"""
    
    content = content.replace("@app.route('/api/dashboard')", api_endpoints)
    
    # 4. Optimizar el procesamiento de eventos
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
        \"\"\"Procesar eventos del dispositivo de forma optimizada\"\"\"
        try:
            if 'AccessControllerEvent' in event:
                acs_event = event['AccessControllerEvent']
                sub_type = acs_event.get('subEventType')
                
                if sub_type == 38:  # Acceso autorizado
                    employee_id = acs_event.get('employeeNoString')
                    
                    if employee_id:
                        # Procesar en hilo separado para no bloquear
                        import threading
                        thread = threading.Thread(
                            target=self.record_attendance,
                            args=(employee_id, datetime.now().isoformat(), 1, 'huella'),
                            daemon=True
                        )
                        thread.start()
                        
                        print(f"⚡ EVENTO PROCESADO: {employee_id}")
        except Exception as e:
            print(f"❌ Error procesando evento: {e}")"""
    
    content = content.replace(old_process, new_process)
    
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Sistema optimizado para notificaciones instantáneas")

if __name__ == '__main__':
    optimize_realtime_system()