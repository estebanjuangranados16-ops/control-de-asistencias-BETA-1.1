@echo off
echo ========================================
echo    CONFIGURACION TUNEL HIKVISION
echo ========================================
echo.
echo Este script configura el acceso remoto al dispositivo
echo.
echo PASOS:
echo 1. Descargar ngrok: https://ngrok.com/download
echo 2. Crear cuenta gratuita en ngrok.com
echo 3. Obtener authtoken desde dashboard
echo 4. Ejecutar: ngrok config add-authtoken TU_TOKEN
echo 5. Ejecutar: ngrok http 172.10.1.62:80
echo.
echo La URL generada (ej: https://abc123.ngrok-free.app)
echo debe usarse como DEVICE_IP en el hosting
echo.
echo IMPORTANTE: Mantener esta ventana abierta
echo mientras el sistema esté en producción
echo.
pause
echo.
echo Iniciando tunel...
ngrok http 172.10.1.62:80