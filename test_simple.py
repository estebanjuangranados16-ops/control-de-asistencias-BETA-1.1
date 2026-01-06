"""
Test simple de conexión a Supabase
Sin dependencias externas
"""

def test_connection():
    print("🔍 PROBANDO CONEXIÓN A SUPABASE")
    print("=" * 40)
    
    # URL directa (sin .env)
    database_url = "postgresql://postgres:Control2024Hikvision!@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres"
    
    print("📡 Conectando...")
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Probar consulta
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        conn.close()
        
        print("✅ CONEXIÓN EXITOSA!")
        print(f"📊 PostgreSQL: {version[:50]}...")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_tables():
    """Crear tablas del sistema"""
    print("📋 CREANDO TABLAS...")
    
    database_url = "postgresql://postgres:Control2024Hikvision!@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres"
    
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
        
        # Insertar admin
        cursor.execute('''
            INSERT INTO employees (employee_id, name, department) 
            VALUES ('1', 'Administrador', 'Administración')
            ON CONFLICT (employee_id) DO NOTHING
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ TABLAS CREADAS!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        create = input("¿Crear tablas? (s/N): ").strip().lower()
        if create == 's':
            if create_tables():
                print("\n🎉 ¡LISTO!")
                print("🚀 Ejecuta: python system_optimized.py")
    else:
        print("❌ Conexión fallida")