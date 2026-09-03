-- Migration 180: Crear Matriz de Conversión y Reglas de Reclasificación de Orden de Pago (2.1.1.9 a 2.1.1.1)
-- Propósito: Formalizar en contabilidad.matriz_conversion el evento patrimonial de Orden de Pago (Momento Ejercido / mc_id = 5)
-- permitiendo que el Contador General gestione en 03.1.2 el traspaso automático de la cuenta puente concentradora
-- '2.1.1.9.1000.0001' hacia el pasivo líquido exigible '2.1.1.1.1000.0001 Remuneraciones por Pagar' sin código duro.

DO $$
DECLARE
    v_momento_eje_id INTEGER;
    v_matriz_id BIGINT;
    v_regla_id BIGINT;
    v_cta_puente_id INTEGER;
    v_cta_permanente_id INTEGER;
    v_cta_transitorio_id INTEGER;
    v_cta_pension_id INTEGER;
BEGIN
    -- 1. Obtener ID de Momento Presupuestal Ejercido (EJE)
    SELECT mc_id INTO v_momento_eje_id
      FROM config.catalogo_momentos
     WHERE mc_clave = 'EJE' AND estatus_registro = 1
     LIMIT 1;

    IF v_momento_eje_id IS NULL THEN
        v_momento_eje_id := 5; -- Fallback histórico
    END IF;

    -- 2. Obtener IDs de las cuentas contables involucradas
    SELECT cc_id INTO v_cta_puente_id FROM contabilidad.catalogo_cuentas WHERE cc_cuentapuntos = '2.1.1.9.1000.0001' LIMIT 1;
    SELECT cc_id INTO v_cta_permanente_id FROM contabilidad.catalogo_cuentas WHERE cc_cuentapuntos = '2.1.1.1.1000.0001' LIMIT 1;
    SELECT cc_id INTO v_cta_transitorio_id FROM contabilidad.catalogo_cuentas WHERE cc_cuentapuntos = '2.1.1.1.2000.0001' LIMIT 1;
    SELECT cc_id INTO v_cta_pension_id FROM contabilidad.catalogo_cuentas WHERE cc_cuentapuntos = '2.1.1.9.3000.0001' LIMIT 1;

    IF v_cta_puente_id IS NULL OR v_cta_permanente_id IS NULL THEN
        RAISE EXCEPTION 'No se encontraron las cuentas requeridas (2.1.1.9.1000.0001 o 2.1.1.1.1000.0001) en catalogo_cuentas.';
    END IF;

    -- 3. Registrar Evento en contabilidad.catalogo_eventos_matriz si no existe
    INSERT INTO contabilidad.catalogo_eventos_matriz (
        cem_codigo, cem_nombre, cem_familia_conac, cem_descripcion, estatus_registro, usuario_c, fecha_c
    ) VALUES (
        'RECLASIFICACION_OP',
        'Reclasificación de pasivo por Orden de Pago',
        'EJE',
        'Reclasifica pasivo concentrador (2.1.1.9) a pasivo líquido exigible (2.1.1.1) al autorizar la Orden de Pago.',
        1, 'MIGRACION_180', clock_timestamp()
    ) ON CONFLICT (cem_codigo) DO UPDATE
      SET cem_nombre = EXCLUDED.cem_nombre,
          cem_descripcion = EXCLUDED.cem_descripcion,
          usuario_m = 'MIGRACION_180',
          fecha_m = clock_timestamp();

    -- 4. Registrar Cabecera de Matriz en contabilidad.matriz_conversion
    INSERT INTO contabilidad.matriz_conversion (
        mcv_clave, mcv_nombre, mcv_descripcion, mcv_ambito, mcv_momento_id,
        mcv_ejercicio, mcv_version, mcv_vigencia_inicio, mcv_vigencia_fin,
        mcv_estado, estatus_registro, usuario_c, fecha_c,
        mcv_lock_version, mcv_tipo_registro, mcv_familia_conac,
        mcv_area_pjev, mcv_procedimiento_pjev
    ) VALUES (
        'A0_RECLASIFICA_ORDEN_PAGO',
        'Reclasificación Pasiva de Órdenes de Pago',
        'Traspaso patrimonial de cuentas puente 2.1.1.9 a pasivos exigibles 2.1.1.1 al autorizar órdenes de pago de nómina.',
        'E',
        v_momento_eje_id,
        2026,
        1,
        '2026-01-01',
        '2026-12-31',
        'BORRADOR',
        1,
        'MIGRACION_180',
        clock_timestamp(),
        1,
        'MATRIZ_CONVERSION_CONAC',
        NULL,
        'SUBDIRECCION_RECURSOS_FINANCIEROS/DEPARTAMENTO_TESORERIA',
        'ORDENES_DE_PAGO'
    ) ON CONFLICT (mcv_clave, mcv_ejercicio, mcv_version) DO UPDATE
      SET mcv_nombre = EXCLUDED.mcv_nombre,
          mcv_descripcion = EXCLUDED.mcv_descripcion,
          mcv_estado = 'BORRADOR', -- Temporal para permitir modificar reglas
          usuario_m = 'MIGRACION_180',
          fecha_m = clock_timestamp()
    RETURNING mcv_id INTO v_matriz_id;

    -- 5. Regla 1: Reclasificación Nómina Personal Permanente
    INSERT INTO contabilidad.matriz_conversion_regla (
        mcr_matriz_id, mcr_clave, mcr_descripcion, mcr_prioridad,
        mcr_cog_id, mcr_tipo_gasto, mcr_nivel_afectacion, mcr_tipo_proveedor_id,
        mcr_procedimiento_codigo, mcr_evento_codigo,
        mcr_tipo_operacion, mcr_perfil,
        mcr_clasificacion_estado, mcr_clasificacion_motivo,
        mcr_es_predeterminada, estatus_registro, usuario_c, fecha_c
    ) VALUES (
        v_matriz_id,
        'R_OP_NOMINA_NETA',
        'Reclasificación Nómina Permanente: 2.1.1.9.1000.0001 a 2.1.1.1.1000.0001',
        100,
        6, -- COG 11300001 Sueldos base al personal permanente
        1,
        'EMPLEADO',
        0,
        'NOMINA',
        'RECLASIFICACION_OP',
        'DEVENGAR_NOMINA',
        'EGRESO',
        'DETERMINADA',
        'Reclasificación de pasivo concentrador a pasivo líquido exigible de remuneraciones.',
        0,
        1,
        'MIGRACION_180',
        clock_timestamp()
    ) ON CONFLICT (mcr_matriz_id, mcr_clave) DO UPDATE
      SET mcr_descripcion = EXCLUDED.mcr_descripcion,
          mcr_cog_id = EXCLUDED.mcr_cog_id,
          mcr_procedimiento_codigo = EXCLUDED.mcr_procedimiento_codigo,
          mcr_evento_codigo = EXCLUDED.mcr_evento_codigo,
          usuario_m = 'MIGRACION_180',
          fecha_m = clock_timestamp()
    RETURNING mcr_id INTO v_regla_id;

    -- Limpiar movimientos previos de la regla para garantizar idempotencia
    DELETE FROM contabilidad.matriz_conversion_movimiento WHERE mcm_regla_id = v_regla_id;

    -- Movimiento 1 (Cargo / Debe): Cancelación de la cuenta puente concentradora
    INSERT INTO contabilidad.matriz_conversion_movimiento (
        mcm_regla_id, mcm_orden, mcm_ambito, mcm_naturaleza, mcm_origen_cuenta,
        mcm_cuenta_id, mcm_formula_importe, mcm_descripcion, mcm_es_obligatorio,
        estatus_registro, usuario_c, fecha_c
    ) VALUES (
        v_regla_id, 1, 'C', 'D', 'FIJA',
        v_cta_puente_id, 'NETO_PAGAR',
        'Cancelación pasivo concentrador nómina en cuenta puente (Nómina por Liquidar)', 1,
        1, 'MIGRACION_180', clock_timestamp()
    );

    -- Movimiento 2 (Abono / Haber): Reconocimiento del pasivo líquido exigible
    INSERT INTO contabilidad.matriz_conversion_movimiento (
        mcm_regla_id, mcm_orden, mcm_ambito, mcm_naturaleza, mcm_origen_cuenta,
        mcm_cuenta_id, mcm_formula_importe, mcm_descripcion, mcm_es_obligatorio,
        estatus_registro, usuario_c, fecha_c
    ) VALUES (
        v_regla_id, 2, 'C', 'H', 'FIJA',
        v_cta_permanente_id, 'NETO_PAGAR',
        'Reconocimiento pasivo líquido exigible de remuneraciones por pagar', 1,
        1, 'MIGRACION_180', clock_timestamp()
    );

    -- 6. Regla 2: Reclasificación Nómina Personal Transitorio
    IF v_cta_transitorio_id IS NOT NULL THEN
        INSERT INTO contabilidad.matriz_conversion_regla (
            mcr_matriz_id, mcr_clave, mcr_descripcion, mcr_prioridad,
            mcr_cog_id, mcr_tipo_gasto, mcr_nivel_afectacion, mcr_tipo_proveedor_id,
            mcr_procedimiento_codigo, mcr_evento_codigo,
            mcr_tipo_operacion, mcr_perfil,
            mcr_clasificacion_estado, mcr_clasificacion_motivo,
            mcr_es_predeterminada, estatus_registro, usuario_c, fecha_c
        ) VALUES (
            v_matriz_id,
            'R_OP_NOMINA_TRANSITORIO',
            'Reclasificación Nómina Transitoria: 2.1.1.9.1000.0001 a 2.1.1.1.2000.0001',
            100,
            329, -- COG 12200001 Sueldos base al personal eventual
            1,
            'EMPLEADO',
            0,
            'NOMINA',
            'RECLASIFICACION_OP',
            'DEVENGAR_NOMINA',
            'EGRESO',
            'DETERMINADA',
            'Reclasificación de pasivo concentrador a personal transitorio.',
            0,
            1,
            'MIGRACION_180',
            clock_timestamp()
        ) ON CONFLICT (mcr_matriz_id, mcr_clave) DO UPDATE
          SET mcr_descripcion = EXCLUDED.mcr_descripcion,
              mcr_cog_id = EXCLUDED.mcr_cog_id,
              mcr_procedimiento_codigo = EXCLUDED.mcr_procedimiento_codigo,
              mcr_evento_codigo = EXCLUDED.mcr_evento_codigo,
              usuario_m = 'MIGRACION_180',
              fecha_m = clock_timestamp()
        RETURNING mcr_id INTO v_regla_id;

        DELETE FROM contabilidad.matriz_conversion_movimiento WHERE mcm_regla_id = v_regla_id;

        INSERT INTO contabilidad.matriz_conversion_movimiento (
            mcm_regla_id, mcm_orden, mcm_ambito, mcm_naturaleza, mcm_origen_cuenta,
            mcm_cuenta_id, mcm_formula_importe, mcm_descripcion, mcm_es_obligatorio,
            estatus_registro, usuario_c, fecha_c
        ) VALUES (
            v_regla_id, 1, 'C', 'D', 'FIJA',
            v_cta_puente_id, 'NETO_PAGAR',
            'Cancelación pasivo concentrador nómina personal transitorio', 1,
            1, 'MIGRACION_180', clock_timestamp()
        ), (
            v_regla_id, 2, 'C', 'H', 'FIJA',
            v_cta_transitorio_id, 'NETO_PAGAR',
            'Reconocimiento pasivo líquido personal transitorio por pagar', 1,
            1, 'MIGRACION_180', clock_timestamp()
        );
    END IF;

    -- 7. Regla 3: Reclasificación Pensión Alimenticia Judicial
    IF v_cta_pension_id IS NOT NULL THEN
        INSERT INTO contabilidad.matriz_conversion_regla (
            mcr_matriz_id, mcr_clave, mcr_descripcion, mcr_prioridad,
            mcr_cog_id, mcr_tipo_gasto, mcr_nivel_afectacion, mcr_tipo_proveedor_id,
            mcr_procedimiento_codigo, mcr_evento_codigo,
            mcr_tipo_operacion, mcr_perfil,
            mcr_clasificacion_estado, mcr_clasificacion_motivo,
            mcr_es_predeterminada, estatus_registro, usuario_c, fecha_c
        ) VALUES (
            v_matriz_id,
            'R_OP_PENSION_ALIMENTICIA',
            'Reclasificación Pensión Alimenticia Judicial: 2.1.1.9.1000.0001 a 2.1.1.9.3000.0001',
            100,
            6, -- COG 11300001 Sueldos base
            1,
            'BENEFICIARIO_PENSION_ALIMENTICIA',
            0,
            'NOMINA',
            'RECLASIFICACION_OP',
            'DEVENGAR_NOMINA',
            'EGRESO',
            'DETERMINADA',
            'Reclasificación de pasivo concentrador por pensión alimenticia judicial.',
            0,
            1,
            'MIGRACION_180',
            clock_timestamp()
        ) ON CONFLICT (mcr_matriz_id, mcr_clave) DO UPDATE
          SET mcr_descripcion = EXCLUDED.mcr_descripcion,
              mcr_cog_id = EXCLUDED.mcr_cog_id,
              mcr_procedimiento_codigo = EXCLUDED.mcr_procedimiento_codigo,
              mcr_evento_codigo = EXCLUDED.mcr_evento_codigo,
              usuario_m = 'MIGRACION_180',
              fecha_m = clock_timestamp()
        RETURNING mcr_id INTO v_regla_id;

        DELETE FROM contabilidad.matriz_conversion_movimiento WHERE mcm_regla_id = v_regla_id;

        INSERT INTO contabilidad.matriz_conversion_movimiento (
            mcm_regla_id, mcm_orden, mcm_ambito, mcm_naturaleza, mcm_origen_cuenta,
            mcm_cuenta_id, mcm_formula_importe, mcm_descripcion, mcm_es_obligatorio,
            estatus_registro, usuario_c, fecha_c
        ) VALUES (
            v_regla_id, 1, 'C', 'D', 'FIJA',
            v_cta_puente_id, 'NETO_PAGAR',
            'Cancelación pasivo concentrador nómina por pensión alimenticia', 1,
            1, 'MIGRACION_180', clock_timestamp()
        ), (
            v_regla_id, 2, 'C', 'H', 'FIJA',
            v_cta_pension_id, 'NETO_PAGAR',
            'Reconocimiento pasivo exigible para beneficiarias de pensión alimenticia', 1,
            1, 'MIGRACION_180', clock_timestamp()
        );
    END IF;

    -- 8. Activar la Matriz una vez configuradas todas sus reglas y movimientos
    UPDATE contabilidad.matriz_conversion
       SET mcv_estado = 'ACTIVA',
           usuario_m = 'MIGRACION_180',
           fecha_m = clock_timestamp()
     WHERE mcv_id = v_matriz_id;

    RAISE NOTICE 'Migración 180 ejecutada con éxito. Matriz de Reclasificación ID: %, Reglas y Movimientos creados y Matriz ACTIVA.', v_matriz_id;
END;
$$;
