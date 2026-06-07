const fs = require('fs');
const path = require('path');

const targetDir = 'C:/dixsys/siaf_pjev/docs/sitio_web/03_contabilidad';
if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
}

const pages = [
  { id: '03.1.1', filename: '03.1.1-alta-cuentas.html', title: 'Plan de Cuentas', desc: 'Alta de Cuentas Contables en el SAFPOJ (243).', group: '03.1 Catálogos y Configuraciones' },
  { id: '03.1.2', filename: '03.1.2-matriz-conversion.html', title: 'Matriz de Conversión', desc: 'Reglas para generar asientos contables automáticos.', group: '03.1 Catálogos y Configuraciones' },
  { id: '03.1.3', filename: '03.1.3-modulo-retenciones.html', title: 'Módulo de Retenciones', desc: 'Registro de información en Módulo de Retenciones (239).', group: '03.1 Catálogos y Configuraciones' },
  
  { id: '03.2.1', filename: '03.2.1-visor-polizas-automaticas.html', title: 'Visor de Pólizas Automáticas', desc: 'Generación de Pólizas Diario Automatizadas (246).', group: '03.2 Registro Transaccional' },
  { id: '03.2.2', filename: '03.2.2-polizas-diario-manuales.html', title: 'Pólizas Manuales', desc: 'Contabilización de Pólizas Diario Manuales (253, 257).', group: '03.2 Registro Transaccional' },
  { id: '03.2.3', filename: '03.2.3-contabilidad-fideicomisos.html', title: 'Fideicomisos', desc: 'Contabilidad de Fideicomisos de Administración e Inversión (291).', group: '03.2 Registro Transaccional' },
  { id: '03.2.4', filename: '03.2.4-boveda-cfdi.html', title: 'Bóveda CFDI', desc: 'Respaldo de Archivos de CFDI de comprobaciones y pagos (352).', group: '03.2 Registro Transaccional' },
  
  { id: '03.3.1', filename: '03.3.1-descarga-contable-masiva.html', title: 'Descarga Contable Masiva', desc: 'Carga masiva de afectaciones contables.', group: '03.3 Procesos y Cierres' },
  { id: '03.3.2', filename: '03.3.2-conciliacion-bancaria.html', title: 'Conciliación Bancaria', desc: 'Conciliación bancaria automatizada (325) y manual (330).', group: '03.3 Procesos y Cierres' },
  { id: '03.3.3', filename: '03.3.3-conciliacion-ministraciones.html', title: 'Conciliación de Ministraciones', desc: 'Conciliación de Ministraciones (334).', group: '03.3 Procesos y Cierres' },
  { id: '03.3.4', filename: '03.3.4-conciliacion-presupuesto-contable.html', title: 'Presupuestal vs Contable', desc: 'Ingresos y Egresos (278).', group: '03.3 Procesos y Cierres' },
  { id: '03.3.5', filename: '03.3.5-conciliacion-intersistemas.html', title: 'Conciliación Inter-Sistemas', desc: 'Cruce con RRHH, Materiales y TCA (309, 302, 314).', group: '03.3 Procesos y Cierres' },
  { id: '03.3.6', filename: '03.3.6-conciliacion-obra-publica.html', title: 'Conciliación Obra Pública', desc: 'Conciliación Obra Pública en proceso (321).', group: '03.3 Procesos y Cierres' },
  
  { id: '03.4.1', filename: '03.4.1-antiguedad-saldos.html', title: 'Antigüedad de Saldos', desc: 'Determinación de la antigüedad de saldos (270, 274).', group: '03.4 Integración de Saldos' },
  { id: '03.4.2', filename: '03.4.2-integracion-activo-circulante.html', title: 'Integración Activo Circulante', desc: 'Integración de Saldos a sexto nivel: CxC, Deudores (338).', group: '03.4 Integración de Saldos' },
  { id: '03.4.3', filename: '03.4.3-integracion-pasivo-circulante.html', title: 'Integración Pasivo Circulante', desc: 'Integración de Saldos a sexto nivel: Retenciones (342).', group: '03.4 Integración de Saldos' },
  { id: '03.4.4', filename: '03.4.4-integracion-activo-no-circulante.html', title: 'Integración Activo Fijo', desc: 'Activo No Circulante y Construcciones (346).', group: '03.4 Integración de Saldos' },
  
  { id: '03.5.1', filename: '03.5.1-estados-trimestrales-cuenta-publica.html', title: 'Trimestrales y Cta. Pública', desc: 'Elaboración de Estados Contables y Cuenta Pública (261).', group: '03.5 Estados Financieros' },
  { id: '03.5.2', filename: '03.5.2-notas-estados-financieros.html', title: 'Notas a los Edos. Financieros', desc: 'Elaboración de Notas a los Estados Financieros (282).', group: '03.5 Estados Financieros' }
];

pages.forEach(p => {
  const content = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${p.filename}</title>
<link rel="stylesheet" href="../shared.css">
<style>
  body { padding: 36px 44px 80px; background: var(--pjev-crema); }
  .wf-box { border:2px dashed #ccc; border-radius:8px; padding: 60px 40px; text-align:center; background:#fff; margin-top:20px; color:#999; }
</style>
</head>
<body>
<div class="doc-main-inner">
    <div class="elem-breadcrumb">
      <a href="../index.html">Análisis Funcional</a> › <span>Contabilidad</span> › <span>${p.group.substring(5)}</span>
    </div>
    <div class="elem-header">
      <div>
        <div class="elem-id">${p.id}</div>
        <h1 class="elem-title">${p.title}</h1>
        <p class="elem-desc">${p.desc}</p>
      </div>
    </div>
    <div class="wf-box">
        <h2 style="color:#666;">Área de Trabajo (Wireframe en Construcción 🚧)</h2>
        <p>Pendiente de diseñar interfaz para este procedimiento del Manual del PJEV.</p>
    </div>
</div>
</body></html>`;
  fs.writeFileSync(path.join(targetDir, p.filename), content);
});

console.log("Created " + pages.length + " HTML files.");
