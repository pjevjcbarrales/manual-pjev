-- ==============================================================================
-- SISTEMA INTEGRAL DE ADMINISTRACIÓN Y FINANZAS (SIAF-PJEV)
-- SUBSISTEMA TRANSVERSAL DE GESTIÓN DOCUMENTAL Y ARCHIVOS DIGITALES
-- ==============================================================================
-- Fundamentación:
--   1. Ley General de Archivos (LGA - DOF 15-06-2018)
--   2. Ley de Archivos del Estado de Veracruz de Ignacio de la Llave
--   3. Norma Oficial Mexicana NOM-151-SCFI-2016
--   4. Lineamientos Técnicos del Archivo General de la Nación (AGN)
--   5. Ley General de Contabilidad Gubernamental (LGCG / CONAC)
--   6. Código Fiscal de la Federación (Art. 30 - Conservación de Contabilidad)
--   7. LGPDPPSO y Lineamientos de Transparencia del SNT / IVAI
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS "archivos";

COMMENT ON SCHEMA "archivos" IS 'Esquema transversal de gestión documental, archivo de trámite digital y preservación institucional del PJEV conforme a la LGA y NOM-151-SCFI-2016.';

-- ------------------------------------------------------------------------------
-- 1. CATÁLOGOS DE CONTROL ARCHIVÍSTICO INSTITUCIONAL (LGA ARTS. 13 Y 14)
-- ------------------------------------------------------------------------------

-- Cuadro General de Clasificación Archivística (CGCA)
CREATE TABLE IF NOT EXISTS "archivos"."cgca_catalogo" (
    "cgca_id" SERIAL PRIMARY KEY,
    "cgca_codigo" VARCHAR(50) NOT NULL UNIQUE,       -- Ej: 'PJEV-DGA-RF-01.01'
    "fondo" VARCHAR(100) NOT NULL DEFAULT 'PODER JUDICIAL DEL ESTADO DE VERACRUZ',
    "subfondo" VARCHAR(100) NULL,
    "seccion" VARCHAR(100) NOT NULL,                 -- Ej: 'RECURSOS FINANCIEROS', 'RECURSOS MATERIALES'
    "serie" VARCHAR(150) NOT NULL,                   -- Ej: 'POLIZAS CONTABLES Y PRESUPUESTALES'
    "subserie" VARCHAR(150) NULL,                    -- Ej: 'POLIZAS DE EGRESOS'
    "descripcion" TEXT NULL,
    "estatus_registro" SMALLINT NOT NULL DEFAULT 1,
    "usuario_c" VARCHAR(50) NOT NULL,
    "fecha_c" TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    "usuario_m" VARCHAR(50) NULL,
    "fecha_m" TIMESTAMPTZ NULL
);

-- Catálogo de Disposición Documental (CADIDO)
CREATE TABLE IF NOT EXISTS "archivos"."cadido_catalogo" (
    "cadido_id" SERIAL PRIMARY KEY,
    "cgca_codigo" VARCHAR(50) NOT NULL REFERENCES "archivos"."cgca_catalogo"("cgca_codigo") ON UPDATE CASCADE,
    "valor_administrativo" BOOLEAN NOT NULL DEFAULT FALSE,
    "valor_legal" BOOLEAN NOT NULL DEFAULT FALSE,
    "valor_fiscal_contable" BOOLEAN NOT NULL DEFAULT TRUE,
    "valor_tecnico" BOOLEAN NOT NULL DEFAULT FALSE,
    "vigencia_tramite_anios" INT NOT NULL DEFAULT 1,        -- Años en Archivo de Trámite
    "vigencia_concentracion_anios" INT NOT NULL DEFAULT 5,  -- Años en Archivo de Concentración
    "destino_final" VARCHAR(25) NOT NULL DEFAULT 'BAJA_DOCUMENTAL', -- 'BAJA_DOCUMENTAL' o 'TRANSFERENCIA_HISTORICA'
    "fundamento_legal" TEXT NOT NULL,                      -- Ej: 'CFF Art. 30, LGCG Art. 44, LGA Art. 14'
    "estatus_registro" SMALLINT NOT NULL DEFAULT 1,
    "usuario_c" VARCHAR(50) NOT NULL,
    "fecha_c" TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    "usuario_m" VARCHAR(50) NULL,
    "fecha_m" TIMESTAMPTZ NULL
);

