/* Corte funcional y tecnico del SIAF-PJEV al 31-08-2026. */
(function reconstruirTableroPm() {
  const perfiles = {
    cfg: { f0: 100, f1: 80, f3: 65, f4: 25, f5: 40, f6: 55, f7: 65 },
    ppto: { f0: 100, f1: 100, f3: 55, f4: 55, f5: 55, f6: 68, f7: 70 },
    conta: { f0: 100, f1: 100, f3: 65, f4: 70, f5: 35, f6: 75, f7: 60 },
    fin: { f0: 100, f1: 100, f3: 75, f4: 90, f5: 20, f6: 65, f7: 45 },
    ing: { f0: 100, f1: 95, f3: 85, f4: 40, f5: 80, f6: 70, f7: 30 },
    rm: { f0: 100, f1: 100, f3: 45, f4: 30, f5: 45, f6: 50, f7: 35 }
  };
  const pesos = { f1: .10, f2: .15, f3: .20, f4: .20, f5: .10, f6: .20, f7: .05 };
  const anteriores = pmData.modulos.slice();
  const porId = new Map(anteriores.map((m) => [m.id, m]));
  const modulos = [];

  function calificar(perfil, f2, tope59 = false) {
    if (!perfil || f2 === null || f2 === undefined) return null;
    const f = { ...perfiles[perfil], f2 };
    const valor = Object.entries(pesos).reduce((total, [fase, peso]) => total + f[fase] * peso, 0);
    f.final = Math.round(tope59 ? Math.min(valor, 59) : valor);
    return f;
  }

  function agregar(id, sistema, subsistema, modulo, datos = {}) {
    const anterior = porId.get(id) || {};
    const fases = calificar(datos.perfil, datos.f2, datos.tope59);
    modulos.push({
      id, sistema, subsistema, modulo, nombre: modulo,
      opciones: datos.opciones || [], rutas: datos.rutas || [],
      desarrollador_asignado: datos.responsable || anterior.desarrollador_asignado || 'Sin asignar',
      analista_asignado: datos.analista || anterior.analista_asignado || 'Julio Cesar',
      estado: datos.estado || (datos.rutas?.length ? 'Desarrollado; requiere estabilizacion' : 'Pendiente'),
      alcance: datos.alcance || 'Etapa actual',
      documentacion: datos.documentacion || 'Pendiente de documentar',
      documento: datos.documento || '',
      evidencia_actualizacion: datos.evidencia || '',
      fases, cumplimiento_final: fases?.final ?? null,
      fecha_corte: '2026-08-31'
    });
  }

  const cfg = (id, sub, nombre, datos = {}) => agregar(id, '01 Configuración Inicial', sub, nombre, {
    perfil: datos.rutas?.length ? 'cfg' : null,
    responsable: datos.responsable || (datos.rutas?.length ? 'Daryl' : 'Sin asignar'), ...datos
  });

  const configuracion = [
    ['01.1.1','01.1 Entidad y Ejercicios','Entidad','/cfg/ent/entidad',90,'01_cfg/01.1.1-entidad.html'],
    ['01.1.2','01.1 Entidad y Ejercicios','Ejercicios fiscales','/cfg/ent/ejercicios',90,'01_cfg/01.1.2-ejercicios.html'],
    ['01.1.3','01.1 Entidad y Ejercicios','Periodos contables','/cfg/ent/periodos',90,'01_cfg/01.1.3-periodos.html'],
    ['01.2.1','01.2 Catálogos Base','Unidades administrativas','/cfg/cat/unidades',55,'01_cfg/01.2.1-unidades-administrativas.html'],
    ['01.2.2','01.2 Catálogos Base','COG','/cfg/cpp/cog',55,'01_cfg/01.2.2-cog.html'],
    ['01.2.3','01.2 Catálogos Base','Programas','/cfg/cpp/programas',90,'01_cfg/01.2.3-programas.html'],
    ['01.2.4','01.2 Catálogos Base','Fuentes de financiamiento','/cfg/cpp/fuentesf',55,'01_cfg/01.2.4-fuentes-financiamiento.html'],
    ['01.2.5','01.2 Catálogos Base','CUCOP','/cfg/cpp/cucop',55,'01_cfg/01.2.5-cucop.html'],
    ['01.2.6','01.2 Catálogos Base','Subprogramas','/cfg/cpp/subprogramas',55,'01_cfg/01.2.6-subprogramas.html'],
    ['01.2.7','01.2 Catálogos Base','CRI','/cfg/cpp/cri',55,'01_cfg/01.2.7-cri.html'],
    ['01.2.8','01.2 Catálogos Base','Proyectos','/cfg/cpp/proyectos',55,'01_cfg/01.2.8-proyectos.html'],
    ['01.2.9','01.2 Catálogos Base','Centros de costo','/cfg/cpp/centroscos',90,'01_cfg/01.2.9-centros-costos.html'],
    ['01.3.1','01.3 Terceros y Padrón','Proveedores','/cfg/cat/proveedores',55,'01_cfg/01.3.1-proveedores.html'],
    ['01.3.2','01.3 Terceros y Padrón','Subtipos de proveedor','/cfg/catalogos/subtipo-proveedor',55,'01_cfg/01.3.2-subtipo-proveedor.html'],
    ['01.3.3','01.3 Terceros y Padrón','Empleados','/cfg/cat/empleados',90,'01_cfg/01.3.3-empleados.html'],
    ['01.3.4','01.3 Terceros y Padrón','Terceros institucionales','/cfg/cat/tinstitucionales',55,'01_cfg/01.3.4-terceros-inst.html'],
    ['01.3.5','01.3 Terceros y Padrón','Terceros beneficiarios','/cfg/cat/tbeneficiarios',55,'01_cfg/01.3.5-terceros.html'],
    ['01.4.1','01.4 Bancarios','Bancos','/cfg/cat/bancos',55,'01_cfg/01.4.1-bancos.html'],
    ['01.4.2','01.4 Bancarios','Cuentas bancarias','/cfg/cat/cbancarios',55,''],
    ['01.4.3','01.4 Bancarios','Tipos de cuenta bancaria','/cfg/cat/tcbancarios',55,''],
    ['01.4.4','01.4 Bancarios','Chequeras','/cfg/cat/chequeras',65,'01_cfg/01.4.2-chequeras.html'],
    ['01.5.1','01.5 Sistema y Seguridad','Sistemas','/cfg/seg/sistemas',60,'01_cfg/01.5.1-sistemas.html'],
    ['01.5.2','01.5 Sistema y Seguridad','Subsistemas','/cfg/seg/subsistemas',60,'01_cfg/01.5.2-subsistemas.html'],
    ['01.5.3','01.5 Sistema y Seguridad','Módulos de navegación','/cfg/seg/modulos',60,'01_cfg/01.5.3-modulos.html'],
    ['01.5.4','01.5 Sistema y Seguridad','Roles de seguridad','/cfg/seg/roles',60,'01_cfg/01.5.4-roles.html'],
    ['01.5.5','01.5 Sistema y Seguridad','Usuarios','/cfg/seg/usuarios',60,''],
    ['01.5.6','01.5 Sistema y Seguridad','Grupos de seguridad','/cfg/seg/grupos',60,''],
    ['01.6.2','01.6 Operativos','Funciones','/cfg/cpp/funcion',55,'01_cfg/01.6.2-funcion.html'],
    ['01.6.5','01.6 Operativos','Documentos y expedientes digitales','/cfg/documentos',55,'']
  ];
  configuracion.forEach(([id, sub, nombre, ruta, f2, documento]) => cfg(id, sub, nombre, {
    rutas: [ruta], f2, documento,
    documentacion: documento ? 'Documentado' : 'Pendiente de documentar'
  }));
  cfg('01.4.5','01.4 Bancarios','Conceptos bancarios',{ documento:'01_cfg/01.4.3-conceptos-bancarios.html', documentacion:'Analisis documentado; desarrollo pendiente', alcance:'Planeado' });
  cfg('01.6.1','01.6 Operativos','Clasificacion funcional',{ documento:'01_cfg/01.6.1-clasificacion-funcional.html', documentacion:'Documentado; sin ruta independiente verificada', estado:'Pendiente de definicion funcional' });
  cfg('01.6.3','01.6 Operativos','Momentos',{ documento:'01_cfg/01.6.3-momentos.html', documentacion:'Analisis documentado; desarrollo pendiente', alcance:'Planeado' });
  cfg('01.6.4','01.6 Operativos','Tipos de documento',{ documento:'01_cfg/01.6.4-tipo-documento.html', documentacion:'Analisis documentado; desarrollo pendiente', alcance:'Planeado' });
  cfg('01.7.1','01.7 Documentos y Autorizaciones','Firmas',{
    rutas:['/cfg/fir/doc','/cfg/fir/roles','/cfg/fir/matriz','/cfg/fir/firm'], f2:65, responsable:'Julio Cesar',
    opciones:['Documentos de firma','Roles de firma','Matriz documento-rol','Catalogo y vigencia de firmas'],
    documentacion:'Pendiente de documentar',
    evidencia:'Firmas es un modulo transversal; sus cuatro pantallas son opciones, no subsistemas ni modulos separados.'
  });

  const avances = {
    '02.1.1':[90,'/ppto/reg/catalogoclavepresupuestal'], '02.1.2':[68,'/ppto/reg/presupuestoautorizado'],
    '02.2.1':[80,'/ppto/inf/calendarizacion'], '02.2.2':[80,'/ppto/inf/recalendarizacion'],
    '02.2.3':[62,'/ppto/reg/transferencias'], '02.2.4':[55,'/ppto/reg/ampliaciones-reducciones'],
    '02.2.5':[55,'/ppto/reg/arrendamientos'], '02.2.6':[75,'/ppto/pro/operaciones-especiales'],
    '03.1.1':[90,'/conta/reg/catalogocuentas'], '03.1.2':[55,'/conta/cat/matrices'],
    '03.2.1':[60,'/conta/reg/polizas'], '03.2.2':[65,'/conta/reg/polaut'],
    '03.3.1':[80,'/conta/proc/descarga'], '03.3.2':[60,'/conta/proc/conciliacion-bancaria'],
    '03.3.3':[90,'/conta/proc/conciliacion-ministraciones'], '03.3.4':[80,'/conta/proc/conciliacion-presupuesto-contable'],
    '03.4.1':[75,'/conta/inf/auxiliar'], '03.4.2':[75,'/conta/inf/libro-diario'],
    '03.5.1':[75,'/conta/inf/balanza'], '03.5.2':[75,'/conta/inf/consola'],
    '03.5.3':[80,'/conta/ef'], '03.3.7':[90,'/conta/proc/cierre-mensual']
  };

  anteriores.filter((m) => /^(02|03)\./.test(m.id)).forEach((m) => {
    if (/^02\.3\.[123]$/.test(m.id) || /^02\.3\.4\./.test(m.id) || ['03.2.3','03.2.4'].includes(m.id)) return;
    const idTablero = m.id === '03.6.1' ? '03.3.7' : m.id;
    const sistema = m.id.startsWith('02.') ? '02 Presupuesto' : '03 Contabilidad';
    const perfil = m.id.startsWith('02.') ? 'ppto' : 'conta';
    const actual = avances[idTablero];
    const fase2 = actual?.[0];
    let estado = actual ? 'Desarrollado; requiere estabilizacion' : 'Pendiente';
    let alcance = 'Etapa actual';
    if (m.id === '02.2.7' || m.id === '03.2.5') { estado = 'Fase 2'; alcance = 'Fase 2'; }
    if (m.id === '03.3.5') estado = 'Pendiente de definicion funcional';
    if (m.id === '03.3.6') { estado = 'Fuera del alcance actual'; alcance = 'Corresponde a Obra'; }
    const subsistema = idTablero === '03.3.7'
      ? '03.3 Procesos y Cierres'
      : `${idTablero.split('.').slice(0,2).join('.')} ${m.subsistema || 'Sin clasificar'}`;
    agregar(idTablero, sistema, subsistema, m.nombre, {
      perfil: actual ? perfil : null, f2: fase2, rutas: actual ? [actual[1]] : [],
      responsable: m.desarrollador_asignado,
      documentacion: 'Documentado en el manual vigente', estado, alcance
    });
  });

  const buscar = (id) => modulos.find((m) => m.id === id);
  const inmuebles = buscar('02.1.3');
  if (inmuebles) Object.assign(inmuebles, { rutas:['/cfg/cco/inmuebles','/cfg/catalogos/bienes-inmuebles'], fases:calificar('cfg',55), cumplimiento_final:53, estado:'Desarrollado; requiere estabilizacion', evidencia_actualizacion:'Propiedad funcional de Presupuesto; implementacion tecnica compartida en Configuracion.' });
  const contratos = buscar('02.1.4');
  if (contratos) Object.assign(contratos, { rutas:['/cfg/cco/contratos'], fases:calificar('cfg',55), cumplimiento_final:53, estado:'Desarrollado; requiere estabilizacion', evidencia_actualizacion:'Propiedad funcional de Presupuesto; implementacion tecnica compartida en Configuracion.' });
  const bovedaCfdiLegacy = modulos.findIndex((modulo) => modulo.id === '03.2.5');
  if (bovedaCfdiLegacy >= 0) modulos.splice(bovedaCfdiLegacy, 1);
  const consola = buscar('02.3.4');
  if (consola) Object.assign(consola, {
    rutas:['/ppto/inf/consola','/ppto/inf/conac','/ppto/inf/consulta-global-mensual','/ppto/inf/avance-sector'], fases:calificar('ppto',75), cumplimiento_final:66,
    estado:'Desarrollado; requiere estabilizacion',
    opciones:['Avance presupuestal','Clasificacion administrativa','Clasificacion economica','Objeto del gasto','Clasificacion funcional','Estado analitico de ingresos','Gastos de operacion por unidad administrativa'],
    evidencia_actualizacion:'Los elementos 02.3.4.x son opciones de la consola, no modulos adicionales.'
  });

  const presupuestoAutorizado = buscar('02.1.2');
  if (presupuestoAutorizado) {
    presupuestoAutorizado.rutas.push('/ppto/techo-presupuestal');
    presupuestoAutorizado.opciones = [...presupuestoAutorizado.opciones, 'Techo presupuestal'];
    presupuestoAutorizado.evidencia_actualizacion = 'Techo presupuestal queda integrado como opcion de Presupuesto autorizado; no es un modulo independiente.';
  }
  const operacionesEspeciales = buscar('02.2.6');
  if (operacionesEspeciales) {
    operacionesEspeciales.modulo = 'Operaciones especiales presupuestales';
    operacionesEspeciales.nombre = operacionesEspeciales.modulo;
    operacionesEspeciales.opciones = [
      'Compromiso presupuestal del capitulo 1000',
      'Poliza de apertura del presupuesto de ingresos',
      'Movimientos al presupuesto de ingresos'
    ];
    operacionesEspeciales.estado = 'Desarrollado';
    operacionesEspeciales.evidencia_actualizacion = 'Modulo renombrado y desarrollado en frontend, backend y persistencia.';
  }
  agregar('02.2.8','02 Presupuesto','02.2 Proceso','Polizas presupuestarias',{ perfil:'ppto',f2:50,rutas:['/ppto/pro/polizas'],responsable:'Eunice',documentacion:'Pendiente de documentar',opciones:['Generacion y consulta de polizas','Bitacora de adecuaciones'],evidencia:'La bitacora de adecuaciones se conserva como consulta interna; no es un modulo independiente.' });
  agregar('02.2.9','02 Presupuesto','02.2 Proceso','Solicitud de suficiencia presupuestal',{ perfil:'ppto',f2:65,rutas:['/ppto/pro/sufi','/adq/reg/sol_sufpresupuestal'],responsable:'Daryl',documentacion:'Documentacion por reubicar desde Materiales',opciones:['Captura por area solicitante','Envio a revision presupuestal','Seguimiento de folios, montos reservados y comprometidos'],evidencia:'Desarrollado por Daryl. Acceso para Materiales, Recursos Humanos, Informatica y Financieros. El seguimiento de suficiencias se conserva como opcion interna y la autorizacion se realiza en 02.2.10.' });
  agregar('02.2.10','02 Presupuesto','02.2 Proceso','Autorizacion de reserva / suficiencia',{ perfil:'ppto',f2:65,rutas:['/ppto/pro/aprobacion-suficiencia-presupuestal'],responsable:'Eunice',documentacion:'Documentado en el manual vigente',opciones:['Revision de disponibilidad','Autorizacion o rechazo','Emision de oficio'],evidencia:'Concentra la decision presupuestal sobre la reserva o suficiencia.' });
  agregar('02.4.1','02 Presupuesto','02.4 Integraciones','Seguimiento FASP y recursos etiquetados',{estado:'Pendiente de integracion',alcance:'Presupuesto da seguimiento; operacion corresponde a Obra'});
  agregar('02.4.2','02 Presupuesto','02.4 Integraciones','Control presupuestal del capitulo 1000',{estado:'Pendiente de integracion con RH',alcance:'Sin proyeccion de vacantes en esta etapa'});
  ['Formulacion integral del anteproyecto y proyecto','Distribucion formal del presupuesto autorizado','Atencion a auditorias','Reglas de austeridad'].forEach((nombre,i)=>agregar(`02.5.${i+1}`,'02 Presupuesto','02.5 Planeacion Fase 2',nombre,{estado:i===3?'Fase 2 / hotfix':'Fase 2',alcance:'Fase 2'}));

  agregar('03.4.3','03 Contabilidad','03.4 Imprimir reportes contables','Libro diario consolidado',{perfil:'conta',f2:80,rutas:['/conta/inf/libro-diario-consolidado'],responsable:'Cristian'});
  agregar('03.4.4','03 Contabilidad','03.4 Imprimir reportes contables','Libro mayor',{perfil:'conta',f2:80,rutas:['/conta/inf/libro-mayor'],responsable:'Cristian'});
  const balanza = buscar('03.5.1');
  if (balanza) {
    balanza.id = '03.4.5';
    balanza.subsistema = '03.4 Imprimir reportes contables';
  }
  const panelFinanciero = buscar('03.5.2');
  if (panelFinanciero) {
    panelFinanciero.id = '03.6.1';
    panelFinanciero.subsistema = '03.6 Concentradores de informes';
    panelFinanciero.modulo = 'Panel de reportes financieros';
    panelFinanciero.nombre = panelFinanciero.modulo;
    panelFinanciero.opciones = ['Reportes contables','Estados e informacion contable CONAC','Formatos de disciplina financiera'];
    panelFinanciero.evidencia_actualizacion = 'Concentrador de informes; los reportes se desglosan individualmente en 03.4.x y 03.5.x.';
  }
  const panelConac = buscar('03.5.3');
  if (panelConac) {
    panelConac.id = '03.6.2';
    panelConac.subsistema = '03.6 Concentradores de informes';
    panelConac.modulo = 'Panel de estados e informacion contable CONAC';
    panelConac.nombre = panelConac.modulo;
    panelConac.opciones = ['Estados e informacion contable','Seleccion de ejercicio y periodo','Vista previa y emision'];
    panelConac.evidencia_actualizacion = 'Concentrador CONAC implementado en /conta/ef; no sustituye el desglose de cada informe.';
  }

  const reportesConac = [
    ['03.5.1','Estado de Actividades','actividades',true],
    ['03.5.2','Estado de Situacion Financiera','situacion',true],
    ['03.5.3','Estado de Variacion en la Hacienda Publica','variacion-hp',true],
    ['03.5.4','Estado de Cambios en la Situacion Financiera','cambios-situacion',true],
    ['03.5.5','Estado de Flujos de Efectivo','flujos-efectivo',true],
    ['03.5.6','Estado Analitico del Activo','analitico-activo',true],
    ['03.5.7','Estado Analitico de la Deuda y Otros Pasivos','analitico-deuda',true],
    ['03.5.8','Informe sobre Pasivos Contingentes','pasivos-contingentes',false],
    ['03.5.9','Notas a los Estados Financieros','notas',true]
  ];
  reportesConac.forEach(([id,nombre,vista,disponible]) => agregar(id,'03 Contabilidad','03.5 Estados financieros y disciplina financiera',nombre,{
    perfil:disponible ? 'conta' : null,
    f2:disponible ? 80 : null,
    rutas:disponible ? ['/conta/ef'] : [],
    responsable:'Cristian',
    estado:'Pendiente de revision y validacion funcional',
    documentacion:disponible ? 'Evidencia tecnica disponible; revision y validacion funcional pendientes' : 'Normativa CONAC identificada; desarrollo pendiente',
    evidencia:disponible
      ? `Implementacion tecnica localizada en el panel CONAC y en el endpoint /contabilidad/estados-financieros/${vista}/reporte. No existe certeza funcional sobre la generacion correcta de la informacion.`
      : 'Requerido por el Manual de Contabilidad Gubernamental; la pantalla lo identifica como no disponible.'
  }));

  const reportesLdf = [
    ['03.5.10','LDF 1 - Estado de Situacion Financiera Detallado',[]],
    ['03.5.11','LDF 2 - Informe Analitico de la Deuda Publica y Otros Pasivos',[]],
    ['03.5.12','LDF 3 - Informe Analitico de Obligaciones Diferentes de Financiamientos',[]],
    ['03.5.13','LDF 4 - Balance Presupuestario',[]],
    ['03.5.14','LDF 5 - Estado Analitico de Ingresos Detallado',[]],
    ['03.5.15','LDF 6 - Estado Analitico del Ejercicio del Presupuesto de Egresos Detallado',['Por objeto del gasto','Clasificacion administrativa','Clasificacion funcional','Servicios personales por categoria']],
    ['03.5.16','LDF 7 - Proyecciones y Resultados de Ingresos y Egresos',['Proyecciones de ingresos','Proyecciones de egresos','Resultados de ingresos','Resultados de egresos']],
    ['03.5.17','LDF 8 - Informe sobre Estudios Actuariales',[]]
  ];
  reportesLdf.forEach(([id,nombre,opciones]) => agregar(id,'03 Contabilidad','03.5 Estados financieros y disciplina financiera',nombre,{
    responsable:'Cristian',estado:'Pendiente de desarrollo',opciones,
    documentacion:'Normativa LDF identificada; analisis funcional y desarrollo pendientes',
    evidencia:'Formato requerido por los Criterios CONAC para la Ley de Disciplina Financiera; sin ruta implementada verificada.'
  }));
  const catCuentas=buscar('03.1.1'); if(catCuentas){catCuentas.modulo='Catalogo institucional de cuentas';catCuentas.nombre=catCuentas.modulo;catCuentas.estado='Requiere validacion funcional de Contabilidad';}
  agregar('03.1.3','03 Contabilidad','03.1 Catalogos','Catalogo correlacionado',{
    perfil:'conta',f2:90,rutas:['/conta/cat/catrel'],responsable:'Cristian',
    estado:'Desarrollado',documentacion:'Pendiente de documentar',
    opciones:['Consulta y filtros','Correlacion SAFPOJ-SIAF','Validacion para importacion de polizas'],
    evidencia:'Implementado con frontend, servicio y controlador backend, y funciones PostgreSQL de lectura e importacion.'
  });
  const matrices=buscar('03.1.2'); if(matrices){matrices.desarrollador_asignado='Julio Cesar';matrices.opciones=['Matrices versionadas','Reglas y movimientos','Simulador','Ruta legacy por retirar'];matrices.rutas.push('/conta/reg/matriz-conversion');matrices.evidencia_actualizacion='Modulo desarrollado por Julio Cesar.';}
  const polizas=buscar('03.2.1'); if(polizas){polizas.opciones=['Captura manual','Importacion SAFPOJ'];polizas.rutas.push('/conta/reg/polizas/importar-safpoj');}
  const cierre=buscar('03.3.7'); if(cierre){cierre.opciones=['Cuenta pólizas','Validar pólizas','Cerrar mes contable'];cierre.rutas.push('/conta/pro/cierre');cierre.estado='Pendiente de revision y validacion funcional';cierre.evidencia_actualizacion='El flujo requerido comprende Cuenta polizas, Validar polizas y Cerrar mes contable. Se conserva la evidencia tecnica, pero el modulo permanece pendiente de desarrollo.';}
  const conciliacionPresupuestaria = buscar('03.3.4');
  if (conciliacionPresupuestaria) Object.assign(conciliacionPresupuestaria, {
    id:'03.4.6',
    subsistema:'03.4 Imprimir reportes contables',
    modulo:'Conciliación entre egresos presupuestarios y gastos contables',
    nombre:'Conciliación entre egresos presupuestarios y gastos contables',
    evidencia_actualizacion:'Reporte de conciliacion requerido por CONAC; se reclasifica desde Procesos y Cierres hacia reportes contables.'
  });
  ['03.3.2','03.3.3','03.3.5','03.3.6','03.4.6'].forEach((id) => {
    const conciliacion = buscar(id);
    if (conciliacion) {
      conciliacion.estado = 'En desarrollo; requiere completar, revisar y validar';
      conciliacion.evidencia_actualizacion = `${conciliacion.evidencia_actualizacion ? `${conciliacion.evidencia_actualizacion} ` : ''}La conciliacion se registra en desarrollo hasta completar y validar su operacion.`;
    }
  });
  modulos.filter((modulo) => modulo.sistema === '03 Contabilidad' && /^03\.1\./.test(modulo.id))
    .forEach((modulo) => { modulo.subsistema = '03.1 Catálogos'; });
  modulos.filter((modulo) => modulo.sistema === '03 Contabilidad' && /^03\.3\./.test(modulo.id))
    .forEach((modulo) => { modulo.subsistema = '03.3 Procesos y Cierres'; });

  const ing = (id, sub, nombre, datos={}) => agregar(id,'04 Ingresos',sub,nombre,datos);
  ing('04.1.1','04.1 Catálogos','Conceptos de ingreso',{
    perfil:'ing',
    f2:90,
    rutas:['/ing/conceptos'],
    responsable:'Eunice',
    documentacion:'Análisis funcional canónico',
    documento:'04_ingresos/04.1.1-conceptos-ingreso.html',
    nombre:'Tipos y subtipos de trámite de ingreso',
    opciones:[
      '1. Ministraciones (Ordinaria, Extraordinaria, Convenios Federales)',
      '2. Ingresos Propios (Rendimientos bancarios, Arrendamientos, Derechos, Venta de bases)',
      '3. Reintegros y Recuperaciones (Viáticos, Nómina indebida, Devolución anticipos)',
      '4. Fondos en Tránsito (Depósitos no identificados, Aclaración y reclasificación)'
    ],
    evidencia:'Catálogo rector estructurado en 4 macro-familias y 12 procedimientos canónicos (espejo con Egresos 05.2.1) que alimenta el Wizard Modal de Registro y parametriza el enlace a CRI y Matriz CONAC.'
  });
  ing('04.1.2','04.1 Catálogos','Motivos de ajuste o cancelación',{
    perfil:'ing',
    f2:90,
    rutas:['/ing/motivos-ajuste'],
    responsable:'Eunice',
    documentacion:'Análisis funcional canónico',
    documento:'04_ingresos/04.1.2-motivos-ajuste-cancelacion.html',
    opciones:[
      '1. Error de captura',
      '2. Registro duplicado',
      '3. Importe incorrecto',
      '4. Fecha incorrecta',
      '5. Cuenta bancaria incorrecta',
      '6. Concepto o CRI incorrecto',
      '7. Fuente de financiamiento incorrecta',
      '8. Fondo o capítulo incorrecto',
      '9. Depósito no identificado',
      '10. Corrección contable',
      '11. Reclasificación presupuestaria',
      '12. Otro motivo autorizado'
    ],
    evidencia:'Catálogo tipificado de causales de ajuste y cancelación con severidad (BAJA, MEDIA, ALTA) y autorizaciones requeridas, consumido por registro, conciliación y cierre.'
  });
  ing('04.1.3','04.1 Catálogos','Claves presupuestales y carteras SEFIPLAN',{
    perfil:'ing',
    f2:90,
    rutas:['/ing/claves-sefiplan'],
    responsable:'Eunice',
    documentacion:'Análisis funcional canónico',
    documento:'04_ingresos/04.1.3-claves-sefiplan.html',
    nombre:'Claves presupuestales y carteras SEFIPLAN',
    opciones:[
      '1. Padrón anual por ejercicio fiscal (2026)',
      '2. Homologación Órgano (TSJ, TCA, TDJ, OAJ) y Capítulos (1000..6000)',
      '3. Desglose y validación de los 11 segmentos programáticos SEFIPLAN',
      '4. Mapeo de carteras oficiales (000184001, 000186001, 000618001, 000619001)',
      '5. Nemotécnicos de Caja (1 OPE-1, 1 NOM-1, 1 OPE-2, 1 OPE-7, 1 OPE-8)',
      '6. Servicio REST /resolver para autocompletado en movimientos 04.2.1'
    ],
    evidencia:'Catálogo de enlace interinstitucional con SEFIPLAN que administra por ejercicio fiscal las carteras y claves programáticas de 11 segmentos para autocompletar los movimientos de ministración sin captura manual.'
  });
  ing('04.1.4','04.1 Catálogos','Cuentas bancarias recaudadoras',{
    perfil:'ing',
    f2:90,
    rutas:['/ing/cuentas-recaudadoras'],
    responsable:'Eunice',
    documentacion:'Análisis funcional canónico',
    documento:'04_ingresos/04.1.4-cuentas-recaudadoras.html',
    nombre:'Cuentas bancarias recaudadoras',
    opciones:[
      '1. Padrón institucional de cuentas (BBVA, Banorte, Santander)',
      '2. Validación estricta de CLABE Interbancaria (18 dígitos numéricos)',
      '3. Convenios CIE y referencias bancarias para ventanilla y practicajas',
      '4. Clasificación por fondo (Ministración, Fondo Auxiliar, Recursos Propios, Juzgados)',
      '5. Enlace contable obligatorio con subcuentas 1.1.1.2 Bancos/Tesorería del COA',
      '6. Protección contra bajas lógicas de cuentas con movimientos vigentes'
    ],
    evidencia:'Catálogo institucional de tesorería que administra las cuentas bancarias receptoras de recursos, validando CLABEs de 18 dígitos y enlazando obligatoriamente a la cuenta 1.1.1.2 del COA.'
  });
  ing('04.2.1','04.2 Registro','Registro de ingresos',{
    responsable:'Eunice',
    estado:'Pendiente de desarrollo',
    documentacion:'Análisis funcional completo',
    documento:'04_ingresos/04.2.1-registro-ingresos.html',
    opciones:[
      'Wizard Modal de selección de Trámite (Paso 0: 4 macro-familias / 12 subtipos)',
      'Formulario Compuesto (Maestro-Detalle): Encabezado de ministración con importe total',
      'Carga obligatoria de 2 Archivos Físicos Digitalizados (Oficio con acuse + Orden debidamente firmada)',
      'Sección de Movimientos Presupuestales en Grid PJEV-UI con botón [+ Agregar Partida]',
      'Modal PJEV-UI con autocompletado paramétrico de clave SEFIPLAN (11 segmentos) y nemotécnico de Caja',
      'Barra de cuadre financiero obligatorio en tiempo real (Σ Movimientos = Total Encabezado, Dif: $0.00)',
      'Afectación contable subyacente en segundo plano (Matriz CONAC 03.1.2 B.1 Devengado)',
      'Registro simple de comprobante bancario y recaudación subyacente (Paso 2: Principio KISS)',
      'Tablero de mensajes y bitácora de trazabilidad forense (IngresoHistorialTimeline y Modales)'
    ],
    evidencia:'Módulo central transaccional con Formulario Compuesto homologado con Egresos 05.2.1, soporte estricto de doble archivo físico firmado, grid interactivo PJEV-UI con barra de cuadre en vivo y contabilidad subyacente.'
  });
  ing('04.3.1','04.3 Procesos','Conciliación de ingresos',{
    perfil:'conta',
    f2:70,
    rutas:['/conta/proc/conciliacion-ministraciones'],
    responsable:'Eunice',
    estado:'Disponible parcialmente; requiere completar y validar',
    documentacion:'Análisis funcional inicial',
    documento:'04_ingresos/04.3.1-conciliacion-ingresos.html',
    opciones:[
      'Ejecutar conciliación',
      'Consultar detalle',
      'Vincular depósito',
      'Aplicar depósito',
      'Registrar observación',
      'Marcar diferencia como aclarada',
      'Enviar a corrección',
      'Exportar resultados',
      'Consultar historial'
    ],
    evidencia:'Existe implementación previa orientada a ministraciones (/conta/proc/conciliacion-ministraciones); se documenta su ampliación integral para conciliar todos los conceptos de ingreso, parcialidades y depósitos no identificados.'
  });
  ing('04.3.2','04.3 Procesos','Cierre mensual de ingresos',{
    responsable:'Eunice',
    estado:'Pendiente de desarrollo',
    documentacion:'Análisis funcional inicial',
    documento:'04_ingresos/04.3.2-cierre-mensual-ingresos.html',
    opciones:[
      'Ejecutar validación previa',
      'Consultar incidencias',
      'Navegar al registro que requiere corrección',
      'Registrar justificación',
      'Cerrar mes',
      'Solicitar reapertura',
      'Reabrir con autorización',
      'Consultar historial de cierres'
    ],
    evidencia:'Consola de certificación de 13 validaciones de integridad financiera, congelamiento transaccional y coordinación con Contabilidad y Presupuesto.'
  });
  ing('04.4.1','04.4 Informes','Informes y control de ingresos',{
    responsable:'Eunice',
    estado:'Pendiente de desarrollo',
    documentacion:'Análisis funcional inicial',
    documento:'04_ingresos/04.4.1-informes-control-ingresos.html',
    opciones:[
      'Ingresos esperados y recibidos',
      'Relación de depósitos',
      'Ingresos por clasificación',
      'Ministraciones',
      'Reintegros, rentas y otros ingresos',
      'Depósitos pendientes',
      'Diferencias de conciliación',
      'Auxiliar de ingresos',
      'Estado del cierre mensual',
      'Estado Analítico de Ingresos'
    ],
    evidencia:'Concentrador analítico de 10 informes operativos, presupuestarios, contables y de control de ingresos; provee vista al Estado Analítico de Ingresos canónico de Presupuesto (02.3.4.6) sin duplicidad.'
  });

  const cxp = (id, sub, nombre, datos={}) => agregar(id,'05 Cuentas por Pagar',sub,nombre,datos);
  cxp('05.1.1','05.1 Catálogos','Requisitos documentales',{perfil:'cxp',f2:100,rutas:['/cxp/requisitos-documentales'],responsable:'Cristian',estado:'Desarrollado',documentacion:'Documentado en el manual vigente',evidencia:'Matriz checklist de 16 documentos soporte cruzada contra los 12 procedimientos canónicos de gasto con validador transaccional.'});
  cxp('05.1.2','05.1 Catálogos','Tarifas y zonas de viáticos',{perfil:'cxp',f2:100,rutas:['/cxp/tarifas-viaticos'],responsable:'Cristian',estado:'Desarrollado',documentacion:'Documentado en el manual vigente',opciones:['Zona 1 Estado de Veracruz','Zona 2 Nacional / CDMX','Zona 3 Extranjero','4 Niveles jerárquicos','Techo máximo sin CFDI 20%','Calculadora oficial de comisiones'],evidencia:'Tabulador oficial de viáticos y pasajes del PJEV con motor de cálculo de techos financieros por rubro (hospedaje, alimentos, pasajes).'});
  cxp('05.1.3','05.1 Catálogos','Conceptos de retención y deducción',{perfil:'cxp',f2:100,rutas:['/cxp/conceptos-retencion'],responsable:'Cristian',estado:'Desarrollado',documentacion:'Documentado en el manual vigente',opciones:['Retención ISR Honorarios (10%)','Retención ISR RESICO (1.25%)','Retención ISR Arrendamiento (10%)','Retención IVA (2/3 y 100%)','5 al millar de Obra Pública (0.5%)','Deducciones de nómina e IPE'],evidencia:'Catálogo de 10 retenciones fiscales y laborales con mapeo contable a sexto nivel en 2.1.1.7 y enlace con Terceros Institucionales.'});
  cxp('05.2.1','05.2 Registro','Afectación del gasto',{perfil:'cxp',f2:100,tope59:false,rutas:['/fin/reg/afectaciongasto','/cxp/afectaciones'],responsable:'Julio Cesar',estado:'Desarrollado',documentacion:'Documentado en el manual vigente',opciones:['4 Tipos de Pago (Directo, Pedido, Comprobar, No afecta ppto)','15 Subtipos/Procedimientos con descripciones breves UI','Workflow oficial 6 estados','CFDI 4.0 y cuadratura con partidas','Póliza automática de devengo CONAC A.1','Integración con Checklist 05.1.1'],evidencia:'Hegemonía consolidada: erradicado hardcodeo de 1 y 2, incorporada modalidad No Afecta Presupuesto y sincronización de póliza contable con matriz de conversión.'});
  cxp('05.2.2','05.2 Registro','Orden de pago',{responsable:'Daryl',estado:'Pendiente de desarrollo',opciones:['Servicios personales','Recursos materiales','Gastos por comprobar','Terceros institucionales'],evidencia:'Formaliza la obligación autorizada y su envío a la Bandeja de pagos.'});
  cxp('05.2.3','05.2 Registro','Gastos a comprobar',{responsable:'Daryl',estado:'Pendiente de desarrollo',opciones:['Entrega de recursos','Responsable y fecha límite','Saldo pendiente','Reintegro']});
  cxp('05.2.4','05.2 Registro','Comprobación y revisión de gastos',{responsable:'Daryl',estado:'Pendiente de desarrollo',opciones:['Recepción de comprobaciones','Facturas XML y PDF','Peajes y recibos','Validación fiscal y duplicados','Observaciones, aceptación o rechazo','Reintegros y cierre'],evidencia:'Fusiona comprobación, recepción y revisión y se vincula con Gastos a comprobar y el Repositorio CFDI.'});
  cxp('05.3.1','05.3 Procesos','Pre-pólizas',{responsable:'Daryl',estado:'Pendiente de desarrollo'});
  cxp('05.3.2','05.3 Procesos','Programación de pagos',{responsable:'Daryl',estado:'Pendiente de desarrollo'});
  cxp('05.3.3','05.3 Procesos','Control y entero de retenciones',{responsable:'Daryl',estado:'Pendiente de desarrollo'});
  cxp('05.3.4','05.3 Procesos','DIOT',{responsable:'Daryl',estado:'Pendiente de desarrollo'});
  cxp('05.3.5','05.3 Procesos','Movimientos de fideicomisos',{responsable:'Eunice',estado:'Pendiente de desarrollo',documentacion:'Análisis heredado de Contabilidad; debe actualizarse'});
  cxp('05.4.1','05.4 Informes','Informes de Cuentas por Pagar',{responsable:'Daryl',estado:'Pendiente de desarrollo',opciones:['Cuentas pendientes de pago','Órdenes por estado y beneficiario','Antigüedad de adeudos','Gastos a comprobar pendientes','Comprobaciones pendientes o rechazadas','Retenciones y obligaciones fiscales','Información para DIOT','Gastos por tipo, procedimiento y unidad administrativa','Movimientos de fideicomisos']});

  const pagos = (id, sub, nombre, datos={}) => agregar(id,'06 Pagos',sub,nombre,datos);
  pagos('06.1.1','06.1 Catálogos','Medios de pago',{responsable:'Eunice',estado:'Pendiente de desarrollo',opciones:['Cheque','Transferencia electrónica','SPEI','Dispersión','Otros medios autorizados'],evidencia:'Bancos, chequeras y conceptos bancarios se reutilizan desde Configuración Inicial.'});
  pagos('06.2.1','06.2 Registro','Bandeja de pagos',{responsable:'Eunice',estado:'Pendiente de desarrollo',opciones:['Recepción desde órdenes de pago','Priorización y fecha propuesta','Disponibilidad proyectada','Alertas y acciones permitidas']});
  pagos('06.2.2','06.2 Registro','Registro y control de pagos',{responsable:'Eunice',estado:'Pendiente de desarrollo',opciones:['Cheques','Transferencias electrónicas','Programación de fecha y lote','Cuenta pagadora','Autorización y liberación','Aplicación del pago','Pago a terceros institucionales','Rechazo, cancelación, devolución y reexpedición'],evidencia:'Cheques, transferencias y pagos a terceros son modalidades del registro, no módulos independientes.'});
  pagos('06.2.3','06.2 Registro','Traspasos entre cuentas',{responsable:'Eunice',estado:'Pendiente de desarrollo'});
  pagos('06.2.4','06.2 Registro','Inversiones y rendimientos',{responsable:'Eunice',estado:'Segunda etapa',alcance:'Segunda etapa',opciones:['Colocaciones','Renovaciones y vencimientos','Retiros y reinversiones','Rendimientos']});
  pagos('06.3.1','06.3 Procesos','Conciliación bancaria',{perfil:'conta',f2:60,rutas:['/conta/proc/conciliacion-bancaria'],responsable:'Eunice',estado:'Disponible parcialmente; requiere completar y validar',documentacion:'Documentado en el manual vigente'});
  pagos('06.4.1','06.4 Informes','Informes de pagos y bancos',{responsable:'Eunice',estado:'Pendiente de desarrollo',opciones:['Pagos diarios','Programados, liberados, aplicados y cancelados','Libro de bancos','Disponibilidad financiera','Cheques y transferencias','Traspasos','Inversiones y rendimientos','Gastos de operación y liberación de recursos']});

  const cfdi = (id, sub, nombre, datos={}) => agregar(id,'07 Repositorio CFDI',sub,nombre,datos);
  cfdi('07.1.1','07.1 Registro','Bóveda CFDI',{perfil:'cfg',f2:55,rutas:['/cfg/documentos'],responsable:'Cristian',estado:'Segunda etapa',alcance:'Transversal para Tesorería, Contabilidad y procesos que reciben comprobantes fiscales',opciones:['Carga individual y masiva de XML','Asociación de PDF','Complementos de pago','Consulta fiscal','CFDI relacionados','Vinculación con expedientes','Descarga autorizada e historial'],documentacion:'Evidencia técnica disponible; análisis funcional integral pendiente',evidencia:'Cada CFDI debe registrarse una sola vez por UUID y hash; los demás módulos crean vínculos, no copias.'});
  cfdi('07.2.1','07.2 Procesos','Validación y vinculación fiscal',{responsable:'Cristian',estado:'Segunda etapa',alcance:'Segunda etapa',opciones:['Validación estructural','Consulta ante SAT','Detección de duplicados','Vinculación con afectación, orden y pago','Vinculación con viáticos y gastos a comprobar','Control de complementos','CFDI sustituidos o cancelados','Integración del expediente digital']});
  cfdi('07.3.1','07.3 Informes','Control y auditoría CFDI',{responsable:'Cristian',estado:'Segunda etapa',alcance:'Segunda etapa',opciones:['CFDI inválidos o cancelados','Duplicados o reutilizados','Comprobantes sin vincular','Complementos pendientes','Expedientes incompletos','Diferencias entre CFDI, afectación y pago','Trazabilidad y auditoría documental']});

  const rm = (id,sub,nombre,datos={}) => agregar(id,'08 Materiales',sub.replace(/^05\./, '08.'),nombre,{
    perfil:datos.rutas?.length ? (datos.perfil || 'rm') : null,
    estado:datos.estado || 'Stand by', alcance:'Stand by', ...datos
  });
  rm('08.1.1','08.1 Catalogos de Adquisiciones','Documentos requisito',{rutas:['/adq/catad/docs_requisito'],f2:90,documentacion:'Documentado'});
  rm('08.1.2','08.1 Catalogos de Adquisiciones','Matriz checklist',{rutas:['/adq/catad/matriz_checklist'],f2:75,documentacion:'Documentado'});
  rm('08.1.3','08.1 Catalogos de Adquisiciones','Modalidades',{rutas:['/adq/catad/modalidades'],f2:90,documentacion:'Documentado'});
  rm('08.1.4','08.1 Catalogos de Adquisiciones','Procedimientos de contratacion',{rutas:['/adq/catad/procedimientos'],f2:50,documentacion:'Pendiente de actualizar'});
  rm('08.1.5','08.1 Catalogos de Adquisiciones','CUCOP',{rutas:['/cfg/cpp/cucop'],perfil:'cfg',f2:55,responsable:'Daryl',documentacion:'Catalogo compartido documentado'});
  rm('08.2.1','08.2 Requerimientos','Requerimientos de adquisiciones',{rutas:['/adq/catad/req_adquisiciones'],f2:90,responsable:'Julio Cesar',documentacion:'Documentado'});
  rm('08.2.2','08.2 Requerimientos','Expediente de compra',{opciones:['Cotizaciones e investigacion de mercado','Pedidos, ordenes y contratos','Recepcion y conformidad','Factura y CFDI']});
  rm('08.3.1','08.3 Procedimientos de Contratacion','Adjudicacion directa',{documentacion:'Documentado; desarrollo integral pendiente'});
  rm('08.3.2','08.3 Procedimientos de Contratacion','Invitacion a cuando menos tres',{documentacion:'Documentado; desarrollo integral pendiente'});
  rm('08.3.3','08.3 Procedimientos de Contratacion','Licitacion publica',{documentacion:'Documentado; desarrollo integral pendiente'});
  rm('08.3.4','08.3 Procedimientos de Contratacion','Formalizacion, recepcion y devengado',{opciones:['Formalizacion y comprometido','Recepcion, CFDI y devengado']});
  rm('08.4.1','08.4 Reportes e Informes','Seguimiento de adquisiciones',{opciones:['Programa anual','Seguimiento de requerimientos','Cuadro comparativo','Seguimiento de procedimientos','Pedidos y contratos','Recepciones y CFDI','Trazabilidad y auditoria']});

  const responsablesTesoreria = {
    '04 Ingresos': 'Daryl',
    '05 Cuentas por Pagar': 'Eunice',
    '06 Pagos': 'Eunice',
    '07 Repositorio CFDI': 'Cristian'
  };
  const responsablesPorModulo = {
    '04.1.1': 'Eunice',
    '04.1.2': 'Eunice',
    '04.1.3': 'Eunice',
    '04.1.4': 'Eunice',
    '04.2.1': 'Eunice',
    '04.3.1': 'Eunice',
    '04.3.2': 'Eunice',
    '04.4.1': 'Eunice',
    '05.2.1': 'Julio Cesar'
  };

  modulos.forEach(modulo => {
    if (responsablesPorModulo[modulo.id] || responsablesTesoreria[modulo.sistema]) {
      modulo.desarrollador_asignado = responsablesPorModulo[modulo.id] || responsablesTesoreria[modulo.sistema];
    }
    const estadoAnterior = modulo.estado;
    const diferido = modulo.sistema === '08 Materiales' || /fase 2|segunda etapa|stand by|fuera del alcance/i.test(estadoAnterior);
    const parcial = /parcial|catálogo disponible|catalogo disponible|disponible parcialmente|requiere validación|requiere validacion/i.test(estadoAnterior);
    const pendienteValidacion = /pendiente de revisi[oó]n y validaci[oó]n funcional/i.test(estadoAnterior);
    const enDesarrollo = /^en desarrollo/i.test(estadoAnterior);
    const reinicioIngresos = modulo.sistema === '04 Ingresos';

    if (reinicioIngresos) modulo.estado = 'Pendiente de desarrollo';
    else if (diferido) modulo.estado = 'Segunda etapa';
    else if (pendienteValidacion) modulo.estado = 'Pendiente de desarrollo';
    else if (enDesarrollo) modulo.estado = 'En desarrollo';
    else if (!modulo.rutas.length) modulo.estado = 'Pendiente de desarrollo';
    else if (parcial) modulo.estado = 'En desarrollo';
    else modulo.estado = 'Desarrollado';

    modulo.detalle_estado = reinicioIngresos
      ? 'Existe desarrollo incipiente como antecedente, pero el módulo se desarrollará nuevamente desde cero.'
      : (estadoAnterior === modulo.estado ? '' : estadoAnterior);

    if (modulo.id === '04.1.2') {
      modulo.detalle_estado = 'Documentación funcional canónica creada; catálogo tipificado de enmiendas y cancelaciones.';
    }

    if (modulo.fases && !reinicioIngresos) {
      modulo.evaluacion = {
        persistencia_logica: Math.round((modulo.fases.f2 + modulo.fases.f3) / 2),
        backend: modulo.fases.f4,
        frontend: modulo.fases.f5,
        normatividad: Math.round((modulo.fases.f1 + modulo.fases.f6) / 2)
      };
      modulo.cumplimiento_final = Math.round(
        (modulo.evaluacion.persistencia_logica +
         modulo.evaluacion.backend +
         modulo.evaluacion.frontend +
         modulo.evaluacion.normatividad) / 4
      );
    } else {
      modulo.evaluacion = null;
      modulo.cumplimiento_final = null;
    }
  });

  pmData.modulos = modulos.sort((a,b)=>a.id.localeCompare(b.id,undefined,{numeric:true}));
  pmData.meta = {
    fecha_corte:'2026-08-31',
    jerarquia:'Sistema > Subsistema > Modulo > opciones internas',
    documentos_rectores:8,
    estados_kanban:['Pendiente de desarrollo','En desarrollo','Desarrollado','Segunda etapa'],
    dimensiones_cumplimiento:['Persistencia y Logica de Negocios','Backend','Frontend','Normatividad'],
    ponderacion_dimensiones:'25% cada dimension',
    nota_normativa:'Las calificaciones son evidencia tecnica y no constituyen certificacion normativa.'
  };
})();
