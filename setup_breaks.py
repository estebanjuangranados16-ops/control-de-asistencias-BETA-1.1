"""
Script para ejecutar la configuración del sistema de breaks
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_breaks_system():
    """Configurar sistema de breaks en la base de datos"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL no configurada")
            return False
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🔧 Configurando sistema de breaks...")
        
        # Leer y ejecutar el script SQL
        with open('setup_breaks_system.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar script por partes
        sql_commands = sql_script.split(';')
        
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    print(f"✅ Ejecutado: {command[:50]}...")
                except Exception as e:
                    print(f"⚠️ Error en comando: {e}")
        
        conn.commit()
        conn.close()
        
        print("✅ Sistema de breaks configurado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando sistema: {e}")
        return False

if __name__ == "__main__":
    setup_breaks_system()