"""
Probar conexión a Supabase
"""
import os
from dotenv import load_dotenv

def test_connection():
    print("🔍 PROBANDO CONEXIÓN A SUPABASE")
    print("=" * 40)
    
    # Cargar variables de entorno
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    
    print(f"🔗 URL: {database_url[:50]}...")
    
    try:
        import psycopg2
        
        print("📡 Conectando...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Probar consulta
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        # Probar crear tabla simple
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_connection (
                id SERIAL PRIMARY KEY,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insertar registro de prueba
        cursor.execute("INSERT INTO test_connection (message) VALUES ('Conexión exitosa!')")
        
        # Leer registro
        cursor.execute("SELECT message FROM test_connection ORDER BY created_at DESC LIMIT 1")
        test_message = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        print("✅ CONEXIÓN EXITOSA!")
        print(f"📊 PostgreSQL: {version[:50]}...")
        print(f"💬 Mensaje de prueba: {test_message}")
        print()
        print("🚀 LISTO PARA CREAR TABLAS DEL SISTEMA")
        
        return True
        
    except ImportError:
        print("❌ psycopg2 no instalado")
        print("💡 Ejecutar: pip install psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Verifica que hayas guardado la contraseña en Supabase")
        return False

def create_system_tables():
    """Crear tablas del sistema de asistencia"""
    print("\n📋 CREANDO TABLAS DEL SISTEMA...")
    
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Tabla employees
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
        
        # Tabla attendance_records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_records (
                id SERIAL PRIMARY KEY,
                employee_id TEXT NOT NULL,
                event_type TEXT NOT NULL CHECK (event_type IN ('entrada', 'salida')),
                timestamp TIMESTAMP NOT NULL,
                reader_no INTEGER DEFAULT 1,
                verify_method TEXT DEFAULT 'huella',
                status TEXT DEFAULT 'autorizado',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla blocked_attempts (anti-duplicados)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocked_attempts (
                id SERIAL PRIMARY KEY,
                employee_id TEXT,
                event_type TEXT,
                reason TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar admin por defecto
        cursor.execute('''
            INSERT INTO employees (employee_id, name, department) 
            VALUES ('1', 'Administrador', 'Administración')
            ON CONFLICT (employee_id) DO NOTHING
        ''')
        
        # Crear índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_employee_date ON attendance_records (employee_id, DATE(timestamp))')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance_records (timestamp DESC)')
        
        conn.commit()
        conn.close()
        
        print("✅ TABLAS CREADAS EXITOSAMENTE!")
        print("📊 Sistema listo para usar")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        create_tables = input("\n¿Crear tablas del sistema? (s/N): ").strip().lower()
        if create_tables == 's':
            create_system_tables()
            print("\n🎉 CONFIGURACIÓN COMPLETADA!")
            print("🚀 Ejecuta: python system_optimized.py")
    else:
        print("\n❌ Configuración fallida")
        print("Revisa la contraseña en Supabase")