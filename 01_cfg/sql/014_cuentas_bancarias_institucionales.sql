-- =============================================================================
-- SISTEMA INTEGRAL DE ADMINISTRACIÓN FINANCIERA DEL PODER JUDICIAL (SIAF-PJEV)
-- Subsistema: 01 · Configuración Inicial / Tesorería
-- Módulo: 01.4.2 Cuentas Bancarias Institucionales (Cuentas Ordenantes)
-- Marco Normativo: Art. 67 LGCG (Pago Electrónico Obligatorio) y CONAC (1.1.1.2)
-- Archivo: 014_cuentas_bancarias_institucionales.sql
-- =============================================================================

-- 1. ESQUEMAS Y EXTENSIONES
CREATE SCHEMA IF NOT EXISTS config;
CREATE SCHEMA IF NOT EXISTS contabilidad;
CREATE SCHEMA IF NOT EXISTS cxp;
CREATE SCHEMA IF NOT EXISTS ingresos;

-- 2. TABLA MAESTRA DE INSTITUCIONES BANCARIAS (01.4.1)
CREATE TABLE IF NOT EXISTS config.cat_bancos (
    banco_id SERIAL PRIMARY KEY,
    nombre_banco VARCHAR(150) NOT NULL UNIQUE,
    clave_banxico VARCHAR(5) NOT NULL UNIQUE,
    nombre_corto VARCHAR(50),
    estatus_registro SMALLINT DEFAULT 1 CHECK (estatus_registro IN (0, 1)),
    usuario_c VARCHAR(50) DEFAULT CURRENT_USER,
    fecha_c TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    usuario_m VARCHAR(50),
    fecha_m TIMESTAMP WITH TIME ZONE
);

-- Inserción de Bancos Semilla del Sistema Financiero Mexicano
INSERT INTO config.cat_bancos (nombre_banco, clave_banxico, nombre_corto) VALUES
('BBVA México, S.A., Institución de Banca Múltiple', '012', 'BBVA México'),
('Banco Mercantil del Norte, S.A. (Banorte)', '072', 'Banorte'),
('Banco Santander México, S.A.', '014', 'Santander'),
('Banco Nacional de México, S.A. (Citibanamex)', '002', 'Citibanamex'),
('HSBC México, S.A.', '021', 'HSBC'),
('Banco Scotiabank Inverlat, S.A.', '044', 'Scotiabank')
ON CONFLICT (clave_banxico) DO UPDATE 
SET nombre_banco = EXCLUDED.nombre_banco,
    nombre_corto = EXCLUDED.nombre_corto;

-- 3. TABLA MAESTRA DE CUENTAS BANCARIAS INSTITUCIONALES (01.4.2)
CREATE TABLE IF NOT EXISTS config.cat_cuentas_bancarias (
    cuenta_bancaria_id BIGSERIAL PRIMARY KEY,
    banco_id INTEGER NOT NULL REFERENCES config.cat_bancos(banco_id),
    institucion_bancaria VARCHAR(100) NOT NULL,
    numero_cuenta VARCHAR(30) NOT NULL,
    clabe_interbancaria VARCHAR(18) NOT NULL,
    sucursal VARCHAR(80),
    convenio_cie VARCHAR(30),
    nombre_identificador VARCHAR(200) NOT NULL,
    tipo_fondo VARCHAR(50) NOT NULL CHECK (
        tipo_fondo IN (
            'MINISTRACION_ESTATAL',
            'FONDO_AUXILIAR',
            'RECURSOS_PROPIOS',
            'DEPOSITOS_JUZGADOS',
            'FONDOS_FEDERALES_FASP'
        )
    ),
    cuenta_contable_id BIGINT NOT NULL,
    es_recaudadora BOOLEAN DEFAULT TRUE NOT NULL,
    es_pagadora BOOLEAN DEFAULT TRUE NOT NULL,
    saldo_inicial NUMERIC(16, 2) DEFAULT 0.00 NOT NULL,
    estatus_registro SMALLINT DEFAULT 1 NOT NULL CHECK (estatus_registro IN (0, 1)),
    usuario_c VARCHAR(50) DEFAULT CURRENT_USER NOT NULL,
    fecha_c TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    usuario_m VARCHAR(50),
    fecha_m TIMESTAMP WITH TIME ZONE,
    
    -- Restricciones de Integridad
    CONSTRAINT chk_clabe_18_digitos CHECK (length(clabe_interbancaria) = 18 AND clabe_interbancaria ~ '^[0-9]{18}$'),
    CONSTRAINT uq_cuenta_banco_activa UNIQUE (banco_id, numero_cuenta),
    CONSTRAINT uq_clabe_interbancaria UNIQUE (clabe_interbancaria)
);

