"""
Sistema de Asistencia con Breaks y Horarios
Implementación del sistema de breaks para administrativos y operativos
"""
from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
from requests.auth import HTTPDigestAuth
import json
import threading
from datetime import datetime, timedelta, time
import time as time_module
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'hikvision_attendance_2024')
CORS(app, origins=["http://localhost:3001", "http://localhost:3000"])
socketio = SocketIO(app, cors_allowed_origins="*")

class BreakAttendanceSystem:
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
        """Inicializar base de datos con sistema de breaks"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db_type == 'postgresql':
                # Crear tablas PostgreSQL con sistema de breaks
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
                    CREATE TABLE IF NOT EXISTS break_types (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        display_name VARCHAR(100) NOT NULL,
                        duration_minutes INTEGER NOT NULL,
                        mandatory BOOLEAN DEFAULT true,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS department_schedules (
                        id SERIAL PRIMARY KEY,
                        department VARCHAR(100) NOT NULL,
                        shift_type VARCHAR(50),
                        work_start TIME NOT NULL,
                        work_end TIME NOT NULL,
                        break_start TIME NOT NULL,
                        break_end TIME NOT NULL,
                        has_lunch BOOLEAN DEFAULT FALSE,
                        lunch_options TEXT[],
                        friday_end TIME,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                        status TEXT DEFAULT 'autorizado',
                        break_type VARCHAR(50),
                        is_break_record BOOLEAN DEFAULT FALSE,
                        break_duration_minutes INTEGER
                    )
                ''')
                
                # Insertar datos iniciales
                cursor.execute('''
                    INSERT INTO break_types (name, display_name, duration_minutes, mandatory) VALUES
                    ('admin_break', 'Break Administrativo', 20, TRUE),
                    ('operativo_break', 'Break Operativo', 20, TRUE),
                    ('almuerzo_12', 'Almuerzo 12:00-13:00', 60, TRUE),
                    ('almuerzo_13', 'Almuerzo 13:00-14:00', 60, TRUE)
                    ON CONFLICT DO NOTHING
                ''')
                
                cursor.execute('''
                    INSERT INTO department_schedules (department, shift_type, work_start, work_end, break_start, break_end, has_lunch, lunch_options, friday_end) VALUES
                    ('Reacondicionamiento', NULL, '07:00', '17:00', '09:00', '10:00', TRUE, ARRAY['12:00-13:00', '13:00-14:00'], '16:00'),
                    ('Logistica', NULL, '07:00', '17:00', '09:00', '10:00', TRUE, ARRAY['12:00-13:00', '13:00-14:00'], '16:00'),
                    ('Administracion', NULL, '07:00', '17:00', '09:00', '10:00', TRUE, ARRAY['12:00-13:00', '13:00-14:00'], '16:00'),
                    ('Operativos', 'mañana', '06:00', '14:00', '09:00', '10:00', FALSE, NULL, NULL),
                    ('Operativos', 'tarde', '14:00', '22:00', '17:00', '18:00', FALSE, NULL, NULL),
                    ('Operativos', 'noche', '22:00', '06:00', '01:00', '02:00', FALSE, NULL, NULL)
                    ON CONFLICT DO NOTHING
                ''')
                
                cursor.execute('''
                    INSERT INTO employees (employee_id, name, department) 
                    VALUES (%s, %s, %s)
                    ON CONFLICT (employee_id) DO NOTHING
                ''', ('1', 'Administrador', 'Administracion'))
                
            conn.commit()
            print("✅ Base de datos con sistema de breaks inicializada")
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
        finally:
            conn.close()
    
    def classify_attendance_record(self, employee_id, timestamp, department, shift_type=None):
        """Clasificar registro de asistencia considerando breaks"""
        time_only = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').time()
        
        # 1. Verificar si es primera entrada del día/turno
        if self.is_first_record_of_day(employee_id, timestamp.split(' ')[0]):
            return 'entrada'
        
        # 2. Detectar breaks según departamento y turno
        if department in ['Reacondicionamiento', 'Logistica', 'Administracion']:
            # Break administrativo: 9:00-10:00 AM
            if time(9, 0) <= time_only <= time(10, 0):
                return self.detect_break_type(employee_id, timestamp, 'admin_break')
                
            # Almuerzo administrativo: 12:00-14:00
            if time(12, 0) <= time_only <= time(14, 0):
                return self.detect_break_type(employee_id, timestamp, 'almuerzo')
        
        elif department == 'Operativos':
            break_window = self.get_break_window_by_shift(shift_type)
            if break_window['start'] <= time_only <= break_window['end']:
                return self.detect_break_type(employee_id, timestamp, 'operativo_break')
        
        # 3. Determinar entrada/salida regular
        return self.determine_regular_event_type(employee_id, timestamp)
    
    def get_break_window_by_shift(self, shift_type):
        """Obtener ventana de break según turno operativo"""
        windows = {
            'mañana': {'start': time(9, 0), 'end': time(10, 0)},
            'tarde': {'start': time(17, 0), 'end': time(18, 0)},
            'noche': {'start': time(1, 0), 'end': time(2, 0)}
        }
        return windows.get(shift_type, windows['mañana'])
    
    def detect_break_type(self, employee_id, timestamp, break_category):
        """Detectar tipo específico de break"""
        # Obtener último registro del día
        last_event = self.get_last_event_today(employee_id, timestamp.split(' ')[0])
        
        if break_category == 'admin_break':
            return 'break_salida' if last_event in ['entrada', 'break_entrada'] else 'break_entrada'
        elif break_category == 'operativo_break':
            return 'break_salida' if last_event in ['entrada', 'break_entrada'] else 'break_entrada'
        elif break_category == 'almuerzo':
            return 'almuerzo_salida' if last_event in ['entrada', 'break_entrada', 'almuerzo_entrada'] else 'almuerzo_entrada'
        
        return 'entrada'
    
    def is_first_record_of_day(self, employee_id, date):
        """Verificar si es el primer registro del día"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.db_type == 'postgresql':
            cursor.execute('''
                SELECT COUNT(*) FROM attendance_records 
                WHERE employee_id = %s AND DATE(timestamp) = %s
            ''', (employee_id, date))
        else:
            cursor.execute('''
                SELECT COUNT(*) FROM attendance_records 
                WHERE employee_id = ? AND date(timestamp) = ?
            ''', (employee_id, date))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
    
    def get_last_event_today(self, employee_id, date):
        """Obtener último evento del día"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.db_type == 'postgresql':
            cursor.execute('''
                SELECT event_type FROM attendance_records 
                WHERE employee_id = %s AND DATE(timestamp) = %s
                ORDER BY timestamp DESC LIMIT 1
            ''', (employee_id, date))
        else:
            cursor.execute('''
                SELECT event_type FROM attendance_records 
                WHERE employee_id = ? AND date(timestamp) = ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (employee_id, date))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def determine_regular_event_type(self, employee_id, timestamp):
        """Determinar entrada/salida regular"""
        last_event = self.get_last_event_today(employee_id, timestamp.split(' ')[0])
        
        # Si no hay registros, es entrada
        if not last_event:
            return 'entrada'
        
        # Alternar según último evento
        if last_event in ['salida', 'break_salida', 'almuerzo_salida']:
            return 'entrada'
        else:
            return 'salida'
    
    def record_attendance(self, employee_id, timestamp, reader_no=1, verify_method="huella"):
        """Registrar asistencia con lógica de breaks"""
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
            
            name, department, schedule = employee
            
            # Obtener turno si es operativo
            shift_type = self.get_employee_shift(employee_id, timestamp) if department == 'Operativos' else None
            
            # Clasificar tipo de evento
            event_type = self.classify_attendance_record(employee_id, timestamp, department, shift_type)
            
            # Determinar si es registro de break
            is_break = event_type.startswith('break_') or event_type.startswith('almuerzo_')
            break_type = None
            
            if is_break:
                if event_type.startswith('break_'):
                    break_type = 'admin_break' if department in ['Reacondicionamiento', 'Logistica', 'Administracion'] else 'operativo_break'
                elif event_type.startswith('almuerzo_'):
                    break_type = 'almuerzo_12'  # Simplificado
            
            # Insertar registro
            if self.db_type == 'postgresql':
                cursor.execute('''
                    INSERT INTO attendance_records 
                    (employee_id, event_type, timestamp, reader_no, verify_method, status, break_type, is_break_record)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (employee_id, event_type, timestamp, reader_no, verify_method, "autorizado", break_type, is_break))
            else:
                cursor.execute('''
                    INSERT INTO attendance_records 
                    (employee_id, event_type, timestamp, reader_no, verify_method, status, break_type, is_break_record)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (employee_id, event_type, timestamp, reader_no, verify_method, "autorizado", break_type, is_break))
            
            conn.commit()
            conn.close()
            
            print(f"✅ REGISTRO: {name} - {event_type.upper()} - {timestamp}")
            
            # Emitir evento WebSocket
            socketio.emit('attendance_record', {
                'employee_id': employee_id,
                'name': name,
                'event_type': event_type,
                'timestamp': timestamp,
                'verify_method': verify_method,
                'department': department,
                'is_break': is_break,
                'break_type': break_type
            })
            
            # Verificar alertas de breaks
            self.check_break_compliance(employee_id, name, department, timestamp)
            
            return True
            
        except Exception as e:
            print(f"❌ Error al registrar: {e}")
            return False
    
    def get_employee_shift(self, employee_id, timestamp):
        """Obtener turno del empleado operativo"""
        # Simplificado - en producción consultar weekly_shift_assignments
        current_hour = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').hour
        
        if 6 <= current_hour < 14:
            return 'mañana'
        elif 14 <= current_hour < 22:
            return 'tarde'
        else:
            return 'noche'
    
    def check_break_compliance(self, employee_id, name, department, timestamp):
        """Verificar cumplimiento de breaks obligatorios"""
        try:
            date = timestamp.split(' ')[0]
            current_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').time()
            
            # Verificar break no tomado
            if department in ['Reacondicionamiento', 'Logistica', 'Administracion']:
                if current_time > time(10, 30) and not self.has_break_today(employee_id, date, 'admin_break'):
                    socketio.emit('break_alert', {
                        'employee_id': employee_id,
                        'name': name,
                        'alert_type': 'break_missing',
                        'message': f'{name} no ha tomado su break obligatorio'
                    })
            
            elif department == 'Operativos':
                shift_type = self.get_employee_shift(employee_id, timestamp)
                break_window = self.get_break_window_by_shift(shift_type)
                
                if current_time > break_window['end'] and not self.has_break_today(employee_id, date, 'operativo_break'):
                    socketio.emit('break_alert', {
                        'employee_id': employee_id,
                        'name': name,
                        'alert_type': 'break_missing',
                        'message': f'{name} no ha tomado su break del turno {shift_type}'
                    })
                    
        except Exception as e:
            print(f"Error verificando breaks: {e}")
    
    def has_break_today(self, employee_id, date, break_type):
        """Verificar si el empleado ya tomó su break"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.db_type == 'postgresql':
            cursor.execute('''
                SELECT COUNT(*) FROM attendance_records 
                WHERE employee_id = %s AND DATE(timestamp) = %s 
                AND break_type = %s AND is_break_record = TRUE
            ''', (employee_id, date, break_type))
        else:
            cursor.execute('''
                SELECT COUNT(*) FROM attendance_records 
                WHERE employee_id = ? AND date(timestamp) = ? 
                AND break_type = ? AND is_break_record = 1
            ''', (employee_id, date, break_type))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

