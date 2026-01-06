# Configuración para PythonAnywhere
# Archivo: wsgi.py

import sys
import os

# Agregar el directorio del proyecto al path
project_home = '/home/tuusuario/control-de-asistencias'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configurar variables de entorno
os.environ['DATABASE_URL'] = 'postgresql://...'  # Tu URL de Supabase
os.environ['DEVICE_IP'] = '172.10.1.62'
os.environ['DEVICE_USER'] = 'admin'
os.environ['DEVICE_PASS'] = 'PC2024*+'
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_SECRET_KEY'] = 'pcshek_secret_2024'

# Importar la aplicación
from system_optimized_v2 import app as application

if __name__ == "__main__":
    application.run()