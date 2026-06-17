import codecs

file_path = r'c:\dixsys\manual_pjev\sitio_web\index.html'
with codecs.open(file_path, 'r', 'utf-8') as f:
    html = f.read()

# We need to insert the 02.4 subgroup before the "03 - Contabilidad" group starts
# Find the next group after 02
insert_marker = '<div class="sidebar-group-label">03'
insert_idx = html.find(insert_marker)

if insert_idx != -1:
    # Walk back to find the closing div of the previous subgroup, or the start of the 03 group container
    # The structure is:
    # </div>
    # <div class="sidebar-group">
    #   <div class="sidebar-group-label">03...
    
    group_start_idx = html.rfind('<div class="sidebar-group">', 0, insert_idx)
    
    subgroup_html = '''
      <div class="sidebar-subgroup">
        <div class="sidebar-subgroup-label">02.4 — Manuales de Usuario</div>
        <a class="sidebar-link" target="contentFrame" href="02_presupuesto/02.4.1-manual-bienes-inmuebles.html">Catálogo de Bienes Inmuebles <span class="sidebar-id">02.4.1</span></a>
        <a class="sidebar-link" target="contentFrame" href="02_presupuesto/02.4.2-manual-contratos.html">Registro de Contratos <span class="sidebar-id">02.4.2</span></a>
      </div>
    '''
    
    html = html[:group_start_idx] + subgroup_html + html[group_start_idx:]
    
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.write(html)
    print("index.html updated successfully.")
else:
    print("Could not find '03' section in index.html.")
