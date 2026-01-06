@echo off
echo ========================================
echo SOLUCION RAPIDA - PROBLEMA CSS VISIBLE
echo ========================================
echo.
echo El problema que ves es que el CSS se muestra
echo como texto en lugar de aplicarse como estilos.
echo.
echo SOLUCION:
echo.
echo 1. LIMPIAR CACHE DEL NAVEGADOR:
echo    - Presiona Ctrl+F5 para refrescar
echo    - O Ctrl+Shift+R
echo    - O abre en ventana incognito
echo.
echo 2. REINICIAR EL SISTEMA:
echo    - Detener: Ctrl+C en la consola
echo    - Reiniciar: python system_optimized.py
echo.
echo 3. VERIFICAR PUERTO:
echo    - Asegurate de usar: http://localhost:5000
echo    - No http://localhost:3000
echo.
echo ========================================
echo.
echo REINICIANDO SISTEMA AUTOMATICAMENTE...
echo.
timeout /t 3 /nobreak >nul
echo Iniciando sistema con diseño PCSHEK...
python system_optimized.py