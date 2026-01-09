# 🌐 Guía de Deployment - PythonAnywhere

## Paso 1: Crear Cuenta
1. Ir a: https://www.pythonanywhere.com
2. Crear cuenta gratuita (o pagar $5/mes para mejor rendimiento)
3. Confirmar email

## Paso 2: Subir Código
1. En PythonAnywhere Dashboard → "Files"
2. Crear carpeta: `control-de-asistencias`
3. Subir todos los archivos del proyecto
4. O usar Git: `git clone https://github.com/estebanjuangranados16-ops/control-de-asistencias-BETA-1.1.git`

## Paso 3: Instalar Dependencias
1. Ir a "Consoles" → "Bash"
2. Ejecutar:
```bash
cd control-de-asistencias
pip3.10 install --user -r requirements_production.txt
```

## Paso 4: Configurar Web App
1. Ir a "Web" → "Add a new web app"
2. Seleccionar "Manual configuration"
3. Python 3.10
4. En "Code":
   - Source code: `/home/tuusuario/control-de-asistencias`
   - Working directory: `/home/tuusuario/control-de-asistencias`
   - WSGI configuration file: `/var/www/tuusuario_pythonanywhere_com_wsgi.py`

## Paso 5: Configurar WSGI
1. Editar el archivo WSGI
2. Reemplazar contenido con el archivo `wsgi.py` del proyecto
3. Actualizar rutas con tu usuario

## Paso 6: Variables de Entorno
En el archivo WSGI, configurar:
```python
os.environ['DATABASE_URL'] = 'postgresql://postgres.gyoxiqcnkaimovbuyaas:Control2024Hikvision!@aws-1-us-east-1.pooler.supabase.com:5432/postgres'
os.environ['DEVICE_IP'] = 'TU_IP_PUBLICA_O_NGROK'
```

## Paso 7: Configurar Acceso al Dispositivo

### Opción A: IP Pública (Recomendado)
1. Configurar port forwarding en router
2. Puerto 80 del dispositivo → Puerto público
3. Usar IP pública en DEVICE_IP

### Opción B: ngrok (Temporal)
1. En tu PC local ejecutar: `ngrok http 172.10.1.62:80`
2. Copiar URL generada (ej: https://abc123.ngrok.io)
3. Usar esa URL como DEVICE_IP

## Paso 8: Activar
1. Click "Reload" en la pestaña Web
2. Tu app estará en: `https://tuusuario.pythonanywhere.com`

## 🔧 Troubleshooting

### Error de módulos:
```bash
pip3.10 install --user flask flask-socketio flask-cors psycopg2-binary python-dotenv
```

### Error de base de datos:
- Verificar que Supabase esté funcionando
- Comprobar URL de conexión

### Error de dispositivo:
- Verificar que ngrok esté activo
- O que port forwarding esté configurado

## 📱 Resultado Final
URL pública: `https://tuusuario.pythonanywhere.com`
Accesible desde cualquier dispositivo con internet