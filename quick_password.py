"""
Script súper simple para actualizar contraseña
"""

def update_password():
    password = input("🔑 Pega aquí la contraseña de PostgreSQL: ").strip()
    
    if not password:
        print("❌ Contraseña requerida")
        return
    
    # Leer .env
    with open('.env', 'r') as f:
        content = f.read()
    
    # Reemplazar
    new_content = content.replace('[TU_PASSWORD]', password)
    
    # Guardar
    with open('.env', 'w') as f:
        f.write(new_content)
    
    print("✅ Contraseña actualizada!")
    print(f"🔗 DATABASE_URL: postgresql://postgres:{password}@db.gyoxiqcnkaimovbuyaas.supabase.co:5432/postgres")

if __name__ == "__main__":
    update_password()