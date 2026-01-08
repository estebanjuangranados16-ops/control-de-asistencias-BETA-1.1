-- Sistema de Breaks y Horarios PCSHEK
-- Configuración de horarios por departamento y turno

-- Tabla para tipos de marcaje (breaks, almuerzo, etc.)
CREATE TABLE IF NOT EXISTS break_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    duration_minutes INTEGER NOT NULL,
    mandatory BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de configuración de horarios por departamento
CREATE TABLE IF NOT EXISTS department_schedules (
    id SERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    shift_type VARCHAR(50), -- NULL para admin, 'mañana'/'tarde'/'noche' para operativos
    work_start TIME NOT NULL,
    work_end TIME NOT NULL,
    break_start TIME NOT NULL,
    break_end TIME NOT NULL,
    has_lunch BOOLEAN DEFAULT FALSE,
    lunch_options TEXT[],
    friday_end TIME, -- Horario especial viernes para administrativos
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Modificar tabla attendance_records para incluir información de breaks
ALTER TABLE attendance_records 
ADD COLUMN IF NOT EXISTS break_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS is_break_record BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS break_duration_minutes INTEGER;

-- Insertar tipos de breaks
INSERT INTO break_types (name, display_name, duration_minutes, mandatory) VALUES
('admin_break', 'Break Administrativo', 20, TRUE),
('operativo_break', 'Break Operativo', 20, TRUE),
('almuerzo_12', 'Almuerzo 12:00-13:00', 60, TRUE),
('almuerzo_13', 'Almuerzo 13:00-14:00', 60, TRUE)
ON CONFLICT DO NOTHING;

-- Insertar configuraciones de horarios
INSERT INTO department_schedules (department, shift_type, work_start, work_end, break_start, break_end, has_lunch, lunch_options, friday_end) VALUES
-- Administrativos
('Reacondicionamiento', NULL, '07:00', '17:00', '09:00', '10:00', TRUE, ARRAY['12:00-13:00', '13:00-14:00'], '16:00'),
('Logística', NULL, '07:00', '17:00', '09:00', '10:00', TRUE, ARRAY['12:00-13:00', '13:00-14:00'], '16:00'),
('Administración', NULL, '07:00', '17:00', '09:00', '10:00', TRUE, ARRAY['12:00-13:00', '13:00-14:00'], '16:00'),

-- Operativos por turno
('Operativos', 'mañana', '06:00', '14:00', '09:00', '10:00', FALSE, NULL, NULL),
('Operativos', 'tarde', '14:00', '22:00', '17:00', '18:00', FALSE, NULL, NULL),
('Operativos', 'noche', '22:00', '06:00', '01:00', '02:00', FALSE, NULL, NULL)
ON CONFLICT DO NOTHING;

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_attendance_break_type ON attendance_records(break_type);
CREATE INDEX IF NOT EXISTS idx_attendance_is_break ON attendance_records(is_break_record);
CREATE INDEX IF NOT EXISTS idx_department_schedules_dept ON department_schedules(department);
CREATE INDEX IF NOT EXISTS idx_department_schedules_shift ON department_schedules(shift_type);