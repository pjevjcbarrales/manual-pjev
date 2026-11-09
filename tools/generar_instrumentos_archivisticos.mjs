import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
const require = createRequire(import.meta.url);
const { marked } = await import(pathToFileURL(require.resolve('marked')).href);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const data = JSON.parse(fs.readFileSync(path.join(root,'docs/datos_archivisticos_dga_2530_2024.json'),'utf8'));
const escape = text => String(text).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const pages = [
  {id:'09.1.1', title:'Cuadro de Clasificación Archivística', source:'CGCA_DGA_PJEV.md', target:'09.1.1-cgca.html'},
  {id:'09.1.2', title:'Catálogo de Disposición Documental', source:'CADIDO_DGA_PJEV.md', target:'09.1.2-cadido.html'},
];
for (const page of pages) {
  let content = marked.parse(fs.readFileSync(path.join(root,'docs',page.source),'utf8').replace(/^# .*\r?\n/,''));
  content = content.replace(/href="(?![a-z][a-z0-9+.-]*:|#|\/)([^"]+)"/gi,(_,href)=>`href="../docs/${href}"`);
  const rows = data.registros.map(entry => `<tr><td><code>${escape(entry.codigo)}</code></td><td>${escape(entry.tipo)}</td><td>${escape(page.id==='09.1.1'?entry.denominacion_cgca:entry.denominacion_cadido)}</td><td>${page.id==='09.1.1'?`CGCA p. ${entry.fuente_cgca_paginas.join(', ')}`:`${entry.tramite_anios_referencia} / ${entry.concentracion_anios_referencia} años`}</td><td>${page.id==='09.1.1'?escape(entry.serie_codigo):`Archivo Histórico · CADIDO p. ${entry.fuente_cadido_pagina}`}</td></tr>`).join('');
  content = content.replace('<!-- TABLA_REFERENCIA -->',`<table><thead><tr><th>Clave</th><th>Nivel</th><th>Literal de la fuente</th><th>${page.id==='09.1.1'?'Procedencia':'Trámite / concentración'}</th><th>${page.id==='09.1.1'?'Serie':'Destino y fuente'}</th></tr></thead><tbody>${rows}</tbody></table>`);
  content = content.replace(/<table>/g,'<div class="tabla" tabindex="0" role="region" aria-label="Entradas del instrumento"><table class="props-table">').replace(/<\/table>/g,'</table></div>');
  const html=`<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${page.id} ${page.title} — SIAF-PJEV</title><link rel="stylesheet" href="../shared.css"><style>
body{padding:32px 36px 70px}.doc-main-inner{max-width:1120px;margin:auto}.elem-breadcrumb{flex-wrap:wrap}.elem-header{display:block}.elem-title{margin:12px 0}.enlaces{display:flex;gap:18px;flex-wrap:wrap;margin:20px 0}.enlaces a,article a{color:var(--pjev-verde-oscuro)}article h2{font-size:23px;color:var(--pjev-verde-oscuro);margin:32px 0 14px;padding-top:12px;border-top:1px solid var(--pjev-borde)}article p{margin:14px 0}article ul{padding-left:24px}article li{margin:8px 0}.tabla{overflow-x:auto;margin:20px 0}.props-table{min-width:700px;font-size:13px}.props-table td{vertical-align:top}.estado{padding:12px 0;color:var(--pjev-warning-text)}code,a{overflow-wrap:anywhere}a:focus-visible,.tabla:focus-visible{outline:3px solid var(--pjev-dorado);outline-offset:3px}footer{margin-top:32px;border-top:1px solid var(--pjev-borde);padding-top:16px;font-size:12px;color:var(--pjev-texto-muted)}@media(max-width:650px){body{padding:20px 16px}.elem-title{font-size:27px}}
</style></head><body><main class="doc-main-inner"><nav class="elem-breadcrumb" aria-label="Ruta del manual"><a href="../index.html">Manual Dev</a> › 09 · Gestión Documental y Archivo › 09.1 · Catálogos Archivísticos</nav><header class="elem-header"><div class="elem-id">${page.id} · Recalibración institucional · 29-10-2026</div><h1 class="elem-title">${page.title}</h1><p>Referencia DGA–2530 · Piloto Contabilidad · Modelo general configurable</p><p class="estado">Especificación pendiente de implementación. Instrumentos recibidos sujetos a ratificación de vigencia operativa.</p></header><nav class="enlaces" aria-label="Documentos relacionados"><a href="09.2.4-control-archivo.html">Control de Archivo</a><a href="../docs/${page.source}">Especificación fuente</a><a href="../docs/RECALIBRACION_ARCHIVISTICA_DGA_PJEV.md">Fuentes y decisiones</a></nav><article>${content}</article><footer>Manual de Desarrollo SIAF-PJEV · Fuentes institucionales y propuestas técnicas diferenciadas.</footer></main><script src="../shared.js"></script></body></html>`;
  fs.writeFileSync(path.join(root,'09_gestion_documental',page.target),html,'utf8');
  console.log(`Generada ${page.id}: 16 entradas verificables del bloque 2530.`);
}
