import json

html_content = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>02.1.4 Registro de contrato</title>
<link rel="stylesheet" href="../shared.css">
<style>
  body { padding: 36px 44px 80px; background: var(--pjev-crema); }
  .mod-header-badges { display:flex; gap:8px; margin-top:10px; flex-wrap:wrap; }
  .mod-badge { font-size:10px; font-weight:700; padding:3px 10px; border-radius:10px; }
  .badge-c { background:#f3e8ff; color:#6b21a8; border:1px solid #d8b4fe; }
  
  .wireframe-tabs { display:flex; gap:4px; margin-bottom:12px; flex-wrap:wrap; }
  .wf-tab { padding:6px 14px; font-size:11px; font-weight:600; border-radius:5px; border:1px solid var(--pjev-borde); background:var(--pjev-blanco); cursor:pointer; color:var(--pjev-texto-muted); transition:all 0.15s; }
  .wf-tab.active { background:var(--pjev-verde-oscuro); color:#fff; border-color:var(--pjev-verde-oscuro); }
  .wf-panel { display:none; }
  .wf-panel.active { display:block; }
  .wf-box { border:1px solid var(--pjev-borde); border-radius:8px; overflow:hidden; background:var(--pjev-blanco); }
  .wf-bar { background:var(--pjev-blanco); border-bottom:1px solid var(--pjev-borde); padding:8px 14px; display:flex; align-items:center; justify-content:space-between; }
  .wf-bar-label { font-size:11px; font-weight:600; color:var(--pjev-texto-muted); text-transform:uppercase; letter-spacing:0.8px; }
  .wf-svg-area { background:#f9f9f9; padding:16px; overflow-x:auto; text-align:center; }
  
  .sp-tabs { display: flex; gap: 8px; border-bottom: 2px solid var(--pjev-gris-borde); margin-bottom: 15px; }
  .sp-tab { padding: 8px 16px; border: none; background: transparent; cursor: pointer; color: var(--pjev-texto-muted); font-size: 13px; font-weight: bold; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 0.2s; }
  .sp-tab:hover { color: var(--pjev-verde-oscuro); }
  .sp-tab.active { color: var(--pjev-verde-oscuro); border-bottom-color: var(--pjev-verde-oscuro); }
  .sp-panel { display: none; }
  .sp-panel.active { display: block; animation: fadeIn 0.3s ease; }
</style>
</head>
<body>
<div class="doc-main-inner">

    <div class="elem-breadcrumb">
      <a href="../index.html">Inicio</a> ›
      <span>Análisis Funcional</span> ›
      <span>02.1.4 Registro de contrato</span>
    </div>

    <div class="elem-header">
      <div>
        <div class="elem-id">02.1.4</div>
        <h1 class="elem-title">Registro de contrato</h1>
        <p class="elem-desc">Análisis Funcional, Reglas de Negocio y Diseño de Interfaces.</p>
        <div class="mod-header-badges">
          <span class="mod-badge badge-c">Tipo: Formulario Compuesto (Maestro-Detalle)</span>
        </div>
      </div>
    </div>

    <!-- 1. Descripción General -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">1</span> Descripción General</div>
      <p>El submódulo "Registro de contrato" tiene como objetivo el control, captura y seguimiento administrativo-legal de los contratos celebrados por el Instituto (ya sea derivados de un procedimiento de licitación/adjudicación o de forma directa). Su función principal es consolidar la información legal, montos, garantías, vigencias y la vinculación preparatoria de los Oficios de Reserva, actuando como la antesala normativa indispensable para la posterior formalización contable del compromiso.</p>
    </div>

    <!-- 2. Marco Normativo -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">2</span> Marco Normativo (SIAF / CONAC)</div>
      <ul>
        <li><strong>LGCG (Art. 46):</strong> Exige mantener un padrón detallado de contratos y convenios que soporten el ejercicio del gasto.</li>
        <li><strong>Ley de Seguros y de Fianzas (Art. 166):</strong> Sustento normativo para exigir, calcular y validar que la póliza de garantía de cumplimiento corresponda estrictamente al 10% del contrato (sin IVA).</li>
        <li><strong>Transparencia:</strong> Mantenimiento de información pública estandarizada para dar cumplimiento a las obligaciones de transparencia (Portal del INAI y locales).</li>
      </ul>
    </div>

    <!-- 3. Roles que intervienen -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">3</span> Roles que intervienen</div>
      <table class="props-table">
        <thead>
          <tr>
            <th>Rol</th>
            <th>Acción permitida</th>
            <th>Restricción</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Director de RM</td>
            <td>Aprobar/rechazar registros, firmar electrónicamente.</td>
            <td>No puede alterar información de la póliza comprometida si esta ya fue validada por Contabilidad.</td>
          </tr>
          <tr>
            <td>Jefe de Contratos</td>
            <td>Alta, baja, cambio, consulta e impresión de contratos. Carga de garantías.</td>
            <td>Solo puede editar si el id_poliza_comprometido es NULL (es decir, no se ha comprometido).</td>
          </tr>
          <tr>
            <td>Analista de Contratos</td>
            <td>Borradores de contratos. Carga de detalles.</td>
            <td>No puede firmar electrónicamente.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 4. Modelo de Datos -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">4</span> Modelo de Datos (Maestro-Detalle)</div>
      
      <p style="font-size:13px; color:var(--pjev-texto-muted); margin-bottom:10px;">Cabecera (Master): <strong><code>recursos_materiales.cat_contratos</code></strong></p>
      <table class="props-table" style="margin-bottom:20px;">
        <thead><tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr></thead>
        <tbody>
          <tr><td><code>id_contrato</code></td><td><code>INT (PK)</code></td><td>Identificador único del contrato.</td></tr>
          <tr><td><code>numero_contrato</code></td><td><code>VARCHAR(50)</code></td><td>Folio / Número oficial del contrato.</td></tr>
          <tr><td><code>fecha_contrato</code></td><td><code>DATE</code></td><td>Fecha de celebración.</td></tr>
          <tr><td><code>tipo_contrato</code></td><td><code>VARCHAR(20)</code></td><td>A = Abierto, C = Cerrado.</td></tr>
          <tr><td><code>id_proveedor</code></td><td><code>INT (FK)</code></td><td>Identificador del proveedor adjudicado.</td></tr>
          <tr><td><code>id_procedimiento</code></td><td><code>INT (FK)</code></td><td>Procedimiento de licitación o adjudicación del que deriva.</td></tr>
          <tr><td><code>descripcion_contrato</code></td><td><code>TEXT</code></td><td>Objeto del contrato.</td></tr>
          <tr><td><code>monto_minimo</code></td><td><code>NUMERIC(18,2)</code></td><td>Para contratos abiertos. Subtotal sin IVA.</td></tr>
          <tr><td><code>monto_minimo_iva</code></td><td><code>NUMERIC(18,2)</code></td><td>IVA del monto mínimo.</td></tr>
          <tr><td><code>monto_minimo_total</code></td><td><code>NUMERIC(18,2)</code></td><td>Total mínimo (con IVA).</td></tr>
          <tr><td><code>monto_maximo</code></td><td><code>NUMERIC(18,2)</code></td><td>Para contratos cerrados y abiertos. Subtotal sin IVA.</td></tr>
          <tr><td><code>monto_maximo_iva</code></td><td><code>NUMERIC(18,2)</code></td><td>IVA del monto máximo.</td></tr>
          <tr><td><code>monto_maximo_total</code></td><td><code>NUMERIC(18,2)</code></td><td>Total máximo (con IVA).</td></tr>
          <tr><td><code>vigencia_inicio</code></td><td><code>DATE</code></td><td>Inicio de la vigencia.</td></tr>
          <tr><td><code>vigencia_fin</code></td><td><code>DATE</code></td><td>Fin de la vigencia.</td></tr>
          <tr><td><code>tiene_garantia_cumplimiento</code></td><td><code>BOOLEAN</code></td><td>Indica si aplica garantía de cumplimiento.</td></tr>
          <tr><td><code>monto_garantia_cumplimiento</code></td><td><code>NUMERIC(18,2)</code></td><td>10% del monto_maximo.</td></tr>
          <tr><td><code>fecha_entrega_garantia</code></td><td><code>DATE</code></td><td>Fecha en la que el proveedor entregó la fianza.</td></tr>
          <tr><td><code>id_poliza_comprometido</code></td><td><code>INT</code></td><td>ID de la póliza contable (Módulo de compromisos). <strong>[Read-Only para Contratos]</strong></td></tr>
          <tr><td><code>usuario_captura</code></td><td><code>VARCHAR(20)</code></td><td>Auditoría: Usuario que creó.</td></tr>
          <tr><td><code>fecha_captura</code></td><td><code>TIMESTAMP</code></td><td>Auditoría: Fecha de creación.</td></tr>
          <tr><td><code>usuario_modificacion</code></td><td><code>VARCHAR(20)</code></td><td>Auditoría: Usuario que modificó.</td></tr>
          <tr><td><code>fecha_modificacion</code></td><td><code>TIMESTAMP</code></td><td>Auditoría: Fecha de modificación.</td></tr>
        </tbody>
      </table>

      <p style="font-size:13px; color:var(--pjev-texto-muted); margin-bottom:10px;">Detalles (Detail): <strong><code>recursos_materiales.cat_contrato_detalle</code></strong></p>
      <table class="props-table" style="margin-bottom:20px;">
        <thead><tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr></thead>
        <tbody>
          <tr><td><code>id_contrato_detalle</code></td><td><code>INT (PK)</code></td><td>Identificador único del detalle.</td></tr>
          <tr><td><code>id_contrato</code></td><td><code>INT (FK)</code></td><td>Relación con la cabecera.</td></tr>
          <tr><td><code>id_oficio_reserva</code></td><td><code>INT (FK)</code></td><td>Vínculo con Suficiencia Presupuestal.</td></tr>
          <tr><td><code>id_partida</code></td><td><code>INT (FK)</code></td><td>Partida específica (COG).</td></tr>
          <tr><td><code>id_centro_costo</code></td><td><code>INT (FK)</code></td><td>Área responsable / solicitante.</td></tr>
          <tr><td><code>monto_detalle</code></td><td><code>NUMERIC(18,2)</code></td><td>Subtotal asignado a este detalle.</td></tr>
          <tr><td><code>iva_detalle</code></td><td><code>NUMERIC(18,2)</code></td><td>IVA del detalle.</td></tr>
          <tr><td><code>total_detalle</code></td><td><code>NUMERIC(18,2)</code></td><td>Total con IVA del detalle.</td></tr>
          <tr><td><code>usuario_captura</code>, <code>fecha_captura</code>, <code>usuario_modificacion</code>, <code>fecha_modificacion</code></td><td><code>AUDIT</code></td><td>Campos estándar de auditoría de creación y actualización.</td></tr>
        </tbody>
      </table>

      <p style="font-size:13px; color:var(--pjev-texto-muted); margin-bottom:10px;">Historial de Firmas: <strong><code>recursos_materiales.cat_contrato_historial_firmas</code></strong></p>
      <table class="props-table">
        <thead><tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr></thead>
        <tbody>
          <tr><td><code>id_firma</code></td><td><code>INT (PK)</code></td><td>Identificador de la firma.</td></tr>
          <tr><td><code>id_contrato</code></td><td><code>INT (FK)</code></td><td>Contrato firmado.</td></tr>
          <tr><td><code>usuario_firma</code></td><td><code>VARCHAR(50)</code></td><td>Usuario que realizó la firma.</td></tr>
          <tr><td><code>fecha_firma</code></td><td><code>TIMESTAMP</code></td><td>Momento exacto de la firma electrónica.</td></tr>
          <tr><td><code>cadena_original</code></td><td><code>TEXT</code></td><td>Cadena de validación criptográfica.</td></tr>
          <tr><td><code>usuario_captura</code>, <code>fecha_captura</code>, <code>usuario_modificacion</code>, <code>fecha_modificacion</code></td><td><code>AUDIT</code></td><td>Campos estándar de auditoría de creación y actualización.</td></tr>
        </tbody>
      </table>
    </div>

    <!-- 5. Stored Procedures -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">5</span> Stored Procedures (SPs)</div>
      
      <div class="sp-tabs">
        <button class="sp-tab active" onclick="showSP('sp1',this)">fn_leer_contratos</button>
        <button class="sp-tab" onclick="showSP('sp2',this)">fn_abc_contratos</button>
      </div>

      <!-- TAB 1: LEER CONTRATOS -->
      <div id="sp-sp1" class="sp-panel active">
        <table class="props-table">
          <thead><tr><th>Parámetros de Entrada (IN)</th><th>Tipo</th><th>Descripción</th></tr></thead>
          <tbody>
            <tr><td><code>@p_accion</code></td><td><code>INT</code></td><td>0: Leer Maestro, 1: Leer Detalle, 2: Leer Maestro+Detalle</td></tr>
            <tr><td><code>@p_id_contrato</code></td><td><code>INT</code></td><td>Null/0 para listado, >0 para registro único</td></tr>
            <tr><td><code>@p_numero_contrato</code></td><td><code>VARCHAR</code></td><td>Filtro de búsqueda por folio</td></tr>
            <tr><td><code>@p_id_proveedor</code></td><td><code>INT</code></td><td>Filtro de búsqueda por proveedor</td></tr>
          </tbody>
        </table>
        <h3 style="font-size: 13px; color: var(--pjev-verde-oscuro); margin-top: 20px; margin-bottom: 8px;">Definición SQL (PostgreSQL)</h3>
        <div class="code-wrap" style="margin-top: 0; max-height: 400px; overflow-y: auto;">
          <div class="code-block">
<pre><span style="color:#5c6370;">-- ==========================================
-- 1. LEER CONTRATOS
-- ==========================================</span>
CREATE OR REPLACE FUNCTION recursos_materiales.fn_leer_contratos(
    p_accion integer,
    p_id_contrato integer DEFAULT NULL,
    p_numero_contrato varchar DEFAULT NULL,
    p_id_proveedor integer DEFAULT NULL
) RETURNS jsonb LANGUAGE plpgsql AS $$
DECLARE v_resultado jsonb;
BEGIN
    IF p_accion = 0 THEN
        IF p_id_contrato > 0 THEN
            SELECT row_to_json(c) INTO v_resultado 
            FROM recursos_materiales.cat_contratos c 
            WHERE c.id_contrato = p_id_contrato;
        ELSE
            SELECT jsonb_build_object('registros', COALESCE(jsonb_agg(row_to_json(t)), '[]'::jsonb)) INTO v_resultado
            FROM (
                SELECT c.*, p.razon_social as proveedor_nombre 
                FROM recursos_materiales.cat_contratos c
                LEFT JOIN proveedores p ON c.id_proveedor = p.id_proveedor
                WHERE (p_numero_contrato IS NULL OR c.numero_contrato ILIKE '%' || p_numero_contrato || '%')
                  AND (p_id_proveedor IS NULL OR c.id_proveedor = p_id_proveedor)
            ) t;
        END IF;
    ELSIF p_accion = 1 THEN
        SELECT jsonb_build_object('registros', COALESCE(jsonb_agg(row_to_json(d)), '[]'::jsonb)) INTO v_resultado
        FROM recursos_materiales.cat_contrato_detalle d
        WHERE d.id_contrato = p_id_contrato;
    END IF;
    RETURN jsonb_build_object('cod_resultado', 0, 'msg_resultado', 'OK', 'data', v_resultado);
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object('cod_resultado', -2, 'msg_resultado', SQLERRM, 'data', NULL);
END;
$$;</pre>
          </div>
        </div>
      </div>

      <!-- TAB 2: ABC CONTRATOS -->
      <div id="sp-sp2" class="sp-panel">
        <table class="props-table">
          <thead><tr><th>Parámetros de Entrada (IN)</th><th>Tipo</th><th>Descripción</th></tr></thead>
          <tbody>
            <tr><td><code>@p_accion</code></td><td><code>INT</code></td><td>1: Alta, 2: Modificación, 3: Baja Lógica</td></tr>
            <tr><td><code>@p_usuario</code></td><td><code>VARCHAR</code></td><td>Usuario activo (Auditoría)</td></tr>
            <tr><td><code>@p_json_contrato</code></td><td><code>JSONB</code></td><td>Cabecera (Monto, Vigencia, etc)</td></tr>
            <tr><td><code>@p_json_detalles</code></td><td><code>JSONB</code></td><td>Arreglo con los detalles contables del contrato</td></tr>
          </tbody>
        </table>
        <h3 style="font-size: 13px; color: var(--pjev-verde-oscuro); margin-top: 20px; margin-bottom: 8px;">Definición SQL (PostgreSQL) - SIN ABSTRACCIONES</h3>
        <div class="code-wrap" style="margin-top: 0; max-height: 400px; overflow-y: auto;">
          <div class="code-block">
<pre><span style="color:#5c6370;">-- ==========================================
-- 2. ABC CONTRATOS (CABECERA Y DETALLE EN UNA TRANSACCIÓN)
-- ==========================================</span>
CREATE OR REPLACE FUNCTION recursos_materiales.fn_abc_contratos(
    p_accion integer,
    p_usuario varchar,
    p_json_contrato jsonb,
    p_json_detalles jsonb DEFAULT '[]'::jsonb
) RETURNS jsonb LANGUAGE plpgsql AS $$
DECLARE 
    v_id_contrato integer;
    v_detalle jsonb;
    v_poliza_comprometido integer;
BEGIN
    -- Validar si ya está comprometido (Solo en UPDATE / DELETE)
    IF p_accion IN (2, 3) THEN
        v_id_contrato := (p_json_contrato->>'id_contrato')::integer;
        SELECT id_poliza_comprometido INTO v_poliza_comprometido FROM recursos_materiales.cat_contratos WHERE id_contrato = v_id_contrato;
        IF v_poliza_comprometido IS NOT NULL THEN
            RETURN jsonb_build_object('cod_resultado', -1, 'msg_resultado', 'No se puede modificar un contrato que ya cuenta con póliza comprometida.', 'data', NULL);
        END IF;
    END IF;

    IF p_accion = 1 THEN
        -- Insertar Cabecera
        INSERT INTO recursos_materiales.cat_contratos (
            numero_contrato, fecha_contrato, tipo_contrato, id_proveedor, id_procedimiento,
            descripcion_contrato, monto_minimo, monto_minimo_iva, monto_minimo_total,
            monto_maximo, monto_maximo_iva, monto_maximo_total, vigencia_inicio, vigencia_fin,
            tiene_garantia_cumplimiento, monto_garantia_cumplimiento, fecha_entrega_garantia,
            usuario_captura, fecha_captura
        ) VALUES (
            p_json_contrato->>'numero_contrato', (p_json_contrato->>'fecha_contrato')::date, p_json_contrato->>'tipo_contrato',
            (p_json_contrato->>'id_proveedor')::integer, (p_json_contrato->>'id_procedimiento')::integer,
            p_json_contrato->>'descripcion_contrato', (p_json_contrato->>'monto_minimo')::numeric, 
            (p_json_contrato->>'monto_minimo_iva')::numeric, (p_json_contrato->>'monto_minimo_total')::numeric,
            (p_json_contrato->>'monto_maximo')::numeric, (p_json_contrato->>'monto_maximo_iva')::numeric, 
            (p_json_contrato->>'monto_maximo_total')::numeric, (p_json_contrato->>'vigencia_inicio')::date, 
            (p_json_contrato->>'vigencia_fin')::date, (p_json_contrato->>'tiene_garantia_cumplimiento')::boolean, 
            (p_json_contrato->>'monto_garantia_cumplimiento')::numeric, (p_json_contrato->>'fecha_entrega_garantia')::date,
            p_usuario, current_timestamp
        ) RETURNING id_contrato INTO v_id_contrato;
        
        -- Insertar Detalles (Loop completo, literal)
        FOR v_detalle IN SELECT * FROM jsonb_array_elements(p_json_detalles)
        LOOP
            INSERT INTO recursos_materiales.cat_contrato_detalle (
                id_contrato, id_oficio_reserva, id_partida, id_centro_costo,
                monto_detalle, iva_detalle, total_detalle, usuario_captura, fecha_captura
            ) VALUES (
                v_id_contrato, (v_detalle->>'id_oficio_reserva')::integer, (v_detalle->>'id_partida')::integer, (v_detalle->>'id_centro_costo')::integer,
                (v_detalle->>'monto_detalle')::numeric, (v_detalle->>'iva_detalle')::numeric, (v_detalle->>'total_detalle')::numeric,
                p_usuario, current_timestamp
            );
        END LOOP;
        
    ELSIF p_accion = 2 THEN
        -- Modificar Cabecera
        UPDATE recursos_materiales.cat_contratos SET
            numero_contrato = p_json_contrato->>'numero_contrato',
            fecha_contrato = (p_json_contrato->>'fecha_contrato')::date,
            tipo_contrato = p_json_contrato->>'tipo_contrato',
            id_proveedor = (p_json_contrato->>'id_proveedor')::integer,
            id_procedimiento = (p_json_contrato->>'id_procedimiento')::integer,
            descripcion_contrato = p_json_contrato->>'descripcion_contrato',
            monto_minimo = (p_json_contrato->>'monto_minimo')::numeric,
            monto_minimo_iva = (p_json_contrato->>'monto_minimo_iva')::numeric,
            monto_minimo_total = (p_json_contrato->>'monto_minimo_total')::numeric,
            monto_maximo = (p_json_contrato->>'monto_maximo')::numeric,
            monto_maximo_iva = (p_json_contrato->>'monto_maximo_iva')::numeric,
            monto_maximo_total = (p_json_contrato->>'monto_maximo_total')::numeric,
            vigencia_inicio = (p_json_contrato->>'vigencia_inicio')::date,
            vigencia_fin = (p_json_contrato->>'vigencia_fin')::date,
            tiene_garantia_cumplimiento = (p_json_contrato->>'tiene_garantia_cumplimiento')::boolean,
            monto_garantia_cumplimiento = (p_json_contrato->>'monto_garantia_cumplimiento')::numeric,
            fecha_entrega_garantia = (p_json_contrato->>'fecha_entrega_garantia')::date,
            usuario_modificacion = p_usuario,
            fecha_modificacion = current_timestamp
        WHERE id_contrato = v_id_contrato;
        
        -- Actualización de Detalles (Borrado y Re-inserción)
        DELETE FROM recursos_materiales.cat_contrato_detalle WHERE id_contrato = v_id_contrato;
        FOR v_detalle IN SELECT * FROM jsonb_array_elements(p_json_detalles)
        LOOP
            INSERT INTO recursos_materiales.cat_contrato_detalle (
                id_contrato, id_oficio_reserva, id_partida, id_centro_costo,
                monto_detalle, iva_detalle, total_detalle, usuario_captura, fecha_captura
            ) VALUES (
                v_id_contrato, (v_detalle->>'id_oficio_reserva')::integer, (v_detalle->>'id_partida')::integer, (v_detalle->>'id_centro_costo')::integer,
                (v_detalle->>'monto_detalle')::numeric, (v_detalle->>'iva_detalle')::numeric, (v_detalle->>'total_detalle')::numeric,
                p_usuario, current_timestamp
            );
        END LOOP;
        
    END IF;

    RETURN jsonb_build_object('cod_resultado', 0, 'msg_resultado', 'Guardado correctamente', 'data', jsonb_build_object('id_contrato', v_id_contrato));
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object('cod_resultado', -2, 'msg_resultado', SQLERRM);
END;
$$;</pre>
          </div>
        </div>
      </div>

    </div>

    <!-- 6. Servicios REST -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">6</span> Servicios REST</div>
      <table class="props-table">
        <thead><tr><th>Método</th><th>Endpoint</th><th>Descripción</th></tr></thead>
        <tbody>
          <tr><td><span class="method get">GET</span></td><td><code>/recursos_materiales/contratos</code></td><td>Llama a <code>fn_leer_contratos</code> (p_accion=0).</td></tr>
          <tr><td><span class="method post">POST</span> / <span class="method patch">PATCH</span></td><td><code>/recursos_materiales/contratos</code></td><td>Llama a <code>fn_abc_contratos</code> (p_accion=1 o 2).</td></tr>
          <tr><td><span class="method get">GET</span></td><td><code>/recursos_materiales/contratos/:id/detalles</code></td><td>Llama a <code>fn_leer_contratos</code> (p_accion=1).</td></tr>
        </tbody>
      </table>
    </div>

    <!-- 7. Acciones del Módulo -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">7</span> Acciones del Módulo</div>
      <ul style="font-size: 13px; color: var(--pjev-texto); padding-left: 20px;">
        <li style="margin-bottom: 8px;"><strong>Guardar contrato:</strong> Persiste la cabecera y el detalle contable en una sola transacción. Habilitado sólo si <code>id_poliza_comprometido</code> es nulo o vacío.</li>
        <li style="margin-bottom: 8px;"><strong>Ver PDF del Contrato:</strong> Genera la impresión de las cláusulas.</li>
        <li style="margin-bottom: 8px;"><strong>Firma Electrónica:</strong> Se despliega un modal donde el Director ingresa su e-firma; esta acción bloquea el contrato para modificaciones subsecuentes y estampa el certificado en la base de datos.</li>
      </ul>
    </div>

    <!-- 8. Diseño de Interfaces (UI) -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">8</span> Diseño de Interfaces (UI / Wireframes)</div>
      
      <div class="wireframe-tabs">
        <button class="wf-tab active" onclick="showWF('p1',this)">Pantalla Leer (Grilla)</button>
        <button class="wf-tab" onclick="showWF('p2',this)">Modal: Agregar Contrato (Vacío)</button>
        <button class="wf-tab" onclick="showWF('p3',this)">Modal: Editar Contrato (Con Valores)</button>
      </div>

      <!-- TAB 1: Pantalla Leer -->
      <div id="wf-p1" class="wf-panel active">
        <div class="wf-box">
          <div class="wf-bar"><span class="wf-bar-label">Listado Principal de Contratos</span></div>
          <div class="wf-svg-area">
            <svg viewBox="0 0 1000 400" xmlns="http://www.w3.org/2000/svg">
              <rect width="1000" height="400" fill="#f5f0e8" rx="4"/>
              
              <text x="20" y="30" font-size="16" font-weight="bold" fill="#183125">Catálogo de Contratos</text>
              <rect x="850" y="15" width="130" height="25" fill="#183125" rx="4"/>
              <text x="915" y="32" fill="#fff" font-size="11" text-anchor="middle" font-weight="bold">+ Nuevo Contrato</text>
              
              <rect x="20" y="60" width="960" height="60" fill="#fff" stroke="#d4c9b5" rx="4"/>
              <text x="35" y="80" font-size="10" fill="#5a5a5a">Folio del Contrato</text>
              <text x="200" y="80" font-size="10" fill="#5a5a5a">Proveedor</text>
              
              <rect x="35" y="88" width="150" height="20" fill="#fff" stroke="#ccc" rx="2"/>
              <text x="40" y="102" font-size="10" fill="#ccc">Ingresar número...</text>
              
              <rect x="200" y="88" width="200" height="20" fill="#fff" stroke="#ccc" rx="2"/>
              <text x="205" y="102" font-size="10" fill="#ccc">Seleccionar proveedor...</text>
              
              <rect x="420" y="88" width="80" height="20" fill="#183125" rx="2"/>
              <text x="460" y="102" fill="#fff" font-size="10" text-anchor="middle">Buscar</text>

              <rect x="20" y="140" width="960" height="240" fill="#fff" stroke="#d4c9b5" rx="4"/>
              <rect x="20" y="140" width="960" height="25" fill="#eef3ef"/>
              <text x="30" y="156" font-size="10" font-weight="bold" fill="#183125">FOLIO CONTRATO</text>
              <text x="180" y="156" font-size="10" font-weight="bold" fill="#183125">PROVEEDOR</text>
              <text x="400" y="156" font-size="10" font-weight="bold" fill="#183125">FECHA</text>
              <text x="500" y="156" font-size="10" font-weight="bold" fill="#183125">TIPO</text>
              <text x="580" y="156" font-size="10" font-weight="bold" fill="#183125">MONTO MÁX TOTAL</text>
              <text x="750" y="156" font-size="10" font-weight="bold" fill="#183125">ESTADO (COMPROMETIDO)</text>
              <text x="920" y="156" font-size="10" font-weight="bold" fill="#183125">ACCIONES</text>
              
              <!-- Row 1 -->
              <text x="30" y="180" font-size="11" fill="#333">PJEV-RM-001-2026</text>
              <text x="180" y="180" font-size="11" fill="#333">Computación Golfo S.A.</text>
              <text x="400" y="180" font-size="11" fill="#333">2026-06-01</text>
              <text x="500" y="180" font-size="11" fill="#333">Cerrado</text>
              <text x="580" y="180" font-size="11" fill="#333">$ 116,000.00</text>
              <rect x="750" y="170" width="70" height="15" fill="#edf8ef" stroke="#8fd19e" rx="7"/>
              <text x="785" y="181" font-size="8" fill="#166534" font-weight="bold" text-anchor="middle">COMPROMETIDO</text>
              <rect x="910" y="170" width="50" height="15" fill="#f3f3f3" rx="2" stroke="#ccc"/>
              <text x="935" y="181" font-size="9" fill="#333" text-anchor="middle">Ver</text>

              <!-- Row 2 -->
              <text x="30" y="210" font-size="11" fill="#333">PJEV-RM-002-2026</text>
              <text x="180" y="210" font-size="11" fill="#333">Papelería Centro</text>
              <text x="400" y="210" font-size="11" fill="#333">2026-06-15</text>
              <text x="500" y="210" font-size="11" fill="#333">Abierto</text>
              <text x="580" y="210" font-size="11" fill="#333">$ 58,000.00</text>
              <rect x="750" y="200" width="70" height="15" fill="#fffbeb" stroke="#f5d565" rx="7"/>
              <text x="785" y="211" font-size="8" fill="#854d0e" font-weight="bold" text-anchor="middle">PENDIENTE</text>
              <rect x="910" y="200" width="50" height="15" fill="#f3f3f3" rx="2" stroke="#ccc"/>
              <text x="935" y="211" font-size="9" fill="#333" text-anchor="middle">Editar</text>
              
            </svg>
          </div>
        </div>
      </div>

      <!-- TAB 2: Modal Agregar -->
      <div id="wf-p2" class="wf-panel">
        <div class="wf-box">
          <div class="wf-bar"><span class="wf-bar-label">Modal: Agregar Contrato (Vacío)</span></div>
          <div class="wf-svg-area">
            <svg viewBox="0 0 1000 650" xmlns="http://www.w3.org/2000/svg">
              <rect width="1000" height="650" fill="#000" opacity="0.3"/>
              
              <rect x="100" y="30" width="800" height="580" fill="#fff" rx="6"/>
              <text x="120" y="60" font-size="16" font-weight="bold" fill="#183125">Nuevo Contrato</text>
              <line x1="100" y1="75" x2="900" y2="75" stroke="#d4c9b5"/>
              
              <text x="120" y="100" font-size="12" fill="#5a5a5a">Folio / Número *</text>
              <rect x="120" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              
              <text x="370" y="100" font-size="12" fill="#5a5a5a">Fecha Contrato *</text>
              <rect x="370" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              
              <text x="620" y="100" font-size="12" fill="#5a5a5a">Tipo *</text>
              <rect x="620" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>

              <text x="120" y="150" font-size="12" fill="#5a5a5a">Proveedor *</text>
              <rect x="120" y="155" width="350" height="24" fill="#fff" stroke="#ccc" rx="3"/>

              <text x="490" y="150" font-size="12" fill="#5a5a5a">Procedimiento Origen *</text>
              <rect x="490" y="155" width="360" height="24" fill="#fff" stroke="#ccc" rx="3"/>

              <text x="120" y="200" font-size="12" fill="#5a5a5a">Objeto / Descripción *</text>
              <rect x="120" y="205" width="730" height="40" fill="#fff" stroke="#ccc" rx="3"/>
              
              <line x1="120" y1="260" x2="850" y2="260" stroke="#eee"/>
              
              <text x="120" y="280" font-size="14" font-weight="bold" fill="#183125">Importes Generales (Sin IVA)</text>
              
              <text x="120" y="310" font-size="12" fill="#5a5a5a">Monto Mínimo</text>
              <rect x="120" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              
              <text x="370" y="310" font-size="12" fill="#5a5a5a">Monto Máximo *</text>
              <rect x="370" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>

              <line x1="120" y1="360" x2="850" y2="360" stroke="#eee"/>

              <text x="120" y="380" font-size="14" font-weight="bold" fill="#183125">Detalle Presupuestal</text>
              <rect x="120" y="400" width="730" height="120" fill="#f9f9f9" stroke="#ddd" rx="4"/>
              <text x="130" y="420" font-size="11" fill="#666" font-weight="bold">ID OFICIO RESERVA | PARTIDA | MONTO | IVA | TOTAL</text>
              <text x="480" y="460" font-size="11" fill="#999" text-anchor="middle">No hay detalles registrados...</text>
              
              <rect x="730" y="560" width="120" height="30" fill="#183125" rx="4"/>
              <text x="790" y="579" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Guardar</text>
              <text x="680" y="579" fill="#183125" font-size="12" text-anchor="middle">Cancelar</text>
            </svg>
          </div>
        </div>
      </div>

      <!-- TAB 3: Modal Editar -->
      <div id="wf-p3" class="wf-panel">
        <div class="wf-box">
          <div class="wf-bar"><span class="wf-bar-label">Modal: Editar Contrato (Poblado)</span></div>
          <div class="wf-svg-area">
            <svg viewBox="0 0 1000 650" xmlns="http://www.w3.org/2000/svg">
              <rect width="1000" height="650" fill="#000" opacity="0.3"/>
              
              <rect x="100" y="30" width="800" height="580" fill="#fff" rx="6"/>
              <text x="120" y="60" font-size="16" font-weight="bold" fill="#183125">Editar Contrato: PJEV-RM-002-2026</text>
              <line x1="100" y1="75" x2="900" y2="75" stroke="#d4c9b5"/>
              
              <text x="120" y="100" font-size="12" fill="#5a5a5a">Folio / Número *</text>
              <rect x="120" y="105" width="230" height="24" fill="#f0ede6" stroke="#ccc" rx="3"/>
              <text x="130" y="122" font-size="11" fill="#333">PJEV-RM-002-2026</text>
              
              <text x="370" y="100" font-size="12" fill="#5a5a5a">Fecha Contrato *</text>
              <rect x="370" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="380" y="122" font-size="11" fill="#333">2026-06-15</text>
              
              <text x="620" y="100" font-size="12" fill="#5a5a5a">Tipo *</text>
              <rect x="620" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="630" y="122" font-size="11" fill="#333">A - Abierto</text>

              <text x="120" y="150" font-size="12" fill="#5a5a5a">Proveedor *</text>
              <rect x="120" y="155" width="350" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="172" font-size="11" fill="#333">Papelería Centro</text>

              <text x="490" y="150" font-size="12" fill="#5a5a5a">Procedimiento Origen *</text>
              <rect x="490" y="155" width="360" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="500" y="172" font-size="11" fill="#333">Licitación LPN-002-2026</text>

              <text x="120" y="200" font-size="12" fill="#5a5a5a">Objeto / Descripción *</text>
              <rect x="120" y="205" width="730" height="40" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="222" font-size="11" fill="#333">Adquisición de insumos de papelería general.</text>
              
              <line x1="120" y1="260" x2="850" y2="260" stroke="#eee"/>
              
              <text x="120" y="280" font-size="14" font-weight="bold" fill="#183125">Importes Generales (Sin IVA)</text>
              
              <text x="120" y="310" font-size="12" fill="#5a5a5a">Monto Mínimo</text>
              <rect x="120" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="332" font-size="11" fill="#333">20,000.00</text>
              
              <text x="370" y="310" font-size="12" fill="#5a5a5a">Monto Máximo *</text>
              <rect x="370" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="380" y="332" font-size="11" fill="#333">50,000.00</text>
              
              <text x="620" y="310" font-size="12" fill="#5a5a5a">Garantía (10%)</text>
              <rect x="620" y="315" width="230" height="24" fill="#f0ede6" stroke="#ccc" rx="3"/>
              <text x="630" y="332" font-size="11" fill="#333">5,000.00</text>

              <line x1="120" y1="360" x2="850" y2="360" stroke="#eee"/>

              <text x="120" y="380" font-size="14" font-weight="bold" fill="#183125">Detalle Presupuestal</text>
              <rect x="120" y="400" width="730" height="120" fill="#fff" stroke="#ccc" rx="4"/>
              <rect x="120" y="400" width="730" height="25" fill="#f0f0f0" rx="4"/>
              <text x="130" y="416" font-size="10" fill="#333" font-weight="bold">ID OFICIO RESERVA | PARTIDA | MONTO | IVA | TOTAL | ACCIÓN</text>
              
              <!-- Fila Detalle -->
              <text x="130" y="440" font-size="11" fill="#333">OR-2026-05</text>
              <text x="260" y="440" font-size="11" fill="#333">21101 - Mat. y Útiles</text>
              <text x="400" y="440" font-size="11" fill="#333">50,000.00</text>
              <text x="500" y="440" font-size="11" fill="#333">8,000.00</text>
              <text x="600" y="440" font-size="11" fill="#333">58,000.00</text>
              <text x="730" y="440" font-size="10" fill="#991B1B">Eliminar</text>

              <!-- Agregar fila btn -->
              <rect x="130" y="480" width="120" height="24" fill="#fff" stroke="#183125" rx="3"/>
              <text x="190" y="496" fill="#183125" font-size="11" text-anchor="middle">+ Agregar Renglón</text>
              
              <rect x="730" y="560" width="120" height="30" fill="#183125" rx="4"/>
              <text x="790" y="579" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Guardar</text>
              <text x="680" y="579" fill="#183125" font-size="12" text-anchor="middle">Cancelar</text>
            </svg>
          </div>
        </div>
      </div>

    </div>

    <!-- 9. Reglas de Negocio -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">9</span> Reglas de Negocio Especiales</div>
      <ul>
        <li><strong>Restricción del 40% (Contratos Abiertos):</strong> <code>monto_minimo</code> no debe ser mayor al 40% del <code>monto_maximo</code>, de acuerdo con la validación de control interno. El formulario debe notificar y bloquear la captura si esto ocurre.</li>
        <li><strong>Fianza de Cumplimiento:</strong> Si <code>tiene_garantia_cumplimiento</code> es Verdadero, entonces <code>monto_garantia_cumplimiento</code> equivale automáticamente y sin excepción al 10% de <code>monto_maximo</code> (sin IVA incluido). Es un campo Read-Only o de auto-cálculo.</li>
        <li><strong>Bloqueo por Compromiso:</strong> Si <code>id_poliza_comprometido</code> NO ES NULO, la pantalla debe ser completamente inhabilitada para el Jefe de Contratos (modo "Sólo Lectura").</li>
      </ul>
    </div>

    <!-- 10. Validaciones de Interfaz -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">10</span> Validaciones de Interfaz</div>
      <ul>
        <li>Carga asíncrona (AJAX) al escribir el <code>id_proveedor</code> para traer su Razón Social de inmediato.</li>
        <li>El <code>id_oficio_reserva</code> en los detalles no puede elegirse si no tiene saldo suficiente para cubrir el <code>total_detalle</code>.</li>
        <li>Validación matemática en front-end: Suma de (<code>monto_detalle</code> + <code>iva_detalle</code>) debe ser exactamente igual a <code>total_detalle</code> antes de enviarse en el JSON de Guardar.</li>
      </ul>
    </div>

    <!-- 11. Reportes y Salidas -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">11</span> Reportes y Salidas Físicas</div>
      <p>El sistema genera una representación impresa en PDF que muestra el desglose del contrato, su vigencia, firmas electrónicas del área y las fianzas asociadas, de forma que sea transparente e inalterable.</p>
    </div>

    <!-- 12. Notificaciones y Alertas -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">12</span> Notificaciones y Alertas</div>
      <p>Cuando un contrato se aprueba y se firma, el sistema envía una notificación vía inbox interno del SIAF-PJEV al departamento de Contabilidad para que estos procedan con la generación de la Póliza de Compromiso en su módulo correspondiente.</p>
    </div>

</div>

<script src="../shared.js"></script>
<script>
function showWF(id, btn) {
  document.querySelectorAll('.wf-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.wf-tab').forEach(b => b.classList.remove('active'));
  document.getElementById('wf-' + id).classList.add('active');
  btn.classList.add('active');
}
function showSP(id, btn) {
  document.querySelectorAll('.sp-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.sp-tab').forEach(b => b.classList.remove('active'));
  document.getElementById('sp-' + id).classList.add('active');
  btn.classList.add('active');
}
</script>
</body>
</html>
"""

with open(r'c:\dixsys\manual_pjev\sitio_web\07_recursos_materiales\02.1.4-registro-contrato.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
