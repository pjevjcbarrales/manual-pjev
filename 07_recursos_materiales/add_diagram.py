import codecs

file_path = r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.1.4-registro-contratos.html'
with codecs.open(file_path, 'r', 'utf-8') as f:
    html = f.read()

svg_diagram = '''
<div id="modal-diagrama" class="modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:10000; align-items:center; justify-content:center;">
    <div class="modal-box" style="background:#fff; padding:25px; border-radius:8px; max-width:1050px; width:95%; max-height:90vh; overflow-y:auto; position:relative; box-shadow:0 10px 25px rgba(0,0,0,0.2);">
        <div class="modal-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;">
            <h3 style="color: var(--pjev-verde-oscuro); font-size: 16px; margin: 0;">Anexo 1: Diagrama de Flujo de Canal (Interfuncional)</h3>
            <button class="modal-close" onclick="document.getElementById('modal-diagrama').style.display='none'" style="background:none; border:none; color:#991b1b; cursor:pointer; font-weight:bold; font-size:14px;">❌ Cerrar</button>
        </div>
        <div class="modal-body" style="text-align: center; background:#fafafa; border:1px solid #eee; border-radius:6px; padding:15px;">
            
            <svg viewBox="0 0 1000 850" xmlns="http://www.w3.org/2000/svg" style="max-width:100%; height:auto; background:#fff; font-family:sans-serif;">
              <defs>
                <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#1B3A2D" />
                </marker>
                
                <style>
                  .lane-header { font-size:12px; font-weight:bold; fill:#fff; text-anchor:middle; }
                  .node-rect { fill:#fff; stroke:#1B3A2D; stroke-width:2; rx:6; }
                  .node-text { font-size:11px; fill:#1B3A2D; font-weight:bold; text-anchor:middle; }
                  .node-desc { font-size:9px; fill:#666; text-anchor:middle; }
                  .path-line { fill:none; stroke:#1B3A2D; stroke-width:2; marker-end:url(#arrow); }
                </style>
              </defs>

              <!-- Swimlanes Backgrounds -->
              <rect x="0" y="0" width="250" height="850" fill="#f8fafc" stroke="#e2e8f0"/>
              <rect x="250" y="0" width="250" height="850" fill="#f0fdf4" stroke="#e2e8f0"/>
              <rect x="500" y="0" width="250" height="850" fill="#fefce8" stroke="#e2e8f0"/>
              <rect x="750" y="0" width="250" height="850" fill="#f8fafc" stroke="#e2e8f0"/>
              
              <!-- Swimlanes Headers -->
              <rect x="0" y="0" width="250" height="30" fill="#334155"/>
              <text x="125" y="19" class="lane-header">Asuntos Jurídicos / Comités</text>
              
              <rect x="250" y="0" width="250" height="30" fill="#166534"/>
              <text x="375" y="19" class="lane-header">Recursos Materiales / Obra</text>
              
              <rect x="500" y="0" width="250" height="30" fill="#854d0e"/>
              <text x="625" y="19" class="lane-header">Presupuesto</text>

              <rect x="750" y="0" width="250" height="30" fill="#334155"/>
              <text x="875" y="19" class="lane-header">Contabilidad / Egresos</text>

              <!-- Nodes -->
              <!-- 1. INICIO -->
              <circle cx="125" cy="80" r="20" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
              <text x="125" y="84" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">INICIO</text>

              <!-- 2. Firma -->
              <rect x="50" y="140" width="150" height="50" class="node-rect"/>
              <text x="125" y="165" class="node-text">Firma de Contrato</text>
              <text x="125" y="178" class="node-desc">Dictamen legal y rúbricas</text>

              <!-- 3. Cabecera -->
              <rect x="300" y="240" width="150" height="50" class="node-rect"/>
              <text x="375" y="265" class="node-text">Registro de Cabecera</text>
              <text x="375" y="278" class="node-desc">Módulo 02.1.4</text>

              <!-- 4. Bolsa -->
              <rect x="300" y="340" width="150" height="50" class="node-rect"/>
              <text x="375" y="365" class="node-text">Asignación de Partidas</text>
              <text x="375" y="378" class="node-desc">Aportación a la "Bolsa"</text>

              <!-- 5. Autorizacion Presupuesto -->
              <rect x="550" y="440" width="150" height="50" class="node-rect"/>
              <text x="625" y="465" class="node-text">Compromiso Presupuestal</text>
              <text x="625" y="478" class="node-desc">Módulo 02.2.6 (Autoriza)</text>

              <!-- 6. Devengado -->
              <rect x="300" y="540" width="150" height="50" class="node-rect"/>
              <text x="375" y="565" class="node-text">Recepción de Bienes</text>
              <text x="375" y="578" class="node-desc">Entrada de Almacén (Devenga)</text>

              <!-- 7. Pago -->
              <rect x="800" y="640" width="150" height="50" class="node-rect"/>
              <text x="875" y="665" class="node-text">Emisión de Pago</text>
              <text x="875" y="678" class="node-desc">Módulo Egresos (Póliza)</text>

              <!-- 8. FIN -->
              <circle cx="875" cy="760" r="20" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
              <text x="875" y="764" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">FIN</text>

              <!-- Arrows -->
              <!-- 1 to 2 -->
              <path d="M 125 100 L 125 130" class="path-line"/>
              <!-- 2 to 3 -->
              <path d="M 125 190 L 125 215 L 375 215 L 375 230" class="path-line"/>
              <!-- 3 to 4 -->
              <path d="M 375 290 L 375 330" class="path-line"/>
              <!-- 4 to 5 -->
              <path d="M 375 390 L 375 415 L 625 415 L 625 430" class="path-line"/>
              <!-- 5 to 6 -->
              <path d="M 625 490 L 625 515 L 375 515 L 375 530" class="path-line"/>
              <!-- 6 to 7 -->
              <path d="M 375 590 L 375 615 L 875 615 L 875 630" class="path-line"/>
              <!-- 7 to 8 -->
              <path d="M 875 690 L 875 730" class="path-line"/>

            </svg>
        </div>
    </div>
</div>
'''

# Check if modal-diagrama already exists, to avoid duplicates
if 'id="modal-diagrama"' not in html:
    # Insert it right before the anexos-impresos modal
    insert_idx = html.find('<div id="anexos-impresos"')
    if insert_idx != -1:
        html = html[:insert_idx] + svg_diagram + '\n' + html[insert_idx:]
        
        # Modify the JS to hook the Diagram button to the diagram modal
        # Replace the old JS listener
        old_js = """if (b.innerText.includes('Proceso Funcional') || b.innerText.includes('Ver Diagrama')) {
        b.onclick = () => {
          document.getElementById('anexos-impresos').style.display = 'flex';
        };
      }"""
      
        new_js = """if (b.innerText.includes('Proceso Funcional')) {
        b.onclick = () => { document.getElementById('anexos-impresos').style.display = 'flex'; };
      }
      if (b.innerText.includes('Ver Diagrama')) {
        b.onclick = () => { document.getElementById('modal-diagrama').style.display = 'flex'; };
      }"""
        html = html.replace(old_js, new_js)

        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(html)
        print("Diagram added successfully.")
    else:
        print("Could not find anexos-impresos div.")
else:
    print("modal-diagrama already exists.")

