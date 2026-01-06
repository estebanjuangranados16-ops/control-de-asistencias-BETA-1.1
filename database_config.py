"""
Configuración de base de datos para el sistema de asistencia
Soporta SQLite (desarrollo) y PostgreSQL (producción)
"""
import os
from urllib.parse import urlparse

class DatabaseConfig:
    def __init__(self):
        # Detectar si estamos en producción o desarrollo
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///attendance.db')
        self.is_postgres = self.database_url.startswith('postgresql')
        
        if self.is_postgres:
            self.setup_postgres()
        else:
            self.setup_sqlite()
    
    def setup_postgres(self):
        """Configuración para PostgreSQL"""
        parsed = urlparse(self.database_url)
        
        self.config = {
            'type': 'postgresql',
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path[1:],  # Remove leading slash
            'username': parsed.username,
            'password': parsed.password,
            'connection_string': self.database_url
        }
        
        # Importar driver PostgreSQL
        try:
            import psycopg2
            self.driver = psycopg2
        except ImportError:
            print("❌ psycopg2 no instalado. Ejecutar: pip install psycopg2-binary")
            raise
    
    def setup_sqlite(self):
        """Configuración para SQLite"""
        db_path = self.database_url.replace('sqlite:///', '')
        
        self.config = {
            'type': 'sqlite',
            'path': db_path,
            'connection_string': db_path
        }
        
        import sqlite3
        self.driver = sqlite3
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        if self.is_postgres:
            return self.driver.connect(self.database_url)
        else:
            return self.driver.connect(self.config['connection_string'])
    
    def get_connection_string(self):
        """Obtener string de conexión"""
        return self.config['connection_string']

# Instancia global
db_config = DatabaseConfig()