# Sistema de Control de Asistencia Hikvision

Sistema completo para monitorear y gestionar la asistencia de empleados usando dispositivos Hikvision con lector de huella dactilar y base de datos PostgreSQL (Supabase).

## 🚀 Características

- **Monitoreo en tiempo real** de eventos de huella dactilar
- **Base de datos PostgreSQL** (Supabase) con fallback a SQLite
- **Dashboard web** para visualización en tiempo real
- **Detección automática** de entrada/salida
- **Sistema de breaks y almuerzos** por departamento
- **Reportes avanzados** con exportación Excel/PDF
- **Gestión completa de empleados**
- **Horarios diferenciados** por departamento

## 📋 Estructura del Proyecto

```
control-de-asistencias/
├── system_optimized_v2.py     # Sistema principal
├── templates/                 # Plantillas HTML
│   ├── dashboard_pcshek.html
│   └── employees_simple.html
├── static/                    # Archivos estáticos
│   ├── images/
│   └── js/
├── requirements.txt           # Dependencias Python
├── .env.example              # Plantilla de configuración
└── README.md                 # Este archivo
```

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/control-de-asistencias.git
cd control-de-asistencias
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
# Copiar plantilla de configuración
cp .env.example .env

# Editar .env con tus datos reales
```

### 4. Configurar Supabase (Recomendado)

1. Crear proyecto en [Supabase](https://supabase.com)
2. Ir a **Settings → Database**
3. Cambiar a **Session pooler** en Connect
4. Copiar la connection string
5. Actualizar `DATABASE_URL` en `.env`

### 5. Ejecutar el sistema
```bash
python system_optimized_v2.py
```

## 📱 Uso del Sistema

### Dashboard Web
- **URL**: http://localhost:5000
- **Empleados**: http://localhost:5000/employees
- **Actualización automática** cada 30 segundos

### Funcionalidades Principales

#### 1. Monitoreo en Tiempo Real
- Detecta eventos de huella dactilar automáticamente
- Determina entrada/salida según último evento
- Maneja breaks y almuerzos por departamento

#### 2. Gestión de Empleados
- CRUD completo de empleados
- Departamentos: Reacondicionamiento, Logística, Administración, Operativos
- Estados activo/inactivo

#### 3. Sistema de Breaks
- **Administrativos**: Break 9-10am + Almuerzo 12-2pm
- **Operativos**: Break según turno asignado
- Seguimiento de duración y estado

#### 4. Reportes Avanzados
- Reportes diarios, semanales y mensuales
- Exportación a Excel y PDF
- Cálculo automático de horas trabajadas
- Detección de tardanzas

## 🗄️ Base de Datos

### Tablas Principales

#### `employees`
- Información básica de empleados
- Departamentos y horarios
- Estado activo/inactivo

#### `attendance_records`
- Registros de entrada/salida
- Eventos de breaks y almuerzos
- Timestamps y métodos de verificación

#### `daily_summaries`
- Resúmenes diarios por empleado
- Horas trabajadas y tardanzas
- Días laborables vs no laborables

#### `weekly_shift_assignments`
- Asignación de turnos para operativos
- Horarios rotativos por semana

## 🔧 Configuración del Dispositivo

### Credenciales por defecto:
```env
DEVICE_IP=172.10.1.62
DEVICE_USER=admin
DEVICE_PASS=PC2024*+
```

### Eventos detectados:
- **subEventType 38**: Acceso autorizado ✅
- **subEventType 39**: Acceso denegado ❌

## 📊 Horarios por Departamento

### Administrativos (Reacondicionamiento, Logística, Administración)
- **L-J**: 7:00-17:00
- **V**: 7:00-16:00
- **Break**: 9:00-10:00
- **Almuerzo**: 12:00-14:00

### Operativos
- **Turnos rotativos**: Mañana/Tarde/Noche
- **Break**: 20 minutos según turno
- **Sin almuerzo** (solo break)

## 🚨 Solución de Problemas

### Error de conexión al dispositivo:
1. Verificar IP y credenciales en `.env`
2. Comprobar que ISAPI esté habilitado
3. Verificar conectividad de red

### Error de base de datos:
1. Verificar `DATABASE_URL` en `.env`
2. Comprobar conectividad a Supabase
3. Usar SQLite como fallback

### Dashboard no carga:
1. Verificar que el puerto 5000 esté libre
2. Comprobar logs del sistema
3. Verificar dependencias instaladas

## 🔄 API Endpoints

- `GET /api/dashboard` - Datos del dashboard
- `GET /api/employees` - Lista de empleados
- `POST /api/employees` - Agregar empleado
- `GET /api/records?date=YYYY-MM-DD` - Registros por fecha
- `GET /api/reports/monthly-summary?month=YYYY-MM` - Reporte mensual

## 📈 Próximas Mejoras

- [ ] Notificaciones push en tiempo real
- [ ] App móvil
- [ ] Integración con sistemas de nómina
- [ ] Reconocimiento facial
- [ ] Alertas por email
- [ ] Dashboard de administración avanzado

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🏢 Desarrollado para PCSHEK

Sistema de control de asistencia empresarial con tecnología Hikvision.

---

**¿Necesitas ayuda?** Abre un [issue](https://github.com/TU_USUARIO/control-de-asistencias/issues) en GitHub.