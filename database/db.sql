CREATE SCHEMA IF NOT EXISTS enfermeria_ms;

-- 1. Perfiles de Enfermería
CREATE TABLE enfermeria_ms.perfiles_enfermeria (
    id UUID PRIMARY KEY, -- Debe ser el mismo ID del usuario en el MS de Seguridad
    nombre_completo TEXT NOT NULL,
    cedula_profesional TEXT UNIQUE NOT NULL,
    especialidad TEXT,
    unidad_hospitalaria TEXT,
    fecha_actualizacion TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Gestión de Pacientes (Alineado a NOM-004-SSA3)
CREATE TABLE enfermeria_ms.pacientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre_completo TEXT NOT NULL,
    curp CHAR(18) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero TEXT CHECK (genero IN ('M', 'F', 'O')),
    fecha_ingreso TIMESTAMPTZ DEFAULT NOW(),
    numero_cama TEXT,
    estatus TEXT DEFAULT 'active' CHECK (estatus IN ('active', 'discharged')),
    fecha_creacion TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Bitácora de Registros Clínicos
CREATE TABLE enfermeria_ms.bitacora_registros (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID REFERENCES enfermeria_ms.pacientes(id) ON DELETE CASCADE NOT NULL,
    enfermero_id UUID REFERENCES enfermeria_ms.perfiles_enfermeria(id) NOT NULL,
    turno TEXT CHECK (turno IN ('morning', 'evening', 'night')) NOT NULL,
    
    -- Signos vitales en JSONB para flexibilidad en auditoría
    signos_vitales JSONB DEFAULT '{
        "temperatura": null, 
        "ritmo_cardiaco": null, 
        "presion_arterial": "", 
        "saturacion_oxigeno": null
    }'::jsonb,
    
    observaciones TEXT NOT NULL,
    medicamentos_administrados JSONB DEFAULT '[]'::jsonb, -- Lista de fármacos
    
    -- Control de Sincronización (Offline-First)
    cliente_timestamp TIMESTAMPTZ NOT NULL, -- Fecha/Hora real del suceso en el hospital
    es_sincronizado BOOLEAN DEFAULT FALSE,
    
    fecha_servidor TIMESTAMPTZ DEFAULT NOW(),
    fecha_actualizacion TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Auditoría Clínica (Cumplimiento NOM-024-SSA3)
CREATE TABLE enfermeria_ms.auditoria_clinica (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL,
    accion TEXT NOT NULL,
    tabla_afectada TEXT NOT NULL,
    registro_id UUID NOT NULL,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    fecha_accion TIMESTAMPTZ DEFAULT NOW()
);




--- SEGURIDAD
ALTER TABLE enfermeria_ms.pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE enfermeria_ms.bitacora_registros ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Lectura de pacientes activos" 
ON enfermeria_ms.pacientes FOR SELECT 
TO authenticated 
USING (estatus = 'active');

CREATE POLICY "Edición propia de enfermeros" 
ON enfermeria_ms.bitacora_registros FOR UPDATE 
TO authenticated 
USING (auth.uid() = enfermero_id);




-- =========================
-- ESQUEMA
-- =========================
COMMENT ON SCHEMA enfermeria_ms IS 'Microservicio de enfermería encargado de gestionar perfiles, pacientes, bitácoras clínicas y auditoría conforme a NOM-004 y NOM-024';

-- =========================
-- TABLA: perfiles_enfermeria
-- =========================
COMMENT ON TABLE enfermeria_ms.perfiles_enfermeria IS 'Información profesional de los enfermeros registrados en el sistema';

COMMENT ON COLUMN enfermeria_ms.perfiles_enfermeria.id IS 'UUID del enfermero. Debe coincidir con el ID del usuario en el microservicio de seguridad';
COMMENT ON COLUMN enfermeria_ms.perfiles_enfermeria.nombre_completo IS 'Nombre completo del profesional de enfermería';
COMMENT ON COLUMN enfermeria_ms.perfiles_enfermeria.cedula_profesional IS 'Número de cédula profesional del enfermero registrada ante la autoridad correspondiente';
COMMENT ON COLUMN enfermeria_ms.perfiles_enfermeria.especialidad IS 'Especialidad o área clínica del enfermero';
COMMENT ON COLUMN enfermeria_ms.perfiles_enfermeria.unidad_hospitalaria IS 'Hospital, clínica o unidad médica donde labora el enfermero';
COMMENT ON COLUMN enfermeria_ms.perfiles_enfermeria.fecha_actualizacion IS 'Fecha y hora de la última actualización del perfil';

-- =========================
-- TABLA: pacientes
-- =========================
COMMENT ON TABLE enfermeria_ms.pacientes IS 'Registro de pacientes hospitalizados gestionados por el área de enfermería';

COMMENT ON COLUMN enfermeria_ms.pacientes.id IS 'Identificador único del paciente generado mediante UUID';
COMMENT ON COLUMN enfermeria_ms.pacientes.nombre_completo IS 'Nombre completo del paciente';
COMMENT ON COLUMN enfermeria_ms.pacientes.curp IS 'Clave Única de Registro de Población del paciente';
COMMENT ON COLUMN enfermeria_ms.pacientes.fecha_nacimiento IS 'Fecha de nacimiento del paciente';
COMMENT ON COLUMN enfermeria_ms.pacientes.genero IS 'Género del paciente: M (Masculino), F (Femenino), O (Otro)';
COMMENT ON COLUMN enfermeria_ms.pacientes.fecha_ingreso IS 'Fecha y hora de ingreso del paciente al hospital';
COMMENT ON COLUMN enfermeria_ms.pacientes.numero_cama IS 'Número o identificador de la cama asignada al paciente';
COMMENT ON COLUMN enfermeria_ms.pacientes.estatus IS 'Estado actual del paciente: active (hospitalizado) o discharged (alta médica)';
COMMENT ON COLUMN enfermeria_ms.pacientes.fecha_creacion IS 'Fecha y hora en que el registro del paciente fue creado en el sistema';

-- =========================
-- TABLA: bitacora_registros
-- =========================
COMMENT ON TABLE enfermeria_ms.bitacora_registros IS 'Bitácora de registros clínicos realizados por enfermería durante cada turno';

COMMENT ON COLUMN enfermeria_ms.bitacora_registros.id IS 'Identificador único del registro clínico';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.paciente_id IS 'Referencia al paciente al que pertenece el registro';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.enfermero_id IS 'Referencia al enfermero que realizó el registro';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.turno IS 'Turno en el que se registró la información: morning, evening o night';

COMMENT ON COLUMN enfermeria_ms.bitacora_registros.signos_vitales IS 'Objeto JSON con signos vitales del paciente (temperatura, ritmo cardiaco, presión arterial y saturación de oxígeno)';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.observaciones IS 'Notas clínicas u observaciones realizadas por el personal de enfermería';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.medicamentos_administrados IS 'Lista JSON de medicamentos administrados al paciente durante el turno';

COMMENT ON COLUMN enfermeria_ms.bitacora_registros.cliente_timestamp IS 'Fecha y hora real en la que ocurrió el registro clínico en el hospital, usada para sincronización offline';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.es_sincronizado IS 'Indica si el registro ya fue sincronizado correctamente con el servidor';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.fecha_servidor IS 'Fecha y hora en que el servidor registró el evento';
COMMENT ON COLUMN enfermeria_ms.bitacora_registros.fecha_actualizacion IS 'Fecha y hora de la última modificación del registro';

-- =========================
-- TABLA: auditoria_clinica
-- =========================
COMMENT ON TABLE enfermeria_ms.auditoria_clinica IS 'Registro de auditoría de acciones realizadas en el sistema clínico para cumplimiento normativo';

COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.id IS 'Identificador único del registro de auditoría';
COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.usuario_id IS 'Usuario que realizó la acción dentro del sistema';
COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.accion IS 'Tipo de acción realizada (INSERT, UPDATE, DELETE u otras)';
COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.tabla_afectada IS 'Nombre de la tabla que fue modificada';
COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.registro_id IS 'Identificador del registro afectado por la acción';
COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.datos_anteriores IS 'Datos previos del registro antes de la modificación';
COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.datos_nuevos IS 'Datos del registro después de la modificación';
COMMENT ON COLUMN enfermeria_ms.auditoria_clinica.fecha_accion IS 'Fecha y hora en que se ejecutó la acción';