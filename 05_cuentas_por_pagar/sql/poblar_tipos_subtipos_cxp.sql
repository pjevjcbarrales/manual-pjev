-- ============================================================================
-- SCRIPT OFICIAL DE CREACIÓN Y POBLADO IDEMPOTENTE: TIPOS Y SUBTIPOS DE CXP
-- Esquema: cxp
-- Entidades: catalogo_grupos_tramite (4 Tipos) y catalogo_procedimientos_afectacion (15 Subtipos)
-- ============================================================================

BEGIN;

-- 1. TABLA MAESTRA DE TIPOS DE TRÁMITE (GRUPOS / MACRO-FAMILIAS)
CREATE TABLE IF NOT EXISTS cxp.catalogo_grupos_tramite (
    cgt_codigo VARCHAR(20) PRIMARY KEY,
    cgt_nombre VARCHAR(100) NOT NULL,
    cgt_numero SMALLINT NOT NULL UNIQUE,
    cgt_titulo VARCHAR(100) NOT NULL,
    cgt_subtitulo VARCHAR(150),
    cgt_descripcion VARCHAR(500) NOT NULL,
    cgt_icono VARCHAR(50) DEFAULT 'Receipt',
    cgt_permiso_requerido VARCHAR(50) DEFAULT 'CXP_CAT_GASTO_DIRECTO',
    afecta_presupuesto BOOLEAN NOT NULL DEFAULT true,
    cgt_orden SMALLINT NOT NULL,
    estatus_registro SMALLINT NOT NULL DEFAULT 1 CHECK (estatus_registro IN (0, 1)),
    usuario_c VARCHAR(50) NOT NULL DEFAULT 'MIGRACION_178',
    fecha_c TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    usuario_m VARCHAR(50),
    fecha_m TIMESTAMPTZ
);

ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS cgt_nombre VARCHAR(100);
ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS cgt_numero SMALLINT;
ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS cgt_titulo VARCHAR(100);
ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS cgt_subtitulo VARCHAR(150);
ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS cgt_descripcion VARCHAR(500);
ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS cgt_icono VARCHAR(50) DEFAULT 'Receipt';
ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS cgt_permiso_requerido VARCHAR(50) DEFAULT 'CXP_CAT_GASTO_DIRECTO';
ALTER TABLE cxp.catalogo_grupos_tramite ADD COLUMN IF NOT EXISTS afecta_presupuesto BOOLEAN NOT NULL DEFAULT true;

-- Poblado de los 4 Tipos Principales incluyendo cgt_nombre
INSERT INTO cxp.catalogo_grupos_tramite (
    cgt_codigo, cgt_nombre, cgt_numero, cgt_titulo, cgt_subtitulo, cgt_descripcion,
    cgt_icono, cgt_permiso_requerido, afecta_presupuesto, cgt_orden
) VALUES
(
    'DIRECTO', 'Gasto Directo', 1, '1. Gasto Directo', 'Sin pedido ni licitación',
    'Nómina, servicios básicos, rentas, honorarios y compras menores directas.',
    'Receipt', 'CXP_CAT_GASTO_DIRECTO', true, 1
),
(
    'PEDIDO', 'Por Pedido / Contrato', 2, '2. Por Pedido / Contrato', 'Derivado de adquisiciones/obra',
    'Licitaciones, compras de almacén, contratos de servicios y obra pública.',
    'ShoppingBag', 'CXP_CAT_PEDIDO_CONTRATO', true, 2
),
(
    'COMPROBAR', 'Gastos por Comprobar', 3, '3. Gastos a Comprobar', 'Anticipos y comisiones',
    'Viáticos oficiales (Anexo 6), sujetos a comprobar y reposición de caja chica.',
    'Plane', 'CXP_CAT_GASTOS_COMPROBAR', true, 3
),
(
    'NO_PRESUPUESTARIO', 'No Afecta Presupuesto', 4, '4. No Afecta Presupuesto', 'Cuentas de balance y fondos ajenos',
    'Entero de retenciones fiscales y laborales, devolución de garantías y fondos en custodia.',
    'Scale', 'CXP_CAT_NO_PRESUPUESTARIO', false, 4
)
ON CONFLICT (cgt_codigo) DO UPDATE SET
    cgt_nombre = EXCLUDED.cgt_nombre,
    cgt_numero = EXCLUDED.cgt_numero,
    cgt_titulo = EXCLUDED.cgt_titulo,
    cgt_subtitulo = EXCLUDED.cgt_subtitulo,
    cgt_descripcion = EXCLUDED.cgt_descripcion,
    cgt_icono = EXCLUDED.cgt_icono,
    cgt_permiso_requerido = EXCLUDED.cgt_permiso_requerido,
    afecta_presupuesto = EXCLUDED.afecta_presupuesto,
    cgt_orden = EXCLUDED.cgt_orden,
    estatus_registro = 1,
    fecha_m = clock_timestamp(),
    usuario_m = 'SCRIPT_POBLADO';

