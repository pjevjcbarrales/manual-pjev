import codecs

file_path = r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.1.4-registro-contratos.html'
with codecs.open(file_path, 'r', 'utf-8') as f:
    html = f.read()

# 1. Extract the table from the header
start_table = html.find('<div style="margin-top: 20px; font-size: 14px;')
end_table = html.find('</table>', start_table) + 8

table_html = html[start_table:end_table]

# Remove table from header
html = html[:start_table] + html[end_table:]

# Clean up the table title inside the modal
table_html = table_html.replace('<div style="margin-top: 20px; font-size: 14px; font-weight: 700; color: #183125; border-bottom: 1px solid #d4c9b5; padding-bottom: 5px; margin-bottom: 10px;">PROCESO OPERATIVO Y FUNCIONAL</div>', '')

# Make the table visually match Anexo 2
table_html = table_html.replace('<table class="props-table" style="background:#fff; font-size:12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', '<table class="props-table">')
table_html = table_html.replace('<thead>\n          <tr>', '<thead>\n          <tr style="background: var(--pjev-verde-oscuro); color: white;">')

# 2. Add the Top Bar right after <body>
top_bar = '''
<div style="position: fixed; top: 20px; right: 45px; display: flex; flex-wrap: wrap; justify-content: flex-end; align-items: center; gap: 10px; z-index: 9999; max-width: calc(-60px + 100vw);">
  <button style="padding: 6px 12px; font-size: 11px; font-weight: bold; cursor: pointer; border: 1px solid rgb(27, 58, 45); border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 5px; transition: background 0.2s; white-space: nowrap; display: inline-flex; align-items: center; justify-content: center; background: rgb(27, 58, 45); color: rgb(255, 255, 255);">📊 Ver Diagrama</button>
  <button style="padding: 6px 12px; font-size: 11px; font-weight: bold; cursor: pointer; border: 1px solid rgb(153, 27, 27); border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 5px; transition: background 0.2s; white-space: nowrap; display: inline-flex; align-items: center; justify-content: center; background: rgb(153, 27, 27); color: rgb(255, 255, 255);">📋 Proceso Funcional</button>
  <button style="padding: 6px 12px; font-size: 11px; font-weight: bold; cursor: pointer; border: 1px solid rgb(212, 201, 181); border-radius: 6px; background: rgb(255, 255, 255); color: rgb(27, 58, 45); box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 5px; transition: background 0.2s; white-space: nowrap; display: inline-flex; align-items: center; justify-content: center;" onclick="window.location.reload()">⟳ Refrescar</button>
  <button style="padding: 6px 12px; font-size: 11px; font-weight: bold; cursor: pointer; border: 1px solid rgb(212, 201, 181); border-radius: 6px; background: rgb(255, 255, 255); color: rgb(27, 58, 45); box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 5px; transition: background 0.2s; white-space: nowrap; display: inline-flex; align-items: center; justify-content: center;" onclick="window.print()">🖨 Imprimir</button>
</div>
'''

html = html.replace('<body>', '<body>\n' + top_bar)

# 3. Add Modal and JS at the end before </body>
modal_and_js = f'''
<div id="anexos-impresos" class="modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:10000; align-items:center; justify-content:center;">
    <div class="modal-box" style="background:#fff; padding:25px; border-radius:8px; max-width:850px; width:95%; max-height:90vh; overflow-y:auto; position:relative; box-shadow:0 10px 25px rgba(0,0,0,0.2);">
        <div class="modal-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;">
            <h3 style="color: var(--pjev-verde-oscuro); font-size: 16px; margin: 0;">Anexo 2: Flujograma de Procesos y Descripción</h3>
            <button class="modal-close" onclick="document.getElementById('anexos-impresos').style.display='none'" style="background:none; border:none; color:#991b1b; cursor:pointer; font-weight:bold; font-size:14px;">❌ Cerrar</button>
        </div>
        <div id="module-process-table" class="modal-body">
            {table_html}
        </div>
    </div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', () => {{
    const buttons = document.querySelectorAll('button');
    buttons.forEach(b => {{
      if (b.innerText.includes('Proceso Funcional') || b.innerText.includes('Ver Diagrama')) {{
        b.onclick = () => {{
          document.getElementById('anexos-impresos').style.display = 'flex';
        }};
      }}
    }});
  }});
</script>
'''

html = html.replace('</body>', modal_and_js + '\n</body>')

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(html)
print('Script applied successfully.')