-- Índices de Rendimiento y Búsqueda
CREATE INDEX IF NOT EXISTS idx_cuentas_bancarias_banco ON config.cat_cuentas_bancarias(banco_id);
CREATE INDEX IF NOT EXISTS idx_cuentas_bancarias_fondo ON config.cat_cuentas_bancarias(tipo_fondo);
CREATE INDEX IF NOT EXISTS idx_cuentas_bancarias_contable ON config.cat_cuentas_bancarias(cuenta_contable_id);
CREATE INDEX IF NOT EXISTS idx_cuentas_bancarias_flags ON config.cat_cuentas_bancarias(es_recaudadora, es_pagadora, estatus_registro);

COMMENT ON TABLE config.cat_cuentas_bancarias IS 'Padrón Maestro de Cuentas Bancarias Institucionales (Cuentas Ordenantes) del Poder Judicial del Estado de Veracruz para transferencias SPEI y recaudación.';
COMMENT ON COLUMN config.cat_cuentas_bancarias.clabe_interbancaria IS 'CLABE estandarizada de 18 dígitos requerida para dispersión interbancaria conforme al Art. 67 de la LGCG.';
COMMENT ON COLUMN config.cat_cuentas_bancarias.cuenta_contable_id IS 'Subcuenta de activo de nivel 5 vinculada forzosamente a la clase 1.1.1.2 Bancos / Tesorería del Plan de Cuentas CONAC.';

