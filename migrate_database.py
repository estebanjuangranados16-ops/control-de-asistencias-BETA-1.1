"""
Script de Migración: SQLite → PostgreSQL
Migra todos los datos del sistema de asistencia
"""
import sqlite3
import psycopg2
import os
from datetime import datetime
import json

class DatabaseMigrator:
    def __init__(self, sqlite_path="attendance.db", postgres_url=None):
        self.sqlite_path = sqlite_path
        self.postgres_url = postgres_url or os.getenv('DATABASE_URL')
        
        if not self.postgres_url:
            raise ValueError("DATABASE_URL no configurada")
    
    def migrate(self):
        """Ejecutar migración completa"""
        print("🚀 Iniciando migración SQLite → PostgreSQL")
        print("=" * 50)
        
        try:
            # 1. Verificar conexiones
            self._test_connections()
            
            # 2. Crear esquema en PostgreSQL
            self._create_postgres_schema()
            
            # 3. Migrar datos
            self._migrate_employees()
            self._migrate_attendance_records()
            self._migrate_work_schedules()
            
            # 4. Verificar migración
            self._verify_migration()
            
            print("\n✅ Migración completada exitosamente")
            
        except Exception as e:
            print(f"\n❌ Error en migración: {e}")
            raise
    
    def _test_connections(self):
        """Probar conexiones a ambas bases de datos"""
        print("🔍 Probando conexiones...")
        
        # SQLite
        if not os.path.exists(self.sqlite_path):
            raise FileNotFoundError(f"Base SQLite no encontrada: {self.sqlite_path}")
        
        sqlite_conn = sqlite3.connect(self.sqlite_path)
        sqlite_conn.close()
        print("✅ SQLite conectado")
        
        # PostgreSQL
        postgres_conn = psycopg2.connect(self.postgres_url)
        postgres_conn.close()
        print("✅ PostgreSQL conectado")
    
    def _create_postgres_schema(self):
        """Crear esquema en PostgreSQL"""
        print("📋 Creando esquema PostgreSQL...")
        
        postgres_conn = psycopg2.connect(self.postgres_url)
        cursor = postgres_conn.cursor()
        
        try:
            # Tabla employees
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    employee_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    department TEXT,
                    schedule TEXT DEFAULT 'estandar',
                    phone TEXT DEFAULT '',
                    email TEXT DEFAULT '',
                    active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    synced_to_device BOOLEAN DEFAULT false
                )
            ''')
            
            # Tabla attendance_records
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance_records (
                    id SERIAL PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    reader_no INTEGER DEFAULT 1,
                    verify_method TEXT DEFAULT 'huella',
                    status TEXT DEFAULT 'autorizado',
                    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
                )
            ''')
            
            # Tabla work_schedules
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS work_schedules (
                    id SERIAL PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    day_of_week INTEGER NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    active BOOLEAN DEFAULT true,
                    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
                )
            ''')
            
            # Tabla blocked_attempts (nueva)
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
            
            # Índices para rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_employee_date ON attendance_records (employee_id, DATE(timestamp))')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance_records (timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_active ON employees (active)')
            
            postgres_conn.commit()
            print("✅ Esquema PostgreSQL creado")
            
        finally:
            postgres_conn.close()
    
    def _migrate_employees(self):
        """Migrar tabla employees"""
        print("👥 Migrando empleados...")
        
        sqlite_conn = sqlite3.connect(self.sqlite_path)
        postgres_conn = psycopg2.connect(self.postgres_url)
        
        try:
            # Leer de SQLite
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute('''
                SELECT employee_id, name, department, schedule, phone, email, active, created_at, synced_to_device
                FROM employees
            ''')
            employees = sqlite_cursor.fetchall()
            
            # Escribir a PostgreSQL
            postgres_cursor = postgres_conn.cursor()
            
            migrated = 0
            for emp in employees:
                try:
                    postgres_cursor.execute('''
                        INSERT INTO employees 
                        (employee_id, name, department, schedule, phone, email, active, created_at, synced_to_device)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (employee_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        department = EXCLUDED.department,
                        schedule = EXCLUDED.schedule,
                        phone = EXCLUDED.phone,
                        email = EXCLUDED.email,
                        active = EXCLUDED.active,
                        synced_to_device = EXCLUDED.synced_to_device
                    ''', emp)
                    migrated += 1
                except Exception as e:
                    print(f"⚠️  Error migrando empleado {emp[0]}: {e}")
            
            postgres_conn.commit()
            print(f"✅ {migrated} empleados migrados")
            
        finally:
            sqlite_conn.close()
            postgres_conn.close()
    
    def _migrate_attendance_records(self):
        """Migrar registros de asistencia"""
        print("📊 Migrando registros de asistencia...")
        
        sqlite_conn = sqlite3.connect(self.sqlite_path)
        postgres_conn = psycopg2.connect(self.postgres_url)
        
        try:
            # Leer de SQLite
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute('''
                SELECT employee_id, event_type, timestamp, reader_no, verify_method, status
                FROM attendance_records
                ORDER BY timestamp
            ''')
            records = sqlite_cursor.fetchall()
            
            # Escribir a PostgreSQL en lotes
            postgres_cursor = postgres_conn.cursor()
            
            batch_size = 1000
            migrated = 0
            
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                postgres_cursor.executemany('''
                    INSERT INTO attendance_records 
                    (employee_id, event_type, timestamp, reader_no, verify_method, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', batch)
                
                migrated += len(batch)
                print(f"  📈 {migrated}/{len(records)} registros migrados")
            
            postgres_conn.commit()
            print(f"✅ {migrated} registros de asistencia migrados")
            
        finally:
            sqlite_conn.close()
            postgres_conn.close()
    
    def _migrate_work_schedules(self):
        """Migrar horarios de trabajo"""
        print("⏰ Migrando horarios de trabajo...")
        
        sqlite_conn = sqlite3.connect(self.sqlite_path)
        postgres_conn = psycopg2.connect(self.postgres_url)
        
        try:
            # Verificar si existe la tabla en SQLite
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute('''
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='work_schedules'
            ''')
            
            if not sqlite_cursor.fetchone():
                print("⚠️  Tabla work_schedules no existe en SQLite")
                return
            
            # Leer de SQLite
            sqlite_cursor.execute('''
                SELECT employee_id, day_of_week, start_time, end_time, active
                FROM work_schedules
            ''')
            schedules = sqlite_cursor.fetchall()
            
            if not schedules:
                print("ℹ️  No hay horarios para migrar")
                return
            
            # Escribir a PostgreSQL
            postgres_cursor = postgres_conn.cursor()
            
            migrated = 0
            for schedule in schedules:
                try:
                    postgres_cursor.execute('''
                        INSERT INTO work_schedules 
                        (employee_id, day_of_week, start_time, end_time, active)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', schedule)
                    migrated += 1
                except Exception as e:
                    print(f"⚠️  Error migrando horario: {e}")
            
            postgres_conn.commit()
            print(f"✅ {migrated} horarios migrados")
            
        finally:
            sqlite_conn.close()
            postgres_conn.close()
    
    def _verify_migration(self):
        """Verificar que la migración fue exitosa"""
        print("🔍 Verificando migración...")
        
        sqlite_conn = sqlite3.connect(self.sqlite_path)
        postgres_conn = psycopg2.connect(self.postgres_url)
        
        try:
            # Contar registros en ambas bases
            sqlite_cursor = sqlite_conn.cursor()
            postgres_cursor = postgres_conn.cursor()
            
            # Empleados
            sqlite_cursor.execute('SELECT COUNT(*) FROM employees')
            sqlite_employees = sqlite_cursor.fetchone()[0]
            
            postgres_cursor.execute('SELECT COUNT(*) FROM employees')
            postgres_employees = postgres_cursor.fetchone()[0]
            
            print(f"👥 Empleados: SQLite={sqlite_employees}, PostgreSQL={postgres_employees}")
            
            # Registros de asistencia
            sqlite_cursor.execute('SELECT COUNT(*) FROM attendance_records')
            sqlite_records = sqlite_cursor.fetchone()[0]
            
            postgres_cursor.execute('SELECT COUNT(*) FROM attendance_records')
            postgres_records = postgres_cursor.fetchone()[0]
            
            print(f"📊 Registros: SQLite={sqlite_records}, PostgreSQL={postgres_records}")
            
            # Verificar integridad
            if sqlite_employees == postgres_employees and sqlite_records == postgres_records:
                print("✅ Verificación exitosa - Datos migrados correctamente")
            else:
                print("⚠️  Advertencia: Diferencias en conteos")
            
        finally:
            sqlite_conn.close()
            postgres_conn.close()
    
    def create_backup(self):
        """Crear backup de SQLite antes de migrar"""
        backup_name = f"attendance_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        import shutil
        shutil.copy2(self.sqlite_path, backup_name)
        
        print(f"💾 Backup creado: {backup_name}")
        return backup_name

def main():
    """Función principal de migración"""
    print("🔄 MIGRADOR DE BASE DE DATOS")
    print("SQLite → PostgreSQL")
    print("=" * 30)
    
    # Verificar variables de entorno
    postgres_url = os.getenv('DATABASE_URL')
    if not postgres_url:
        print("❌ Variable DATABASE_URL no configurada")
        print("Ejemplo: export DATABASE_URL='postgresql://user:pass@host:5432/dbname'")
        return
    
    try:
        migrator = DatabaseMigrator()
        
        # Crear backup
        backup_file = migrator.create_backup()
        
        # Confirmar migración
        confirm = input("\n¿Continuar con la migración? (s/N): ").strip().lower()
        if confirm != 's':
            print("Migración cancelada")
            return
        
        # Ejecutar migración
        migrator.migrate()
        
        print(f"\n📋 RESUMEN:")
        print(f"✅ Migración completada")
        print(f"💾 Backup disponible: {backup_file}")
        print(f"🔗 PostgreSQL URL: {postgres_url[:50]}...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Revisa la configuración y vuelve a intentar")

if __name__ == "__main__":
    main()