# DOCUMENTACIÓN COMPLETA - SISTEMA DE CONTROL DE ASISTENCIA HIKVISION

## 📋 ÍNDICE

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes Principales](#componentes-principales)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Estructura de Base de Datos](#estructura-de-base-de-datos)
6. [API y Endpoints](#api-y-endpoints)
7. [Funcionalidades Avanzadas](#funcionalidades-avanzadas)
8. [Guía de Uso](#guía-de-uso)
9. [Solución de Problemas](#solución-de-problemas)
10. [Mantenimiento](#mantenimiento)

---

## 📖 DESCRIPCIÓN GENERAL

### Propósito
Sistema integral de control de asistencia que integra dispositivos Hikvision con lectores de huella dactilar para monitorear y gestionar la asistencia de empleados en tiempo real.

### Características Principales
- **Monitoreo en tiempo real** de eventos de huella dactilar
- **Dashboard web interactivo** con WebSocket para actualizaciones instantáneas
- **Base de datos robusta** (SQLite/PostgreSQL) para almacenar registros
- **Gestión completa de empleados** con sincronización al dispositivo
- **Sistema de breaks y almuerzos** automatizado por departamentos
- **Reportes avanzados** con exportación a Excel/PDF
- **Detección de tardanzas** con alertas automáticas
- **Horarios flexibles** por departamento y turnos rotativos
- **API REST completa** para integraciones externas

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Diagrama de Arquitectura
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dispositivo   │    │   Aplicación    │    │   Base de       │
│   Hikvision     │◄──►│   Python        │◄──►│   Datos         │
│   (ISAPI)       │    │   (Flask)       │    │   (SQLite/PG)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Dashboard     │
                       │   Web (HTML/JS) │
                       └─────────────────┘
```

### Tecnologías Utilizadas
- **Backend**: Python 3.8+, Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Comunicación**: HTTP/HTTPS, WebSocket, ISAPI
- **Exportación**: openpyxl (Excel), reportlab (PDF)
- **Autenticación**: HTTP Digest Auth

---

## 🔧 COMPONENTES PRINCIPALES

### 1. Scripts de Conexión
#### `hikvision_isapi.py`
- **Propósito**: Script básico para probar conexión y monitorear eventos
- **Funciones**:
  - Conexión ISAPI con autenticación Digest
  - Monitoreo de stream de eventos en tiempo real
  - Decodificación de métodos de verificación
  - Manejo de reconexión automática

#### `attendance_system.py`
- **Propósito**: Sistema completo con base de datos
- **Funciones**:
  - Gestión de empleados
  - Registro automático de asistencia
  - Determinación inteligente de entrada/salida
  - Reportes diarios

### 2. Sistemas Avanzados
#### `system_optimized_v2.py`
- **Propósito**: Sistema optimizado con funcionalidades avanzadas
- **Características**:
  - Soporte PostgreSQL y SQLite
  - Sistema de breaks y almuerzos automatizado
  - Detección de tardanzas con alertas
  - Exportación a Excel/PDF
  - Horarios por departamento
  - Turnos rotativos para operativos
  - Cache de empleados para optimización
  - WebSocket para tiempo real

#### `unified_system.py`
- **Propósito**: Sistema unificado con sincronización de dispositivos
- **Funciones**:
  - Sincronización bidireccional con dispositivo
  - Gestión avanzada de empleados
  - Monitoreo robusto con reconexión
  - Dashboard unificado

### 3. Dashboard Web
#### `web_dashboard.py`
- **Propósito**: Interfaz web básica
- **Características**:
  - Resumen diario
  - Estado de empleados (dentro/fuera)
  - Registros recientes
  - API REST básica

### 4. Templates HTML
- `dashboard_pcshek.html`: Dashboard principal con branding PCSHEK
- `employees_pcshek.html`: Gestión de empleados
- `unified_dashboard.html`: Dashboard unificado
- `dashboard_modern.html`: Diseño moderno
- `reports.html`: Página de reportes
- `schedules.html`: Gestión de horarios

---

## 🛠️ INSTALACIÓN Y CONFIGURACIÓN

### Requisitos del Sistema
- Python 3.8 o superior
- Dispositivo Hikvision con ISAPI habilitado
- Red local con conectividad al dispositivo

### Instalación Básica
```bash
# Clonar repositorio
git clone <repository-url>
cd Control-de-asistencias-master

# Instalar dependencias básicas
pip install -r requirements_full.txt

# Para funcionalidades completas
pip install -r requirements_unified.txt
```

### Configuración de Variables de Entorno
Crear archivo `.env`:
```env
# Configuración del dispositivo
DEVICE_IP=172.10.0.66
DEVICE_USER=admin
DEVICE_PASS=PC2024*+

# Base de datos (opcional para PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Flask
FLASK_SECRET_KEY=hikvision_attendance_2024
FLASK_ENV=development
```

### Configuración del Dispositivo Hikvision
1. **Acceder a la interfaz web** del dispositivo
2. **Habilitar ISAPI** en Configuración → Red → Servicios Avanzados
3. **Configurar usuarios** con permisos de acceso
4. **Registrar huellas** de empleados en el dispositivo
5. **Verificar conectividad** desde la aplicación

---

## 🗄️ ESTRUCTURA DE BASE DE DATOS

### Tabla `employees`
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    department TEXT DEFAULT 'General',
    schedule TEXT DEFAULT 'estandar',
    phone TEXT DEFAULT '',
    email TEXT DEFAULT '',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    synced_to_device BOOLEAN DEFAULT false
);
```

### Tabla `attendance_records`
```sql
CREATE TABLE attendance_records (
    id SERIAL PRIMARY KEY,
    employee_id TEXT NOT NULL,
    event_type TEXT NOT NULL, -- 'entrada', 'salida', 'break_salida', 'break_entrada', 'almuerzo_salida', 'almuerzo_entrada'
    timestamp TIMESTAMP NOT NULL,
    reader_no INTEGER DEFAULT 1,
    verify_method TEXT DEFAULT 'huella',
    status TEXT DEFAULT 'autorizado',
    break_type VARCHAR(50),
    is_break_record BOOLEAN DEFAULT FALSE,
    break_duration_minutes INTEGER
);
```

### Tabla `daily_summaries`
```sql
CREATE TABLE daily_summaries (
    id SERIAL PRIMARY KEY,
    employee_id TEXT NOT NULL,
    date DATE NOT NULL,
    first_entry TIME,
    last_exit TIME,
    total_hours DECIMAL(4,2) DEFAULT 0,
    worked_day BOOLEAN DEFAULT false,
    is_holiday BOOLEAN DEFAULT false,
    is_weekend BOOLEAN DEFAULT false,
    late_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, date)
);
```

### Tabla `weekly_shift_assignments`
```sql
CREATE TABLE weekly_shift_assignments (
    id SERIAL PRIMARY KEY,
    employee_id TEXT NOT NULL,
    week_start DATE NOT NULL,
    week_end DATE NOT NULL,
    shift_type TEXT NOT NULL, -- 'mañana', 'tarde', 'noche'
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, week_start)
);
```

### Tabla `department_schedules`
```sql
CREATE TABLE department_schedules (
    id SERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    shift_type VARCHAR(50),
    work_start TIME NOT NULL,
    work_end TIME NOT NULL,
    break_start TIME NOT NULL,
    break_end TIME NOT NULL,
    has_lunch BOOLEAN DEFAULT FALSE,
    lunch_options TEXT[],
    friday_end TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🌐 API Y ENDPOINTS

### Endpoints Principales

#### Dashboard
- `GET /` - Dashboard principal
- `GET /api/dashboard` - Datos del dashboard en JSON
- `GET /api/records?date=YYYY-MM-DD` - Registros por fecha

#### Empleados
- `GET /api/employees` - Lista de empleados
- `POST /api/employees` - Agregar empleado
- `PUT /api/employees/{id}` - Actualizar empleado
- `DELETE /api/employees/{id}` - Eliminar empleado
- `POST /api/employees/{id}/toggle` - Activar/desactivar empleado

#### Monitoreo
- `POST /api/start_monitoring` - Iniciar monitoreo
- `POST /api/stop_monitoring` - Detener monitoreo
- `POST /api/test_connection` - Probar conexión

#### Reportes
- `GET /api/reports/daily?date=YYYY-MM-DD` - Reporte diario
- `GET /api/reports/weekly?week=YYYY-WNN` - Reporte semanal
- `GET /api/reports/attendance` - Reporte de asistencia personalizado
- `GET /api/export/excel` - Exportar a Excel
- `GET /api/export/pdf` - Exportar a PDF

#### Breaks y Almuerzos
- `GET /api/breaks/status` - Estado actual de breaks
- `GET /api/alerts/late` - Alertas de tardanzas

#### Horarios
- `GET /api/schedules` - Horarios de empleados
- `POST /api/schedules/bulk` - Asignación masiva de turnos
- `GET /api/schedules/weekly-report` - Reporte semanal de turnos
- `GET /api/schedules/export-pdf` - Exportar horarios a PDF

### WebSocket Events
- `attendance_record` - Nuevo registro de asistencia
- `employee_added` - Empleado agregado
- `late_arrival_alert` - Alerta de tardanza
- `connection_lost` - Conexión perdida
- `connection_restored` - Conexión restaurada

---

## ⚡ FUNCIONALIDADES AVANZADAS

### 1. Sistema de Breaks Automatizado
#### Departamentos Administrativos
- **Break matutino**: 9:00-10:00 (20 minutos)
- **Almuerzo**: 12:00-14:00 (60 minutos, horarios rotativos)
- **Detección automática** basada en horario y último evento

#### Departamentos Operativos
- **Turnos rotativos**: Mañana (6:00-14:00), Tarde (14:00-22:00), Noche (22:00-6:00)
- **Breaks por turno**: 20 minutos en horario específico
- **Asignación semanal** de turnos

### 2. Detección de Tardanzas
- **Verificación automática** en primera entrada del día
- **Cálculo de minutos** de retraso
- **Alertas en tiempo real** vía WebSocket
- **Clasificación por severidad**: Leve (<15 min), Moderada (15-30 min), Severa (>30 min)

### 3. Reportes Avanzados
#### Reporte de Asistencia
- **Análisis de puntualidad** con cálculo de tardanzas
- **Horas trabajadas** con descuento automático de breaks
- **Estado diario**: Presente, Ausente, Sin entrada, Sin salida
- **Exportación** a Excel y PDF con formato profesional

#### Reporte Mensual para Nómina
- **Resumen mensual** por empleado
- **Total de días trabajados** y horas
- **Días de fin de semana** y feriados
- **Integración** con sistemas de nómina

### 4. Gestión de Horarios
#### Horarios por Departamento
```javascript
const schedules = {
    'Reacondicionamiento': {
        'lunes-jueves': '07:00-17:00',
        'viernes': '07:00-16:00',
        'break': '09:00-10:00',
        'almuerzo': ['12:00-13:00', '13:00-14:00']
    },
    'Operativos': {
        'turnos': ['mañana', 'tarde', 'noche'],
        'rotativo': true
    }
};
```

#### Asignación de Turnos
- **Asignación masiva** de turnos semanales
- **Validación de conflictos** automática
- **Reporte de turnos** con exportación PDF

---

## 📱 GUÍA DE USO

### Inicio del Sistema
```bash
# Sistema básico
python hikvision_isapi.py

# Sistema completo
python attendance_system.py

# Sistema optimizado (recomendado)
python system_optimized_v2.py

# Sistema unificado
python unified_system.py
```

### Dashboard Web
1. **Acceder** a http://localhost:5000
2. **Monitorear** registros en tiempo real
3. **Gestionar empleados** desde la interfaz
4. **Generar reportes** personalizados
5. **Exportar datos** en múltiples formatos

### Gestión de Empleados
#### Agregar Empleado
```javascript
// Vía API
POST /api/employees
{
    "employee_id": "123",
    "name": "Juan Pérez",
    "department": "Reacondicionamiento",
    "phone": "555-1234",
    "email": "juan@empresa.com"
}
```

#### Sincronización con Dispositivo
- **Automática**: Al agregar empleado
- **Manual**: Botón "Sincronizar" en interfaz
- **Masiva**: Importar desde dispositivo

### Monitoreo en Tiempo Real
1. **Iniciar monitoreo** desde dashboard
2. **Observar eventos** en tiempo real
3. **Recibir alertas** de tardanzas
4. **Monitorear breaks** y almuerzos

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Problemas de Conexión
#### Error: "Dispositivo no disponible"
**Causas posibles:**
- IP incorrecta del dispositivo
- Credenciales inválidas
- ISAPI deshabilitado
- Problemas de red

**Soluciones:**
```bash
# Verificar conectividad
ping 172.10.0.66

# Probar conexión HTTP
curl -u admin:password http://172.10.0.66/ISAPI/System/deviceInfo

# Verificar configuración
python diagnose_connection.py
```

#### Error: "Stream desconectado"
**Causas:**
- Timeout de red
- Dispositivo reiniciado
- Límite de conexiones

**Soluciones:**
- Verificar estabilidad de red
- Reiniciar aplicación
- Revisar logs del dispositivo

### Problemas de Base de Datos
#### Error: "Database locked"
**Solución:**
```bash
# Para SQLite
python fix_database.py

# Verificar integridad
sqlite3 attendance.db "PRAGMA integrity_check;"
```

#### Migración a PostgreSQL
```bash
# Configurar variables de entorno
export DATABASE_URL="postgresql://user:pass@host:port/dbname"

# Ejecutar migración
python migrate_database.py
```

### Problemas de Rendimiento
#### Dashboard lento
**Optimizaciones:**
- Habilitar cache de empleados
- Limitar registros mostrados
- Usar índices de base de datos

#### Memoria alta
**Soluciones:**
- Limpiar logs antiguos
- Optimizar consultas SQL
- Reiniciar aplicación periódicamente

---

## 🔧 MANTENIMIENTO

### Tareas Diarias
- **Verificar conexión** con dispositivo
- **Revisar logs** de errores
- **Monitorear registros** de asistencia
- **Validar sincronización** de empleados

### Tareas Semanales
- **Generar reportes** semanales
- **Asignar turnos** para operativos
- **Revisar tardanzas** acumuladas
- **Backup de base de datos**

### Tareas Mensuales
- **Reporte mensual** para nómina
- **Limpieza de logs** antiguos
- **Actualización de horarios** si es necesario
- **Revisión de rendimiento**

### Backup y Restauración
```bash
# Backup SQLite
cp attendance.db backup/attendance_$(date +%Y%m%d).db

# Backup PostgreSQL
pg_dump $DATABASE_URL > backup/attendance_$(date +%Y%m%d).sql

# Restauración
sqlite3 attendance.db < backup/attendance_20241201.sql
```

### Logs y Monitoreo
```bash
# Ver logs en tiempo real
tail -f logs/attendance.log

# Buscar errores
grep "ERROR" logs/attendance.log

# Estadísticas de uso
python status_today.py
```

### Actualizaciones
1. **Backup** de base de datos
2. **Detener** aplicación
3. **Actualizar** código
4. **Migrar** base de datos si es necesario
5. **Reiniciar** aplicación
6. **Verificar** funcionamiento

---

## 📊 MÉTRICAS Y ESTADÍSTICAS

### KPIs del Sistema
- **Uptime**: Tiempo de funcionamiento
- **Registros procesados**: Por día/semana/mes
- **Empleados activos**: Total y por departamento
- **Tardanzas**: Frecuencia y duración promedio
- **Breaks completados**: Porcentaje de cumplimiento

### Reportes Disponibles
1. **Reporte Diario**: Asistencia del día
2. **Reporte Semanal**: Resumen semanal
3. **Reporte Mensual**: Para nómina
4. **Reporte de Tardanzas**: Análisis de puntualidad
5. **Reporte de Breaks**: Cumplimiento de descansos
6. **Reporte de Turnos**: Asignaciones semanales

---

## 🔐 SEGURIDAD

### Autenticación
- **HTTP Digest Auth** para dispositivo Hikvision
- **Session management** para dashboard web
- **API keys** para integraciones externas

### Datos Sensibles
- **Encriptación** de credenciales en .env
- **Logs sanitizados** sin información personal
- **Backup seguro** de base de datos

### Acceso
- **Control de acceso** por roles
- **Logs de auditoría** de cambios
- **Validación** de entrada de datos

---

## 🚀 DESPLIEGUE EN PRODUCCIÓN

### Configuración de Producción
```bash
# Variables de entorno
export FLASK_ENV=production
export DATABASE_URL=postgresql://...

# Servidor WSGI
gunicorn --bind 0.0.0.0:5000 wsgi:app

# Con Docker
docker-compose up -d
```

### Monitoreo en Producción
- **Health checks** automáticos
- **Alertas** por email/SMS
- **Métricas** de rendimiento
- **Logs centralizados**

### Escalabilidad
- **Load balancer** para múltiples instancias
- **Base de datos** replicada
- **Cache** distribuido (Redis)
- **CDN** para assets estáticos

---

## 📞 SOPORTE Y CONTACTO

### Documentación Adicional
- **README.md**: Guía de inicio rápido
- **BREAKS_SYSTEM_DOCUMENTATION.md**: Sistema de breaks
- **PYTHONANYWHERE_DEPLOY.md**: Despliegue en PythonAnywhere

### Archivos de Configuración
- **requirements_*.txt**: Dependencias por entorno
- **docker-compose.yml**: Configuración Docker
- **railway.json**: Configuración Railway
- **.env.example**: Plantilla de variables de entorno

### Scripts de Utilidad
- **diagnose_connection.py**: Diagnóstico de conexión
- **fix_database.py**: Reparación de base de datos
- **migrate_database.py**: Migración de datos
- **status_today.py**: Estado actual del sistema

---

**Desarrollado para PCSHEK - Control de Asistencia Empresarial** 🏢

*Última actualización: Enero 2025*