@echo off
echo ========================================
echo INICIANDO FRONTEND REACT
echo ========================================
echo.
echo Verificando si Node.js esta instalado...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js no esta instalado
    echo Descarga e instala Node.js desde: https://nodejs.org
    pause
    exit /b 1
)

echo Node.js encontrado
echo.
echo Cambiando al directorio frontend...
cd frontend

echo.
echo Verificando dependencias...
if not exist "node_modules" (
    echo Instalando dependencias...
    npm install
)

echo.
echo Iniciando servidor de desarrollo...
echo Frontend estara disponible en: http://localhost:3000
echo Backend debe estar en: http://localhost:5000
echo.
npm run dev