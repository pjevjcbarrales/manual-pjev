import XLSX from 'xlsx';

const readRows = (file, sheet) => XLSX.utils.sheet_to_json(XLSX.readFile(file).Sheets[sheet], { defval: null, raw: false });
const employees = readRows('Catalogo_Empleados.xlsx', 'Empleados');
const accountRows = readRows('catalogo_cuentas_2026-07-22.xls', 'Sheet1');
const accounts = accountRows.filter(r => r['Cuenta contable'] != null && !String(r['Cuenta contable']).startsWith('==='));
const balance = readRows('balanza_comprobacion_enero.xlsx', 'Balanza (PDF)');
const norm = s => String(s ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase().replace(/[^A-ZÑ0-9 ]/g,' ').replace(/\s+/g,' ').trim();
const stripLeadingNumbers = s => norm(s).replace(/^(?:\d+\s+)+/, '').trim();
const tokenKey = s => stripLeadingNumbers(s).split(' ').filter(Boolean).sort().join(' ');
const byName = new Map();
const byTokens = new Map();
for (const e of employees) {
  const n = norm(e.Nombre);
  if (!byName.has(n)) byName.set(n, []);
  byName.get(n).push(e);
  const tk = tokenKey(e.Nombre);
  if (!byTokens.has(tk)) byTokens.set(tk, []);
  byTokens.get(tk).push(e);
}

const exactAccounts = [];
for (const a of accounts) {
  const n = norm(a['Descripción']);
  const n2 = stripLeadingNumbers(a['Descripción']);
  const found = byName.get(n) ?? byName.get(n2) ?? byTokens.get(tokenKey(a['Descripción']));
  if (found) exactAccounts.push({ cuenta:a['Cuenta contable'], nivel:a.Nivel, descripcion:a['Descripción'], empleados:found.map(e=>e['Número Empleado']) });
}

const cleanAcct = s => String(s ?? '').replace(/\D/g,'');
const balanceAccounts = new Set(balance.map(r => cleanAcct(r['Cuenta Contable'] ?? r.Cuenta)));
const exactInBalance = exactAccounts.filter(x => balanceAccounts.has(cleanAcct(x.cuenta)));
console.log(JSON.stringify({ employees:employees.length, accounts:accounts.length, balance:balance.length, exactAccounts:exactAccounts.length, exactInBalance:exactInBalance.length }, null, 2));
console.log('NIVELES', [...new Set(accountRows.map(r=>String(r.Nivel)))].slice(0,30));
console.log('NIVEL6', accountRows.filter(r=>String(r.Nivel).trim()==='6').slice(0,20));
for (const needle of ['0000782302','ABAD','PASTRANA','LINA','682968']) {
  console.log('BUSCA', needle, accountRows.filter(r=>JSON.stringify(r).toUpperCase().includes(needle)).slice(0,10));
}
console.log('\nEXACTOS EN BALANZA');
for (const x of exactInBalance.slice(0,100)) console.log(JSON.stringify(x));
console.log('\nCUENTAS EXACTAS EJEMPLOS');
for (const x of exactAccounts.slice(0,100)) console.log(JSON.stringify(x));

console.log('\nBALANZA SIN EXACTO, POSIBLES NOMBRES');
for (const b of balance) {
  const desc = stripLeadingNumbers(b.Descripcion ?? b['Descripción']);
  const candidates = employees.filter(e => {
    const en = norm(e.Nombre);
    return desc === en || desc.includes(en) || en.includes(desc);
  });
  if (candidates.length) console.log(JSON.stringify({cuenta:b['Cuenta Contable'], desc:b.Descripcion ?? b['Descripción'], candidatos:candidates.map(e=>[e['Número Empleado'],e.Nombre])}));
}
console.log('\nBALANZA COMPLETA');
for (const b of balance) console.log(JSON.stringify({cuenta:b['Cuenta Contable'], desc:b.Descripcion ?? b['Descripción'], si:b['Saldo Inicial'], cargo:b.Cargo, abono:b.Abono, sf:b['Saldo Final']}));
