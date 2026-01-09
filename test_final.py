"""
Test con URL correcta de Supabase
"""

def test_connection():
    print("🔍 PROBANDO CONEXIÓN SUPABASE (URL CORRECTA)")
    print("=" * 50)
    
    # URL correcta con connection pooling
    database_url = "postgresql://postgres.gyoxiqcnkaimovbuyaas:Control2024Hikvision!@aws-1-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
    
    print("📡 Conectando con pooling...")
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Probar consulta
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        # Probar crear tabla
        cursor.execute("CREATE TABLE IF NOT EXISTS test_connection (id SERIAL PRIMARY KEY, message TEXT)")
        cursor.execute("INSERT INTO test_connection (message) VALUES ('¡Conexión exitosa!')")
        cursor.execute("SELECT message FROM test_connection ORDER BY id DESC LIMIT 1")
        message = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        print("✅ CONEXIÓN EXITOSA!")
        print(f"📊 PostgreSQL: {version[:60]}...")
        print(f"💬 Test: {message}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Probar con conexión directa
        print("\n🔄 Probando conexión directa...")
        return test_direct_connection()

def test_direct_connection():
    """Probar conexión directa (sin pooling)"""
    direct_url = "postgresql://postgres.gyoxiqcnkaimovbuyaas:Control2024Hikvision!@aws-1-us-east-1.pooler.supabase.com:5432/postgres"
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(direct_url)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1")
        conn.close()
        
        print("✅ CONEXIÓN DIRECTA EXITOSA!")
        return True
        
    except Exception as e:
        print(f"❌ Error conexión directa: {e}")
        return False

def create_tables():
    """Crear tablas del sistema"""
    print("📋 CREANDO TABLAS DEL SISTEMA...")
    
    # Usar conexión directa para crear tablas
    database_url = "postgresql://postgres.gyoxiqcnkaimovbuyaas:Control2024Hikvision!@aws-1-us-east-1.pooler.supabase.com:5432/postgres"
    
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
                status TEXT DEFAULT 'autorizado'
            )
        ''')
        
        # Tabla blocked_attempts
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
        
        # Insertar admin
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
        create = input("\n¿Crear tablas del sistema? (s/N): ").strip().lower()
        if create == 's':
            if create_tables():
                print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
                print("🚀 Ejecuta: python system_optimized.py")
                print("🌐 Abre: http://localhost:5000")
    else:
        print("\n❌ No se pudo conectar a Supabase")
        print("💡 Verifica tu conexión a internet")