-- 2. TABLA DE SUBTIPOS / PROCEDIMIENTOS OPERATIVOS
CREATE TABLE IF NOT EXISTS cxp.catalogo_procedimientos_afectacion (
    cpa_codigo VARCHAR(40) PRIMARY KEY,
    f_grupo_codigo VARCHAR(20) NOT NULL REFERENCES cxp.catalogo_grupos_tramite(cgt_codigo),
    cpa_nombre VARCHAR(150) NOT NULL,
    cpa_subtitulo VARCHAR(150),
    cpa_descripcion VARCHAR(500) NOT NULL,
    cpa_icono VARCHAR(50) DEFAULT 'FileText',
    cpa_badge VARCHAR(50) DEFAULT 'Recursos Materiales',
    cpa_tipo_beneficiario VARCHAR(30) NOT NULL DEFAULT 'PROVEEDOR',
    cpa_tipo_pago SMALLINT NOT NULL CHECK (cpa_tipo_pago IN (1, 2, 3, 4)),
    cpa_orden SMALLINT NOT NULL,
    cpa_seleccionable BOOLEAN NOT NULL DEFAULT true,
    cpa_estado_definicion VARCHAR(20) NOT NULL DEFAULT 'VALIDADO',
    cpa_observacion_normativa VARCHAR(1000),
    estatus_registro SMALLINT NOT NULL DEFAULT 1 CHECK (estatus_registro IN (0, 1)),
    usuario_c VARCHAR(50) NOT NULL DEFAULT 'MIGRACION_178',
    fecha_c TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    usuario_m VARCHAR(50),
    fecha_m TIMESTAMPTZ
);

ALTER TABLE cxp.catalogo_procedimientos_afectacion ADD COLUMN IF NOT EXISTS cpa_subtitulo VARCHAR(150);
ALTER TABLE cxp.catalogo_procedimientos_afectacion ADD COLUMN IF NOT EXISTS cpa_icono VARCHAR(50) DEFAULT 'FileText';
ALTER TABLE cxp.catalogo_procedimientos_afectacion ADD COLUMN IF NOT EXISTS cpa_badge VARCHAR(50) DEFAULT 'Recursos Materiales';
ALTER TABLE cxp.catalogo_procedimientos_afectacion ADD COLUMN IF NOT EXISTS cpa_tipo_beneficiario VARCHAR(30) DEFAULT 'PROVEEDOR';

-- Retirar de forma segura cualquier CHECK previo en cpa_tipo_pago
DO $do$
DECLARE r record;
BEGIN
  FOR r IN (
    SELECT conname FROM pg_constraint 
     WHERE conrelid = 'cxp.catalogo_procedimientos_afectacion'::regclass 
       AND contype = 'c' 
       AND pg_get_constraintdef(oid) LIKE '%cpa_tipo_pago%'
  ) LOOP
    EXECUTE 'ALTER TABLE cxp.catalogo_procedimientos_afectacion DROP CONSTRAINT ' || quote_ident(r.conname);
  END LOOP;
END $do$;

ALTER TABLE cxp.catalogo_procedimientos_afectacion 
    ADD CONSTRAINT ck_cpa_tipo_pago CHECK (cpa_tipo_pago IN (1, 2, 3, 4));

