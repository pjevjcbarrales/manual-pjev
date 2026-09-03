-- Migration 179: Actualizar cuenta de abono en Matriz A.1 (Devengado) para el Capítulo 1000 hacia la cuenta puente concentradora 2.1.1.9.1000.0001
-- Propósito: Desacoplar el reconocimiento del gasto devengado de la dispersión neta.
-- En el devengo del Capítulo 1000 (Servicios Personales / Nómina), el pasivo se reconoce en la cuenta puente concentradora
-- '2.1.1.9.1000.0001 OTRAS CUENTAS POR PAGAR VARIAS', permitiendo que en la Orden de Pago (05.2.2) se reclasifique
-- hacia las cuentas exigibles '2.1.1.1.xxxx Remuneraciones por Pagar' para su posterior liquidación bancaria en Tesorería (06.2.1).

DO $$
DECLARE
    v_cuenta_puente_id INTEGER;
    v_actualizados INTEGER := 0;
BEGIN
    -- 1. Obtener ID de la cuenta puente 2.1.1.9.1000.0001
    SELECT cc_id INTO v_cuenta_puente_id
      FROM contabilidad.catalogo_cuentas
     WHERE cc_cuentapuntos = '2.1.1.9.1000.0001'
       AND estatus_registro = 1
     LIMIT 1;

    IF v_cuenta_puente_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró la cuenta 2.1.1.9.1000.0001 en contabilidad.catalogo_cuentas.';
    END IF;

    -- 2. Actualizar los movimientos de abono contable (Haber) en todas las reglas del Capítulo 1000 de Matriz A.1 (mcv_id = 12)
    UPDATE contabilidad.matriz_conversion_movimiento mcm
       SET mcm_cuenta_id = v_cuenta_puente_id,
           mcm_origen_cuenta = 'FIJA',
           mcm_descripcion = 'Reconocimiento pasivo concentrador nómina en cuenta puente (Nómina por Liquidar)',
           usuario_m = 'MIGRACION_179',
           fecha_m = clock_timestamp()
      FROM contabilidad.matriz_conversion_regla mcr
     WHERE mcm.mcm_regla_id = mcr.mcr_id
       AND mcr.mcr_matriz_id = 12
       AND mcr.mcr_clave LIKE 'R_A1_1%'
       AND mcm.mcm_ambito = 'C'
       AND mcm.mcm_naturaleza = 'H';

    GET DIAGNOSTICS v_actualizados = ROW_COUNT;
    RAISE NOTICE 'Migración 179 ejecutada con éxito. Total movimientos de abono actualizados a 2.1.1.9.1000.0001: %', v_actualizados;
END;
$$;
