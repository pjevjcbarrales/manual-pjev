import codecs
import re

file_path = r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.1.4-registro-contratos.html'
with codecs.open(file_path, 'r', 'utf-8') as f:
    html = f.read()

# Find the table block that we just added
start_str = '<div class="section-title" style="margin-top:20px; font-size:16px;"><span class="section-num">1.1</span> Proceso Funcional</div>'
start_idx = html.find(start_str)

if start_idx != -1:
    end_idx = html.find('</table>', start_idx) + 8
    
    table_block = html[start_idx:end_idx]
    
    # Remove it from the current location
    html = html[:start_idx] + html[end_idx:]
    
    # Reformat the title to match the header style
    table_block = table_block.replace(start_str, '<div style="margin-top: 20px; font-size: 14px; font-weight: 700; color: #183125; border-bottom: 1px solid #d4c9b5; padding-bottom: 5px; margin-bottom: 10px;">PROCESO OPERATIVO Y FUNCIONAL</div>')
    
    # Also adjust the table background for the header (crema background)
    table_block = table_block.replace('<table class="props-table">', '<table class="props-table" style="background:#fff; font-size:12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">')

    # Find where to insert it in the header
    # We want it inside the elem-header div
    badge_end = html.find('</div>', html.find('class="mod-header-badges"')) + 6
    
    # Insert it right after the badges in the header
    html = html[:badge_end] + '\n\n        ' + table_block + html[badge_end:]
    
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.write(html)
    print("Table successfully moved to the header")
else:
    print("Table block not found")
