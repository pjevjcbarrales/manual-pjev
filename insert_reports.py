import sys
import json
import re

filepath = r'c:\dixsys\manual_pjev\sitio_web\pm_data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const pmData = (\{.*\});?', content, re.DOTALL)
if match:
    json_str = match.group(1)
    data = json.loads(json_str)
    
    nuevos_reportes = [
        {
            "id": "07.4.1",
            "nombre": "Programa Anual de Adquisiciones (PAAAS)",
            "sistema": "Recursos Materiales",
            "subsistema": "Informes",
            "tipo_formulario": "Reporte",
            "modo_codigo": "A",
            "desarrollador_asignado": "Daryl",
            "estado": "Pendiente",
            "avance_desarrollo": 0,
            "analisis_funcional": 0
        },
        {
            "id": "07.4.2",
            "nombre": "Cuadro Comparativo de Cotizaciones",
            "sistema": "Recursos Materiales",
            "subsistema": "Informes",
            "tipo_formulario": "Reporte",
            "modo_codigo": "A",
            "desarrollador_asignado": "Daryl",
            "estado": "Pendiente",
            "avance_desarrollo": 0,
            "analisis_funcional": 0
        },
        {
            "id": "07.4.3",
            "nombre": "Contratos y Pedidos Adjudicados",
            "sistema": "Recursos Materiales",
            "subsistema": "Informes",
            "tipo_formulario": "Reporte",
            "modo_codigo": "A",
            "desarrollador_asignado": "Daryl",
            "estado": "Pendiente",
            "avance_desarrollo": 0,
            "analisis_funcional": 0
        },
        {
            "id": "07.4.4",
            "nombre": "Padrón de Proveedores",
            "sistema": "Recursos Materiales",
            "subsistema": "Informes",
            "tipo_formulario": "Reporte",
            "modo_codigo": "A",
            "desarrollador_asignado": "Daryl",
            "estado": "Pendiente",
            "avance_desarrollo": 0,
            "analisis_funcional": 0
        },
        {
            "id": "07.4.5",
            "nombre": "Reporte de Fallos y Actas del Comité",
            "sistema": "Recursos Materiales",
            "subsistema": "Informes",
            "tipo_formulario": "Reporte",
            "modo_codigo": "A",
            "desarrollador_asignado": "Daryl",
            "estado": "Pendiente",
            "avance_desarrollo": 0,
            "analisis_funcional": 0
        }
    ]
    
    # Prepend the reports to the modulos list or append them. We'll append them.
    # Actually, appending at the end is fine.
    data['modulos'].extend(nuevos_reportes)

    new_json_str = json.dumps(data, indent=4, ensure_ascii=False)
    new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Éxito: Se agregaron {len(nuevos_reportes)} reportes a pm_data.js")
else:
    print("Error: No se encontró pmData.")