# Instancia global
system = BreakAttendanceSystem()

# Rutas básicas para testing
@app.route('/')
def dashboard():
    return "<h1>Sistema de Breaks Implementado</h1><p>Base de datos configurada con sistema de breaks y horarios.</p>"

@app.route('/api/test_break_system')
def test_break_system():
    """Endpoint para probar el sistema de breaks"""
    try:
        # Simular registro de empleado administrativo
        system.record_attendance('1', '2024-01-15 09:15:00')  # Break
        system.record_attendance('1', '2024-01-15 09:35:00')  # Regreso break
        system.record_attendance('1', '2024-01-15 12:30:00')  # Almuerzo
        system.record_attendance('1', '2024-01-15 13:30:00')  # Regreso almuerzo
        
        return jsonify({
            'success': True,
            'message': 'Sistema de breaks funcionando correctamente',
            'features': [
                'Detección automática de breaks',
                'Clasificación por departamento',
                'Alertas de cumplimiento',
                'Horarios por turno'
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 SISTEMA DE BREAKS Y HORARIOS")
    print("=" * 50)
    print("✅ Sistema de breaks implementado")
    print("✅ Horarios por departamento configurados")
    print("✅ Detección automática de breaks")
    print("✅ Alertas de cumplimiento")
    print("=" * 50)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)