-- ------------------------------------------------------------------------------
-- 2. TABLA MAESTRA DE DOCUMENTOS (LGA ART. 45 Y NOM-151-SCFI-2016)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "archivos"."documento" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "nombre_original" VARCHAR(255) NOT NULL,
    "nombre_almacenamiento" VARCHAR(500) NOT NULL UNIQUE,   -- 'storage/siaf/modulo/2026/09/uuid.pdf'
    "extension" VARCHAR(10) NOT NULL,                       -- 'pdf', 'xml', 'xlsx', 'png'
    "mime_type" VARCHAR(100) NOT NULL,                      -- 'application/pdf', 'text/xml'
    "tamanio_bytes" BIGINT NOT NULL,
    "hash_sha256" CHAR(64) NOT NULL,                       -- Resumen criptográfico obligatorio
    "ruta_storage" TEXT NOT NULL,                          -- URI/Ruta en Storage Driver
    "descripcion" TEXT NULL,

    -- Control Archivístico Institucional (LGA Arts. 11, 13, 14, 46)
    "cgca_codigo" VARCHAR(50) NULL REFERENCES "archivos"."cgca_catalogo"("cgca_codigo") ON UPDATE CASCADE,
    "valor_documental" VARCHAR(25) NOT NULL DEFAULT 'FISCAL_CONTABLE',
    "vigencia_tramite_anios" INT NOT NULL DEFAULT 1,
    "vigencia_concentracion_anios" INT NOT NULL DEFAULT 5,
    "fecha_cierre_tramite" DATE NULL,
    "destino_final" VARCHAR(25) NOT NULL DEFAULT 'BAJA_DOCUMENTAL',
    "estado_archivistico" VARCHAR(20) NOT NULL DEFAULT 'TRAMITE', -- 'TRAMITE', 'CONCENTRACION', 'HISTORICO', 'BAJA'

    -- Seguridad, Confidencialidad y Transparencia (LGTAIP / IVAI)
    "clasificacion_acceso" VARCHAR(20) NOT NULL DEFAULT 'CONFIDENCIAL', -- 'PUBLICO', 'RESERVADO', 'CONFIDENCIAL'
    "acuerdo_reserva_id" VARCHAR(100) NULL,                -- Folio del Acuerdo de Reserva del Comité de Transparencia
    "posee_version_publica" BOOLEAN NOT NULL DEFAULT FALSE, -- Si existe versión con datos testados

    -- Certificación NOM-151 y Firma Electrónica
    "es_digitalizado" BOOLEAN NOT NULL DEFAULT FALSE,        -- Si proviene de escaneo papel
    "folio_constancia_nom151" VARCHAR(150) NULL,           -- Folio emitido por PSC acreditado
    "posee_firma_electronica" BOOLEAN NOT NULL DEFAULT FALSE,

    -- Control de Ciclo de Vida y Transacciones Temporales
    "es_temporal" BOOLEAN NOT NULL DEFAULT FALSE,           -- TRUE mientras el formulario padre no consolida
    "ticket_temporal" UUID NULL,                           -- Token de sesión de alta

    -- Auditoría Estándar SIAF-PJEV
    "estatus_registro" SMALLINT NOT NULL DEFAULT 1,         -- 1 = Activo, 0 = Baja lógica
    "usuario_c" VARCHAR(50) NOT NULL,
    "fecha_c" TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    "usuario_m" VARCHAR(50) NULL,
    "fecha_m" TIMESTAMPTZ NULL
);

-- Índices de alto rendimiento para búsqueda e integridad
CREATE INDEX IF NOT EXISTS "idx_doc_hash_sha256" ON "archivos"."documento"("hash_sha256");
CREATE INDEX IF NOT EXISTS "idx_doc_estado_archivistico" ON "archivos"."documento"("estado_archivistico");
CREATE INDEX IF NOT EXISTS "idx_doc_cgca_codigo" ON "archivos"."documento"("cgca_codigo");
CREATE INDEX IF NOT EXISTS "idx_doc_temporales" ON "archivos"."documento"("es_temporal", "fecha_c") WHERE "es_temporal" = TRUE;

