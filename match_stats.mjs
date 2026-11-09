import XLSX from 'xlsx';
const rows=(f,s)=>XLSX.utils.sheet_to_json(XLSX.readFile(f).Sheets[s],{defval:null,raw:false});
const emp=rows('Catalogo_Empleados.xlsx','Empleados');
const bal=rows('balanza_comprobacion_enero.xlsx','Balanza (PDF)');
const norm=s=>String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase().replace(/\bHEDZ\b/g,'HERNANDEZ').replace(/[^A-Z0-9 ]/g,' ').replace(/\s+/g,' ').trim();
const person=s=>norm(s).replace(/^(DEUDOR(?:ES)?|EMPLEADO)\s+/,'').trim();
const key=s=>person(s).split(' ').filter(Boolean).sort().join(' ');
const map=new Map(); for(const e of emp){const k=key(e.Nombre); if(!map.has(k))map.set(k,[]);map.get(k).push(e)}
const candidates=bal.filter(b=>{const a=String(b['Cuenta Contable']??'');const d=norm(b.Descripcion??b['Descripción']);return (/^(11233|11234|21191)/.test(a)&&!/(VARIOS|EJERCICIOS|CHEQUES|RETENCIONES|CONTRIB)/.test(d));});
let matched=0; const misses=[];
for(const b of candidates){const found=map.get(key(b.Descripcion??b['Descripción']))??[];if(found.length===1)matched++;else misses.push({cuenta:b['Cuenta Contable'],desc:b.Descripcion??b['Descripción'],key:key(b.Descripcion??b['Descripción']),found:found.map(e=>e.Nombre)});}
console.log({candidates:candidates.length,matched,misses:misses.length});
console.log(JSON.stringify(misses,null,2));