-- Retirar y recrear el constraint de tipo beneficiario alineado con la migración 160
DO $do$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_cpa_tipo_beneficiario') THEN
    ALTER TABLE cxp.catalogo_procedimientos_afectacion DROP CONSTRAINT ck_cpa_tipo_beneficiario;
  END IF;
  ALTER TABLE cxp.catalogo_procedimientos_afectacion
    ADD CONSTRAINT ck_cpa_tipo_beneficiario CHECK (
      cpa_tipo_beneficiario IS NULL OR cpa_tipo_beneficiario IN
      ('PROVEEDOR','EMPLEADO','UNIDAD_ADMINISTRATIVA','TERCERO_EMPLEADO',
       'TERCERO_INSTITUCIONAL','BIEN_INMUEBLE')
    );
END $do$;

-- Inserción / Actualización de los 15 Procedimientos
INSERT INTO cxp.catalogo_procedimientos_afectacion (
    cpa_codigo, f_grupo_codigo, cpa_nombre, cpa_subtitulo, cpa_descripcion,
    cpa_icono, cpa_badge, cpa_tipo_beneficiario, cpa_tipo_pago, cpa_orden,
    cpa_seleccionable, cpa_estado_definicion, cpa_observacion_normativa
) VALUES
-- ============================================================================
-- GRUPO 1: GASTO DIRECTO (cpa_tipo_pago = 1)
-- ============================================================================
(
    'NOMINA', 'DIRECTO', 'Nómina Quincenal / Prestaciones', 'Sueldos y compensaciones',
    'Afectación presupuestal de sueldos, compensaciones y prestaciones del personal jurisdiccional y administrativo.',
    'Users', 'Servicios Personales', 'UNIDAD_ADMINISTRATIVA', 1, 1,
    true, 'VALIDADO', 'Afecta Capítulo 1000 conforme al tabulador de plazas vigente.'
),
(
    'ARRENDAMIENTO', 'DIRECTO', 'Arrendamiento de Inmuebles', 'Rentas de juzgados y sedes',
    'Pago mensual de rentas de bienes inmuebles para juzgados foráneos y sedes judiciales del Estado.',
    'Building', 'Recursos Materiales', 'BIEN_INMUEBLE', 1, 2,
    true, 'VALIDADO', 'Exige CFDI vigente, contrato de arrendamiento y visto bueno de Adquisiciones.'
),
(
    'SERVICIOS_BASICOS', 'DIRECTO', 'Servicios Básicos (CFE, CAEV, Telecom)', 'Energía, agua y telecomunicaciones',
    'Pago continuo de energía eléctrica, agua potable, telefonía e internet institucional.',
    'Zap', 'Recursos Materiales', 'TERCERO_INSTITUCIONAL', 1, 3,
    true, 'VALIDADO', 'No genera orden de compra; se liquida contra aviso-recibo o factura del proveedor.'
),
(
    'HONORARIOS', 'DIRECTO', 'Honorarios / Servicios Profesionales', 'Servicios de personas físicas',
    'Servicios profesionales independientes de personas físicas para peritajes, asesorías y dictámenes con retención.',
    'FileText', 'Recursos Materiales', 'PROVEEDOR', 1, 4,
    true, 'VALIDADO', 'Aplica retención de 10% ISR y dos terceras partes de IVA conforme a ley.'
),
(
    'GASTO_DIRECTO_GENERAL', 'DIRECTO', 'Compra Directa / Gastos Menores', 'Suministros y mostrador urgente',
    'Adquisiciones o servicios menores urgentes que no requieren proceso licitatorio ni entrega en almacén central.',
    'Tag', 'Recursos Materiales', 'PROVEEDOR', 1, 5,
    true, 'VALIDADO', 'Sujeto a techo máximo fijado en los lineamientos de adquisiciones del PJEV.'
),
(
    'BENEFICIARIOS_EMPLEADOS', 'DIRECTO', 'Pago a Beneficiarios de Empleados', 'Pensiones alimenticias judiciales',
    'Pago a acreedores de pensiones alimenticias o beneficiarios vinculados legalmente a un trabajador.',
    'UserCheck', 'Servicios Personales', 'TERCERO_EMPLEADO', 1, 6,
    true, 'VALIDADO', 'Derivado de orden emitida por juez familiar competente sobre la nómina.'
),

