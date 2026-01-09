@echo off
echo Creando tunel para dispositivo Hikvision...
echo.
echo 1. Descargar ngrok desde: https://ngrok.com/download
echo 2. Registrarse y obtener authtoken
echo 3. Ejecutar: ngrok authtoken TU_TOKEN
echo 4. Ejecutar: ngrok http 172.10.1.62:80
echo.
echo La URL generada (ej: https://abc123.ngrok.io) usar como DEVICE_IP
pause