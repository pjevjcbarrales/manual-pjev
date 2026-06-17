import codecs
import sys
sys.path.append(r'c:\dixsys\manual_pjev\sitio_web\07_recursos_materiales')
from temp_svgs_inmuebles import SVGS as SVGS_INMUEBLES
from temp_svgs_contratos import SVGS as SVGS_CONTRATOS

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — SIAF-PJEV</title>
<link rel="stylesheet" href="../shared.css">
<style>
  body {{ padding: 36px 44px 80px; background: var(--pjev-crema); }}
  .code-wrap {{
    background: var(--code-bg); color: var(--code-text);
    border-radius: 8px; font-family: var(--font-mono); font-size: 13px;
    padding: 20px; overflow-x: auto; line-height: 1.6; margin-bottom: 24px;
  }}
  .mod-header-badges {{ display:flex; gap:8px; margin-top:10px; flex-wrap:wrap; }}
  .wf-box {{ border: 1px solid var(--pjev-borde); border-radius: 8px; overflow: hidden; margin-bottom: 20px; }}
  .wf-bar {{ background: var(--pjev-crema); padding: 8px 16px; border-bottom: 1px solid var(--pjev-borde); font-size: 11px; font-weight: bold; color: var(--pjev-texto-muted); }}
  .wf-svg-area {{ padding: 20px; background: #fff; overflow-x: auto; }}
</style>
</head>
<body>
<div style="position: fixed; top: 20px; right: 45px; display: flex; flex-wrap: wrap; justify-content: flex-end; align-items: center; gap: 10px; z-index: 9999; max-width: calc(-60px + 100vw);">
  <button style="padding: 6px 12px; font-size: 11px; font-weight: bold; cursor: pointer; border: 1px solid rgb(212, 201, 181); border-radius: 6px; background: rgb(255, 255, 255); color: rgb(27, 58, 45); box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 5px;" onclick="window.location.reload()">⟳ Refrescar</button>
  <button style="padding: 6px 12px; font-size: 11px; font-weight: bold; cursor: pointer; border: 1px solid rgb(212, 201, 181); border-radius: 6px; background: rgb(255, 255, 255); color: rgb(27, 58, 45); box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 5px;" onclick="window.print()">🖨 Imprimir Manual</button>
</div>
<div class="doc-main-inner">

    <!-- BREADCRUMB -->
    <div class="elem-breadcrumb">
      <a href="../index.html">Inicio</a> ›
      <span>Presupuesto</span> ›
      <span>Manuales de Usuario</span> ›
      <span>{elem_id} {title_short}</span>
    </div>

    <!-- 1. Título -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">1</span> Manual de Usuario: {title_short}</div>
      <div class="section-content">
        <p style="font-size: 16px; font-weight: bold; color: var(--pjev-verde-oscuro);">{title_long}</p>
      </div>
    </div>

    <!-- 2. Objetivo -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">2</span> Objetivo del Módulo</div>
      <div class="section-content">
        {objetivo}
      </div>
    </div>

    <!-- 3. Normatividad -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">3</span> Reglas de Operación</div>
      <div class="section-content">
        {normatividad}
      </div>
    </div>

    <!-- 4. Procesos -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">4</span> Procesos Paso a Paso</div>
      <div class="section-content">
        {procesos}
      </div>
    </div>

</div>
</body>
</html>"""

# ==========================================
# 02.4.1 MANUAL BIENES INMUEBLES
# ==========================================
obj_inmuebles = """<p style="margin-bottom: 10px;">Proporcionar una guía visual y paso a paso para el usuario de Recursos Materiales sobre cómo interactuar con el Catálogo de Bienes Inmuebles dentro del SIAF-PJEV.</p>
<p>El usuario aprenderá a consultar bienes inmuebles existentes en la matriz y a dar de alta o modificar la información de nuevos inmuebles (como Terrenos, Edificios, etc.) capturando el costo de adquisición, dimensiones y ubicación.</p>"""

norm_inmuebles = """<ul style="list-style-type: disc; margin-left: 20px; line-height: 1.8; color: #444;">
  <li><strong>Campos Obligatorios:</strong> El sistema requiere que el <em>Costo de Adquisición</em>, <em>Número de Escritura</em>, <em>Clave Catastral</em> y <em>Ubicación</em> estén correctamente llenados para guardar el registro.</li>
  <li><strong>Autogeneración de Folios:</strong> El <em>Número de Inventario</em> es generado automáticamente por el sistema para garantizar que sea único e irrepetible.</li>
  <li><strong>Modificaciones:</strong> Una vez guardado, los datos catastrales o de dimensiones pueden ajustarse si hay un error de captura, pero las modificaciones quedarán registradas en la bitácora del sistema (auditoría).</li>
</ul>"""

proc_inmuebles = f"""<h3 style="color: var(--pjev-verde-oscuro); margin-bottom: 10px; font-size: 14px;">Paso 1. Consultar el Catálogo (Pantalla Principal)</h3>
<p style="margin-bottom: 15px; color: #555;">El usuario ingresa al menú <strong>Catálogos -> Bienes Inmuebles</strong>. Verá un listado con todos los inmuebles dados de alta previamente. Desde aquí puede buscar un inmueble o presionar el botón <strong>+ NUEVO BIEN INMUEBLE</strong>.</p>
<div style="margin-bottom:20px; padding: 20px; background: white; border-radius: 8px; border: 1px solid #ddd;">
  <div class="wf-box" style="margin-top: 15px;">
    <div class="wf-bar">Vista de la Pantalla Principal</div>
    <div class="wf-svg-area" style="text-align: center;">
      {SVGS_INMUEBLES[0] if len(SVGS_INMUEBLES)>0 else ''}
    </div>
  </div>
</div>

<h3 style="color: var(--pjev-verde-oscuro); margin-bottom: 10px; font-size: 14px;">Paso 2. Registrar o Modificar un Inmueble (Formulario)</h3>
<p style="margin-bottom: 15px; color: #555;">Al hacer clic en Nuevo o en Editar, se abrirá el formulario donde se deben capturar los datos técnicos y legales del inmueble. Tras llenar los datos, presione el botón <strong>Guardar Registro</strong>.</p>
<div style="margin-bottom:20px; padding: 20px; background: white; border-radius: 8px; border: 1px solid #ddd;">
  <div class="wf-box" style="margin-top: 15px;">
    <div class="wf-bar">Vista del Formulario de Captura</div>
    <div class="wf-svg-area" style="text-align: center; background:#222;">
      {SVGS_INMUEBLES[1] if len(SVGS_INMUEBLES)>1 else ''}
    </div>
  </div>
</div>"""

html_1 = html_template.format(
    elem_id="02.4.1",
    title="02.4.1 Manual de Bienes Inmuebles",
    title_short="Catálogo de Bienes Inmuebles",
    title_long="Módulo de Control y Registro de Bienes Inmuebles",
    objetivo=obj_inmuebles,
    normatividad=norm_inmuebles,
    procesos=proc_inmuebles
)
with codecs.open(r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.4.1-manual-bienes-inmuebles.html', 'w', 'utf-8') as f:
    f.write(html_1)

# ==========================================
# 02.4.2 MANUAL CONTRATOS
# ==========================================
obj_contratos = """<p style="margin-bottom: 10px;">Proporcionar una guía visual al usuario operativo para el registro de los contratos originados por adjudicación directa o licitación.</p>
<p>El usuario aprenderá a utilizar la pantalla de "Cabecera" para ingresar los datos jurídicos (Vigencias, Proveedor, Folio) y a utilizar el "Detalle" presupuestal para mapear el contrato contra las partidas presupuestales (Bolsa).</p>"""

norm_contratos = """<ul style="list-style-type: disc; margin-left: 20px; line-height: 1.8; color: #444;">
  <li><strong>Cuadre Obligatorio:</strong> La suma de los montos asignados a las partidas en el detalle debe cuadrar exactamente ($0.00 de diferencia) con el "Monto Total" o "Monto Máximo" capturado en la cabecera.</li>
  <li><strong>Bloqueo Presupuestal:</strong> Una vez que el contrato pasa a estado "COMPROMETIDO" (porque Presupuesto generó la póliza), el contrato queda bloqueado para edición. No se puede modificar ni borrar.</li>
</ul>"""

# Contratoes has 5 SVGs in the array. Indices might be:
# 0: Leer (Param)
# 1: Leer (Valores)
# 2: ABC (Param)
# 3: ABC (Valores)
# 4: Swimlane SVG (Wait, is the Swimlane an SVG? Yes, we injected it!)
proc_contratos = f"""<h3 style="color: var(--pjev-verde-oscuro); margin-bottom: 10px; font-size: 14px;">Paso 1. Bandeja de Contratos</h3>
<p style="margin-bottom: 15px; color: #555;">El usuario ingresa al menú <strong>Recursos Materiales -> Contratos</strong>. El sistema le mostrará un listado con los contratos registrados en el ejercicio fiscal. Desde ahí puede buscar o agregar un <strong>+ NUEVO CONTRATO</strong>.</p>
<div style="margin-bottom:20px; padding: 20px; background: white; border-radius: 8px; border: 1px solid #ddd;">
  <div class="wf-box" style="margin-top: 15px;">
    <div class="wf-bar">Pantalla Principal (Ejemplo con datos)</div>
    <div class="wf-svg-area" style="text-align: center;">
      {SVGS_CONTRATOS[1] if len(SVGS_CONTRATOS)>1 else ''}
    </div>
  </div>
</div>

<h3 style="color: var(--pjev-verde-oscuro); margin-bottom: 10px; font-size: 14px;">Paso 2. Captura del Contrato y la Bolsa</h3>
<p style="margin-bottom: 15px; color: #555;">El formulario está dividido en dos partes. Arriba, se captura la cabecera (Proveedor, Folio, Fechas). Abajo, se agregan las partidas de donde saldrá el dinero. Todo debe cuadrar para poder <strong>Guardar</strong>.</p>
<div style="margin-bottom:20px; padding: 20px; background: white; border-radius: 8px; border: 1px solid #ddd;">
  <div class="wf-box" style="margin-top: 15px;">
    <div class="wf-bar">Formulario de Captura Maestro-Detalle</div>
    <div class="wf-svg-area" style="text-align: center; background:#222;">
      {SVGS_CONTRATOS[3] if len(SVGS_CONTRATOS)>3 else ''}
    </div>
  </div>
</div>

<h3 style="color: var(--pjev-verde-oscuro); margin-bottom: 10px; font-size: 14px;">Anexo: Proceso Global del Contrato</h3>
<p style="margin-bottom: 15px; color: #555;">El siguiente diagrama muestra por qué módulos viaja su contrato después de que lo captura en este módulo.</p>
<div style="margin-bottom:20px; padding: 20px; background: white; border-radius: 8px; border: 1px solid #ddd; text-align:center;">
    {SVGS_CONTRATOS[4] if len(SVGS_CONTRATOS)>4 else ''}
</div>
"""

html_2 = html_template.format(
    elem_id="02.4.2",
    title="02.4.2 Manual de Contratos",
    title_short="Registro de Contratos",
    title_long="Módulo de Registro Legal y Presupuestal de Contratos",
    objetivo=obj_contratos,
    normatividad=norm_contratos,
    procesos=proc_contratos
)
with codecs.open(r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.4.2-manual-contratos.html', 'w', 'utf-8') as f:
    f.write(html_2)

print("Generated both User Manuals successfully.")
