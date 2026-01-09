"""
Script rápido para actualizar contraseña de Supabase
"""
import os

def update_password():
    print("🔑 ACTUALIZAR CONTRASEÑA SUPABASE")
    print("=" * 40)
    
    # Leer archivo .env actual
    if not os.path.exists('.env'):
        print("❌ Archivo .env no encontrado")
        return
    
    with open('.env', 'r') as f:
        content = f.read()
    
    print("📋 Pasos para obtener la contraseña:")
    print("1. Ve a tu proyecto Supabase")
    print("2. Settings > Database")
    print("3. Busca 'Connection string'")
    print("4. Copia la contraseña después de 'postgres:'")
    print()
    
    # Solicitar contraseña
    password = input("🔑 Pega aquí tu contraseña: ").strip()
    
    if not password:
        print("❌ Contraseña requerida")
        return
    
    # Reemplazar en el contenido
    new_content = content.replace('[TU_PASSWORD]', password)
    
    # Guardar archivo actualizado
    with open('.env', 'w') as f:
        f.write(new_content)
    
    print("✅ Contraseña actualizada en .env")
    print("🔗 DATABASE_URL configurada correctamente")
    
    # Probar conexión
    test_connection(password)

def test_connection(password):
    """Probar conexión rápida"""
    print("\n🔍 Probando conexión...")
    
    database_url = f"postgresql://postgres:{password}@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres"
    
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        
        print("✅ Conexión exitosa!")
        print("🚀 Listo para crear tablas")
        
        # Preguntar si crear tablas
        create = input("\n¿Crear tablas del sistema ahora? (s/N): ").strip().lower()
        if create == 's':
            create_tables(database_url)
        
    except ImportError:
        print("❌ psycopg2 no instalado")
        print("💡 Ejecutar: pip install psycopg2-binary")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica que la contraseña sea correcta")

def create_tables(database_url):
    """Crear tablas básicas"""
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Crear tablas básicas
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
        
        # Insertar admin por defecto
        cursor.execute('''
            INSERT INTO employees (employee_id, name, department) 
            VALUES ('1', 'Administrador', 'Administración')
            ON CONFLICT (employee_id) DO NOTHING
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Tablas creadas exitosamente!")
        print("📊 Sistema listo para usar")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")

if __name__ == "__main__":
    update_password()