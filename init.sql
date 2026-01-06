-- Script de Inicialización PostgreSQL
-- Sistema de Asistencia Hikvision

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de empleados
CREATE TABLE IF NOT EXISTS employees (
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

-- Tabla de registros de asistencia
CREATE TABLE IF NOT EXISTS attendance_records (
    id SERIAL PRIMARY KEY,
    employee_id TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('entrada', 'salida')),
    timestamp TIMESTAMP NOT NULL,
    reader_no INTEGER DEFAULT 1,
    verify_method TEXT DEFAULT 'huella',
    status TEXT DEFAULT 'autorizado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE CASCADE
);

-- Tabla de horarios de trabajo
CREATE TABLE IF NOT EXISTS work_schedules (
    id SERIAL PRIMARY KEY,
    employee_id TEXT NOT NULL,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE CASCADE
);

-- Tabla de intentos bloqueados (anti-duplicados)
CREATE TABLE IF NOT EXISTS blocked_attempts (
    id SERIAL PRIMARY KEY,
    employee_id TEXT,
    event_type TEXT,
    reason TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de configuración del sistema
CREATE TABLE IF NOT EXISTS system_config (
    id SERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_attendance_employee_date ON attendance_records (employee_id, DATE(timestamp));
CREATE INDEX IF NOT EXISTS idx_attendance_timestamp ON attendance_records (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_employees_active ON employees (active) WHERE active = true;
CREATE INDEX IF NOT EXISTS idx_blocked_attempts_date ON blocked_attempts (DATE(created_at));

-- Insertar empleado administrador por defecto
INSERT INTO employees (employee_id, name, department, schedule, active) 
VALUES ('1', 'Administrador', 'Administración', 'estandar', true)
ON CONFLICT (employee_id) DO NOTHING;

-- Insertar configuración inicial
INSERT INTO system_config (key, value, description) VALUES
('anti_duplicate_same_event_window', '30', 'Segundos para bloquear mismo evento'),
('anti_duplicate_different_event_window', '300', 'Segundos mínimos entre entrada/salida'),
('max_daily_records', '8', 'Máximo registros por empleado por día'),
('valid_hours_start', '05:00', 'Hora inicio válida para registros'),
('valid_hours_end', '23:00', 'Hora fin válida para registros'),
('backup_enabled', 'true', 'Backup automático habilitado'),
('system_version', '2.0.0', 'Versión del sistema')
ON CONFLICT (key) DO NOTHING;

-- Función para limpiar registros antiguos (opcional)
CREATE OR REPLACE FUNCTION cleanup_old_records()
RETURNS void AS $$
BEGIN
    -- Eliminar intentos bloqueados mayores a 30 días
    DELETE FROM blocked_attempts 
    WHERE created_at < NOW() - INTERVAL '30 days';
    
    -- Log de limpieza
    RAISE NOTICE 'Limpieza de registros antiguos completada';
END;
$$ LANGUAGE plpgsql;

-- Crear vista para reportes rápidos
CREATE OR REPLACE VIEW daily_attendance_summary AS
SELECT 
    DATE(ar.timestamp) as date,
    e.name,
    e.employee_id,
    e.department,
    MIN(CASE WHEN ar.event_type = 'entrada' THEN ar.timestamp END) as first_entry,
    MAX(CASE WHEN ar.event_type = 'salida' THEN ar.timestamp END) as last_exit,
    COUNT(*) as total_records
FROM attendance_records ar
JOIN employees e ON ar.employee_id = e.employee_id
WHERE e.active = true
GROUP BY DATE(ar.timestamp), e.employee_id, e.name, e.department
ORDER BY date DESC, e.name;

-- Comentarios en tablas
COMMENT ON TABLE employees IS 'Información de empleados del sistema';
COMMENT ON TABLE attendance_records IS 'Registros de entrada/salida de empleados';
COMMENT ON TABLE work_schedules IS 'Horarios de trabajo por empleado';
COMMENT ON TABLE blocked_attempts IS 'Intentos de registro bloqueados por anti-duplicados';
COMMENT ON TABLE system_config IS 'Configuración del sistema';

-- Mensaje de finalización
DO $$
BEGIN
    RAISE NOTICE 'Base de datos inicializada correctamente para Sistema de Asistencia Hikvision v2.0';
END $$;