-- ============================================================================
-- GRUPO 2: POR PEDIDO / CONTRATO (cpa_tipo_pago = 2)
-- ============================================================================
(
    'COMPRA_PEDIDO', 'PEDIDO', 'Pedido de Adquisiciones / Almacén', 'Compras con entrada sellada',
    'Compra de bienes y suministros formalizada mediante pedido institucional y remisión con entrada sellada de almacén.',
    'ShoppingCart', 'Recursos Materiales', 'PROVEEDOR', 2, 1,
    true, 'VALIDADO', 'Exige factura CFDI, pedido formalizado y constancia de alta en inventarios si aplica.'
),
(
    'CONTRATO_SERVICIOS', 'PEDIDO', 'Contrato de Servicios Generales', 'Servicios continuos licitados',
    'Servicios continuos formalizados bajo contrato (vigilancia, limpieza, aseguramiento patrimonial y licencias de software).',
    'FileContract', 'Recursos Materiales', 'PROVEEDOR', 2, 2,
    true, 'VALIDADO', 'Vinculado a contrato plurianual o anual de adquisiciones y acta de recepción de servicios.'
),
(
    'OBRA_PUBLICA', 'PEDIDO', 'Contrato de Obra Pública', 'Infraestructura judicial y mantenimiento',
    'Anticipos, estimaciones autorizadas por supervisión de infraestructura y finiquitos de ciudades judiciales.',
    'HardHat', 'Obra y Proyectos', 'PROVEEDOR', 2, 3,
    true, 'VALIDADO', 'Exige expediente técnico, estimación autorizada por residencia de obra y retención 5 al millar.'
),

-- ============================================================================
-- GRUPO 3: GASTOS A COMPROBAR (cpa_tipo_pago = 3)
-- ============================================================================
(
    'COMPROBACION_VIATICOS', 'COMPROBAR', 'Comprobación de Viáticos y Pasajes', 'Comisiones oficiales (Anexo 6)',
    'Comprobación oficial de viáticos de servidores públicos conforme al tabulador autorizado y facturas fiscales.',
    'Plane', 'Gastos por Comprobar', 'EMPLEADO', 3, 1,
    true, 'VALIDADO', 'Sujeto al tabulador oficial (05.1.2) y verificación del Anexo 5 y Anexo 6.'
),
(
    'SUJETOS_COMPROBAR', 'COMPROBAR', 'Sujetos a Comprobar (Gastos Operativos)', 'Operación de juzgados foráneos',
    'Comprobación de recursos asignados a titulares de juzgados foráneos y áreas jurisdiccionales (Anexo 15).',
    'FolderCheck', 'Gastos por Comprobar', 'EMPLEADO', 3, 2,
    true, 'VALIDADO', 'Requiere informe detallado de aplicación del recurso y facturas fiscales a nombre del PJEV.'
),
(
    'FONDO_REVOLVENTE', 'COMPROBAR', 'Reposición de Fondo Revolvente', 'Caja chica institucional',
    'Reposición periódica de caja chica y fondos revolventes amparada con comprobantes fiscales de gastos menores.',
    'RotateCcw', 'Fondo Rotatorio', 'EMPLEADO', 3, 3,
    true, 'VALIDADO', 'Reposición exclusivamente por el importe comprobado; no modifica el saldo del fondo.'
),