-- 4. PROCEDIMIENTO ALMACENADO: LEER CUENTAS BANCARIAS (config.fn_leer_cuentas_bancarias)
CREATE OR REPLACE FUNCTION config.fn_leer_cuentas_bancarias(
    p_usuario VARCHAR,
    p_tipo_fondo VARCHAR DEFAULT NULL,
    p_solo_recaudadoras BOOLEAN DEFAULT FALSE,
    p_solo_pagadoras BOOLEAN DEFAULT FALSE,
    p_solo_activos BOOLEAN DEFAULT TRUE
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = config, contabilidad, public
AS $$
DECLARE
    v_data JSONB;
BEGIN
    SELECT jsonb_agg(
        jsonb_build_object(
            'cuenta_bancaria_id', cb.cuenta_bancaria_id,
            'banco_id', cb.banco_id,
            'nombre_banco', b.nombre_banco,
            'nombre_corto_banco', b.nombre_corto,
            'clave_banxico', b.clave_banxico,
            'institucion_bancaria', cb.institucion_bancaria,
            'numero_cuenta', cb.numero_cuenta,
            'clabe_interbancaria', cb.clabe_interbancaria,
            'sucursal', cb.sucursal,
            'convenio_cie', cb.convenio_cie,
            'nombre_identificador', cb.nombre_identificador,
            'tipo_fondo', cb.tipo_fondo,
            'cuenta_contable_id', cb.cuenta_contable_id,
            'cuenta_contable_clave', COALESCE(cc.clave, '1.1.1.2.XX.XXX'),
            'cuenta_contable_desc', COALESCE(cc.nombre, 'Subcuenta Bancos'),
            'es_recaudadora', cb.es_recaudadora,
            'es_pagadora', cb.es_pagadora,
            'saldo_inicial', cb.saldo_inicial,
            'estatus_registro', cb.estatus_registro
        ) ORDER BY cb.cuenta_bancaria_id
    )
    INTO v_data
    FROM config.cat_cuentas_bancarias cb
    JOIN config.cat_bancos b ON b.banco_id = cb.banco_id
    LEFT JOIN contabilidad.cat_cuentas cc ON cc.cuenta_id = cb.cuenta_contable_id
    WHERE (NOT p_solo_activos OR cb.estatus_registro = 1)
      AND (p_tipo_fondo IS NULL OR cb.tipo_fondo = p_tipo_fondo)
      AND (NOT p_solo_recaudadoras OR cb.es_recaudadora = TRUE)
      AND (NOT p_solo_pagadoras OR cb.es_pagadora = TRUE);

    RETURN jsonb_build_object(
        'error', 0,
        'mensaje', 'Padrón de cuentas bancarias recuperado exitosamente.',
        'data', COALESCE(v_data, '[]'::jsonb)
    );
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object(
        'error', -2,
        'mensaje', 'Error al consultar cuentas bancarias: ' || SQLERRM,
        'data', NULL
    );
END;
$$;

-- 5. PROCEDIMIENTO ALMACENADO: CRUD CUENTAS BANCARIAS (config.fn_crud_cuentas_bancarias)
CREATE OR REPLACE FUNCTION config.fn_crud_cuentas_bancarias(
    p_accion VARCHAR,
    p_usuario VARCHAR,
    p_payload JSONB
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = config, contabilidad, cxp, ingresos, public
AS $$
DECLARE
    v_id BIGINT;
    v_banco_id INTEGER;
    v_banco_nom VARCHAR;
    v_cuenta VARCHAR;
    v_clabe VARCHAR;
    v_cta_contable_id BIGINT;
BEGIN
    -- -------------------------------------------------------------------------
    -- ACCIÓN: CREAR
    -- -------------------------------------------------------------------------
    IF p_accion = 'CREAR' THEN
        v_banco_id        := (p_payload->>'banco_id')::INTEGER;
        v_cuenta          := TRIM(COALESCE(p_payload->>'numero_cuenta', ''));
        v_clabe           := TRIM(COALESCE(p_payload->>'clabe_interbancaria', ''));
        v_cta_contable_id := (p_payload->>'cuenta_contable_id')::BIGINT;

        -- 1. Obtener nombre oficial del banco si no se envió
        SELECT nombre_banco INTO v_banco_nom FROM config.cat_bancos WHERE banco_id = v_banco_id;
        IF v_banco_nom IS NULL THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'La institución bancaria seleccionada no es válida.');
        END IF;

        -- 2. Validación de 18 dígitos exclusivamente numéricos en CLABE (Art. 67 LGCG)
        IF length(v_clabe) != 18 OR v_clabe !~ '^[0-9]{18}$' THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'La CLABE interbancaria debe contener exactamente 18 dígitos numéricos.');
        END IF;

        -- 3. Unicidad de cuenta bancaria en el mismo banco
        IF EXISTS (
            SELECT 1 FROM config.cat_cuentas_bancarias
            WHERE banco_id = v_banco_id
              AND numero_cuenta = v_cuenta
              AND estatus_registro = 1
        ) THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'Ya existe una cuenta bancaria activa con ese número para ' || v_banco_nom);
        END IF;

        -- 4. Unicidad global de CLABE
        IF EXISTS (
            SELECT 1 FROM config.cat_cuentas_bancarias
            WHERE clabe_interbancaria = v_clabe
              AND estatus_registro = 1
        ) THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'La CLABE interbancaria ya se encuentra registrada en otra cuenta activa.');
        END IF;

        -- 5. Validación de subcuenta contable CONAC (1.1.1.2 Bancos / Tesorería)
        IF v_cta_contable_id IS NULL THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'Es obligatorio asociar la subcuenta contable CONAC (Clase 1.1.1.2).');
        END IF;

        INSERT INTO config.cat_cuentas_bancarias (
            banco_id, institucion_bancaria, numero_cuenta, clabe_interbancaria, sucursal,
            convenio_cie, nombre_identificador, tipo_fondo, cuenta_contable_id,
            es_recaudadora, es_pagadora, saldo_inicial, estatus_registro,
            usuario_c, fecha_c
        ) VALUES (
            v_banco_id, v_banco_nom, v_cuenta, v_clabe, TRIM(p_payload->>'sucursal'),
            TRIM(p_payload->>'convenio_cie'), TRIM(p_payload->>'nombre_identificador'),
            p_payload->>'tipo_fondo', v_cta_contable_id,
            COALESCE((p_payload->>'es_recaudadora')::BOOLEAN, TRUE),
            COALESCE((p_payload->>'es_pagadora')::BOOLEAN, TRUE),
            COALESCE((p_payload->>'saldo_inicial')::NUMERIC, 0.00),
            1, p_usuario, CURRENT_TIMESTAMP
        ) RETURNING cuenta_bancaria_id INTO v_id;

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Cuenta bancaria institucional registrada exitosamente.',
            'data', jsonb_build_object('cuenta_bancaria_id', v_id)
        );

    -- -------------------------------------------------------------------------
    -- ACCIÓN: EDITAR
    -- -------------------------------------------------------------------------
    ELSIF p_accion = 'EDITAR' THEN
        v_id := (p_payload->>'cuenta_bancaria_id')::BIGINT;
        v_clabe := TRIM(COALESCE(p_payload->>'clabe_interbancaria', ''));

        IF length(v_clabe) != 18 OR v_clabe !~ '^[0-9]{18}$' THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'La CLABE interbancaria debe tener exactamente 18 dígitos numéricos.');
        END IF;

        -- Verificar que no choque con otra cuenta
        IF EXISTS (
            SELECT 1 FROM config.cat_cuentas_bancarias
            WHERE clabe_interbancaria = v_clabe
              AND cuenta_bancaria_id != v_id
              AND estatus_registro = 1
        ) THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'La CLABE ingresada ya pertenece a otra cuenta bancaria activa.');
        END IF;

        UPDATE config.cat_cuentas_bancarias SET
            clabe_interbancaria  = v_clabe,
            sucursal             = TRIM(p_payload->>'sucursal'),
            convenio_cie         = TRIM(p_payload->>'convenio_cie'),
            nombre_identificador = TRIM(p_payload->>'nombre_identificador'),
            es_recaudadora       = (p_payload->>'es_recaudadora')::BOOLEAN,
            es_pagadora          = (p_payload->>'es_pagadora')::BOOLEAN,
            usuario_m            = p_usuario,
            fecha_m              = CURRENT_TIMESTAMP
        WHERE cuenta_bancaria_id = v_id;

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Cuenta bancaria actualizada correctamente.',
            'data', jsonb_build_object('cuenta_bancaria_id', v_id)
        );

    -- -------------------------------------------------------------------------
    -- ACCIÓN: CAMBIAR_ESTATUS (Baja lógica / Reactivación)
    -- -------------------------------------------------------------------------
    ELSIF p_accion = 'CAMBIAR_ESTATUS' THEN
        v_id := (p_payload->>'cuenta_bancaria_id')::BIGINT;

        -- Protección: No inactivar si existen transferencias u operaciones en trámite
        IF (p_payload->>'estatus_registro')::SMALLINT = 0 THEN
            IF EXISTS (
                SELECT 1 FROM information_schema.tables WHERE table_schema = 'cxp' AND table_name = 'cxp_ordenes_pago'
            ) THEN
                IF EXISTS (
                    SELECT 1 FROM cxp.cxp_ordenes_pago
                    WHERE cuenta_bancaria_origen_id = v_id
                      AND estado_orden NOT IN ('CANCELADA', 'PAGADA')
                ) THEN
                    RETURN jsonb_build_object('error', -1, 'mensaje', 'No se puede inactivar la cuenta bancaria porque tiene órdenes de pago en trámite.');
                END IF;
            END IF;

            IF EXISTS (
                SELECT 1 FROM information_schema.tables WHERE table_schema = 'ingresos' AND table_name = 'ing_ingresos'
            ) THEN
                IF EXISTS (
                    SELECT 1 FROM ingresos.ing_ingresos
                    WHERE cuenta_bancaria_id = v_id
                      AND estado_ingreso NOT IN ('CANCELADO')
                ) THEN
                    RETURN jsonb_build_object('error', -1, 'mensaje', 'No se puede inactivar la cuenta bancaria porque tiene depósitos en trámite de conciliación.');
                END IF;
            END IF;
        END IF;

        UPDATE config.cat_cuentas_bancarias SET
            estatus_registro = (p_payload->>'estatus_registro')::SMALLINT,
            usuario_m        = p_usuario,
            fecha_m          = CURRENT_TIMESTAMP
        WHERE cuenta_bancaria_id = v_id;

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Estatus de la cuenta bancaria actualizado con éxito.',
            'data', jsonb_build_object('cuenta_bancaria_id', v_id)
        );
    END IF;

    RETURN jsonb_build_object('error', -1, 'mensaje', 'Acción no soportada: ' || p_accion, 'data', NULL);
