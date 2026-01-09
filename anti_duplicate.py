"""
Sistema Anti-Duplicados Inteligente
Previene registros duplicados con múltiples niveles de validación
"""
from datetime import datetime, timedelta, time
import logging

class AntiDuplicateSystem:
    def __init__(self, db_connection_func):
        self.get_connection = db_connection_func
        self.setup_logging()
        
        # Configuración de ventanas de tiempo
        self.SAME_EVENT_WINDOW = 30  # 30 segundos para mismo tipo
        self.DIFFERENT_EVENT_WINDOW = 300  # 5 minutos entre entrada/salida
        self.MAX_DAILY_RECORDS = 8  # Máximo registros por día
        
        # Horarios válidos (evitar registros a medianoche)
        self.VALID_HOURS = {
            'start': time(5, 0),   # 5:00 AM
            'end': time(23, 0)     # 11:00 PM
        }
    
    def setup_logging(self):
        """Configurar logging para duplicados"""
        logging.basicConfig(
            filename='anti_duplicate.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_attendance(self, employee_id, event_type, timestamp=None):
        """
        Validar si el registro de asistencia es válido
        
        Returns:
            tuple: (is_valid: bool, reason: str, suggested_action: str)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Nivel 1: Validación de horario
        if not self._is_valid_time(timestamp):
            return False, "Horario fuera del rango válido (5:00-23:00)", "ignore"
        
        # Nivel 2: Verificar duplicados recientes
        duplicate_check = self._check_recent_duplicates(employee_id, event_type, timestamp)
        if not duplicate_check[0]:
            return duplicate_check
        
        # Nivel 3: Validar patrón de comportamiento
        pattern_check = self._validate_daily_pattern(employee_id, timestamp)
        if not pattern_check[0]:
            return pattern_check
        
        # Nivel 4: Validar lógica de entrada/salida
        logic_check = self._validate_entry_exit_logic(employee_id, event_type, timestamp)
        if not logic_check[0]:
            return logic_check
        
        return True, "Registro válido", "proceed"
    
    def _is_valid_time(self, timestamp):
        """Verificar si la hora está en rango válido"""
        current_time = timestamp.time()
        return self.VALID_HOURS['start'] <= current_time <= self.VALID_HOURS['end']
    
    def _check_recent_duplicates(self, employee_id, event_type, timestamp):
        """Verificar duplicados recientes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar mismo tipo de evento en ventana corta
            if hasattr(conn, 'execute'):  # SQLite
                cursor.execute('''
                    SELECT timestamp, event_type FROM attendance_records 
                    WHERE employee_id = ? 
                    AND datetime(timestamp) > datetime(?, '-{} seconds')
                    ORDER BY timestamp DESC LIMIT 1
                '''.format(self.SAME_EVENT_WINDOW), (employee_id, timestamp.isoformat()))
            else:  # PostgreSQL
                cursor.execute('''
                    SELECT timestamp, event_type FROM attendance_records 
                    WHERE employee_id = %s 
                    AND timestamp > %s - INTERVAL '%s seconds'
                    ORDER BY timestamp DESC LIMIT 1
                ''', (employee_id, timestamp, self.SAME_EVENT_WINDOW))
            
            recent = cursor.fetchone()
            
            if recent:
                recent_time, recent_event = recent
                time_diff = (timestamp - datetime.fromisoformat(str(recent_time))).total_seconds()
                
                # Si es el mismo tipo de evento y muy reciente
                if recent_event == event_type and time_diff < self.SAME_EVENT_WINDOW:
                    self.logger.warning(f"Duplicado mismo evento: {employee_id} - {event_type} - {time_diff}s")
                    return False, f"Registro duplicado ({int(time_diff)}s desde último)", "ignore"
                
                # Si es diferente evento pero muy reciente (menos de 5 min)
                if recent_event != event_type and time_diff < self.DIFFERENT_EVENT_WINDOW:
                    self.logger.info(f"Evento muy rápido: {employee_id} - {recent_event}→{event_type} - {time_diff}s")
                    return False, f"Cambio muy rápido de {recent_event} a {event_type} ({int(time_diff/60)}min)", "confirm"
            
            return True, "Sin duplicados recientes", "proceed"
            
        finally:
            conn.close()
    
    def _validate_daily_pattern(self, employee_id, timestamp):
        """Validar patrón diario del empleado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Contar registros del día
            date_str = timestamp.date().isoformat()
            
            if hasattr(conn, 'execute'):  # SQLite
                cursor.execute('''
                    SELECT COUNT(*), GROUP_CONCAT(event_type || ':' || time(timestamp)) 
                    FROM attendance_records 
                    WHERE employee_id = ? AND date(timestamp) = ?
                ''', (employee_id, date_str))
            else:  # PostgreSQL
                cursor.execute('''
                    SELECT COUNT(*), STRING_AGG(event_type || ':' || TO_CHAR(timestamp, 'HH24:MI'), ', ') 
                    FROM attendance_records 
                    WHERE employee_id = %s AND DATE(timestamp) = %s
                ''', (employee_id, date_str))
            
            count, pattern = cursor.fetchone()
            
            if count >= self.MAX_DAILY_RECORDS:
                self.logger.warning(f"Demasiados registros: {employee_id} - {count} registros hoy")
                return False, f"Demasiados registros hoy ({count}/{self.MAX_DAILY_RECORDS})", "review"
            
            # Log del patrón para análisis
            if pattern:
                self.logger.info(f"Patrón diario {employee_id}: {pattern}")
            
            return True, "Patrón diario normal", "proceed"
            
        finally:
            conn.close()
    
    def _validate_entry_exit_logic(self, employee_id, event_type, timestamp):
        """Validar lógica de entrada/salida"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener último registro del día
            date_str = timestamp.date().isoformat()
            
            if hasattr(conn, 'execute'):  # SQLite
                cursor.execute('''
                    SELECT event_type, time(timestamp) FROM attendance_records 
                    WHERE employee_id = ? AND date(timestamp) = ?
                    ORDER BY timestamp DESC LIMIT 1
                ''', (employee_id, date_str))
            else:  # PostgreSQL
                cursor.execute('''
                    SELECT event_type, TO_CHAR(timestamp, 'HH24:MI:SS') FROM attendance_records 
                    WHERE employee_id = %s AND DATE(timestamp) = %s
                    ORDER BY timestamp DESC LIMIT 1
                ''', (employee_id, date_str))
            
            last_record = cursor.fetchone()
            
            if last_record:
                last_event, last_time = last_record
                
                # Validar secuencia lógica
                if last_event == event_type:
                    # Mismo evento consecutivo - puede ser válido en algunos casos
                    current_hour = timestamp.hour
                    
                    # Permitir múltiples entradas/salidas en horarios de descanso
                    if self._is_break_time(current_hour):
                        return True, f"Múltiple {event_type} en horario de descanso", "proceed"
                    else:
                        self.logger.info(f"Evento consecutivo: {employee_id} - {event_type} repetido")
                        return False, f"Evento {event_type} consecutivo (último: {last_time})", "confirm"
            
            return True, "Lógica de entrada/salida válida", "proceed"
            
        finally:
            conn.close()
    
    def _is_break_time(self, hour):
        """Verificar si está en horario de descanso"""
        # Horarios típicos de descanso
        break_hours = [9, 10, 12, 13, 14, 15]  # 9-10 AM, 12-3 PM
        return hour in break_hours
    
    def log_blocked_attempt(self, employee_id, event_type, reason, timestamp=None):
        """Registrar intento bloqueado para análisis"""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.logger.warning(f"BLOQUEADO: {employee_id} - {event_type} - {reason} - {timestamp}")
        
        # Opcional: Guardar en tabla de intentos bloqueados
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if hasattr(conn, 'execute'):  # SQLite
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS blocked_attempts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT,
                        event_type TEXT,
                        reason TEXT,
                        timestamp TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    INSERT INTO blocked_attempts (employee_id, event_type, reason, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (employee_id, event_type, reason, timestamp))
            else:  # PostgreSQL
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS blocked_attempts (
                        id SERIAL PRIMARY KEY,
                        employee_id TEXT,
                        event_type TEXT,
                        reason TEXT,
                        timestamp TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    INSERT INTO blocked_attempts (employee_id, event_type, reason, timestamp)
                    VALUES (%s, %s, %s, %s)
                ''', (employee_id, event_type, reason, timestamp))
            
            conn.commit()
            
        except Exception as e:
            self.logger.error(f"Error guardando intento bloqueado: {e}")
        finally:
            conn.close()
    
    def get_daily_stats(self, date=None):
        """Obtener estadísticas diarias de duplicados"""
        if date is None:
            date = datetime.now().date()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_str = date.isoformat()
            
            if hasattr(conn, 'execute'):  # SQLite
                cursor.execute('''
                    SELECT COUNT(*), COUNT(DISTINCT employee_id) 
                    FROM blocked_attempts 
                    WHERE date(created_at) = ?
                ''', (date_str,))
            else:  # PostgreSQL
                cursor.execute('''
                    SELECT COUNT(*), COUNT(DISTINCT employee_id) 
                    FROM blocked_attempts 
                    WHERE DATE(created_at) = %s
                ''', (date_str,))
            
            total_blocked, employees_affected = cursor.fetchone() or (0, 0)
            
            return {
                'date': date_str,
                'total_blocked': total_blocked,
                'employees_affected': employees_affected
            }
            
        finally:
            conn.close()