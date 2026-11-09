import fs from 'node:fs/promises';
import path from 'node:path';
import XLSX from 'xlsx';
import ExcelJS from 'exceljs';

const OUTPUT_DIR = path.resolve('outputs', 'correlacion_20260721');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'Correlacion_Empleados_Cuentas_Balanza_Enero.xlsx');

const readRows = (file, sheet) => XLSX.utils.sheet_to_json(XLSX.readFile(file).Sheets[sheet], { defval: null, raw: false });
const employeeRows = readRows('Catalogo_Empleados.xlsx', 'Empleados');
const accountRows = readRows('catalogo_cuentas_2026-07-22.xls', 'Sheet1').filter(r => r['Cuenta contable'] != null && /^\d/.test(String(r['Cuenta contable']).trim()));
const balanceRows = readRows('balanza_comprobacion_enero.xlsx', 'Balanza (PDF)');

const cleanAccount = value => String(value ?? '').replace(/\D/g, '');
const normalize = value => String(value ?? '')
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .toUpperCase().replace(/\bHEDZ\b/g, 'HERNANDEZ')
  .replace(/[^A-Z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
const personName = value => normalize(value).replace(/^(DEUDOR(?:ES)?|EMPLEADO)\s+/, '').trim();
const personKey = value => personName(value).split(' ').filter(Boolean).sort().join(' ');
const parseAmount = value => {
  if (value == null || value === '') return null;
  const n = Number(String(value).replace(/,/g, ''));
  return Number.isFinite(n) ? n : null;
};
const isPersonRow = row => {
  const account = cleanAccount(row['Cuenta Contable'] ?? row.Cuenta);
  const desc = normalize(row.Descripcion ?? row['Descripción']);
  if (/^(DEUDOR\s|EMPLEADO\s)/.test(desc)) return true;
  return account.startsWith('21191') && !/(CHEQUES|RETENCIONES|CONTRIB|DIVERSOS|VARIOS|EJERCICIOS)/.test(desc);
};

const accountMap = new Map();
for (const row of accountRows) {
  const key = cleanAccount(row['Cuenta contable']);
  if (!key) continue;
  const current = accountMap.get(key);
  if (!current || Number(row.Nivel) > Number(current.Nivel)) accountMap.set(key, row);
}

const employeeMap = new Map();
for (const row of employeeRows) {
  const key = personKey(row.Nombre);
  if (!employeeMap.has(key)) employeeMap.set(key, []);
  employeeMap.get(key).push(row);
}

const correlated = balanceRows.map((balance, index) => {
  const accountClean = cleanAccount(balance['Cuenta Contable'] ?? balance.Cuenta);
  const account = accountMap.get(accountClean) ?? null;
  const appliesEmployee = isPersonRow(balance);
  const matches = appliesEmployee ? (employeeMap.get(personKey(balance.Descripcion ?? balance['Descripción'])) ?? []) : [];
  const employee = matches.length === 1 ? matches[0] : null;
  const employeeStatus = !appliesEmployee ? 'No aplica' : matches.length === 1 ? 'Coincidencia única' : matches.length > 1 ? 'Coincidencia ambigua' : 'Sin coincidencia';
  return {
    consecutivo: index + 1,
    cuentaBalanza: balance.Cuenta,
    cuentaLimpia: accountClean,
    descripcionBalanza: balance.Descripcion ?? balance['Descripción'],
    saldoInicial: parseAmount(balance['Saldo Inicial']),
    cargo: parseAmount(balance.Cargo),
    abono: parseAmount(balance.Abono),
    saldoFinal: parseAmount(balance['Saldo Final']),
    cuentaCatalogo: account?.['Cuenta contable'] ?? null,
    descripcionCatalogo: account?.['Descripción'] ?? null,
    nivel: account?.Nivel ?? null,
    tipo: account?.Tipo ?? null,
    naturaleza: account?.Naturaleza ?? null,
    nivelAfectacion: account?.['Nivel afectación'] ?? null,
    criCog: account?.['CRI/COG'] ?? null,
    estatusCuenta: account?.Estatus ?? null,
    resultadoCuenta: account ? 'Coincidencia exacta' : 'Sin coincidencia',
    esPersona: appliesEmployee ? 'Sí' : 'No',
    numeroEmpleado: employee?.['Número Empleado'] ?? null,
    nombreEmpleado: employee?.Nombre ?? null,
    rfc: employee?.RFC ?? null,
    curp: employee?.CURP ?? null,
    puesto: employee?.Puesto ?? null,
    categoria: employee?.['Categoría'] ?? null,
    email: employee?.['Email Institucional'] ?? null,
    estatusEmpleado: employee?.Estatus ?? null,
    resultadoEmpleado: employeeStatus,
    metodo: employee ? 'Nombre normalizado; prefijo removido; orden de palabras indiferente' : null,
    observacion: appliesEmployee && !employee ? 'Revisar manualmente contra el catálogo de empleados' : null,
  };
});

const wb = new ExcelJS.Workbook();
wb.creator = 'OpenAI Codex';
wb.created = new Date();
wb.modified = new Date();
wb.subject = 'Correlación de catálogo de empleados, catálogo de cuentas y balanza de comprobación';

const colors = { navy: '17365D', blue: '1F4E78', lightBlue: 'D9EAF7', green: 'E2F0D9', yellow: 'FFF2CC', red: 'FCE4D6', gray: 'E7E6E6', white: 'FFFFFF' };
const thinBorder = { top:{style:'thin',color:{argb:'FFD9E1F2'}}, left:{style:'thin',color:{argb:'FFD9E1F2'}}, bottom:{style:'thin',color:{argb:'FFD9E1F2'}}, right:{style:'thin',color:{argb:'FFD9E1F2'}} };

function title(ws, text, subtitle, lastCol) {
  ws.mergeCells(1, 1, 1, lastCol);
  ws.getCell(1,1).value = text;
  ws.getCell(1,1).font = { bold:true, size:16, color:{argb:colors.white} };
  ws.getCell(1,1).fill = { type:'pattern', pattern:'solid', fgColor:{argb:colors.navy} };
  ws.getCell(1,1).alignment = { vertical:'middle', horizontal:'left' };
  ws.getRow(1).height = 28;
  ws.mergeCells(2, 1, 2, lastCol);
  ws.getCell(2,1).value = subtitle;
  ws.getCell(2,1).font = { italic:true, size:10, color:{argb:'FF404040'} };
  ws.getCell(2,1).fill = { type:'pattern', pattern:'solid', fgColor:{argb:'FFF2F2F2'} };
  ws.getCell(2,1).alignment = { vertical:'middle' };
  ws.getRow(2).height = 23;
}

const columns = [
  ['Consecutivo','consecutivo',11], ['Cuenta balanza','cuentaBalanza',21], ['Cuenta limpia','cuentaLimpia',16], ['Descripción balanza','descripcionBalanza',44],
  ['Saldo inicial','saldoInicial',16], ['Cargo','cargo',14], ['Abono','abono',14], ['Saldo final','saldoFinal',16],
  ['Cuenta catálogo','cuentaCatalogo',21], ['Descripción catálogo','descripcionCatalogo',44], ['Nivel','nivel',9], ['Tipo','tipo',15], ['Naturaleza','naturaleza',14],
  ['Nivel afectación','nivelAfectacion',20], ['CRI/COG','criCog',15], ['Estatus cuenta','estatusCuenta',15], ['Resultado cuenta','resultadoCuenta',19], ['Es persona','esPersona',11],
  ['Número empleado','numeroEmpleado',17], ['Nombre empleado','nombreEmpleado',38], ['RFC','rfc',16], ['CURP','curp',20], ['Puesto','puesto',32], ['Categoría','categoria',30],
  ['Email institucional','email',32], ['Estatus empleado','estatusEmpleado',16], ['Resultado empleado','resultadoEmpleado',21], ['Método','metodo',44], ['Observación','observacion',44],
];

function addDataSheet(name, titleText, subtitle, data) {
  const ws = wb.addWorksheet(name, { views:[{state:'frozen', ySplit:3, xSplit:3}] });
  title(ws, titleText, subtitle, columns.length);
  ws.columns = columns.map(([header,key,width]) => ({ header, key, width }));
  const headerRow = ws.getRow(3);
  columns.forEach(([header], i) => headerRow.getCell(i+1).value = header);
  headerRow.height = 33;
  headerRow.eachCell(cell => { cell.font={bold:true,color:{argb:colors.white}}; cell.fill={type:'pattern',pattern:'solid',fgColor:{argb:colors.blue}}; cell.alignment={horizontal:'center',vertical:'middle',wrapText:true}; cell.border=thinBorder; });
  for (const item of data) {
    const row = ws.addRow(item);
    row.eachCell({includeEmpty:true}, cell => { cell.border=thinBorder; cell.alignment={vertical:'top',wrapText:false}; });
    for (const idx of [5,6,7,8]) row.getCell(idx).numFmt = '#,##0.00;[Red]-#,##0.00';
    for (const idx of [2,3,9,15,19,21,22]) row.getCell(idx).numFmt = '@';
    const accountStatus = row.getCell(17);
    accountStatus.fill = {type:'pattern',pattern:'solid',fgColor:{argb:item.resultadoCuenta==='Coincidencia exacta'?colors.green:colors.red}};
    const employeeStatus = row.getCell(27);
    employeeStatus.fill = {type:'pattern',pattern:'solid',fgColor:{argb:item.resultadoEmpleado==='Coincidencia única'?colors.green:item.resultadoEmpleado==='No aplica'?colors.gray:colors.yellow}};
  }
  ws.autoFilter = { from:{row:3,column:1}, to:{row:Math.max(3,data.length+3),column:columns.length} };
  ws.pageSetup = { orientation:'landscape', fitToPage:true, fitToWidth:1, fitToHeight:0, paperSize:9, margins:{left:0.25,right:0.25,top:0.5,bottom:0.5,header:0.2,footer:0.2} };
  return ws;
}

addDataSheet('Correlación', 'Correlación integral', 'Balanza de enero cruzada con catálogo de cuentas y catálogo de empleados.', correlated);
const employeeRelated = correlated.filter(r => r.esPersona === 'Sí');
addDataSheet('Cuentas de empleados', 'Cuentas relacionadas con empleados', 'Incluye coincidencias y casos pendientes para revisión manual.', employeeRelated);
addDataSheet('Sin cuenta catálogo', 'Cuentas de balanza sin coincidencia', 'Cuentas cuyo identificador limpio no aparece en el catálogo contable proporcionado.', correlated.filter(r => r.resultadoCuenta === 'Sin coincidencia'));
addDataSheet('Sin empleado', 'Personas sin coincidencia en empleados', 'Nombres detectados en la balanza que no tuvieron una coincidencia única en el catálogo de empleados.', employeeRelated.filter(r => r.resultadoEmpleado !== 'Coincidencia única'));

const summary = wb.addWorksheet('Resumen', { views:[{state:'frozen', ySplit:4}] });
title(summary, 'Resumen y reglas de correlación', 'Resultado del procesamiento de los tres archivos fuente.', 5);
summary.columns = [{width:34},{width:18},{width:18},{width:60},{width:25}];
summary.getRow(3).values = ['Indicador','Cantidad','Porcentaje','Interpretación','Fuente'];
summary.getRow(3).eachCell(c=>{c.font={bold:true,color:{argb:colors.white}};c.fill={type:'pattern',pattern:'solid',fgColor:{argb:colors.blue}};c.alignment={horizontal:'center',vertical:'middle',wrapText:true};c.border=thinBorder;});
const countAccount = correlated.filter(r=>r.resultadoCuenta==='Coincidencia exacta').length;
const countPeople = employeeRelated.length;
const countEmployees = employeeRelated.filter(r=>r.resultadoEmpleado==='Coincidencia única').length;
const metrics = [
  ['Registros de balanza',correlated.length,1,'Total de filas procesadas de la balanza.','balanza_comprobacion_enero.xlsx'],
  ['Cuentas con coincidencia',countAccount,correlated.length?countAccount/correlated.length:0,'Cruce exacto por cuenta sin separadores.','Catálogo de cuentas'],
  ['Cuentas sin coincidencia',correlated.length-countAccount,correlated.length?(correlated.length-countAccount)/correlated.length:0,'Requieren revisión del catálogo contable.','Catálogo de cuentas'],
  ['Filas identificadas como persona',countPeople,correlated.length?countPeople/correlated.length:0,'Descripciones individuales de deudor/empleado.','Balanza'],
  ['Empleados con coincidencia única',countEmployees,countPeople?countEmployees/countPeople:0,'Nombre normalizado encontrado una sola vez.','Catálogo de empleados'],
  ['Personas sin coincidencia única',countPeople-countEmployees,countPeople?(countPeople-countEmployees)/countPeople:0,'Requieren revisión manual.','Catálogo de empleados'],
];
for (const m of metrics) { const r=summary.addRow(m); r.eachCell(c=>{c.border=thinBorder;c.alignment={vertical:'top',wrapText:true};});r.getCell(3).numFmt='0.0%'; }
let row = metrics.length + 6;
summary.mergeCells(row,1,row,5); summary.getCell(row,1).value='Reglas aplicadas'; summary.getCell(row,1).font={bold:true,color:{argb:colors.white}};summary.getCell(row,1).fill={type:'pattern',pattern:'solid',fgColor:{argb:colors.navy}};
const rules = [
  'Cuenta contable: se eliminan puntos, guiones, espacios y otros separadores; la comparación se realiza con la secuencia numérica resultante.',
  'Empleado: solo se intenta correlacionar cuando la balanza identifica una persona mediante “DEUDOR”, “EMPLEADO” o una cuenta individual de acreedores 21191.',
  'Nombre: se eliminan acentos, signos y espacios repetidos; se retiran los prefijos DEUDOR/EMPLEADO; “HEDZ” se interpreta como HERNANDEZ.',
  'El orden de las palabras no afecta la comparación, para conciliar “nombre-apellidos” con “apellidos-nombre”.',
  'Solo se acepta automáticamente una coincidencia única; los casos ambiguos o inexistentes quedan separados para revisión.',
];
for (const rule of rules) { row++; summary.mergeCells(row,1,row,5); const c=summary.getCell(row,1);c.value=`• ${rule}`;c.alignment={wrapText:true,vertical:'top'};c.border=thinBorder;summary.getRow(row).height=32; }
row += 2;
summary.mergeCells(row,1,row,5); summary.getCell(row,1).value='Archivos fuente'; summary.getCell(row,1).font={bold:true,color:{argb:colors.white}};summary.getCell(row,1).fill={type:'pattern',pattern:'solid',fgColor:{argb:colors.navy}};
for (const source of ['Catalogo_Empleados.xlsx','catalogo_cuentas_2026-07-22.xls','balanza_comprobacion_enero.xlsx']) { row++; summary.mergeCells(row,1,row,5); summary.getCell(row,1).value=source;summary.getCell(row,1).border=thinBorder; }

await fs.mkdir(OUTPUT_DIR, { recursive:true });
await wb.xlsx.writeFile(OUTPUT_FILE);
console.log(JSON.stringify({ output:OUTPUT_FILE, rows:correlated.length, accountMatches:countAccount, accountMisses:correlated.length-countAccount, personRows:countPeople, employeeMatches:countEmployees, employeeMisses:countPeople-countEmployees }, null, 2));
