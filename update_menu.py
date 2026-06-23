import json
import os
import re

def main():
    os.chdir('c:/dixsys/manual_pjev/sitio_web')

    # 1. Update pm_data.json
    with open('pm_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for mod in data['modulos']:
        if mod['id'] == '07.2.4.1': mod['id'] = '07.2.5.1'
        elif mod['id'] == '07.2.3.3': mod['id'] = '07.2.4.3'
        elif mod['id'] == '07.2.3.2': mod['id'] = '07.2.4.2'
        elif mod['id'] == '07.2.3.1': mod['id'] = '07.2.4.1'
        elif mod['id'] == '07.2.2.3': mod['id'] = '07.2.3.3'
        elif mod['id'] == '07.2.2.2': mod['id'] = '07.2.3.2'
        elif mod['id'] == '07.2.2.1': mod['id'] = '07.2.3.1'
        elif mod['id'] == '07.2.1': mod['id'] = '07.2.2'

    # insert the new module 07.2.1
    new_mod = {
        "id": "07.2.1",
        "nombre": "Requerimientos de adquisiciones",
        "desarrollador_asignado": "Sin asignar",
        "avance_desarrollo": 0,
        "iteracion_desarrollo": 0,
        "tipo_formulario": "Compuesto",
        "visitas": []
    }
    
    # insert before 07.2.2
    idx_07_2_2 = next((i for i, m in enumerate(data['modulos']) if m['id'] == '07.2.2'), None)
    if idx_07_2_2 is not None:
        data['modulos'].insert(idx_07_2_2, new_mod)
    else:
        data['modulos'].append(new_mod)

    with open('pm_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # 2. Update pm_data.js (it's just 'const pmData = ' + JSON)
    with open('pm_data.js', 'w', encoding='utf-8') as f:
        f.write('const pmData = ')
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write(';\n')

    # 3. Update index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The block we need to replace in index.html is roughly:
    # 07.2.4.1 -> 07.2.5.1
    # 07.2.4 -> 07.2.5
    # 07.2.3.3 -> 07.2.4.3
    # 07.2.3.2 -> 07.2.4.2
    # 07.2.3.1 -> 07.2.4.1
    # 07.2.3 -> 07.2.4
    # 07.2.2.3 -> 07.2.3.3
    # 07.2.2.2 -> 07.2.3.2
    # 07.2.2.1 -> 07.2.3.1
    # 07.2.2 -> 07.2.3
    # 07.2.1-suficiencia.html -> 07.2.2-suficiencia.html
    # 07.2.1 -> 07.2.2
    
    # Let's do string replacements carefully to not mess up.
    replacements = [
        ('07.2.4 Registro de Devengado', '07.2.5 Registro de Devengado'),
        ('07.2.4.1', '07.2.5.1'),
        ('07.2.3 Registro de Comprometido', '07.2.4 Registro de Comprometido'),
        ('07.2.3.3', '07.2.4.3'),
        ('07.2.3.2', '07.2.4.2'),
        ('07.2.3.1', '07.2.4.1'),
        ('07.2.2 Compras', '07.2.3 Compras'),
        ('07.2.2.3', '07.2.3.3'),
        ('07.2.2.2', '07.2.3.2'),
        ('07.2.2.1', '07.2.3.1'),
        ('07.2.1-suficiencia.html', '07.2.2-suficiencia.html'),
        ('>07.2.1<', '>07.2.2<') # for the badge span
    ]
    for old, new in replacements:
        html = html.replace(old, new)
        
    # Now insert the new link for 07.2.1 right after <div class="sidebar-subgroup-label">07.2 · Registros</div>
    new_link = '<a class="sidebar-link" target="contentFrame" href="07_recursos_materiales/07.2.1-requerimientos-adquisiciones.html">Requerimientos de Adquisiciones <span class="sidebar-id">07.2.1</span></a>\n        '
    html = html.replace('<div class="sidebar-subgroup-label">07.2 · Registros</div>', '<div class="sidebar-subgroup-label">07.2 · Registros</div>\n        ' + new_link)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Updates applied to pm_data and index.html")

if __name__ == '__main__':
    main()