-- ------------------------------------------------------------------------------
-- 3. ASOCIACIÓN POLIMÓRFICA DE DOCUMENTOS A ENTIDADES SIAF
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "archivos"."documento_relacion" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "documento_id" UUID NOT NULL REFERENCES "archivos"."documento"("id") ON DELETE RESTRICT,
    "modulo_siaf" VARCHAR(30) NOT NULL,                    -- 'presupuesto', 'contabilidad', 'cxp', 'ingresos', 'rm'
    "entidad_origen" VARCHAR(60) NOT NULL,                 -- 'afectacion_gasto', 'ingreso_registro', 'orden_pago'
    "registro_id" VARCHAR(100) NOT NULL,                   -- ID de la entidad en su tabla nativa
    "tipo_documento" VARCHAR(50) NOT NULL,                 -- 'DOC-CON-TRA', 'DOC-ENT-ALM', 'FACTURA_XML'
    "descripcion" VARCHAR(300) NULL,
    "es_obligatorio" BOOLEAN NOT NULL DEFAULT FALSE,
    "orden" INT NOT NULL DEFAULT 1,

    -- Auditoría Estándar SIAF-PJEV
    "estatus_registro" SMALLINT NOT NULL DEFAULT 1,         -- 1 = Vínculo activo, 0 = Desvinculado
    "usuario_c" VARCHAR(50) NOT NULL,
    "fecha_c" TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    "usuario_m" VARCHAR(50) NULL,
    "fecha_m" TIMESTAMPTZ NULL
);

-- Índice polimórfico compuesto para consulta instantánea por formulario
CREATE INDEX IF NOT EXISTS "idx_doc_rel_entidad" ON "archivos"."documento_relacion"("modulo_siaf", "entidad_origen", "registro_id", "estatus_registro");
CREATE INDEX IF NOT EXISTS "idx_doc_rel_documento" ON "archivos"."documento_relacion"("documento_id");

-- ------------------------------------------------------------------------------
-- 4. VERSIONAMIENTO Y SUSTITUCIÓN CONTROLADA DE DOCUMENTOS
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "archivos"."documento_version" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "documento_id" UUID NOT NULL REFERENCES "archivos"."documento"("id") ON DELETE CASCADE,
    "numero_version" INT NOT NULL,                          -- 1, 2, 3...
    "hash_sha256" CHAR(64) NOT NULL,
    "ruta_storage" TEXT NOT NULL,
    "tamanio_bytes" BIGINT NOT NULL,
    "motivo_cambio" TEXT NOT NULL,                         -- Exigencia de trazabilidad y auditoría
    "es_version_actual" BOOLEAN NOT NULL DEFAULT FALSE,
    "usuario_c" VARCHAR(50) NOT NULL,
    "fecha_c" TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX IF NOT EXISTS "idx_doc_ver_documento" ON "archivos"."documento_version"("documento_id", "numero_version");

-- ------------------------------------------------------------------------------
-- 5. CADENA DE CUSTODIA Y AUDITORÍA INMUTABLE (LGA ART. 45 - TRAZABILIDAD)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "archivos"."documento_bitacora" (
    "id" BIGSERIAL PRIMARY KEY,
    "documento_id" UUID NOT NULL REFERENCES "archivos"."documento"("id") ON DELETE RESTRICT,
    "evento" VARCHAR(40) NOT NULL,                         -- 'CARGA', 'DESCARGA', 'VISUALIZACION', 'VERSION', 'VINCULAR', 'DESVINCULAR', 'BAJA_LOGICA'
    "usuario" VARCHAR(50) NOT NULL,
    "ip_cliente" VARCHAR(45) NULL,
    "user_agent" TEXT NULL,
    "detalles_json" JSONB NULL,                            -- Contexto de la operación
    "fecha_evento" TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX IF NOT EXISTS "idx_doc_bit_doc_fecha" ON "archivos"."documento_bitacora"("documento_id", "fecha_evento");
CREATE INDEX IF NOT EXISTS "idx_doc_bit_evento" ON "archivos"."documento_bitacora"("evento", "fecha_evento");

-- ==============================================================================
-- FIN DEL DDL DEL ESQUEMA ARCHIVOS
-- ==============================================================================
