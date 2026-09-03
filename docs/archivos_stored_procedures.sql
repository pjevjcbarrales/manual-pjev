-- ==============================================================================
-- SISTEMA INTEGRAL DE ADMINISTRACIÓN Y FINANZAS (SIAF-PJEV)
-- STORED PROCEDURES CANÓNICOS: ESQUEMA ARCHIVOS
-- ==============================================================================
-- Convenciones:
--   1. Retorno JSONB estandarizado: { "error": 0, "mensaje": "OK", "data": ... }
--   2. SECURITY DEFINER con SET search_path = archivos, public
--   3. Soft-delete obligatorio (estatus_registro = 0)
--   4. Trazabilidad completa en archivos.documento_bitacora
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. SP: fn_leer_documento
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION "archivos"."fn_leer_documento"(
    p_filtros JSONB DEFAULT '{}'::jsonb
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = archivos, public
AS $$
DECLARE
    v_id UUID;
    v_hash CHAR(64);
    v_modulo VARCHAR(30);
    v_entidad VARCHAR(60);
    v_registro_id VARCHAR(100);
    v_estado_archivistico VARCHAR(20);
    v_ticket_temporal UUID;
    v_resultado JSONB;
BEGIN
    v_id := (p_filtros->>'id')::uuid;
    v_hash := p_filtros->>'hash_sha256';
    v_modulo := p_filtros->>'modulo_siaf';
    v_entidad := p_filtros->>'entidad_origen';
    v_registro_id := p_filtros->>'registro_id';
    v_estado_archivistico := p_filtros->>'estado_archivistico';
    v_ticket_temporal := (p_filtros->>'ticket_temporal')::uuid;

    SELECT COALESCE(jsonb_agg(d_row), '[]'::jsonb)
    INTO v_resultado
    FROM (
        SELECT 
            d.id,
            d.nombre_original,
            d.nombre_almacenamiento,
            d.extension,
            d.mime_type,
            d.tamanio_bytes,
            d.hash_sha256,
            d.ruta_storage,
            d.descripcion,
            d.cgca_codigo,
            c.serie AS cgca_serie_desc,
            d.valor_documental,
            d.vigencia_tramite_anios,
            d.vigencia_concentracion_anios,
            d.fecha_cierre_tramite,
            d.destino_final,
            d.estado_archivistico,
            d.clasificacion_acceso,
            d.acuerdo_reserva_id,
            d.posee_version_publica,
            d.es_digitalizado,
            d.folio_constancia_nom151,
            d.posee_firma_electronica,
            d.es_temporal,
            d.ticket_temporal,
            d.estatus_registro,
            d.usuario_c,
            d.fecha_c,
            d.usuario_m,
            d.fecha_m,
            (
                SELECT COALESCE(jsonb_agg(r_row), '[]'::jsonb)
                FROM (
                    SELECT 
                        r.id AS relacion_id,
                        r.modulo_siaf,
                        r.entidad_origen,
                        r.registro_id,
                        r.tipo_documento,
                        r.descripcion,
                        r.es_obligatorio,
                        r.orden
                    FROM archivos.documento_relacion r
                    WHERE r.documento_id = d.id AND r.estatus_registro = 1
                    ORDER BY r.orden ASC
                ) r_row
            ) AS relaciones,
            (
                SELECT COUNT(*)::int
                FROM archivos.documento_version v
                WHERE v.documento_id = d.id
            ) AS total_versiones
        FROM archivos.documento d
        LEFT JOIN archivos.cgca_catalogo c ON d.cgca_codigo = c.cgca_codigo
        WHERE d.estatus_registro = COALESCE((p_filtros->>'estatus_registro')::smallint, 1)
          AND (v_id IS NULL OR d.id = v_id)
          AND (v_hash IS NULL OR d.hash_sha256 = v_hash)
          AND (v_estado_archivistico IS NULL OR d.estado_archivistico = v_estado_archivistico)
          AND (v_ticket_temporal IS NULL OR d.ticket_temporal = v_ticket_temporal)
          AND (
              v_modulo IS NULL OR EXISTS (
                  SELECT 1 FROM archivos.documento_relacion r 
                  WHERE r.documento_id = d.id 
                    AND r.modulo_siaf = v_modulo
                    AND (v_entidad IS NULL OR r.entidad_origen = v_entidad)
                    AND (v_registro_id IS NULL OR r.registro_id = v_registro_id)
                    AND r.estatus_registro = 1
              )
          )
        ORDER BY d.fecha_c DESC
    ) d_row;

    RETURN jsonb_build_object(
        'error', 0,
        'mensaje', 'OK',
        'data', v_resultado
    );
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object(
        'error', -2,
        'mensaje', 'Error técnico al consultar documentos: ' || SQLERRM,
        'data', '[]'::jsonb
    );
END;
$$;

-- ------------------------------------------------------------------------------
-- 2. SP: fn_crud_documento
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION "archivos"."fn_crud_documento"(
    p_operacion VARCHAR(30),
    p_datos JSONB
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = archivos, public
AS $$
DECLARE
    v_id UUID;
    v_hash CHAR(64);
    v_usuario VARCHAR(50);
    v_ip VARCHAR(45);
    v_doc_existente RECORD;
    v_version_num INT;
BEGIN
    v_usuario := COALESCE(p_datos->>'usuario', 'SISTEMA');
    v_ip := p_datos->>'ip_cliente';

    -- --------------------------------------------------------------------------
    -- OPERACION: INSERT
    -- --------------------------------------------------------------------------
    IF p_operacion = 'INSERT' THEN
        v_hash := p_datos->>'hash_sha256';

        -- Validación de integridad: Verificar si ya existe binario con mismo SHA-256
        SELECT id, nombre_original, estatus_registro INTO v_doc_existente
        FROM archivos.documento
        WHERE hash_sha256 = v_hash AND estatus_registro = 1
        LIMIT 1;

        IF v_doc_existente.id IS NOT NULL AND (p_datos->>'permitir_duplicado')::boolean IS NOT TRUE THEN
            RETURN jsonb_build_object(
                'error', -1,
                'mensaje', 'El archivo ya se encuentra registrado con id ' || v_doc_existente.id || ' (' || v_doc_existente.nombre_original || ').',
                'data', jsonb_build_object('id', v_doc_existente.id, 'es_duplicado', true)
            );
        END IF;

        v_id := COALESCE((p_datos->>'id')::uuid, gen_random_uuid());

        INSERT INTO archivos.documento (
            id, nombre_original, nombre_almacenamiento, extension, mime_type,
            tamanio_bytes, hash_sha256, ruta_storage, descripcion,
            cgca_codigo, valor_documental, vigencia_tramite_anios, vigencia_concentracion_anios,
            destino_final, estado_archivistico, clasificacion_acceso, acuerdo_reserva_id,
            es_digitalizado, folio_constancia_nom151, posee_firma_electronica,
            es_temporal, ticket_temporal, estatus_registro, usuario_c, fecha_c
        ) VALUES (
            v_id,
            p_datos->>'nombre_original',
            p_datos->>'nombre_almacenamiento',
            LOWER(p_datos->>'extension'),
            p_datos->>'mime_type',
            (p_datos->>'tamanio_bytes')::bigint,
            v_hash,
            p_datos->>'ruta_storage',
            p_datos->>'descripcion',
            p_datos->>'cgca_codigo',
            COALESCE(p_datos->>'valor_documental', 'FISCAL_CONTABLE'),
            COALESCE((p_datos->>'vigencia_tramite_anios')::int, 1),
            COALESCE((p_datos->>'vigencia_concentracion_anios')::int, 5),
            COALESCE(p_datos->>'destino_final', 'BAJA_DOCUMENTAL'),
            COALESCE(p_datos->>'estado_archivistico', 'TRAMITE'),
            COALESCE(p_datos->>'clasificacion_acceso', 'CONFIDENCIAL'),
            p_datos->>'acuerdo_reserva_id',
            COALESCE((p_datos->>'es_digitalizado')::boolean, FALSE),
            p_datos->>'folio_constancia_nom151',
            COALESCE((p_datos->>'posee_firma_electronica')::boolean, FALSE),
            COALESCE((p_datos->>'es_temporal')::boolean, FALSE),
            (p_datos->>'ticket_temporal')::uuid,
            1,
            v_usuario,
            clock_timestamp()
        );

        -- Registro en Bitácora inmutable (Cadena de Custodia LGA Art. 45)
        INSERT INTO archivos.documento_bitacora (
            documento_id, evento, usuario, ip_cliente, user_agent, detalles_json, fecha_evento
        ) VALUES (
            v_id, 'CARGA', v_usuario, v_ip, p_datos->>'user_agent',
            jsonb_build_object('hash_sha256', v_hash, 'tamanio_bytes', p_datos->>'tamanio_bytes', 'es_temporal', p_datos->>'es_temporal'),
            clock_timestamp()
        );

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Documento registrado exitosamente.',
            'data', jsonb_build_object('id', v_id)
        );

    -- --------------------------------------------------------------------------
    -- OPERACION: NUEVA_VERSION
    -- --------------------------------------------------------------------------
    ELSIF p_operacion = 'NUEVA_VERSION' THEN
        v_id := (p_datos->>'id')::uuid;

        IF v_id IS NULL THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'Identificador de documento requerido para versionar.', 'data', null);
        END IF;

        IF p_datos->>'motivo_cambio' IS NULL OR LENGTH(TRIM(p_datos->>'motivo_cambio')) = 0 THEN
            RETURN jsonb_build_object('error', -1, 'mensaje', 'Por normativa de archivo y auditoría, el motivo de cambio es obligatorio.', 'data', null);
        END IF;

        -- Obtener consecutivo de versión
        SELECT COALESCE(MAX(numero_version), 0) + 1 INTO v_version_num
        FROM archivos.documento_version
        WHERE documento_id = v_id;

        -- Marcar versiones anteriores como no actuales
        UPDATE archivos.documento_version
        SET es_version_actual = FALSE
        WHERE documento_id = v_id;

        -- Registrar versión
        INSERT INTO archivos.documento_version (
            documento_id, numero_version, hash_sha256, ruta_storage, tamanio_bytes,
            motivo_cambio, es_version_actual, usuario_c, fecha_c
        ) VALUES (
            v_id, v_version_num, p_datos->>'hash_sha256', p_datos->>'ruta_storage',
            (p_datos->>'tamanio_bytes')::bigint, p_datos->>'motivo_cambio', TRUE, v_usuario, clock_timestamp()
        );

        -- Actualizar puntero maestro en documento
        UPDATE archivos.documento
        SET hash_sha256 = p_datos->>'hash_sha256',
            ruta_storage = p_datos->>'ruta_storage',
            tamanio_bytes = (p_datos->>'tamanio_bytes')::bigint,
            usuario_m = v_usuario,
            fecha_m = clock_timestamp()
        WHERE id = v_id;

        -- Bitácora de versionamiento
        INSERT INTO archivos.documento_bitacora (
            documento_id, evento, usuario, ip_cliente, user_agent, detalles_json, fecha_evento
        ) VALUES (
            v_id, 'VERSION', v_usuario, v_ip, p_datos->>'user_agent',
            jsonb_build_object('version', v_version_num, 'motivo', p_datos->>'motivo_cambio', 'nuevo_hash', p_datos->>'hash_sha256'),
            clock_timestamp()
        );

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Nueva versión ' || v_version_num || ' registrada exitosamente.',
            'data', jsonb_build_object('id', v_id, 'version', v_version_num)
        );

    -- --------------------------------------------------------------------------
    -- OPERACION: CONSOLIDAR_TEMPORAL
    -- --------------------------------------------------------------------------
    ELSIF p_operacion = 'CONSOLIDAR_TEMPORAL' THEN
        UPDATE archivos.documento
        SET es_temporal = FALSE,
            ticket_temporal = NULL,
            usuario_m = v_usuario,
            fecha_m = clock_timestamp()
        WHERE ticket_temporal = (p_datos->>'ticket_temporal')::uuid;

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Archivos temporales consolidados con éxito.',
            'data', null
        );

    -- --------------------------------------------------------------------------
    -- OPERACION: DESACTIVAR (Soft-Delete)
    -- --------------------------------------------------------------------------
    ELSIF p_operacion = 'DESACTIVAR' THEN
        v_id := (p_datos->>'id')::uuid;

        UPDATE archivos.documento
        SET estatus_registro = 0,
            usuario_m = v_usuario,
            fecha_m = clock_timestamp()
        WHERE id = v_id;

        -- Bitácora de baja lógica
        INSERT INTO archivos.documento_bitacora (
            documento_id, evento, usuario, ip_cliente, user_agent, detalles_json, fecha_evento
        ) VALUES (
            v_id, 'BAJA_LOGICA', v_usuario, v_ip, p_datos->>'user_agent',
            jsonb_build_object('motivo', p_datos->>'motivo'),
            clock_timestamp()
        );

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Documento deshabilitado con éxito.',
            'data', jsonb_build_object('id', v_id)
        );

    ELSE
        RETURN jsonb_build_object(
            'error', -1,
            'mensaje', 'Operación no reconocida: ' || p_operacion,
            'data', null
        );
    END IF;

EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object(
        'error', -2,
        'mensaje', 'Error técnico en fn_crud_documento: ' || SQLERRM,
        'data', null
    );
END;
$$;

-- ------------------------------------------------------------------------------
-- 3. SP: fn_crud_documento_relacion (Vincular / Desvincular)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION "archivos"."fn_crud_documento_relacion"(
    p_operacion VARCHAR(30),
    p_datos JSONB
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = archivos, public
AS $$
DECLARE
    v_relacion_id UUID;
    v_documento_id UUID;
    v_usuario VARCHAR(50);
BEGIN
    v_usuario := COALESCE(p_datos->>'usuario', 'SISTEMA');

    IF p_operacion = 'VINCULAR' THEN
        v_documento_id := (p_datos->>'documento_id')::uuid;
        v_relacion_id := COALESCE((p_datos->>'id')::uuid, gen_random_uuid());

        INSERT INTO archivos.documento_relacion (
            id, documento_id, modulo_siaf, entidad_origen, registro_id,
            tipo_documento, descripcion, es_obligatorio, orden,
            estatus_registro, usuario_c, fecha_c
        ) VALUES (
            v_relacion_id,
            v_documento_id,
            p_datos->>'modulo_siaf',
            p_datos->>'entidad_origen',
            p_datos->>'registro_id',
            p_datos->>'tipo_documento',
            p_datos->>'descripcion',
            COALESCE((p_datos->>'es_obligatorio')::boolean, FALSE),
            COALESCE((p_datos->>'orden')::int, 1),
            1,
            v_usuario,
            clock_timestamp()
        );

        -- Registrar en bitácora
        INSERT INTO archivos.documento_bitacora (
            documento_id, evento, usuario, ip_cliente, detalles_json, fecha_evento
        ) VALUES (
            v_documento_id, 'VINCULAR', v_usuario, p_datos->>'ip_cliente',
            jsonb_build_object('modulo', p_datos->>'modulo_siaf', 'entidad', p_datos->>'entidad_origen', 'registro_id', p_datos->>'registro_id'),
            clock_timestamp()
        );

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Vínculo documental registrado exitosamente.',
            'data', jsonb_build_object('relacion_id', v_relacion_id)
        );

    ELSIF p_operacion = 'DESVINCULAR' THEN
        v_relacion_id := (p_datos->>'relacion_id')::uuid;

        SELECT documento_id INTO v_documento_id
        FROM archivos.documento_relacion
        WHERE id = v_relacion_id;

        UPDATE archivos.documento_relacion
        SET estatus_registro = 0,
            usuario_m = v_usuario,
            fecha_m = clock_timestamp()
        WHERE id = v_relacion_id;

        -- Registrar en bitácora
        IF v_documento_id IS NOT NULL THEN
            INSERT INTO archivos.documento_bitacora (
                documento_id, evento, usuario, ip_cliente, detalles_json, fecha_evento
            ) VALUES (
                v_documento_id, 'DESVINCULAR', v_usuario, p_datos->>'ip_cliente',
                jsonb_build_object('relacion_id', v_relacion_id, 'motivo', p_datos->>'motivo'),
                clock_timestamp()
            );
        END IF;

        RETURN jsonb_build_object(
            'error', 0,
            'mensaje', 'Vínculo documental cancelado exitosamente.',
            'data', null
        );

    ELSE
        RETURN jsonb_build_object('error', -1, 'mensaje', 'Operación no válida: ' || p_operacion, 'data', null);
    END IF;

EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object('error', -2, 'mensaje', 'Error en fn_crud_documento_relacion: ' || SQLERRM, 'data', null);
END;
$$;

-- ------------------------------------------------------------------------------
-- 4. SP: fn_registrar_evento_bitacora (Descarga, Visualización, Consulta)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION "archivos"."fn_registrar_evento_bitacora"(
    p_datos JSONB
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = archivos, public
AS $$
BEGIN
    INSERT INTO archivos.documento_bitacora (
        documento_id, evento, usuario, ip_cliente, user_agent, detalles_json, fecha_evento
    ) VALUES (
        (p_datos->>'documento_id')::uuid,
        p_datos->>'evento',
        COALESCE(p_datos->>'usuario', 'SISTEMA'),
        p_datos->>'ip_cliente',
        p_datos->>'user_agent',
        p_datos->'detalles',
        clock_timestamp()
    );

    RETURN jsonb_build_object('error', 0, 'mensaje', 'Evento auditado con éxito.', 'data', null);
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object('error', -2, 'mensaje', 'Error al auditar evento: ' || SQLERRM, 'data', null);
END;
$$;

-- ------------------------------------------------------------------------------
-- 5. SP: fn_depurar_archivos_temporales (Garbage Collector Nocturno)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION "archivos"."fn_depurar_archivos_temporales"()
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = archivos, public
AS $$
DECLARE
    v_total_depurados INT;
BEGIN
    -- Se marcan como eliminados los temporales con más de 24 horas sin vincular
    WITH eliminados AS (
        UPDATE archivos.documento
        SET estatus_registro = 0,
            usuario_m = 'JOB_GARBAGE_COLLECTOR',
            fecha_m = clock_timestamp()
        WHERE es_temporal = TRUE 
          AND fecha_c < (clock_timestamp() - INTERVAL '24 hours')
          AND estatus_registro = 1
        RETURNING id
    )
    SELECT COUNT(*) INTO v_total_depurados FROM eliminados;

    RETURN jsonb_build_object(
        'error', 0,
        'mensaje', 'Depuración concluida exitosamente.',
        'data', jsonb_build_object('total_depurados', v_total_depurados)
    );
END;
$$;
