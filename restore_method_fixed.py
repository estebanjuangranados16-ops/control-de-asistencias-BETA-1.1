#!/usr/bin/env python3
"""
Script para restaurar método get_dashboard_data
"""

def restore_method():
    with open('system_optimized_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar donde insertar el método
    insert_point = "    def get_break_status(self):"
    
    method_code = """    def get_dashboard_data(self):
        \"\"\"Obtener datos del dashboard optimizado\"\"\"
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Registros de hoy
            if self.db_type == 'postgresql':
                cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
                total_records = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
                unique_employees = cursor.fetchone()[0]
                
                # Estado de empleados optimizado - solo último evento no-break
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
                ''')
                employees_status = cursor.fetchall()
                
                # Registros recientes
                cursor.execute('''
                    SELECT e.name, ar.event_type, ar.timestamp, ar.verify_method
                    FROM attendance_records ar
                    JOIN employees e ON ar.employee_id = e.employee_id
                    WHERE e.active = true
                    ORDER BY ar.timestamp DESC LIMIT 10
                ''')
                recent_records = cursor.fetchall()
                
            else:
                cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE date(timestamp) = date('now')")
                total_records = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE date(timestamp) = date('now')")
                unique_employees = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT e.name, e.employee_id, ar.event_type, ar.timestamp
                    FROM employees e
                    LEFT JOIN (
                        SELECT employee_id, event_type, timestamp,
                               ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY timestamp DESC) as rn
                        FROM attendance_records
                        WHERE date(timestamp) = date('now')
                              AND event_type IN ('entrada', 'salida')
                              AND (is_break_record = 0 OR is_break_record IS NULL)
                    ) ar ON e.employee_id = ar.employee_id AND ar.rn = 1
                    WHERE e.active = 1
                    ORDER BY e.name
                ''')
                employees_status = cursor.fetchall()
                
                cursor.execute('''
                    SELECT e.name, ar.event_type, ar.timestamp, ar.verify_method
                    FROM attendance_records ar
                    JOIN employees e ON ar.employee_id = e.employee_id
                    WHERE e.active = 1
                    ORDER BY ar.timestamp DESC LIMIT 10
                ''')
                recent_records = cursor.fetchall()
            
            conn.close()
            
            # Procesar estado de empleados
            inside = []
            outside = []
            
            for emp in employees_status:
                name, emp_id, last_event, timestamp = emp
                if last_event == 'entrada':
                    inside.append({'name': name, 'id': emp_id, 'time': timestamp})
                elif last_event == 'salida':
                    outside.append({'name': name, 'id': emp_id, 'time': timestamp})
                else:
                    # Sin registros hoy = fuera
                    outside.append({'name': name, 'id': emp_id, 'time': None})
            
            return {
                'total_records': total_records,
                'unique_employees': unique_employees,
                'employees_inside': inside,
                'employees_outside': outside,
                'recent_records': recent_records,
                'connected': self.connected,
                'monitoring': self.monitoring
            }
            
        except Exception as e:
            print(f"Error obteniendo datos dashboard: {e}")
            conn.close()
            return {
                'total_records': 0,
                'unique_employees': 0,
                'employees_inside': [],
                'employees_outside': [],
                'recent_records': [],
                'connected': self.connected,
                'monitoring': self.monitoring
            }
    
"""
    
    # Insertar el método antes de get_break_status
    content = content.replace(insert_point, method_code + insert_point)
    
    with open('system_optimized_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Método get_dashboard_data restaurado")

if __name__ == '__main__':
    restore_method()