"""
Generador de nueva contraseña para Supabase
Si no encuentras la contraseña original
"""
import secrets
import string

def generate_strong_password():
    """Generar contraseña segura"""
    # Caracteres permitidos (sin símbolos problemáticos para URLs)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    
    # Generar contraseña de 16 caracteres
    password = ''.join(secrets.choice(chars) for _ in range(16))
    
    return password

def main():
    print("🔑 GENERADOR DE CONTRASEÑA SUPABASE")
    print("=" * 40)
    print("Si no encuentras tu contraseña actual, puedes crear una nueva")
    print()
    
    print("📋 PASOS:")
    print("1. Ve a tu proyecto Supabase")
    print("2. Settings > Database")
    print("3. Busca 'Reset database password'")
    print("4. Usa esta contraseña segura:")
    print()
    
    # Generar contraseña
    new_password = generate_strong_password()
    print(f"🔐 NUEVA CONTRASEÑA: {new_password}")
    print()
    
    print("5. Pega esa contraseña en Supabase")
    print("6. Click 'Save'")
    print("7. Ejecuta: python update_password.py")
    print("8. Pega la misma contraseña cuando te la pida")
    print()
    
    print("⚠️  IMPORTANTE: Guarda esta contraseña en un lugar seguro")
    
    # Crear DATABASE_URL completa
    database_url = f"postgresql://postgres:{new_password}@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres"
    
    print("\n🔗 Tu DATABASE_URL será:")
    print(database_url)
    
    # Preguntar si actualizar .env directamente
    update = input("\n¿Actualizar .env directamente con esta contraseña? (s/N): ").strip().lower()
    
    if update == 's':
        update_env_file(new_password)
        print("✅ Archivo .env actualizado")
        print("🚀 Ahora ve a Supabase y cambia la contraseña por la generada")

def update_env_file(password):
    """Actualizar archivo .env"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Reemplazar contraseña
        new_content = content.replace('[TU_PASSWORD]', password)
        
        with open('.env', 'w') as f:
            f.write(new_content)
            
    except Exception as e:
        print(f"❌ Error actualizando .env: {e}")

if __name__ == "__main__":
    main()