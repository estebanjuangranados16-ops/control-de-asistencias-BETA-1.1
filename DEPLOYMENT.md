# 🚀 Guía de Deployment - Sistema PCSHEK

## Opción 1: Railway (Recomendado)

### Pasos:
1. **Crear cuenta en Railway**: https://railway.app
2. **Conectar GitHub**: Autorizar acceso a tu repositorio
3. **Crear nuevo proyecto**: "New Project" → "Deploy from GitHub repo"
4. **Seleccionar repositorio**: Control-de-asistencias-master
5. **Configurar variables de entorno**:
   ```
   DATABASE_URL=postgresql://usuario:password@host:5432/database
   DEVICE_IP=172.10.1.62
   DEVICE_USER=admin
   DEVICE_PASS=PC2024*+
   FLASK_ENV=production
   FLASK_SECRET_KEY=tu_clave_secreta_aqui
   ```
6. **Deploy automático**: Railway detectará el Procfile y desplegará

### Configurar PostgreSQL en Railway:
1. En tu proyecto → "New" → "Database" → "PostgreSQL"
2. Copiar la DATABASE_URL generada
3. Pegarla en las variables de entorno

## Opción 2: Render

### Pasos:
1. **Crear cuenta en Render**: https://render.com
2. **Nuevo Web Service**: "New" → "Web Service"
3. **Conectar repositorio**: Autorizar GitHub
4. **Configuración**:
   - Build Command: `pip install -r requirements_production.txt`
   - Start Command: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT system_optimized_v2:app`
5. **Variables de entorno**: Igual que Railway
6. **PostgreSQL**: Crear base de datos separada en Render

## Opción 3: Manual con VPS

### Requisitos:
- Servidor Ubuntu/CentOS
- Dominio propio
- Certificado SSL

### Comandos:
```bash
# Instalar dependencias
sudo apt update
sudo apt install python3 python3-pip nginx

# Clonar proyecto
git clone tu-repositorio
cd Control-de-asistencias-master

# Instalar requirements
pip3 install -r requirements_production.txt

# Configurar Nginx
sudo nano /etc/nginx/sites-available/pcshek

# Configurar SSL con Let's Encrypt
sudo certbot --nginx -d tu-dominio.com
```

## 🔧 Variables de Entorno Necesarias

```env
DATABASE_URL=postgresql://...
DEVICE_IP=172.10.1.62
DEVICE_USER=admin
DEVICE_PASS=PC2024*+
FLASK_ENV=production
FLASK_SECRET_KEY=clave_super_secreta
PORT=5000
```

## 📱 Acceso Final

Una vez desplegado, el sistema estará disponible en:
- **Railway**: https://tu-proyecto.railway.app
- **Render**: https://tu-proyecto.onrender.com
- **VPS**: https://tu-dominio.com

## ⚡ Características del Deploy

✅ **HTTPS automático**
✅ **Acceso desde cualquier dispositivo**
✅ **Base de datos PostgreSQL en la nube**
✅ **Escalabilidad automática**
✅ **Monitoreo 24/7**
✅ **Backups automáticos**

## 🛠️ Troubleshooting

### Error de conexión a dispositivo:
- El dispositivo Hikvision debe tener IP pública o VPN
- Configurar port forwarding en router
- Usar servicio como ngrok para túnel

### Error de base de datos:
- Verificar DATABASE_URL
- Comprobar que PostgreSQL esté activo
- Revisar logs de la aplicación

## 📞 Soporte

Para problemas de deployment, revisar logs en:
- Railway: Pestaña "Deployments"
- Render: Pestaña "Logs"
- VPS: `journalctl -u tu-servicio`