END;
$$;

-- 6. CARGA SEMILLA DE CUENTAS PRODUCTIVAS DEL PJEV (EJERCICIO 2026)
INSERT INTO config.cat_cuentas_bancarias (
    banco_id, institucion_bancaria, numero_cuenta, clabe_interbancaria, sucursal,
    convenio_cie, nombre_identificador, tipo_fondo, cuenta_contable_id,
    es_recaudadora, es_pagadora, saldo_inicial, estatus_registro, usuario_c
) VALUES 
(
    (SELECT banco_id FROM config.cat_bancos WHERE clave_banxico = '012'),
    'BBVA México, S.A.', '0126144101', '012840001261441017', 'Suc. 0128 Xalapa Centro',
    'CIE-184920', 'BBVA Cta. 0126144101 — Ministración Estatal Ordinaria (Gasto Corriente y Nómina)',
    'MINISTRACION_ESTATAL', 101, TRUE, TRUE, 0.00, 1, 'admin_pjev'
),
(
    (SELECT banco_id FROM config.cat_bancos WHERE clave_banxico = '072'),
    'Banco Mercantil del Norte, S.A. (Banorte)', '0481920194', '072840004819201946', 'Suc. 0481 Las Trancas',
    NULL, 'Banorte Cta. 0481920194 — Fondo Auxiliar para la Impartición de Justicia',
    'FONDO_AUXILIAR', 102, TRUE, TRUE, 0.00, 1, 'admin_pjev'
),
(
    (SELECT banco_id FROM config.cat_bancos WHERE clave_banxico = '012'),
    'BBVA México, S.A.', '0119284712', '012840001192847124', 'Suc. 0128 Xalapa Centro',
    'CIE-192834', 'BBVA Cta. 0119284712 — Recursos Propios y Aranceles Judiciales',
    'RECURSOS_PROPIOS', 103, TRUE, FALSE, 0.00, 1, 'admin_pjev'
),
(
    (SELECT banco_id FROM config.cat_bancos WHERE clave_banxico = '014'),
    'Banco Santander México, S.A.', '6550918234', '014840655091823451', 'Suc. 6550 Plaza Crystal',
    NULL, 'Santander Cta. 6550918234 — Depósitos en Garantía y Consignaciones Juzgados 1ra Instancia',
    'DEPOSITOS_JUZGADOS', 104, TRUE, TRUE, 0.00, 1, 'admin_pjev'
),
(
    (SELECT banco_id FROM config.cat_bancos WHERE clave_banxico = '012'),
    'BBVA México, S.A.', '0118552390', '012840001185523908', 'Suc. 0128 Xalapa Centro',
    NULL, 'BBVA Cta. 0118552390 — Fondo de Aportaciones para la Seguridad Pública (FASP)',
    'FONDOS_FEDERALES_FASP', 105, TRUE, TRUE, 0.00, 1, 'admin_pjev'
)
ON CONFLICT (clabe_interbancaria) DO NOTHING;
