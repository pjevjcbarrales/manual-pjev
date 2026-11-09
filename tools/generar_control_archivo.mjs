// Regenera la página del manual a partir de su especificación Markdown.
// Requiere marked disponible en node_modules o NODE_PATH.
import { createRequire } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const require = createRequire(import.meta.url);
const { marked } = await import(pathToFileURL(require.resolve('marked')).href);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = fs.readFileSync(path.join(root, 'docs/CONTROL_ARCHIVO_REGISTRO_DIGITALIZACION_PJEV.md'), 'utf8');
const diagramasHtml = fs.readFileSync(path.join(root, 'tools/fragmentos/diagramas_analista.html'), 'utf8');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'docs/datos_archivisticos_dga_2530_2024.json'), 'utf8'));
const escapeHtml = value => String(value).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
let content = marked.parse(source.replace(/^# .*\r?\n/, ''));
// Los enlaces del Markdown se resuelven desde docs/, y el HTML vive en 09_gestion_documental/.
content = content.replace(/href="(?![a-z][a-z0-9+.-]*:|#|\/)([^"]+)"/gi, (_, href) => `href="../docs/${href}"`);
const toc = [];
content = content.replace(/<h2>(.*?)<\/h2>/g, (_, title) => {
  const id = `seccion-${toc.length + 1}`;
  toc.push({ id, title });
  return `<h2 id="${id}">${title}</h2>`;
});
content = content.replace(/<h3>(CA-\d+.*?)<\/h3>([\s\S]*?)(?=<h[23]|$)/g, (_, title, body) =>
  `<details class="opcion" id="${title.slice(0, 5).toLowerCase()}"${title.startsWith('CA-01') ? ' open' : ''}><summary>${title}</summary><div class="opcion-body">${body}</div></details>`);
content = content.replace(/<table>/g, '<div class="tabla-scroll" tabindex="0" role="region" aria-label="Tabla de especificación"><table class="props-table">').replace(/<\/table>/g, '</table></div>');

const html = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Primer alcance funcional del Sistema de Control de Archivo del SIAF-PJEV: registro, digitalización, marbetes y ubicación física.">
  <title>09.2.4 Control de Archivo — SIAF-PJEV</title>
  <link rel="stylesheet" href="../shared.css">
  <style>
    body{padding:32px 38px 70px} .doc-main-inner{max-width:1120px;margin:auto}.elem-header{display:block}.elem-title{margin-top:8px}.elem-breadcrumb{flex-wrap:wrap}
    .etiquetas{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}.etiqueta{border:1px solid var(--pjev-borde);border-radius:20px;padding:4px 12px;font-size:12px;background:white}.pendiente{background:var(--pjev-warning-bg);color:var(--pjev-warning-text)}
    .intro{max-width:850px;font-size:16px;margin-top:14px}.barra-enlaces{display:flex;gap:18px;flex-wrap:wrap;margin:18px 0 28px}.barra-enlaces a{font-weight:600;color:var(--pjev-verde-oscuro)}
    .indice{border:1px solid var(--pjev-borde);border-radius:8px;background:#fff;padding:18px 22px;margin:24px 0}.indice ol{display:grid;grid-template-columns:1fr 1fr;gap:5px 30px;padding-left:20px}.indice a{color:var(--pjev-verde-oscuro);font-size:13px}
    .modelo{background:#fff;border:1px solid var(--pjev-borde);border-radius:9px;margin:24px 0;overflow:hidden}.modelo figcaption{padding:12px 18px;border-bottom:1px solid var(--pjev-borde);font-weight:700}.diagrama-scroll{overflow-x:auto}.modelo svg{display:block;width:100%;min-width:800px;height:auto}.nota{font-size:12px;color:var(--pjev-texto-muted);padding:0 18px 16px}
    .diagramas h2{font-size:23px;color:var(--pjev-verde-oscuro);margin:25px 0 12px}.diagramas p{margin:10px 0}.diagramas a{color:var(--pjev-verde-oscuro)}.diagrama-analista{background:#fff;border:1px solid var(--pjev-borde);border-radius:8px;margin:15px 0}.diagrama-analista summary{padding:15px 18px;cursor:pointer;font-weight:700;color:var(--pjev-verde-oscuro)}.diagrama-analista .modelo{border:0;border-radius:0;margin:0}.modelo img{display:block;width:100%;height:auto}.modelo .ciclo{min-width:850px}.modelo .estructura{min-width:1200px}
    article h2{font-size:23px;color:var(--pjev-verde-oscuro);margin:36px 0 14px;padding-top:12px;border-top:2px solid var(--pjev-borde);scroll-margin-top:20px}article p{margin:12px 0}article ul,article ol{padding-left:24px;margin:10px 0}article li{margin:7px 0}article code{overflow-wrap:anywhere}article a{color:var(--pjev-verde-oscuro);overflow-wrap:anywhere}
    .tabla-scroll{overflow-x:auto;margin:18px 0;max-width:100%}.tabla-scroll:focus-visible{outline:3px solid var(--pjev-dorado)}.props-table{min-width:630px;margin:0;font-size:13px}.props-table th,.props-table td{vertical-align:top;white-space:normal}.props-table td{overflow-wrap:anywhere}.props-table th:first-child{min-width:110px}
    .opcion{border:1px solid var(--pjev-borde);border-radius:7px;background:#fff;margin:12px 0;scroll-margin-top:15px}.opcion summary{cursor:pointer;padding:16px 20px;font-weight:700;color:var(--pjev-verde-oscuro);font-size:16px}.opcion[open] summary{border-bottom:1px solid var(--pjev-borde);background:#f4f7f3}.opcion-body{padding:4px 20px 15px}.opcion-body p:last-child{border-left:3px solid var(--pjev-dorado);padding-left:12px}.expandir{font:inherit;padding:8px 12px;border:1px solid var(--pjev-borde);border-radius:5px;background:white;cursor:pointer;color:var(--pjev-verde-oscuro);margin:10px 0}
    .demo{border:1px solid var(--pjev-borde);border-radius:9px;background:white;margin:28px 0;padding:22px}.demo h2{color:var(--pjev-verde-oscuro);font-size:21px}.demo p{margin:8px 0}.demo form{display:flex;align-items:end;gap:10px;margin:16px 0}.demo label{display:block;flex:1;font-weight:600}.demo input,.demo select{display:block;width:100%;min-width:0;font:inherit;padding:10px;border:1px solid #7c8f81;border-radius:5px;margin-top:5px;background:white}.demo button{background:var(--pjev-verde-oscuro);color:white;border:0;border-radius:5px;padding:12px 18px;font:inherit;cursor:pointer}.ejemplos{display:flex;flex-wrap:wrap;gap:8px}.ejemplos button{font-size:12px;background:var(--pjev-crema);color:var(--pjev-verde-oscuro);border:1px solid var(--pjev-borde);padding:6px 10px}.resultado{margin-top:18px;padding:16px;background:#f4f7f3;border-left:4px solid var(--pjev-verde-claro);overflow-wrap:anywhere}.resultado h3{font-size:17px}.resultado dl{display:grid;grid-template-columns:160px 1fr;gap:7px 12px;margin:12px 0}.resultado dt{font-weight:700}.resultado dd{margin:0}.resultado ul{padding-left:22px}.demo-nota{color:var(--pjev-texto-muted);font-size:12px}.mensaje{font-weight:600}.ruta{padding:12px 0;color:var(--pjev-verde-oscuro);font-family:var(--font-mono);font-size:12px;overflow-wrap:anywhere}
    button:focus-visible,a:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid var(--pjev-dorado);outline-offset:3px}footer{margin-top:32px;padding-top:18px;border-top:1px solid var(--pjev-borde);font-size:12px;color:var(--pjev-texto-muted)}
    @media(max-width:700px){body{padding:20px 16px 50px}.indice ol{grid-template-columns:1fr}.demo{padding:16px}.demo form{flex-direction:column;align-items:stretch}.resultado dl{grid-template-columns:1fr;gap:2px}.resultado dd{margin-bottom:9px}.elem-title{font-size:27px}}
    @media print{body{padding:0;background:white}.indice,.expandir,.demo form,.ejemplos,.barra-enlaces{display:none}.opcion{break-inside:avoid}.opcion-body{display:block!important}.tabla-scroll{overflow:visible}.props-table{min-width:0;font-size:10px}.modelo svg,.modelo .ciclo,.modelo .estructura{min-width:0}.diagrama-analista{break-before:page}}
  </style>
</head>
<body>
<main class="doc-main-inner">
  <nav class="elem-breadcrumb" aria-label="Ruta del manual"><a href="../index.html">Manual Dev</a> › <span>09 · Gestión Documental y Archivo</span> › <span>09.2 · Registro y Operación</span></nav>
  <header class="elem-header">
    <div class="elem-id">09.2.4 · Requerimiento de origen 4.1</div>
    <h1 class="elem-title">Sistema de Control de Archivo</h1>
    <p class="intro">Piloto en la Dirección General de Administración → Subdirección de Recursos Financieros (2530), con foco en Contabilidad. Clasificación, expedientes, inventarios y ciclo de vida con un modelo general configurable.</p>
    <div class="etiquetas"><span class="etiqueta">DGA–2530 · Contabilidad</span><span class="etiqueta">CGCA / CADIDO · PADA</span><span class="etiqueta">29 octubre 2026</span><span class="etiqueta pendiente">Diseño recalibrado · Desarrollo pendiente</span></div>
  </header>
  <div class="barra-enlaces"><a href="../docs/CONTROL_ARCHIVO_REGISTRO_DIGITALIZACION_PJEV.md">Especificación fuente</a><a href="../docs/RECALIBRACION_ARCHIVISTICA_DGA_PJEV.md">Fuentes y recalibración</a><a href="09.1.1-cgca.html">CGCA</a><a href="09.1.2-cadido.html">CADIDO</a><a href="09.3.2-transferencias-documentales.html">Transferencias</a></div>

  <section class="demo" aria-labelledby="clasificacion-titulo">
    <h2 id="clasificacion-titulo">Clasificación institucional del piloto</h2>
    <p class="ruta">CGCA: FOPJ01 → PLENOCJP → DGA2500 → 2530</p>
    <p>4 series y 12 subseries de referencia. Alcance confirmado: Contabilidad. Otras áreas se incorporarán por configuración y permisos.</p>
    <p class="demo-nota">Datos transcritos de los instrumentos recibidos, con notas de 2025. La vigencia operativa debe ratificarse. En el CADIDO, el fondo figura como FOPJO1; se conserva la discrepancia.</p>
    <label for="clasificacion-piloto">Serie o subserie de referencia<select id="clasificacion-piloto">${catalog.registros.map(entry => `<option value="${escapeHtml(entry.codigo)}"${entry.codigo==='2530.3a'?' selected':''}>${escapeHtml(entry.codigo)} · ${escapeHtml(entry.denominacion_cgca)}</option>`).join('')}</select></label>
    <div id="ficha-clasificacion" class="resultado" role="status" aria-live="polite" aria-atomic="true"></div>
    <p class="demo-nota">Selector de referencia local. La selección no reclasifica expedientes, no cambia el estado de una póliza ni concede permisos. «Tramitada» y «Liquidada» son nombres de subseries.</p>
  </section>

  ${diagramasHtml}

  <section class="demo demo-marbete" aria-labelledby="demo-titulo">
    <h2 id="demo-titulo">Maqueta de consulta por marbete</h2>
    <p class="demo-nota">Datos ficticios en esta página, sin conexión a servicios. Permite revisar cómo se mostrarían la ubicación, los tomos y un código anterior.</p>
    <form id="consulta-marbete"><label for="codigo-marbete">Número de marbete<input id="codigo-marbete" name="marbete" value="PJEV-ARC-000001" maxlength="80" autocomplete="off" spellcheck="false"></label><button type="submit">Consultar ejemplo</button></form>
    <div class="ejemplos" aria-label="Ejemplos de consulta"><button type="button" data-codigo="PJEV-ARC-000001">Expediente en dos tomos</button><button type="button" data-codigo="ANT-0842">Marbete anterior</button><button type="button" data-codigo="PJEV-CAJ-000020">Caja con contenido</button><button type="button" data-codigo="LEG-0007">Archivo Inicial pendiente</button></div>
    <div id="resultado-marbete" class="resultado" role="status" aria-live="polite" aria-atomic="true"></div>
  </section>

  <nav class="indice" aria-label="Contenido de la especificación"><ol>${toc.map(x => `<li><a href="#${x.id}">${x.title.replace(/^\d+\. /, '')}</a></li>`).join('')}</ol></nav>
  <button type="button" class="expandir" id="expandir-opciones" aria-expanded="false">Abrir las ocho opciones</button>
  <article aria-label="Especificación funcional del bloque 4.1">${content}</article>
  <footer>Manual de Desarrollo SIAF-PJEV · OAJ-DGA · Dix Consultoría · Documento de trabajo. Los contratos y la maqueta no acreditan servicios implementados.</footer>
</main>
<script src="../shared.js"></script>
<script>
(() => {
  'use strict';
  const input = document.getElementById('codigo-marbete');
  const output = document.getElementById('resultado-marbete');
  const records = {
    'PJEV-ARC-000001': { titulo:'Expediente de ejemplo · Pólizas de Ingresos', tipo:'Expediente · DGA–2530 · Contabilidad', vigente:'PJEV-ARC-000001', clasificacion:'2530.3a · Ingresos · Referencia CGCA/CADIDO recibida', digital:'En revisión · 2 documentos observados', ubicaciones:['Tomo 1 · Caja PJEV-CAJ-000020 · Archivo de trámite / Depósito A / Anaquel 03 / Nivel 02 / Posición 01', 'Tomo 2 · Caja PJEV-CAJ-000021 · Archivo de trámite / Depósito A / Anaquel 03 / Nivel 02 / Posición 02'] },
    'PJEV-CAJ-000020': { titulo:'Caja de ejemplo · Archivo de trámite de Contabilidad', tipo:'Caja', vigente:'PJEV-CAJ-000020', clasificacion:'Clasificación conservada por cada expediente', digital:'Estado consultable por cada expediente', ubicaciones:['Archivo de trámite / Depósito A / Anaquel 03 / Nivel 02 / Posición 01'], contenido:['PJEV-ARC-000001 · Tomo 1 · Pólizas de Ingresos · 2530.3a','PJEV-ARC-000002 · Carpeta única · Conciliación contable/presupuestal · 2530.4'] },
    'LEG-0007': { titulo:'Acervo anterior de ejemplo · Lote inicial 01', tipo:'Expediente de Archivo Inicial', vigente:'Pendiente de conciliación', digital:'Pendiente · Inventario sin verificar', ubicaciones:['Ubicación no verificada · Anaquel declarado 08 (sin corroboración física)'] }
  };
  const aliases = { 'ANT-0842':'PJEV-ARC-000001' };
  function el(tag, text) { const node = document.createElement(tag); node.textContent = text; return node; }
  function consultar() {
    const codigo = input.value.trim().toUpperCase();
    const resolved = aliases[codigo] || codigo;
    const record = records[resolved];
    output.replaceChildren();
    if (!record) {
      output.append(el('p', codigo ? 'Sin coincidencia en los datos de ejemplo. Usa uno de los cuatro marbetes sugeridos.' : 'Escribe un número de marbete para consultar los datos de ejemplo.'));
      return;
    }
    if (aliases[codigo]) output.append(el('p', 'Marbete sustituido. El número anterior se conserva como alias del mismo expediente.'));
    output.append(el('h3',record.titulo));
    const dl = document.createElement('dl');
    [['Tipo de objeto', record.tipo],['Marbete vigente',record.vigente],['Clasificación',record.clasificacion||'Pendiente de conciliación'],['Digitalización',record.digital]].forEach(([label,value]) => dl.append(el('dt',label),el('dd',value)));
    output.append(dl, el('strong','Ubicación física'));
    const places = document.createElement('ul'); record.ubicaciones.forEach(x => places.append(el('li',x))); output.append(places);
    if (record.contenido) { output.append(el('strong','Contenido de ejemplo')); const contents = document.createElement('ul'); record.contenido.forEach(x=>contents.append(el('li',x))); output.append(contents); }
    output.append(el('p','La consulta muestra información; cualquier reubicación, sustitución o baja requiere su operación específica.'));
  }
  document.getElementById('consulta-marbete').addEventListener('submit', event => { event.preventDefault(); consultar(); });
  document.querySelectorAll('[data-codigo]').forEach(button=>button.addEventListener('click',()=>{ input.value=button.dataset.codigo; consultar(); }));
  const classificationEntries = ${JSON.stringify(catalog.registros).replaceAll('<','\u003c')};
  const selector = document.getElementById('clasificacion-piloto');
  function showClassification() {
    const entry=classificationEntries.find(item=>item.codigo===selector.value);
    const panel=document.getElementById('ficha-clasificacion');
    panel.replaceChildren();
    if(!entry){panel.append(el('p','Selecciona una entrada del instrumento de referencia.'));return;}
    panel.append(el('h3',entry.codigo+' · '+entry.denominacion_cgca));
    const dl=document.createElement('dl');
    [['Nivel',entry.tipo],['Serie',entry.serie_codigo],['Archivo de trámite',entry.tramite_anios_referencia+' años'],['Concentración',entry.concentracion_anios_referencia+' años'],['Destino marcado','Archivo Histórico'],['Fuente','CGCA p. '+entry.fuente_cgca_paginas.join(', ')+' · CADIDO p. '+entry.fuente_cadido_pagina],['Vencimiento','Pendiente de cierre, evento de cómputo y validación aplicables']].forEach(([label,value])=>dl.append(el('dt',label),el('dd',value)));
    panel.append(dl,el('p','Esta referencia conduce a evaluar transferencia histórica. Cumplir los plazos no habilita baja por vencimiento.'));
    if(entry.marcas_fuente.publica==='X'&&entry.marcas_fuente.reservada==='X')panel.append(el('p','El CADIDO marca Pública y Reservada. La clasificación real y los permisos se determinan para el documento o expediente.'));
    if(entry.denominacion_cadido!==entry.denominacion_cgca)panel.append(el('p','Literal CADIDO conservado: '+entry.denominacion_cadido));
  }
  selector.addEventListener('change',showClassification);showClassification();
  const options = [...document.querySelectorAll('details.opcion')];
  const toggle = document.getElementById('expandir-opciones');
  function syncToggle() { const all = options.every(x=>x.open); toggle.setAttribute('aria-expanded',String(all)); toggle.textContent = all ? 'Cerrar las ocho opciones' : 'Abrir las ocho opciones'; }
  toggle.addEventListener('click',()=>{const open=!options.every(x=>x.open); options.forEach(x=>{x.open=open;});syncToggle();});
  options.forEach(x=>x.addEventListener('toggle',syncToggle));
  const printPanels=[...options,...document.querySelectorAll('.diagrama-analista')];
  window.addEventListener('beforeprint',()=>{ printPanels.forEach(x=>{x.dataset.printOpen=String(x.open);x.open=true;}); });
  window.addEventListener('afterprint',()=>{ printPanels.forEach(x=>{x.open=x.dataset.printOpen==='true';delete x.dataset.printOpen;});syncToggle(); });
  function openHash() { const target=document.getElementById(location.hash.slice(1)); if(target?.matches('details.opcion')) target.open=true; }
  window.addEventListener('hashchange',openHash); openHash(); consultar();
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(root,'09_gestion_documental/09.2.4-control-archivo.html'),html,'utf8');
console.log('Generada 09.2.4-control-archivo.html desde la especificación fuente.');
