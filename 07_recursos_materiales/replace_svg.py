import codecs

file_path = r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.1.4-registro-contratos.html'
with codecs.open(file_path, 'r', 'utf-8') as f:
    html = f.read()

start_svg = html.find('<svg viewBox="0 0 1000 850"')
end_svg = html.find('</svg>', start_svg) + 6

new_svg = '''<svg viewBox="0 0 1000 900" xmlns="http://www.w3.org/2000/svg" style="max-width:100%; height:auto; background:#fff; font-family:sans-serif;">
              <defs>
                <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#1B3A2D" />
                </marker>
                
                <style>
                  .lane-header { font-size:13px; font-weight:bold; fill:#fff; text-anchor:middle; letter-spacing:1px; }
                  .node-area { fill:#f8fafc; stroke:#94a3b8; stroke-width:2; rx:4; }
                  .node-proc { fill:#fff; stroke:#1B3A2D; stroke-width:2; rx:6; }
                  .node-siaf { fill:#fefce8; stroke:#ca8a04; stroke-width:2; rx:6; }
                  
                  .text-area { font-size:11px; fill:#334155; font-weight:bold; text-anchor:middle; }
                  .text-main { font-size:12px; fill:#1B3A2D; font-weight:bold; text-anchor:middle; }
                  .text-sub { font-size:10px; fill:#475569; text-anchor:middle; }
                  
                  .path-line { fill:none; stroke:#1B3A2D; stroke-width:2; marker-end:url(#arrow); }
                  .path-link { fill:none; stroke:#94a3b8; stroke-width:1.5; stroke-dasharray:4,4; }
                </style>
              </defs>

              <!-- Swimlanes Backgrounds -->
              <rect x="0" y="0" width="250" height="900" fill="#f1f5f9" stroke="#cbd5e1"/>
              <rect x="250" y="0" width="400" height="900" fill="#f0fdf4" stroke="#bbf7d0"/>
              <rect x="650" y="0" width="350" height="900" fill="#fffbeb" stroke="#fde68a"/>
              
              <!-- Swimlanes Headers -->
              <rect x="0" y="0" width="250" height="35" fill="#475569"/>
              <text x="125" y="22" class="lane-header">ÁREA RESPONSABLE</text>
              
              <rect x="250" y="0" width="400" height="35" fill="#166534"/>
              <text x="450" y="22" class="lane-header">PASO - PROCESO OPERATIVO</text>
              
              <rect x="650" y="0" width="350" height="35" fill="#854d0e"/>
              <text x="825" y="22" class="lane-header">MÓDULO SIAF-PJEV</text>

              <!-- 1. INICIO -->
              <circle cx="450" cy="70" r="15" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
              <text x="450" y="74" font-size="9" font-weight="bold" fill="#334155" text-anchor="middle">INICIO</text>
              <path d="M 450 85 L 450 110" class="path-line"/>

              <!-- STEP 1 -->
              <!-- Area -->
              <rect x="25" y="110" width="200" height="40" class="node-area"/>
              <text x="125" y="134" class="text-area">Asuntos Jurídicos / Comités</text>
              <!-- Proc -->
              <rect x="300" y="110" width="300" height="50" class="node-proc"/>
              <text x="450" y="130" class="text-main">1. Adjudicación y Firma</text>
              <text x="450" y="145" class="text-sub">Dictamen, validación y firmas físicas</text>
              <!-- SIAF -->
              <rect x="700" y="115" width="250" height="40" class="node-siaf" fill="#f3f4f6" stroke="#9ca3af"/>
              <text x="825" y="139" class="text-sub">N/A (Fuera del Sistema)</text>
              <!-- Links -->
              <path d="M 225 130 L 300 130" class="path-link"/>
              <path d="M 600 135 L 700 135" class="path-link"/>

              <path d="M 450 160 L 450 190" class="path-line"/>

              <!-- STEP 2 -->
              <rect x="25" y="190" width="200" height="40" class="node-area"/>
              <text x="125" y="214" class="text-area">Recursos Materiales</text>
              
              <rect x="300" y="190" width="300" height="50" class="node-proc"/>
              <text x="450" y="210" class="text-main">2. Registro de Cabecera</text>
              <text x="450" y="225" class="text-sub">Captura de folios, montos y vigencias</text>
              
              <rect x="700" y="190" width="250" height="50" class="node-siaf"/>
              <text x="825" y="210" class="text-main">02.1.4 Registro de Contrato</text>
              <text x="825" y="225" class="text-sub">Generación del contrato base</text>
              
              <path d="M 225 210 L 300 210" class="path-link"/>
              <path d="M 600 215 L 700 215" class="path-link"/>

              <path d="M 450 240 L 450 280" class="path-line"/>

              <!-- STEP 3 -->
              <rect x="25" y="280" width="200" height="40" class="node-area"/>
              <text x="125" y="304" class="text-area">Recursos Materiales</text>
              
              <rect x="300" y="280" width="300" height="50" class="node-proc"/>
              <text x="450" y="300" class="text-main">3. Asignación de Partidas ("Bolsa")</text>
              <text x="450" y="315" class="text-sub">Mapeo de COG vs Monto Total</text>
              
              <rect x="700" y="280" width="250" height="50" class="node-siaf"/>
              <text x="825" y="300" class="text-main">02.1.4 Detalle Presupuestal</text>
              <text x="825" y="315" class="text-sub">Cuadre exacto (Regla de Negocio)</text>
              
              <path d="M 225 300 L 300 300" class="path-link"/>
              <path d="M 600 305 L 700 305" class="path-link"/>

              <path d="M 450 330 L 450 370" class="path-line"/>

              <!-- STEP 4 -->
              <rect x="25" y="370" width="200" height="40" class="node-area"/>
              <text x="125" y="394" class="text-area">Presupuesto</text>
              
              <rect x="300" y="370" width="300" height="50" class="node-proc"/>
              <text x="450" y="390" class="text-main">4. Autorización y Compromiso</text>
              <text x="450" y="405" class="text-sub">Inmovilización del recurso etiquetado</text>
              
              <rect x="700" y="370" width="250" height="50" class="node-siaf"/>
              <text x="825" y="390" class="text-main">02.2.6 Compromisos</text>
              <text x="825" y="405" class="text-sub">Póliza D-COMPROME (Bloqueo de 02.1.4)</text>
              
              <path d="M 225 390 L 300 390" class="path-link"/>
              <path d="M 600 395 L 700 395" class="path-link"/>

              <path d="M 450 420 L 450 460" class="path-line"/>

              <!-- STEP 5 -->
              <rect x="25" y="460" width="200" height="40" class="node-area"/>
              <text x="125" y="484" class="text-area">Almacén / Centro de Costo</text>
              
              <rect x="300" y="460" width="300" height="50" class="node-proc"/>
              <text x="450" y="480" class="text-main">5. Recepción (Devengado)</text>
              <text x="450" y="495" class="text-sub">Entrega de bienes y factura validada</text>
              
              <rect x="700" y="460" width="250" height="50" class="node-siaf"/>
              <text x="825" y="480" class="text-main">Módulo de Almacén</text>
              <text x="825" y="495" class="text-sub">Entrada (Consume Saldo de Contrato)</text>
              
              <path d="M 225 480 L 300 480" class="path-link"/>
              <path d="M 600 485 L 700 485" class="path-link"/>

              <path d="M 450 510 L 450 550" class="path-line"/>

              <!-- STEP 6 -->
              <rect x="25" y="550" width="200" height="40" class="node-area"/>
              <text x="125" y="574" class="text-area">Tesorería / Contabilidad</text>
              
              <rect x="300" y="550" width="300" height="50" class="node-proc"/>
              <text x="450" y="570" class="text-main">6. Programación y Pago</text>
              <text x="450" y="585" class="text-sub">Transferencia SPEI al proveedor</text>
              
              <rect x="700" y="550" width="250" height="50" class="node-siaf"/>
              <text x="825" y="570" class="text-main">Módulo de Egresos</text>
              <text x="825" y="585" class="text-sub">Póliza Egreso (Actualiza Pagado)</text>
              
              <path d="M 225 570 L 300 570" class="path-link"/>
              <path d="M 600 575 L 700 575" class="path-link"/>

              <!-- FIN -->
              <path d="M 450 600 L 450 640" class="path-line"/>
              <circle cx="450" cy="655" r="15" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
              <text x="450" y="659" font-size="9" font-weight="bold" fill="#334155" text-anchor="middle">FIN</text>

            </svg>'''

html = html[:start_svg] + new_svg + html[end_svg:]

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(html)
print('New SVG with 3 columns injected successfully.')
