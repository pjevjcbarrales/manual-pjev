import ExcelJS from 'exceljs';
import XLSX from 'xlsx';
const file='outputs/correlacion_20260721/Correlacion_Empleados_Cuentas_Balanza_Enero.xlsx';
const wb=new ExcelJS.Workbook(); await wb.xlsx.readFile(file);
const result={sheets:[],errors:[],totals:{}};
for(const ws of wb.worksheets){
  result.sheets.push({name:ws.name,rows:ws.rowCount,columns:ws.columnCount,filter:!!ws.autoFilter,frozen:ws.views?.[0]?.state==='frozen'});
  ws.eachRow(row=>row.eachCell(cell=>{if(typeof cell.value==='string'&&/#REF!|#DIV\/0!|#VALUE!|#NAME\?|#N\/A/.test(cell.value))result.errors.push(`${ws.name}!${cell.address}:${cell.value}`);}));
}
const corr=wb.getWorksheet('Correlación');
let si=0,cargo=0,abono=0,sf=0,accountMatches=0,employeeMatches=0;
for(let r=4;r<=corr.rowCount;r++){si+=Number(corr.getCell(r,5).value??0);cargo+=Number(corr.getCell(r,6).value??0);abono+=Number(corr.getCell(r,7).value??0);sf+=Number(corr.getCell(r,8).value??0);if(corr.getCell(r,17).value==='Coincidencia exacta')accountMatches++;if(corr.getCell(r,27).value==='Coincidencia única')employeeMatches++;}
result.totals={rows:corr.rowCount-3,saldoInicial:si,cargo,abono,saldoFinal:sf,accountMatches,employeeMatches};
const src=XLSX.utils.sheet_to_json(XLSX.readFile('balanza_comprobacion_enero.xlsx').Sheets['Balanza (PDF)'],{defval:null,raw:false});
const num=v=>Number(String(v??0).replace(/,/g,''));
result.sourceTotals={rows:src.length,saldoInicial:src.reduce((a,r)=>a+num(r['Saldo Inicial']),0),cargo:src.reduce((a,r)=>a+num(r.Cargo),0),abono:src.reduce((a,r)=>a+num(r.Abono),0),saldoFinal:src.reduce((a,r)=>a+num(r['Saldo Final']),0)};
result.reconciles=Object.keys(result.sourceTotals).every(k=>Math.abs((result.sourceTotals[k]??0)-(result.totals[k]??0))<0.005);
console.log(JSON.stringify(result,null,2));
