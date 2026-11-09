import XLSX from 'xlsx';

const files = [
  'Catalogo_Empleados.xlsx',
  'catalogo_cuentas_2026-07-22.xls',
  'balanza_comprobacion_enero.xlsx',
  'Balanza_y_Catalogo_Completos.xlsx',
  'Correspondencia_Balanza_Catalogo.xlsx',
  'Discrepancias_Nivel6.xlsx',
];

for (const file of files) {
  const wb = XLSX.readFile(file, { cellDates: true, cellFormula: true });
  console.log(`\n### ${file}`);
  for (const name of wb.SheetNames) {
    const ws = wb.Sheets[name];
    const range = ws['!ref'] ?? '(vacía)';
    const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: null, raw: false });
    console.log(`-- ${name} ${range} filas=${rows.length}`);
    for (const row of rows.slice(0, 12)) console.log(JSON.stringify(row));
  }
}
