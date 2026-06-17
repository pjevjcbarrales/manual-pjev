import codecs

file_path = r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.1.4-registro-contratos.html'
with codecs.open(file_path, 'r', 'utf-8') as f:
    html = f.read()

start_marker = '<!-- 8. Diseño de Interfaces (UI) -->'
end_marker = '<!-- 9. Reglas de Negocio -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

new_section = '''<!-- 8. Diseño de Interfaces (UI) -->
    <div class="doc-section">
      <div class="section-title"><span class="section-num">8</span> Diseño de Interfaces (UI / Wireframes)</div>
      
      <div class="wireframe-tabs">
        <button class="wf-tab active" onclick="showWF('p1',this)">pantalla_leer consulta de contratos (Parámetros)</button>
        <button class="wf-tab" onclick="showWF('p2',this)">pantalla_leer consulta de contratos (Valores)</button>
        <button class="wf-tab" onclick="showWF('p3',this)">pantalla_abc_compuesta (Parámetros)</button>
        <button class="wf-tab" onclick="showWF('p4',this)">pantalla_abc_compuesta (Valores)</button>
      </div>

      <!-- TAB 1: pantalla_leer Parametros -->
      <div id="wf-p1" class="wf-panel active">
        <div class="wf-box">
          <div class="wf-bar"><span class="wf-bar-label">Listado Principal de Contratos (Parámetros)</span></div>
          <div class="wf-svg-area">
            <svg viewBox="0 0 1000 400" xmlns="http://www.w3.org/2000/svg">
              <rect width="1000" height="400" fill="#fcfcfc" rx="4" stroke="#ddd"/>
              
              <text x="20" y="30" font-size="16" font-weight="bold" fill="#333">Catálogo de Contratos</text>
              <rect x="850" y="15" width="130" height="25" fill="#1B3A2D" rx="4"/>
              <text x="915" y="32" fill="#fff" font-size="11" text-anchor="middle" font-weight="bold">+ Nuevo Contrato</text>
              
              <rect x="20" y="60" width="960" height="60" fill="#fff" stroke="#ccc" rx="4"/>
              <text x="35" y="80" font-size="10" fill="#666">Folio del Contrato</text>
              <text x="200" y="80" font-size="10" fill="#666">Proveedor</text>
              
              <rect x="35" y="88" width="150" height="20" fill="#fff" stroke="#ccc" rx="2"/>
              <text x="40" y="102" font-size="10" fill="#0284c7">@p_numero_contrato</text>
              
              <rect x="200" y="88" width="200" height="20" fill="#fff" stroke="#ccc" rx="2"/>
              <text x="205" y="102" font-size="10" fill="#0284c7">@p_id_proveedor</text>
              
              <rect x=\"420\" y=\"88\" width=\"80\" height=\"20\" fill=\"#183125\" rx=\"2\"/>
              <text x=\"460\" y=\"102\" fill=\"#fff\" font-size=\"10\" text-anchor=\"middle\">Buscar</text>

              <rect x="20" y="140" width="960" height="240" fill="#fcfcfc" stroke="#ccc" rx="4"/>
              <rect x="20" y="140" width="960" height="25" fill="#f0f0f0"/>
              <text x="30" y="156" font-size="10" font-weight="bold" fill="#666">FOLIO CONTRATO</text>
              <text x="180" y="156" font-size="10" font-weight="bold" fill="#666">PROVEEDOR</text>
              <text x="400" y="156" font-size="10" font-weight="bold" fill="#666">FECHA</text>
              <text x="500" y="156" font-size="10" font-weight="bold" fill="#666">TIPO</text>
              <text x="580" y="156" font-size="10" font-weight="bold" fill="#666">MONTO MÁX TOTAL</text>
              <text x="750" y="156" font-size="10" font-weight="bold" fill="#666">ESTADO</text>
              <text x="920" y="156" font-size="10" font-weight="bold" fill="#666">ACCIONES</text>
              
              <!-- Row 1 -->
              <rect x="20" y="165" width="960" height="35" fill="#fff" stroke="#eee"/>
              <text x="30" y="187" font-size="11" font-weight="bold" fill="#0284c7">{numero_contrato}</text>
              <text x="180" y="187" font-size="11" fill="#0284c7">{proveedor_nombre}</text>
              <text x="400" y="187" font-size="11" fill="#0284c7">{fecha_contrato}</text>
              <text x="500" y="187" font-size="11" fill="#0284c7">{tipo_contrato}</text>
              <text x="580" y="187" font-size="11" fill="#0284c7">{monto_maximo_total}</text>
              <text x="750" y="187" font-size="11" fill="#0284c7">{id_poliza_comprometido}</text>
              
              <rect x="900" y="176" width="50" height="15" fill="#f3f3f3" rx="2" stroke="#ccc"/>
              <text x="925" y="187" font-size="9" fill="#333" text-anchor="middle">Ver</text>
            </svg>
          </div>
        </div>
      </div>

      <!-- TAB 2: pantalla_leer Valores -->
      <div id="wf-p2" class="wf-panel">
        <div class="wf-box">
          <div class="wf-bar"><span class="wf-bar-label">Listado Principal de Contratos (Valores)</span></div>
          <div class="wf-svg-area">
            <svg viewBox="0 0 1000 400" xmlns="http://www.w3.org/2000/svg">
              <rect width="1000" height="400" fill="#fcfcfc" rx="4" stroke="#ddd"/>
              
              <text x="20" y="30" font-size="16" font-weight="bold" fill="#333">Catálogo de Contratos</text>
              <rect x="850" y="15" width="130" height="25" fill="#1B3A2D" rx="4"/>
              <text x="915" y="32" fill="#fff" font-size="11" text-anchor="middle" font-weight="bold">+ Nuevo Contrato</text>
              
              <rect x="20" y="60" width="960" height="60" fill="#fff" stroke="#ccc" rx="4"/>
              <text x="35" y="80" font-size="10" fill="#666">Folio del Contrato</text>
              <text x="200" y="80" font-size="10" fill="#666">Proveedor</text>
              
              <rect x="35" y="88" width="150" height="20" fill="#fff" stroke="#ccc" rx="2"/>
              <text x="40" y="102" font-size="10" fill="#ccc">Ingresar número...</text>
              
              <rect x="200" y="88" width="200" height="20" fill="#fff" stroke="#ccc" rx="2"/>
              <text x="205" y="102" font-size="10" fill="#ccc">Seleccionar proveedor...</text>
              
              <rect x="420" y="88" width="80" height="20" fill="#183125" rx="2"/>
              <text x="460" y="102" fill="#fff" font-size="10" text-anchor="middle">Buscar</text>

              <rect x="20" y="140" width="960" height="240" fill="#fcfcfc" stroke="#ccc" rx="4"/>
              <rect x="20" y="140" width="960" height="25" fill="#f0f0f0"/>
              <text x="30" y="156" font-size="10" font-weight="bold" fill="#666">FOLIO CONTRATO</text>
              <text x="180" y="156" font-size="10" font-weight="bold" fill="#666">PROVEEDOR</text>
              <text x="400" y="156" font-size="10" font-weight="bold" fill="#666">FECHA</text>
              <text x="500" y="156" font-size="10" font-weight="bold" fill="#666">TIPO</text>
              <text x="580" y="156" font-size="10" font-weight="bold" fill="#666">MONTO MÁX TOTAL</text>
              <text x="750" y="156" font-size="10" font-weight="bold" fill="#666">ESTADO</text>
              <text x="920" y="156" font-size="10" font-weight="bold" fill="#666">ACCIONES</text>
              
              <rect x="20" y="165" width="960" height="35" fill="#fff" stroke="#eee"/>
              <text x="30" y="187" font-size="11" fill="#333" font-weight="bold">PJEV-RM-001-2026</text>
              <text x="180" y="187" font-size="11" fill="#333">Computación Golfo S.A.</text>
              <text x="400" y="187" font-size="11" fill="#333">2026-06-01</text>
              <text x="500" y="187" font-size="11" fill="#333">Cerrado</text>
              <text x="580" y="187" font-size="11" fill="#333">$ 116,000.00</text>
              <rect x="750" y="174" width="70" height="15" fill="#edf8ef" stroke="#8fd19e" rx="7"/>
              <text x="785" y="185" font-size="8" fill="#166534" font-weight="bold" text-anchor="middle">COMPROMETIDO</text>
              <rect x="900" y="176" width="50" height="15" fill="#f3f3f3" rx="2" stroke="#ccc"/>
              <text x="925" y="187" font-size="9" fill="#333" text-anchor="middle">Ver</text>

              <rect x="20" y="200" width="960" height="35" fill="#fafafa" stroke="#eee"/>
              <text x="30" y="222" font-size="11" fill="#333" font-weight="bold">PJEV-RM-002-2026</text>
              <text x="180" y="222" font-size="11" fill="#333">Papelería Centro</text>
              <text x="400" y="222" font-size="11" fill="#333">2026-06-15</text>
              <text x="500" y="222" font-size="11" fill="#333">Abierto</text>
              <text x="580" y="222" font-size="11" fill="#333">$ 58,000.00</text>
              <rect x="750" y="209" width="70" height="15" fill="#fffbeb" stroke="#f5d565" rx="7"/>
              <text x="785" y="220" font-size="8" fill="#854d0e" font-weight="bold" text-anchor="middle">PENDIENTE</text>
              <rect x="900" y="211" width="50" height="15" fill="#f3f3f3" rx="2" stroke="#ccc"/>
              <text x="925" y="222" font-size="9" fill="#333" text-anchor="middle">Editar</text>
            </svg>
          </div>
        </div>
      </div>

      <!-- TAB 3: pantalla_abc_compuesta Parametros -->
      <div id="wf-p3" class="wf-panel">
        <div class="wf-box">
          <div class="wf-bar"><span class="wf-bar-label">Modal: ABC Compuesta (Parámetros)</span></div>
          <div class="wf-svg-area">
            <svg viewBox="0 0 1000 650" xmlns="http://www.w3.org/2000/svg">
              <rect width="1000" height="650" fill="#000" opacity="0.3"/>
              <rect x="100" y="30" width="800" height="580" fill="#fff" rx="6"/>
              <text x="120" y="60" font-size="16" font-weight="bold" fill="#183125">Contrato (Parámetros de Entrada JSON)</text>
              <line x1="100" y1="75" x2="900" y2="75" stroke="#d4c9b5"/>
              
              <text x="120" y="100" font-size="12" fill="#5a5a5a">Folio / Número *</text>
              <rect x="120" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="122" font-size="11" fill="#0284c7">@p_json_contrato->>'numero_contrato'</text>
              
              <text x="370" y="100" font-size="12" fill="#5a5a5a">Fecha Contrato *</text>
              <rect x="370" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="380" y="122" font-size="11" fill="#0284c7">@p_json_contrato->>'fecha_contrato'</text>
              
              <text x="620" y="100" font-size="12" fill="#5a5a5a">Tipo *</text>
              <rect x="620" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="630" y="122" font-size="11" fill="#0284c7">@p_json_contrato->>'tipo_contrato'</text>

              <text x="120" y="150" font-size="12" fill="#5a5a5a">Proveedor *</text>
              <rect x="120" y="155" width="350" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="172" font-size="11" fill="#0284c7">@p_json_contrato->>'id_proveedor'</text>

              <text x="490" y="150" font-size="12" fill="#5a5a5a">Procedimiento Origen *</text>
              <rect x="490" y="155" width="360" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="500" y="172" font-size="11" fill="#0284c7">@p_json_contrato->>'id_procedimiento'</text>

              <text x="120" y="200" font-size="12" fill="#5a5a5a">Objeto / Descripción *</text>
              <rect x="120" y="205" width="730" height="40" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="222" font-size="11" fill="#0284c7">@p_json_contrato->>'descripcion_contrato'</text>
              
              <line x1="120" y1="260" x2="850" y2="260" stroke="#eee"/>
              <text x="120" y="280" font-size="14" font-weight="bold" fill="#183125">Importes Generales (Sin IVA)</text>
              
              <text x="120" y="310" font-size="12" fill="#5a5a5a">Monto Mínimo</text>
              <rect x="120" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="332" font-size="11" fill="#0284c7">@p_json_contrato->>'monto_minimo'</text>
              
              <text x="370" y="310" font-size="12" fill="#5a5a5a">Monto Máximo *</text>
              <rect x="370" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="380" y="332" font-size="11" fill="#0284c7">@p_json_contrato->>'monto_maximo'</text>
              
              <line x1="120" y1="360" x2="850" y2="360" stroke="#eee"/>

              <text x="120" y="380" font-size="14" font-weight="bold" fill="#183125">Detalle Presupuestal (@p_json_detalles)</text>
              <rect x="120" y="400" width="730" height="120" fill="#fff" stroke="#ccc" rx="4"/>
              <rect x="120" y="400" width="730" height="25" fill="#f0f0f0" rx="4"/>
              <text x="130" y="416" font-size="10" fill="#666" font-weight="bold">ID OFICIO RESERVA | PARTIDA | MONTO | IVA | TOTAL | ACCIÓN</text>
              
              <rect x="120" y="425" width="730" height="35" fill="#fff" stroke="#eee"/>
              <text x="130" y="447" font-size="11" fill="#0284c7">{id_oficio_reserva}</text>
              <text x="260" y="447" font-size="11" fill="#0284c7">{id_partida}</text>
              <text x="400" y="447" font-size="11" fill="#0284c7">{monto_detalle}</text>
              <text x="500" y="447" font-size="11" fill="#0284c7">{iva_detalle}</text>
              <text x="600" y="447" font-size="11" fill="#0284c7">{total_detalle}</text>
              
              <rect x="730" y="560" width="120" height="30" fill="#183125" rx="4"/>
              <text x="790" y="579" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Guardar</text>
            </svg>
          </div>
        </div>
      </div>

      <!-- TAB 4: pantalla_abc_compuesta Valores -->
      <div id="wf-p4" class="wf-panel">
        <div class="wf-box">
          <div class="wf-bar"><span class="wf-bar-label">Modal: ABC Compuesta (Valores)</span></div>
          <div class="wf-svg-area">
            <svg viewBox="0 0 1000 650" xmlns="http://www.w3.org/2000/svg">
              <rect width="1000" height="650" fill="#000" opacity="0.3"/>
              <rect x="100" y="30" width="800" height="580" fill="#fff" rx="6"/>
              <text x="120" y="60" font-size="16" font-weight="bold" fill="#183125">Editar Contrato: PJEV-RM-002-2026</text>
              <line x1="100" y1="75" x2="900" y2="75" stroke="#d4c9b5"/>
              
              <text x="120" y="100" font-size="12" fill="#5a5a5a">Folio / Número *</text>
              <rect x="120" y="105" width="230" height="24" fill="#f0ede6" stroke="#ccc" rx="3"/>
              <text x="130" y="122" font-size="11" fill="#333">PJEV-RM-002-2026</text>
              
              <text x="370" y="100" font-size="12" fill="#5a5a5a">Fecha Contrato *</text>
              <rect x="370" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="380" y="122" font-size="11" fill="#333">2026-06-15</text>
              
              <text x="620" y="100" font-size="12" fill="#5a5a5a">Tipo *</text>
              <rect x="620" y="105" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="630" y="122" font-size="11" fill="#333">A - Abierto</text>

              <text x="120" y="150" font-size="12" fill="#5a5a5a">Proveedor *</text>
              <rect x="120" y="155" width="350" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="172" font-size="11" fill="#333">Papelería Centro</text>

              <text x="490" y="150" font-size="12" fill="#5a5a5a">Procedimiento Origen *</text>
              <rect x="490" y="155" width="360" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="500" y="172" font-size="11" fill="#333">Licitación LPN-002-2026</text>

              <text x="120" y="200" font-size="12" fill="#5a5a5a">Objeto / Descripción *</text>
              <rect x="120" y="205" width="730" height="40" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="222" font-size="11" fill="#333">Adquisición de insumos de papelería general.</text>
              
              <line x1="120" y1="260" x2="850" y2="260" stroke="#eee"/>
              <text x="120" y="280" font-size="14" font-weight="bold" fill="#183125">Importes Generales (Sin IVA)</text>
              
              <text x="120" y="310" font-size="12" fill="#5a5a5a">Monto Mínimo</text>
              <rect x="120" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="130" y="332" font-size="11" fill="#333">20,000.00</text>
              
              <text x="370" y="310" font-size="12" fill="#5a5a5a">Monto Máximo *</text>
              <rect x="370" y="315" width="230" height="24" fill="#fff" stroke="#ccc" rx="3"/>
              <text x="380" y="332" font-size="11" fill="#333">50,000.00</text>
              
              <text x="620" y="310" font-size="12" fill="#5a5a5a">Garantía (10%)</text>
              <rect x="620" y="315" width="230" height="24" fill="#f0ede6" stroke="#ccc" rx="3"/>
              <text x="630" y="332" font-size="11" fill="#333">5,000.00</text>

              <line x1="120" y1="360" x2="850" y2="360" stroke="#eee"/>

              <text x="120" y="380" font-size="14" font-weight="bold" fill="#183125">Detalle Presupuestal</text>
              <rect x="120" y="400" width="730" height="120" fill="#fff" stroke="#ccc" rx="4"/>
              <rect x="120" y="400" width="730" height="25" fill="#f0f0f0" rx="4"/>
              <text x="130" y="416" font-size="10" fill="#666" font-weight="bold">ID OFICIO RESERVA | PARTIDA | MONTO | IVA | TOTAL | ACCIÓN</text>
              
              <rect x="120" y="425" width="730" height="35" fill="#fff" stroke="#eee"/>
              <text x="130" y="447" font-size="11" fill="#333">OR-2026-05</text>
              <text x="260" y="447" font-size="11" fill="#333">21101 - Mat. y Útiles</text>
              <text x="400" y="447" font-size="11" fill="#333">50,000.00</text>
              <text x="500" y="447" font-size="11" fill="#333">8,000.00</text>
              <text x="600" y="447" font-size="11" fill="#333">58,000.00</text>
              <text x="730" y="447" font-size="10" fill="#991B1B">Eliminar</text>

              <rect x="130" y="480" width="120" height="24" fill="#fff" stroke="#183125" rx="3"/>
              <text x="190" y="496" fill="#183125" font-size="11" text-anchor="middle">+ Agregar Renglón</text>
              
              <rect x="730" y="560" width="120" height="30" fill="#183125" rx="4"/>
              <text x="790" y="579" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Guardar</text>
              <text x="680" y="579" fill="#183125" font-size="12" text-anchor="middle">Cancelar</text>
            </svg>
          </div>
        </div>
      </div>
    </div>
'''

html = html[:start_idx] + new_section + html[end_idx:]
with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(html)
print('Updated Section 8 successfully')