-- ============================================================================
-- GRUPO 4: NO AFECTA PRESUPUESTO (cpa_tipo_pago = 4, afecta_presupuesto = false)
-- ============================================================================
(
    'TERCEROS_INST', 'NO_PRESUPUESTARIO', 'Entero de Retenciones Fiscales y Laborales', 'SAT, SEFIPLAN, IPE y sindicatos',
    'Pago y liquidación concentrada de retenciones fiscales (ISR) y laborales (IPE, 3%, cuotas sindicales) sin devengo presupuestario nuevo.',
    'Landmark', 'Pasivo Circulante 2.1.1.7', 'TERCERO_INSTITUCIONAL', 4, 1,
    true, 'VALIDADO', 'Operación de balance patrimonial pura. Disminuye pasivo 2.1.1.7 contra salida bancaria; cero afectación presupuestal.'
),
(
    'DEVOLUCION_GARANTIA', 'NO_PRESUPUESTARIO', 'Devolución de Garantías y Fianzas', 'Reembolso a licitantes y contratistas',
    'Reembolso de depósitos en efectivo entregados por contratistas para sostenimiento de ofertas o vicios ocultos.',
    'ShieldCheck', 'Fondos en Garantía 2.1.6.1', 'PROVEEDOR', 4, 2,
    true, 'VALIDADO', 'Disminuye la cuenta de balance 2.1.6.1 Depósitos de Fondos de Terceros en Garantía.'
),
(
    'FONDOS_CUSTODIA', 'NO_PRESUPUESTARIO', 'Fondos en Custodia y Devoluciones', 'Consignaciones judiciales y pagos indebidos',
    'Devolución de cobros indebidos recibidos en caja y entrega de recursos bajo custodia o consignación judicial.',
    'Scale', 'Operación de Balance', 'TERCERO_INSTITUCIONAL', 4, 3,
    true, 'VALIDADO', 'Mandatos judiciales o devoluciones directas de cobros duplicados en caja de ingresos.'
)
ON CONFLICT (cpa_codigo) DO UPDATE SET
    f_grupo_codigo = EXCLUDED.f_grupo_codigo,
    cpa_nombre = EXCLUDED.cpa_nombre,
    cpa_subtitulo = EXCLUDED.cpa_subtitulo,
    cpa_descripcion = EXCLUDED.cpa_descripcion,
    cpa_icono = EXCLUDED.cpa_icono,
    cpa_badge = EXCLUDED.cpa_badge,
    cpa_tipo_beneficiario = EXCLUDED.cpa_tipo_beneficiario,
    cpa_tipo_pago = EXCLUDED.cpa_tipo_pago,
    cpa_orden = EXCLUDED.cpa_orden,
    cpa_seleccionable = EXCLUDED.cpa_seleccionable,
    cpa_estado_definicion = EXCLUDED.cpa_estado_definicion,
    cpa_observacion_normativa = EXCLUDED.cpa_observacion_normativa,
    estatus_registro = 1,
    fecha_m = clock_timestamp(),
    usuario_m = 'SCRIPT_POBLADO';

-- 3. ALINEACIÓN DE LA TABLA TRANSACCIONAL DE AFECTACIONES
ALTER TABLE cxp.afectaciones_gasto ADD COLUMN IF NOT EXISTS f_grupo_codigo VARCHAR(20);
ALTER TABLE cxp.afectaciones_gasto ADD COLUMN IF NOT EXISTS afecta_presupuesto BOOLEAN DEFAULT true;

DO $do$
DECLARE r record;
BEGIN
  FOR r IN (
    SELECT conname FROM pg_constraint 
     WHERE conrelid = 'cxp.afectaciones_gasto'::regclass 
       AND contype = 'c' 
       AND pg_get_constraintdef(oid) LIKE '%tipo_pago%'
  ) LOOP
    EXECUTE 'ALTER TABLE cxp.afectaciones_gasto DROP CONSTRAINT ' || quote_ident(r.conname);
  END LOOP;
END $do$;

ALTER TABLE cxp.afectaciones_gasto 
    ADD CONSTRAINT afectaciones_gasto_tipo_pago_check 
    CHECK (tipo_pago IN (1, 2, 3, 4));

UPDATE cxp.afectaciones_gasto ag
   SET f_grupo_codigo = cpa.f_grupo_codigo,
       tipo_pago = cpa.cpa_tipo_pago,
       afecta_presupuesto = cgt.afecta_presupuesto
  FROM cxp.catalogo_procedimientos_afectacion cpa
  JOIN cxp.catalogo_grupos_tramite cgt ON cgt.cgt_codigo = cpa.f_grupo_codigo
 WHERE ag.f_procedimiento_codigo = cpa.cpa_codigo
   AND (ag.f_grupo_codigo IS NULL OR ag.tipo_pago <> cpa.cpa_tipo_pago);

COMMIT;
