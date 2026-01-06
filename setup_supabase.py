"""
Configurador de Supabase para Sistema de Asistencia
Guía paso a paso para configurar la base de datos
"""
import os
import sys

def setup_supabase():
    print("🚀 CONFIGURADOR SUPABASE")
    print("=" * 40)
    print("Tu proyecto: gyoxiqcnkaimovbuyaas")
    print("URL: https://gyoxiqcnkaimovbuyaas.supabase.co")
    print()
    
    print("📋 PASOS PARA OBTENER LA CONTRASEÑA:")
    print("1. Ve a tu proyecto Supabase")
    print("2. Click en 'Settings' (⚙️) en el menú izquierdo")
    print("3. Click en 'Database'")
    print("4. En la sección 'Connection string', verás:")
    print("   postgresql://postgres:[YOUR-PASSWORD]@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres")
    print("5. Copia la contraseña que aparece después de 'postgres:'")
    print()
    
    # Solicitar contraseña
    password = input("🔑 Ingresa la contraseña de tu base de datos: ").strip()
    
    if not password:
        print("❌ Contraseña requerida")
        return False
    
    # Crear DATABASE_URL completa
    database_url = f"postgresql://postgres:{password}@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres"
    
    print(f"\n✅ DATABASE_URL configurada:")
    print(f"postgresql://postgres:***@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres")
    
    # Actualizar archivo .env
    update_env_file(database_url)
    
    # Probar conexión
    test_connection(database_url)
    
    return True

def update_env_file(database_url):
    """Actualizar archivo .env con la URL correcta"""
    env_content = f"""# Variables de Entorno - Sistema de Asistencia
# CONFIGURACIÓN SUPABASE

# Base de datos Supabase
DATABASE_URL={database_url}

# Supabase API
SUPABASE_URL=https://gyoxiqcnkaimovbuyaas.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5b3hpcWNua2FpbW92YnV5YWFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU2NzI4NzQsImV4cCI6MjA1MTI0ODg3NH0.sb_publishable_oNfw5YBnfFSVHqpbXozkSg_akIpewYS

# Dispositivo Hikvision
DEVICE_IP=172.10.1.62
DEVICE_USER=admin
DEVICE_PASS=PC2024*+

# Flask
FLASK_ENV=production
FLASK_SECRET_KEY=hikvision_attendance_2024_super_secret

# Seguridad
ALLOWED_ORIGINS=http://localhost:3000,https://gyoxiqcnkaimovbuyaas.supabase.co

# Anti-duplicados
SAME_EVENT_WINDOW=30
DIFFERENT_EVENT_WINDOW=300
MAX_DAILY_RECORDS=8

# Logging
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("📝 Archivo .env actualizado")

def test_connection(database_url):
    """Probar conexión a Supabase"""
    print("\n🔍 Probando conexión...")
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Probar consulta simple
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        conn.close()
        
        print("✅ Conexión exitosa!")
        print(f"📊 PostgreSQL: {version[:50]}...")
        
        return True
        
    except ImportError:
        print("❌ psycopg2 no instalado")
        print("💡 Ejecutar: pip install psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Verifica que la contraseña sea correcta")
        return False

def create_tables():
    """Crear tablas en Supabase"""
    print("\n📋 ¿Quieres crear las tablas del sistema? (s/N): ", end="")
    create = input().strip().lower()
    
    if create != 's':
        print("⏭️  Tablas no creadas. Puedes hacerlo después con migrate_database.py")
        return
    
    try:
        # Cargar variables de entorno
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv('DATABASE_URL')
        
        import psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Leer y ejecutar init.sql
        with open('init.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        cursor.execute(sql_script)
        conn.commit()
        conn.close()
        
        print("✅ Tablas creadas exitosamente!")
        print("📊 Sistema listo para usar")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        print("💡 Puedes crear las tablas manualmente desde Supabase SQL Editor")

def main():
    print("🎯 CONFIGURACIÓN COMPLETA DE SUPABASE")
    print("Para Sistema de Asistencia Hikvision")
    print("=" * 50)
    
    # Verificar si ya existe .env
    if os.path.exists('.env'):
        print("⚠️  Archivo .env ya existe")
        overwrite = input("¿Sobrescribir? (s/N): ").strip().lower()
        if overwrite != 's':
            print("Configuración cancelada")
            return
    
    # Configurar Supabase
    if setup_supabase():
        create_tables()
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA!")
        print("=" * 30)
        print("✅ Supabase configurado")
        print("✅ Variables de entorno creadas")
        print("✅ Conexión probada")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Ejecutar: python migrate_database.py (si tienes datos en SQLite)")
        print("2. Ejecutar: python system_optimized.py")
        print("3. Abrir: http://localhost:5000")
    else:
        print("\n❌ Configuración fallida")
        print("Revisa los pasos y vuelve a intentar")

if __name__ == "__main__":
    main()