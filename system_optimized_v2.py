"""
Sistema de Asistencia Optimizado con PostgreSQL
Versión actualizada que usa la configuración de .env
"""
from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
from requests.auth import HTTPDigestAuth
import json
import threading
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    print("⚠️ openpyxl no disponible - exportación Excel deshabilitada")

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ reportlab no disponible - exportación PDF deshabilitada")

import io

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'hikvision_attendance_2024')
CORS(app, origins=["http://localhost:3001", "http://localhost:3000"])
socketio = SocketIO(app, cors_allowed_origins="*")

class OptimizedAttendanceSystem:
    def __init__(self):
        # Configuración desde variables de entorno
        self.device_ip = os.getenv('DEVICE_IP', '172.10.1.62')
        self.username = os.getenv('DEVICE_USER', 'admin')
        self.password = os.getenv('DEVICE_PASS', 'PC2024*+')
        self.database_url = os.getenv('DATABASE_URL')
        
        # Configurar conexión HTTP
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(self.username, self.password)
        self.session.timeout = 10
        self.base_url = f"http://{self.device_ip}/ISAPI"
        
        # Estado del sistema
        self.monitoring = False
        self.connected = False
        self.last_event_time = time.time()
        
        # Cache para optimización
        self.employees_cache = {}
        self.cache_timestamp = 0
        self.cache_duration = 300  # 5 minutos
        
        # Configurar base de datos
        self.setup_database()
        
    def setup_database(self):
        """Configurar conexión a base de datos"""
        if self.database_url and self.database_url.startswith('postgresql'):
            # Usar PostgreSQL
            import psycopg2
            self.db_type = 'postgresql'
            self.get_connection = lambda: psycopg2.connect(self.database_url)
            print("✅ Configurado para PostgreSQL")
        else:
            # Fallback a SQLite
            import sqlite3
            self.db_type = 'sqlite'
            self.db_path = 'attendance.db'
            self.get_connection = lambda: sqlite3.connect(self.db_path)
            print("⚠️ Usando SQLite como fallback")
        
        self.init_database()
        
    def init_database(self):
        """Inicializar base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db_type == 'postgresql':
                # Crear tablas PostgreSQL
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS employees (
                        id SERIAL PRIMARY KEY,
                        employee_id TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        department TEXT DEFAULT 'General',
                        schedule TEXT DEFAULT 'estandar',
                        phone TEXT DEFAULT '',
                        email TEXT DEFAULT '',
                        active BOOLEAN DEFAULT true,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        synced_to_device BOOLEAN DEFAULT false
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS attendance_records (
                        id SERIAL PRIMARY KEY,
                        employee_id TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        reader_no INTEGER DEFAULT 1,
                        verify_method TEXT DEFAULT 'huella',
                        status TEXT DEFAULT 'autorizado'
                    )
                ''')
                
                # Insertar admin
                cursor.execute('''
                    INSERT INTO employees (employee_id, name, department) 
                    VALUES (%s, %s, %s)
                    ON CONFLICT (employee_id) DO NOTHING
                ''', ('1', 'Administrador', 'Administración'))
                
                # Crear índices para optimización
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_employee_id ON attendance_records(employee_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance_records(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance_records(DATE(timestamp))')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_active ON employees(active)')
                
            else:
                # Crear tablas SQLite
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY,
                        employee_id TEXT UNIQUE,
                        name TEXT,
                        department TEXT DEFAULT 'General',
                        schedule TEXT DEFAULT 'estandar',
                        phone TEXT DEFAULT '',
                        email TEXT DEFAULT '',
                        active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        synced_to_device BOOLEAN DEFAULT 0
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS attendance_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT,
                        event_type TEXT,
                        timestamp TIMESTAMP,
                        reader_no INTEGER DEFAULT 1,
                        verify_method TEXT DEFAULT 'huella',
                        status TEXT DEFAULT 'autorizado'
                    )
                ''')
                
                cursor.execute('''
                    INSERT OR IGNORE INTO employees (employee_id, name, department) 
                    VALUES (?, ?, ?)
                ''', ('1', 'Administrador', 'Administración'))
                
                # Crear índices para optimización SQLite
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_employee_id ON attendance_records(employee_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance_records(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance_records(date(timestamp))')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_active ON employees(active)')
            
            conn.commit()
            print("✅ Base de datos inicializada")
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
        finally:
            conn.close()
    
    def test_connection(self):
        """Probar conexión al dispositivo"""
        try:
            endpoints = [
                f"{self.base_url}/System/deviceInfo",
                f"http://{self.device_ip}/ISAPI/System/status",
                f"http://{self.device_ip}"
            ]
            
            for endpoint in endpoints:
                try:
                    response = self.session.get(endpoint, timeout=2)
                    if response.status_code in [200, 401]:
                        self.connected = True
                        return True
                except:
                    continue
                    
            self.connected = False
            return False
        except:
            self.connected = False
            return False
    
    def record_attendance(self, employee_id, timestamp, reader_no=1, verify_method="huella"):
        """Registrar asistencia"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener información del empleado
            if self.db_type == 'postgresql':
                cursor.execute('SELECT name, department, schedule FROM employees WHERE employee_id = %s', (employee_id,))
            else:
                cursor.execute('SELECT name, department, schedule FROM employees WHERE employee_id = ?', (employee_id,))
            
            employee = cursor.fetchone()
            
            if not employee:
                print(f"Empleado {employee_id} no encontrado")
                conn.close()
                return False
            
            # Usar hora local con zona horaria
            from datetime import timezone, timedelta
            # Zona horaria de Colombia (UTC-5)
            colombia_tz = timezone(timedelta(hours=-5))
            local_timestamp = datetime.now(colombia_tz).strftime('%Y-%m-%d %H:%M:%S')
            
            # Verificar duplicados
            if self.db_type == 'postgresql':
                cursor.execute('''
                    SELECT timestamp FROM attendance_records 
                    WHERE employee_id = %s AND timestamp > NOW() - INTERVAL '10 seconds'
                    ORDER BY timestamp DESC LIMIT 1
                ''', (employee_id,))
            else:
                cursor.execute('''
                    SELECT timestamp FROM attendance_records 
                    WHERE employee_id = ? AND datetime(timestamp) > datetime('now', '-10 seconds')
                    ORDER BY timestamp DESC LIMIT 1
                ''', (employee_id,))
            
            recent_record = cursor.fetchone()
            if recent_record:
                print(f"DUPLICADO EVITADO: {employee[0]} - Registro muy reciente")
                conn.close()
                return False
            
            # Determinar tipo de evento
            event_type = self.determine_event_type(employee_id)
            
            # Insertar registro
            if self.db_type == 'postgresql':
                cursor.execute('''
                    INSERT INTO attendance_records 
                    (employee_id, event_type, timestamp, reader_no, verify_method, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (employee_id, event_type, local_timestamp, reader_no, verify_method, "autorizado"))
            else:
                cursor.execute('''
                    INSERT INTO attendance_records 
                    (employee_id, event_type, timestamp, reader_no, verify_method, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (employee_id, event_type, local_timestamp, reader_no, verify_method, "autorizado"))
            
            conn.commit()
            conn.close()
            
            print(f"✅ REGISTRO: {employee[0]} - {event_type.upper()} - {local_timestamp}")
            
            # Emitir evento WebSocket
            socketio.emit('attendance_record', {
                'employee_id': employee_id,
                'name': employee[0],
                'event_type': event_type,
                'timestamp': local_timestamp,
                'verify_method': verify_method,
                'department': employee[1] or 'General',
                'schedule': employee[2] or 'estandar',
                'real_time': True
            })
            
            # Verificar tardanza para notificación
            if event_type == 'entrada':
                self.check_late_arrival(employee_id, employee[0], employee[1], employee[2], local_timestamp)
            
            return True
            
        except Exception as e:
            print(f"❌ Error al registrar: {e}")
            return False
    
    def determine_event_type(self, employee_id):
        """Determinar entrada o salida"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Obtener último registro del día
        if self.db_type == 'postgresql':
            cursor.execute('''
                SELECT event_type FROM attendance_records 
                WHERE employee_id = %s AND DATE(timestamp) = CURRENT_DATE
                ORDER BY timestamp DESC LIMIT 1
            ''', (employee_id,))
        else:
            cursor.execute('''
                SELECT event_type FROM attendance_records 
                WHERE employee_id = ? AND date(timestamp) = date('now')
                ORDER BY timestamp DESC LIMIT 1
            ''', (employee_id,))
        
        last_record = cursor.fetchone()
        conn.close()
        
        # Si no hay registros, es entrada
        if not last_record:
            return 'entrada'
        
        # Alternar entrada/salida
        return 'entrada' if last_record[0] == 'salida' else 'salida'
    
    def add_employee(self, employee_id, name, department="General", schedule="estandar", phone="", email=""):
        """Agregar empleado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db_type == 'postgresql':
                cursor.execute('''
                    INSERT INTO employees (employee_id, name, department, schedule, phone, email) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (employee_id, name, department, schedule, phone, email))
            else:
                cursor.execute('''
                    INSERT INTO employees (employee_id, name, department, schedule, phone, email) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (employee_id, name, department, schedule, phone, email))
            
            conn.commit()
            conn.close()
            
            # Limpiar cache
            self.employees_cache = {}
            self.cache_timestamp = 0
            
            socketio.emit('employee_added', {
                'employee_id': employee_id,
                'name': name,
                'department': department,
                'schedule': schedule
            })
            
            return True, f"Empleado {name} agregado exitosamente"
            
        except Exception as e:
            conn.close()
            if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                return False, f"El empleado con ID {employee_id} ya existe"
            return False, f"Error: {str(e)}"
    
    def get_employees(self):
        """Obtener lista de empleados con cache"""
        current_time = time.time()
        
        # Usar cache si está vigente
        if (current_time - self.cache_timestamp) < self.cache_duration and self.employees_cache:
            return list(self.employees_cache.values())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT employee_id, name, department, schedule, phone, email, active, synced_to_device, created_at
            FROM employees ORDER BY name
        ''')
        
        employees = cursor.fetchall()
        conn.close()
        
        # Actualizar cache
        self.employees_cache = {}
        for emp in employees:
            employee_data = {
                'employee_id': emp[0], 'name': emp[1], 'department': emp[2] or 'General', 
                'schedule': emp[3] or 'estandar', 'phone': emp[4] or '', 'email': emp[5] or '',
                'active': emp[6], 'synced': emp[7], 'created_at': emp[8]
            }
            self.employees_cache[emp[0]] = employee_data
        
        self.cache_timestamp = current_time
        return list(self.employees_cache.values())
    
    def get_schedule_hours(self, schedule, day_of_week):
        """Obtener horarios según el tipo y día de la semana"""
        schedules = {
            'reacondicionamiento': {
                'monday': ('07:00', '17:00'),
                'tuesday': ('07:00', '17:00'),
                'wednesday': ('07:00', '17:00'),
                'thursday': ('07:00', '17:00'),
                'friday': ('07:00', '16:00'),
                'saturday': None,
                'sunday': None
            },
            'estandar': {
                'monday': ('08:00', '17:00'),
                'tuesday': ('08:00', '17:00'),
                'wednesday': ('08:00', '17:00'),
                'thursday': ('08:00', '17:00'),
                'friday': ('08:00', '17:00'),
                'saturday': None,
                'sunday': None
            }
        }
        
        schedule_key = schedule.lower() if schedule else 'estandar'
        day_key = day_of_week.lower()
        
        return schedules.get(schedule_key, schedules['estandar']).get(day_key)
    
    def generate_attendance_report(self, start_date, end_date, employee_id=None, department=None):
        """Generar reporte de asistencia con análisis de puntualidad"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Construir consulta base
            base_query = '''
                SELECT e.employee_id, e.name, e.department, e.schedule,
                       ar.timestamp, ar.event_type
                FROM employees e
                LEFT JOIN attendance_records ar ON e.employee_id = ar.employee_id
                WHERE e.active = {} AND ar.timestamp BETWEEN {} AND {}
            '''.format(
                'true' if self.db_type == 'postgresql' else '1',
                '%s' if self.db_type == 'postgresql' else '?',
                '%s' if self.db_type == 'postgresql' else '?'
            )
            
            params = [start_date, end_date]
            
            if employee_id:
                base_query += ' AND e.employee_id = {}'
                base_query = base_query.format('%s' if self.db_type == 'postgresql' else '?')
                params.append(employee_id)
            
            if department:
                base_query += ' AND e.department = {}'
                base_query = base_query.format('%s' if self.db_type == 'postgresql' else '?')
                params.append(department)
            
            base_query += ' ORDER BY e.name, ar.timestamp'
            
            cursor.execute(base_query, params)
            records = cursor.fetchall()
            
            # Procesar datos por empleado y día
            report_data = {}
            current_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Obtener todos los empleados activos
            if self.db_type == 'postgresql':
                cursor.execute('SELECT employee_id, name, department, schedule FROM employees WHERE active = true ORDER BY name')
            else:
                cursor.execute('SELECT employee_id, name, department, schedule FROM employees WHERE active = 1 ORDER BY name')
            
            employees = cursor.fetchall()
            
            # Inicializar estructura de datos
            for emp in employees:
                if employee_id and emp[0] != employee_id:
                    continue
                if department and emp[2] != department:
                    continue
                    
                report_data[emp[0]] = {
                    'name': emp[1],
                    'department': emp[2],
                    'schedule': emp[3],
                    'days': {}
                }
            
            # Llenar días del rango
            while current_date <= end_date_obj:
                date_str = current_date.strftime('%Y-%m-%d')
                day_name = current_date.strftime('%A').lower()
                
                for emp_id in report_data:
                    schedule = report_data[emp_id]['schedule']
                    expected_hours = self.get_schedule_hours(schedule, day_name)
                    
                    report_data[emp_id]['days'][date_str] = {
                        'date': current_date.strftime('%d/%m/%Y'),
                        'day_name': current_date.strftime('%A'),
                        'expected_hours': expected_hours,
                        'entrada': None,
                        'salida': None,
                        'status': 'Ausente',
                        'late': False,
                        'early_exit': False,
                        'hours_worked': 0
                    }
                
                current_date += timedelta(days=1)
            
            # Procesar registros de asistencia
            for record in records:
                emp_id, name, dept, schedule, timestamp, event_type = record
                if not timestamp:
                    continue
                    
                if emp_id not in report_data:
                    continue
                    
                record_date = datetime.strptime(str(timestamp)[:10], '%Y-%m-%d')
                date_str = record_date.strftime('%Y-%m-%d')
                record_time = datetime.strptime(str(timestamp)[11:19], '%H:%M:%S').time()
                
                if date_str in report_data[emp_id]['days']:
                    day_data = report_data[emp_id]['days'][date_str]
                    
                    if event_type == 'entrada':
                        if not day_data['entrada'] or record_time < day_data['entrada']:
                            day_data['entrada'] = record_time
                    elif event_type == 'salida':
                        if not day_data['salida'] or record_time > day_data['salida']:
                            day_data['salida'] = record_time
            
            # Calcular estadísticas
            for emp_id in report_data:
                for date_str, day_data in report_data[emp_id]['days'].items():
                    expected_hours = day_data['expected_hours']
                    
                    if not expected_hours:  # Fin de semana
                        day_data['status'] = 'No laborable'
                        continue
                    
                    entrada = day_data['entrada']
                    salida = day_data['salida']
                    
                    if entrada and salida:
                        day_data['status'] = 'Presente'
                        
                        # Verificar tardanza y enviar notificación
                        expected_start = datetime.strptime(expected_hours[0], '%H:%M').time()
                        if entrada > expected_start:
                            day_data['late'] = True
                            # Calcular minutos de tardanza
                            entrada_dt = datetime.combine(datetime.today(), entrada)
                            expected_dt = datetime.combine(datetime.today(), expected_start)
                            late_minutes = int((entrada_dt - expected_dt).total_seconds() / 60)
                            day_data['late_minutes'] = late_minutes
                        
                        # Verificar salida temprana
                        expected_end = datetime.strptime(expected_hours[1], '%H:%M').time()
                        if salida < expected_end:
                            day_data['early_exit'] = True
                            # Calcular minutos de salida temprana
                            salida_dt = datetime.combine(datetime.today(), salida)
                            expected_dt = datetime.combine(datetime.today(), expected_end)
                            early_minutes = int((expected_dt - salida_dt).total_seconds() / 60)
                            day_data['early_minutes'] = early_minutes
                        
                        # Calcular horas trabajadas
                        entrada_dt = datetime.combine(datetime.today(), entrada)
                        salida_dt = datetime.combine(datetime.today(), salida)
                        hours_worked = (salida_dt - entrada_dt).total_seconds() / 3600
                        day_data['hours_worked'] = round(hours_worked, 2)
                        
                    elif entrada:
                        day_data['status'] = 'Sin salida'
                    elif salida:
                        day_data['status'] = 'Sin entrada'
            
            conn.close()
            return report_data
            
        except Exception as e:
            conn.close()
            print(f"Error generando reporte: {e}")
            return {}
    
    def export_to_excel(self, report_data, filename):
        """Exportar reporte a Excel"""
        if not EXCEL_AVAILABLE:
            raise Exception("openpyxl no está instalado")
            
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte de Asistencia"
        
        # Estilos
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        present_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        absent_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        late_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
        
        # Encabezados
        headers = ['Empleado', 'Departamento', 'Fecha', 'Día', 'Horario', 'Entrada', 'Salida', 'Horas', 'Estado', 'Observaciones']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
        
        row = 2
        for emp_id, emp_data in report_data.items():
            for date_str, day_data in sorted(emp_data['days'].items()):
                ws.cell(row=row, column=1, value=emp_data['name'])
                ws.cell(row=row, column=2, value=emp_data['department'])
                ws.cell(row=row, column=3, value=day_data['date'])
                ws.cell(row=row, column=4, value=day_data['day_name'])
                
                if day_data['expected_hours']:
                    ws.cell(row=row, column=5, value=f"{day_data['expected_hours'][0]} - {day_data['expected_hours'][1]}")
                else:
                    ws.cell(row=row, column=5, value="No laborable")
                
                ws.cell(row=row, column=6, value=str(day_data['entrada']) if day_data['entrada'] else "")
                ws.cell(row=row, column=7, value=str(day_data['salida']) if day_data['salida'] else "")
                ws.cell(row=row, column=8, value=day_data['hours_worked'])
                ws.cell(row=row, column=9, value=day_data['status'])
                
                # Observaciones
                obs = []
                if day_data['late']:
                    obs.append("Tardó")
                if day_data['early_exit']:
                    obs.append("Salió temprano")
                ws.cell(row=row, column=10, value=", ".join(obs))
                
                # Colores según estado
                if day_data['status'] == 'Presente':
                    if day_data['late']:
                        for col in range(1, 11):
                            ws.cell(row=row, column=col).fill = late_fill
                    else:
                        for col in range(1, 11):
                            ws.cell(row=row, column=col).fill = present_fill
                elif day_data['status'] == 'Ausente':
                    for col in range(1, 11):
                        ws.cell(row=row, column=col).fill = absent_fill
                
                row += 1
        
        # Ajustar ancho de columnas
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column].width = adjusted_width
        
        # Guardar archivo
        wb.save(filename)
        return filename
    
    def export_to_pdf(self, report_data, filename):
        """Exportar reporte a PDF"""
        if not PDF_AVAILABLE:
            raise Exception("reportlab no está instalado")
            
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title = Paragraph("<b>REPORTE DE ASISTENCIA - PCSHEK</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Crear tabla de datos
        data = [['Empleado', 'Depto', 'Fecha', 'Entrada', 'Salida', 'Horas', 'Estado']]
        
        for emp_id, emp_data in report_data.items():
            for date_str, day_data in sorted(emp_data['days'].items()):
                row = [
                    emp_data['name'][:15],
                    emp_data['department'][:8],
                    day_data['date'],
                    str(day_data['entrada'])[:5] if day_data['entrada'] else "-",
                    str(day_data['salida'])[:5] if day_data['salida'] else "-",
                    str(day_data['hours_worked']),
                    day_data['status'][:10]
                ]
                data.append(row)
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        story.append(table)
        doc.build(story)
        
        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())
        
        return filename
    
    def check_late_arrival(self, employee_id, name, department, schedule, timestamp):
        """Verificar si la llegada es tardía y enviar notificación"""
        try:
            # Obtener día de la semana
            arrival_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            day_name = arrival_time.strftime('%A').lower()
            
            # Obtener horario esperado
            expected_hours = self.get_schedule_hours(schedule, day_name)
            if not expected_hours:
                return
            
            # Verificar tardanza
            arrival_time_only = arrival_time.time()
            expected_start = datetime.strptime(expected_hours[0], '%H:%M').time()
            
            if arrival_time_only > expected_start:
                # Calcular minutos de tardanza
                arrival_dt = datetime.combine(datetime.today(), arrival_time_only)
                expected_dt = datetime.combine(datetime.today(), expected_start)
                late_minutes = int((arrival_dt - expected_dt).total_seconds() / 60)
                
                # Emitir notificación de tardanza
                socketio.emit('late_arrival_alert', {
                    'employee_id': employee_id,
                    'name': name,
                    'department': department,
                    'expected_time': expected_hours[0],
                    'actual_time': arrival_time_only.strftime('%H:%M'),
                    'late_minutes': late_minutes,
                    'timestamp': timestamp,
                    'severity': 'severe' if late_minutes > 30 else 'moderate' if late_minutes > 15 else 'mild'
                })
                
                print(f"⚠️ TARDANZA: {name} llegó {late_minutes} minutos tarde")
                
        except Exception as e:
            print(f"Error verificando tardanza: {e}")
    
    def get_dashboard_data(self):
        """Obtener datos del dashboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Registros de hoy
            if self.db_type == 'postgresql':
                cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
                total_records = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE DATE(timestamp) = CURRENT_DATE")
                unique_employees = cursor.fetchone()[0]
                
                # Estado de empleados
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
                ''')
                employees_status = cursor.fetchall()
                
                # Registros recientes
                cursor.execute('''
                    SELECT e.name, ar.event_type, ar.timestamp, ar.verify_method
                    FROM attendance_records ar
                    JOIN employees e ON ar.employee_id = e.employee_id
                    ORDER BY ar.timestamp DESC LIMIT 20
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
                    ) ar ON e.employee_id = ar.employee_id AND ar.rn = 1
                    WHERE e.active = 1
                ''')
                employees_status = cursor.fetchall()
                
                cursor.execute('''
                    SELECT e.name, ar.event_type, ar.timestamp, ar.verify_method
                    FROM attendance_records ar
                    JOIN employees e ON ar.employee_id = e.employee_id
                    ORDER BY ar.timestamp DESC LIMIT 20
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
                else:
                    outside.append({'name': name, 'id': emp_id, 'time': timestamp})
            
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
            print(f"❌ Error obteniendo datos dashboard: {e}")
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
    
    def start_monitoring(self):
        """Iniciar monitoreo"""
        if not self.monitoring:
            self.monitoring = True
            monitor_thread = threading.Thread(target=self._monitor_events, daemon=True)
            monitor_thread.start()
            print("✅ Monitoreo iniciado")
    
    def stop_monitoring(self):
        """Detener monitoreo"""
        self.monitoring = False
        print("⏹️ Monitoreo detenido")
    
    def _monitor_events(self):
        """Monitoreo de eventos del dispositivo"""
        url = f"http://{self.device_ip}/ISAPI/Event/notification/alertStream"
        
        while self.monitoring:
            try:
                response = self.session.get(url, stream=True, timeout=60)
                
                if response.status_code == 200:
                    self.connected = True
                    print("📡 Stream de eventos activo")
                    
                    buffer = ""
                    for chunk in response.iter_content(chunk_size=1024):
                        if not self.monitoring:
                            break
                            
                        if chunk:
                            try:
                                chunk_str = chunk.decode('utf-8', errors='ignore')
                                buffer += chunk_str
                            except:
                                continue
                            
                            # Procesar eventos JSON
                            while '{' in buffer and '}' in buffer:
                                start = buffer.find('{')
                                if start == -1:
                                    break
                                    
                                brace_count = 0
                                end = start
                                
                                for i in range(start, len(buffer)):
                                    if buffer[i] == '{':
                                        brace_count += 1
                                    elif buffer[i] == '}':
                                        brace_count -= 1
                                        if brace_count == 0:
                                            end = i
                                            break
                                
                                if brace_count == 0:
                                    json_str = buffer[start:end+1]
                                    buffer = buffer[end+1:]
                                    
                                    try:
                                        event = json.loads(json_str)
                                        self._process_event(event)
                                    except json.JSONDecodeError:
                                        pass
                                else:
                                    break
                else:
                    self.connected = False
                    print(f"❌ Error HTTP {response.status_code}")
                    time.sleep(10)
                    
            except Exception as e:
                self.connected = False
                print(f"❌ Error monitoreo: {str(e)[:50]}...")
                time.sleep(5)
    
    def _process_event(self, event):
        """Procesar eventos del dispositivo"""
        if 'AccessControllerEvent' in event:
            acs_event = event['AccessControllerEvent']
            sub_type = acs_event.get('subEventType')
            
            if sub_type == 38:  # Acceso autorizado
                employee_id = acs_event.get('employeeNoString')
                timestamp = event.get('dateTime', datetime.now().isoformat())
                reader_no = acs_event.get('cardReaderNo', 1)
                verify_method = 'huella'  # Simplificado
                
                if employee_id:
                    self.record_attendance(employee_id, timestamp, reader_no, verify_method)

# Instancia global
system = OptimizedAttendanceSystem()

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('👤 Cliente conectado')
    emit('status', {'connected': system.connected, 'monitoring': system.monitoring})

@socketio.on('disconnect')
def handle_disconnect():
    print('👤 Cliente desconectado')

# Rutas web
@app.route('/')
def dashboard():
    return render_template('dashboard_pcshek.html')

@app.route('/employees')
def employees_page():
    return render_template('employees_pcshek.html')

@app.route('/employees/simple')
def employees_simple():
    return render_template('employees_simple.html')

@app.route('/api/dashboard')
def api_dashboard():
    return jsonify(system.get_dashboard_data())

@app.route('/api/employees')
def api_employees():
    return jsonify(system.get_employees())

@app.route('/api/employees', methods=['POST'])
def api_add_employee():
    data = request.json
    
    # Validación de datos
    if not data.get('employee_id') or not data.get('name'):
        return jsonify({'success': False, 'message': 'ID y nombre son obligatorios'})
    
    # Validar formato de email si se proporciona
    email = data.get('email', '').strip()
    if email and '@' not in email:
        return jsonify({'success': False, 'message': 'Formato de email inválido'})
    
    success, message = system.add_employee(
        data['employee_id'].strip(),
        data['name'].strip(),
        data.get('department', 'General'),
        data.get('schedule', 'estandar'),
        data.get('phone', '').strip(),
        email
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/start_monitoring', methods=['POST'])
def api_start_monitoring():
    system.start_monitoring()
    return jsonify({'success': True, 'message': 'Monitoreo iniciado'})

@app.route('/api/stop_monitoring', methods=['POST'])
def api_stop_monitoring():
    system.stop_monitoring()
    return jsonify({'success': True, 'message': 'Monitoreo detenido'})

@app.route('/api/employees/<employee_id>/toggle', methods=['POST'])
def api_toggle_employee(employee_id):
    conn = system.get_connection()
    cursor = conn.cursor()
    
    try:
        if system.db_type == 'postgresql':
            cursor.execute('SELECT name, active FROM employees WHERE employee_id = %s', (employee_id,))
        else:
            cursor.execute('SELECT name, active FROM employees WHERE employee_id = ?', (employee_id,))
        
        employee = cursor.fetchone()
        
        if not employee:
            conn.close()
            return jsonify({'success': False, 'message': 'Empleado no encontrado'})
        
        new_status = not employee[1]
        
        if system.db_type == 'postgresql':
            cursor.execute('UPDATE employees SET active = %s WHERE employee_id = %s', (new_status, employee_id))
        else:
            cursor.execute('UPDATE employees SET active = ? WHERE employee_id = ?', (new_status, employee_id))
        
        conn.commit()
        conn.close()
        
        status_text = "activado" if new_status else "desactivado"
        return jsonify({'success': True, 'message': f"Empleado {employee[0]} {status_text}"})
        
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': f"Error: {str(e)}"})

@app.route('/api/employees/<employee_id>', methods=['PUT'])
def api_update_employee(employee_id):
    data = request.json
    conn = system.get_connection()
    cursor = conn.cursor()
    
    try:
        if system.db_type == 'postgresql':
            cursor.execute('''
                UPDATE employees 
                SET name=%s, department=%s, phone=%s, email=%s, active=%s
                WHERE employee_id=%s
            ''', (data.get('name'), data.get('department'), data.get('phone', ''), 
                  data.get('email', ''), data.get('active', True), employee_id))
        else:
            cursor.execute('''
                UPDATE employees 
                SET name=?, department=?, phone=?, email=?, active=?
                WHERE employee_id=?
            ''', (data.get('name'), data.get('department'), data.get('phone', ''), 
                  data.get('email', ''), data.get('active', True), employee_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': f"Empleado {data.get('name')} actualizado exitosamente"})
        else:
            conn.close()
            return jsonify({'success': False, 'message': 'Empleado no encontrado'})
            
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': f"Error: {str(e)}"})

@app.route('/api/employees/<employee_id>', methods=['DELETE'])
def api_delete_employee(employee_id):
    conn = system.get_connection()
    cursor = conn.cursor()
    
    try:
        # Obtener nombre antes de eliminar
        if system.db_type == 'postgresql':
            cursor.execute('SELECT name FROM employees WHERE employee_id = %s', (employee_id,))
        else:
            cursor.execute('SELECT name FROM employees WHERE employee_id = ?', (employee_id,))
        
        employee = cursor.fetchone()
        
        if not employee:
            conn.close()
            return jsonify({'success': False, 'message': 'Empleado no encontrado'})
        
        # Eliminar empleado
        if system.db_type == 'postgresql':
            cursor.execute('DELETE FROM employees WHERE employee_id = %s', (employee_id,))
        else:
            cursor.execute('DELETE FROM employees WHERE employee_id = ?', (employee_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f"Empleado {employee[0]} eliminado exitosamente"})
        
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': f"Error: {str(e)}"})

@app.route('/api/test_connection', methods=['POST'])
def api_test_connection():
    connected = system.test_connection()
    message = "✅ Dispositivo conectado" if connected else "❌ Dispositivo no disponible"
    return jsonify({'connected': connected, 'message': message})

@app.route('/api/records')
def api_records():
    date = request.args.get('date')
    if not date:
        return jsonify([])
    
    conn = system.get_connection()
    cursor = conn.cursor()
    
    try:
        if system.db_type == 'postgresql':
            cursor.execute('''
                SELECT e.name, ar.event_type, ar.timestamp, ar.verify_method, e.department
                FROM attendance_records ar
                JOIN employees e ON ar.employee_id = e.employee_id
                WHERE DATE(ar.timestamp) = %s
                ORDER BY ar.timestamp DESC
            ''', (date,))
        else:
            cursor.execute('''
                SELECT e.name, ar.event_type, ar.timestamp, ar.verify_method, e.department
                FROM attendance_records ar
                JOIN employees e ON ar.employee_id = e.employee_id
                WHERE date(ar.timestamp) = ?
                ORDER BY ar.timestamp DESC
            ''', (date,))
        
        records = cursor.fetchall()
        conn.close()
        
        return jsonify([{
            'name': record[0],
            'event_type': record[1],
            'timestamp': record[2],
            'verify_method': record[3],
            'department': record[4] or 'General'
        } for record in records])
        
    except Exception as e:
        conn.close()
        return jsonify([])

@app.route('/api/reports/daily')
def api_daily_report():
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'Date required'})
    
    conn = system.get_connection()
    cursor = conn.cursor()
    
    try:
        if system.db_type == 'postgresql':
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE DATE(timestamp) = %s", (date,))
            total_records = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE DATE(timestamp) = %s", (date,))
            unique_employees = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE DATE(timestamp) = %s AND event_type = 'entrada'", (date,))
            entries = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE DATE(timestamp) = %s AND event_type = 'salida'", (date,))
            exits = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT e.name, ar.event_type, ar.timestamp
                FROM attendance_records ar
                JOIN employees e ON ar.employee_id = e.employee_id
                WHERE DATE(ar.timestamp) = %s
                ORDER BY ar.timestamp
            ''', (date,))
            records = cursor.fetchall()
        else:
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE date(timestamp) = ?", (date,))
            total_records = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM attendance_records WHERE date(timestamp) = ?", (date,))
            unique_employees = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE date(timestamp) = ? AND event_type = 'entrada'", (date,))
            entries = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM attendance_records WHERE date(timestamp) = ? AND event_type = 'salida'", (date,))
            exits = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT e.name, ar.event_type, ar.timestamp
                FROM attendance_records ar
                JOIN employees e ON ar.employee_id = e.employee_id
                WHERE date(ar.timestamp) = ?
                ORDER BY ar.timestamp
            ''', (date,))
            records = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'total_records': total_records,
            'unique_employees': unique_employees,
            'entries': entries,
            'exits': exits,
            'records': [{
                'name': record[0],
                'event_type': record[1],
                'timestamp': record[2]
            } for record in records]
        })
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)})

@app.route('/api/reports/weekly')
def api_weekly_report():
    week = request.args.get('week')
    if not week:
        return jsonify({'error': 'Week required'})
    
    # Calcular fechas de la semana
    from datetime import datetime, timedelta
    year, week_num = map(int, week.split('-W'))
    start_date = datetime.strptime(f'{year}-W{week_num}-1', '%Y-W%W-%w')
    end_date = start_date + timedelta(days=6)
    
    conn = system.get_connection()
    cursor = conn.cursor()
    
    try:
        if system.db_type == 'postgresql':
            cursor.execute('''
                SELECT COUNT(*) FROM attendance_records 
                WHERE DATE(timestamp) BETWEEN %s AND %s
            ''', (start_date.date(), end_date.date()))
            total_records = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(DISTINCT employee_id) FROM attendance_records 
                WHERE DATE(timestamp) BETWEEN %s AND %s
            ''', (start_date.date(), end_date.date()))
            active_employees = cursor.fetchone()[0]
        else:
            cursor.execute('''
                SELECT COUNT(*) FROM attendance_records 
                WHERE date(timestamp) BETWEEN ? AND ?
            ''', (start_date.date(), end_date.date()))
            total_records = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(DISTINCT employee_id) FROM attendance_records 
                WHERE date(timestamp) BETWEEN ? AND ?
            ''', (start_date.date(), end_date.date()))
            active_employees = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_records': total_records,
            'active_employees': active_employees,
            'start_date': start_date.date().isoformat(),
            'end_date': end_date.date().isoformat()
        })
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)})

@app.route('/api/reports/attendance')
def api_attendance_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    employee_id = request.args.get('employee_id')
    department = request.args.get('department')
    
    if not start_date or not end_date:
        return jsonify({'error': 'Fechas requeridas'})
    
    try:
        report_data = system.generate_attendance_report(start_date, end_date, employee_id, department)
        return jsonify(report_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/alerts/late')
def api_late_alerts():
    """Obtener alertas de llegadas tardías del día"""
    try:
        conn = system.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        if system.db_type == 'postgresql':
            cursor.execute('''
                SELECT e.employee_id, e.name, e.department, e.schedule,
                       MIN(ar.timestamp) as first_entry
                FROM employees e
                JOIN attendance_records ar ON e.employee_id = ar.employee_id
                WHERE DATE(ar.timestamp) = %s AND ar.event_type = 'entrada' AND e.active = true
                GROUP BY e.employee_id, e.name, e.department, e.schedule
            ''', (today,))
        else:
            cursor.execute('''
                SELECT e.employee_id, e.name, e.department, e.schedule,
                       MIN(ar.timestamp) as first_entry
                FROM employees e
                JOIN attendance_records ar ON e.employee_id = ar.employee_id
                WHERE date(ar.timestamp) = ? AND ar.event_type = 'entrada' AND e.active = 1
                GROUP BY e.employee_id, e.name, e.department, e.schedule
            ''', (today,))
        
        records = cursor.fetchall()
        conn.close()
        
        late_alerts = []
        current_day = datetime.now().strftime('%A').lower()
        
        for record in records:
            emp_id, name, dept, schedule, first_entry = record
            
            # Obtener horario esperado
            expected_hours = system.get_schedule_hours(schedule, current_day)
            if not expected_hours:
                continue
                
            # Extraer hora de entrada
            entry_time = datetime.strptime(str(first_entry)[11:19], '%H:%M:%S').time()
            expected_start = datetime.strptime(expected_hours[0], '%H:%M').time()
            
            if entry_time > expected_start:
                # Calcular minutos de tardanza
                entry_dt = datetime.combine(datetime.today(), entry_time)
                expected_dt = datetime.combine(datetime.today(), expected_start)
                late_minutes = int((entry_dt - expected_dt).total_seconds() / 60)
                
                late_alerts.append({
                    'employee_id': emp_id,
                    'name': name,
                    'department': dept,
                    'expected_time': expected_hours[0],
                    'actual_time': str(entry_time)[:5],
                    'late_minutes': late_minutes,
                    'timestamp': first_entry
                })
        
        return jsonify(late_alerts)
        
    except Exception as e:
        return jsonify({'error': str(e)})
def api_export_excel():
    if not EXCEL_AVAILABLE:
        return jsonify({'error': 'Exportación Excel no disponible. Instala: pip install openpyxl'})
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    employee_id = request.args.get('employee_id')
    department = request.args.get('department')
    
    if not start_date or not end_date:
        return jsonify({'error': 'Fechas requeridas'})
    
    try:
        report_data = system.generate_attendance_report(start_date, end_date, employee_id, department)
        
        if not report_data:
            return jsonify({'error': 'No hay datos para exportar'})
        
        filename = f"reporte_asistencia_{start_date}_{end_date}.xlsx"
        filepath = os.path.join('exports', filename)
        
        # Crear directorio si no existe
        os.makedirs('exports', exist_ok=True)
        
        system.export_to_excel(report_data, filepath)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/export/pdf')
def api_export_pdf():
    if not PDF_AVAILABLE:
        return jsonify({'error': 'Exportación PDF no disponible. Instala: pip install reportlab'})
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    employee_id = request.args.get('employee_id')
    department = request.args.get('department')
    
    if not start_date or not end_date:
        return jsonify({'error': 'Fechas requeridas'})
    
    try:
        report_data = system.generate_attendance_report(start_date, end_date, employee_id, department)
        
        if not report_data:
            return jsonify({'error': 'No hay datos para exportar'})
        
        filename = f"reporte_asistencia_{start_date}_{end_date}.pdf"
        filepath = os.path.join('exports', filename)
        
        # Crear directorio si no existe
        os.makedirs('exports', exist_ok=True)
        
        system.export_to_pdf(report_data, filepath)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 SISTEMA DE ASISTENCIA OPTIMIZADO")
    print("=" * 50)
    print(f"📱 Dispositivo: {system.device_ip}")
    print(f"🗄️ Base de datos: {system.db_type.upper()}")
    print(f"🌐 Dashboard: http://localhost:5000")
    print("=" * 50)
    
    # Probar conexión inicial
    if system.test_connection():
        print("✅ Dispositivo conectado - Monitoreo activo")
        system.start_monitoring()
    else:
        print("⚠️ Dispositivo no disponible - iniciando sin monitoreo")
    
    # Configuración para producción
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)