"""Extrae el bloque 2530 del CADIDO recibido; no modifica fuentes ni bases de datos.

Ejecutar con el Python del runtime de Codex (pdfplumber). El resultado es una
referencia documental versionada, no una migración ni un catálogo autorizado.
"""
import hashlib
import json
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path('C:/Users/jcbar/Downloads')
FILES = [
    ('PADA_2025', 'PROGRAMA_ANUAL_DE_DESARROLLO_ARCHIVISTICO_2025.pdf', 20),
    ('CGCA_2024', 'CUADRO_DE_CLASIFICACION_ARCHIVISTICA_2024.pdf', 34),
    ('CADIDO_2024', 'CATALOGO__DE_DISPOSICION_DOCUMENTAL_2024.pdf', 39),
    ('CADIDO_2024_COPIA', 'CATALOGO__DE_DISPOSICION_DOCUMENTAL_2024 (1).pdf', 39),
    ('XLV_2025_T1', 'XLV_c.xls', None),
]
sources = []
for source_id, filename, pages in FILES:
    source = DOWNLOADS / filename
    sources.append({
        'id': source_id, 'nombre': filename, 'ruta_original': str(source),
        'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'bytes': source.stat().st_size, 'paginas': pages,
        'duplicado_de': 'CADIDO_2024' if source_id == 'CADIDO_2024_COPIA' else None,
    })
assert sources[2]['sha256'] == sources[3]['sha256'], 'Revisar las dos copias de CADIDO'

clean = lambda value: ' '.join((value or '').split())
entries = []
with pdfplumber.open(DOWNLOADS / FILES[2][1]) as pdf:
    parent_code = None
    for page_number in [36, 37]:
        table = pdf.pages[page_number - 1].extract_tables()[-1]
        for row in table[2:]:
            if row[0]:
                parent_code = clean(row[0])
            code = clean(row[2] or row[0])
            assert code.startswith('2530.'), f'Código inesperado: {code}'
            assert clean(row[11]) == '2 AÑOS' and clean(row[12]) == '8 AÑOS'
            assert clean(row[13]) == '' and clean(row[14]) == 'X', f'Destino a revisar: {code}'
            entries.append({
                'codigo': code, 'tipo': 'SUBSERIE' if row[2] else 'SERIE',
                'serie_codigo': parent_code,
                'denominacion_cadido': clean(row[3] or row[1]),
                'denominacion_cgca': clean(row[3] or row[1]),
                'subseccion_codigo': '2530', 'seccion_codigo': 'DGA2500',
                'tramite_anios_referencia': 2, 'concentracion_anios_referencia': 8,
                'destino_final_referencia': 'TRANSFERENCIA_HISTORICA',
                'marcas_fuente': dict(zip(
                    ['administrativo', 'legal', 'contable', 'fiscal', 'publica', 'reservada', 'confidencial', 'baja', 'historico'],
                    [clean(row[i]) for i in [4, 5, 6, 7, 8, 9, 10, 13, 14]],
                )),
                'fuente_cadido_pagina': page_number,
                'fuente_cgca_paginas': [31] if parent_code in ['2530.1', '2530.2'] else [32],
                'vigencia_operativa_confirmada': False,
            })

# Se preserva la diferencia literal entre ambos instrumentos, sin corregir el original.
next(e for e in entries if e['codigo'] == '2530.3d')['denominacion_cgca'] = 'TRANSFERENCIAS PRESUPUESTALES'
next(e for e in entries if e['codigo'] == '2530.4')['denominacion_cgca'] = 'CONCILIACIÓN CONTABLE/PRESUPUESTAL'
assert len(entries) == 16 and len({e['codigo'] for e in entries}) == 16
assert sum(e['tipo'] == 'SERIE' for e in entries) == 4
base = 'https://www.pjeveracruz.gob.mx/pjev/archivos/archivos/transparencia/Ley875/XLV/2025/1384/'
data = {
    'revision': '2026-10-29',
    'naturaleza': 'REFERENCIA_DOCUMENTAL_PARA_DISENO_NO_DESPLEGADA',
    'version_referencia': 'Instrumentos denominados 2024, publicados/reportados en 2025',
    'alcance_inicial': {
        'seccion_codigo': 'DGA2500', 'seccion': 'Dirección General de Administración',
        'subseccion_codigo': '2530', 'subseccion_documental': 'Subdirección de Recursos Financieros',
        'foco_operativo': 'Contabilidad',
        'denominacion_solicitada': 'subdirección de administración y contabilidad',
        'equivalencia_organizacional_confirmada': True,
        'confirmacion': 'Confirmación expresa del usuario en este chat el 29-10-2026',
    },
    'modelo_general': {'niveles': ['FONDO', 'SUBFONDO', 'SECCION', 'SUBSECCION', 'SERIE', 'SUBSERIE'],
                       'subseccion_y_subserie_opcionales_segun_instrumento': True,
                       'apertura_de_otras_areas': 'Configuración posterior por unidad y versión, sin cambiar identidades'},
    'jerarquia_referencia': {
        'fondo_codigo_cgca': 'FOPJ01', 'fondo_codigo_cadido': 'FOPJO1',
        'fondo_equivalencia_validada': False,
        'subfondo_codigo': 'PLENOCJP', 'seccion_codigo': 'DGA2500', 'subseccion_codigo': '2530',
    },
    'subsecciones_dga_contexto': [
        {'codigo': '2510', 'nombre': 'Subdirección de Recursos Humanos', 'piloto': False},
        {'codigo': '2520', 'nombre': 'Subdirección de Recursos Materiales, Infraestructura y Supervisión de Obra', 'piloto': False},
        {'codigo': '2530', 'nombre': 'Subdirección de Recursos Financieros', 'piloto': True},
        {'codigo': '2540', 'nombre': 'Subdirección de Tecnologías de la Información', 'piloto': False},
    ],
    'observaciones': [
        'CGCA p.34: nota de 09-03-2025; transición hacia clasificación funcional.',
        'CADIDO p.39: nota de 09-04-2025; transición hacia clasificación funcional.',
        'Fondo CGCA FOPJ01 y CADIDO FOPJO1: conservar ambas grafías y conciliar, sin normalización automática.',
        '2530.3d: CGCA TRANSFERENCIAS y CADIDO TRANFERENCIAS; conservar ambos literales.',
        'Marcas PÚBLICA y RESERVADA simultáneas no autorizan acceso ni sustituyen clasificación por documento.',
        'XLV_c.xls es registro de publicación; no es inventario de expedientes ni prueba de vigencia actual.',
        'Los 2+8 años son fases de referencia; no se calcula vencimiento sin cierre, disparador y validación aplicables.',
    ],
    'fuentes': sources,
    'enlaces_publicados_xlv': {name: base + name for name in [FILES[0][1], FILES[1][1], FILES[2][1],
        'GUIA_SIMPLE_DE_ARCHIVO_DOCUMENTAL_2024.pdf', 'INFORME_ANUAL_DE_CUMPLIMIENTO_DEL_ARCHIVO_GENERAL_2024.pdf']},
    'registros': entries,
}
target = ROOT / 'docs/datos_archivisticos_dga_2530_2024.json'
target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Referencia extraída: {len(entries)} entradas; 4 series y 12 subseries. Fuentes intactas.')
