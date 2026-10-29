# 4.1. Sistema de Control de Archivo

**Primer bloque:** Registro de documentos y Digitalización.  
**Manual SIAF-PJEV:** 09.2.4 Control de Archivo.  
**Fecha:** 29 de octubre de 2026.  
**Recalibración institucional:** CGCA/CADIDO denominados 2024, notas de 2025; PADA 2025 y registro XLV del primer trimestre de 2025.  
**Estado:** especificación funcional inicial; pendiente de validación institucional y desarrollo. No acredita implementación en base de datos, servicios o producción.

## 1. Objetivo y alcance

Generar y administrar el inventario del acervo documental y de los expedientes del Organismo; relacionar cada expediente con sus documentos digitales y sus unidades físicas, y permitir su identificación, localización, consulta y seguimiento durante su ciclo de vida.

La implantación inicial corresponde a **DGA2500 — Dirección General de Administración → 2530 — Subdirección de Recursos Financieros, con foco en Contabilidad**, equivalencia confirmada por el usuario. La estructura general admite otras unidades, series y versiones mediante configuración; las demás áreas no adquieren permisos por pertenecer a la misma DGA. El ámbito operativo de Contabilidad se distingue de la subsección archivística 2530.

La meta de digitalización integral se medirá contra un inventario validado. Un expediente registrado puede estar pendiente de digitalizar o localizar; no se declarará completo por tener un archivo PDF. La incorporación de expedientes jurisdiccionales requerirá identificar sus procedimientos y permisos específicos. El sistema comprende el ciclo de vida documental, incluidos inventarios, transferencias, préstamos, conservación y seguimiento, además de la digitalización.

La [recalibración institucional](RECALIBRACION_ARCHIVISTICA_DGA_PJEV.md) detalla el contraste de los cinco archivos recibidos. La cotización del Congreso de 2018 queda como antecedente histórico; el CGCA, CADIDO y PADA del PJEV pasan a orientar el diseño institucional.

Se conserva «4.1» como referencia del requerimiento recibido. En la navegación del manual se incorpora como **09.2.4**, dentro de Gestión Documental y Archivo, para mantener la numeración existente. Las ocho opciones se identifican como CA-01 a CA-08; no son ocho subsistemas nuevos.

## 2. Fundamento y naturaleza de las reglas

| Naturaleza | Fuente y contraste | Consecuencia para el diseño |
|---|---|---|
| Requisito normativo | Ley General de Archivos, arts. 11 y 13, 43 a 47: organización, instrumentos de control y gestión electrónica con integridad y trazabilidad. Texto consultado con reforma DOF 14-11-2025. | Relacionar documentos con su expediente y clasificación; registrar cambios. La digitalización no habilita por sí sola la destrucción de originales. |
| Requisito normativo | LGCG, arts. 42 y 43; texto consultado con reforma DOF 14-05-2026. | Conservar el soporte original justificativo y comprobatorio de los registros y facilitar su consulta autorizada. |
| Requisito normativo | Disposiciones Generales para el Archivo Contable Gubernamental, CONAC, apartados IV a VI; obligatorias desde 01-01-2024. | Parametrizar conservación y excepciones: regla general de seis años, contados desde el año siguiente al cierre del ejercicio; soportes patrimoniales hasta la baja del bien; asuntos pendientes y CxC/CxP sujetos a sus reglas particulares. El vencimiento no ejecuta una baja automática. |
| Regla institucional documentada | CGCA recibido, pp. 31–32; CADIDO recibido, pp. 36–37. | Referencia 2530: cuatro series y doce subseries, con 2 años en trámite, 8 en concentración y marca de destino Archivo Histórico. No configurar baja por vencimiento para estas entradas. |
| Planeación institucional documentada | PADA 2025, pp. 12–20. | Inventarios, responsables, transferencias, consulta/préstamos, capacitación, espacios, riesgos y seguimiento de actividades. El programa del ejercicio 2025 no acredita su ejecución ni se convierte en calendario de 2026. |
| Evidencia de publicación | XLV_c.xls, Informacion, filas 7–14. | Enlaces a instrumentos y corte 01-01-2025 a 31-03-2025. No genera expedientes ni inventario de volumen documental. |
| Requerimiento funcional recibido | Ocho opciones del bloque 4.1 proporcionado por el usuario. | Base del alcance funcional; por sí solo no acredita un procedimiento institucional autorizado. |
| Propuesta tecnológica | Identificador estable, marbetes con código de barras, sugerencia de ubicación, SHA-256, OCR, estados separados y control de concurrencia. | Decisiones de diseño sujetas a implementación y validación; no son tecnologías impuestas por la LGA. |

**Validaciones institucionales pendientes para puesta en operación:** acto de aprobación y vigencia de los instrumentos recibidos, equivalencias con su actualización funcional, discrepancia de fondo `FOPJ01`/`FOPJO1`, eventos de inicio de cómputo, autoridad y evidencias para transferencia/disposición, política de acceso y formatos de inventario/marbetes. Las fuentes ya están identificadas y contrastadas; la validación de vigencia no se presume por su descarga en 2026. La nota final del CGCA está fechada 09-03-2025 y la del CADIDO 09-04-2025; ambas informan transición hacia clasificación funcional.

NOM-151, firma electrónica, formatos de preservación y certificaciones se evaluarán según el acto y soporte aplicables. Escaneo, OCR y hash de integridad no equivalen a certificación ni otorgan por sí solos valor de original.

### Jerarquía y clasificación inicial

El CGCA publica `FOPJ01 → PLENOCJP → DGA2500 → 2530`. El CADIDO escribe el fondo como `FOPJO1`: se conservan ambas grafías como incidencia documental, sin fusionarlas automáticamente. La [referencia estructurada](datos_archivisticos_dga_2530_2024.json) mantiene los literales, páginas y huellas de las fuentes.

| Serie | Denominación | Subseries | Trámite / concentración | Destino en CADIDO |
|---|---|---|---|---|
| 2530.1 | Estados contables | a Mensual; b Trimestral; c Anual. | 2 / 8 años | Archivo Histórico |
| 2530.2 | Información presupuestaria y programática | a Mensual; b Trimestral; c Anual. | 2 / 8 años | Archivo Histórico |
| 2530.3 | Pólizas | a Ingresos; b Tramitada; c Liquidada; d Transferencias presupuestales; e Traspasos bancarios; f Manuales. | 2 / 8 años | Archivo Histórico |
| 2530.4 | Conciliación contable/presupuestal | Sin subserie publicada en el bloque. | 2 / 8 años | Archivo Histórico |

Las denominaciones Tramitada/Liquidada son subseries del instrumento, independientes del estado financiero de un trámite. La correspondencia con tipos de póliza del sistema se validará expresamente. Los dos CADIDO recibidos son idénticos por SHA-256 y representan una sola versión lógica.

Los plazos 2/8 son fases de referencia, no una fecha de destrucción a diez años. Se requieren cierre formal, evento de cómputo y procedimiento de transferencia; las marcas de Información Pública/Reservada del CADIDO tampoco conceden permisos automáticamente.

### Antecedente histórico subordinado

Se revisó la cotización de Velasco Asesores para digitalizar el archivo contable de la LXIV Legislatura del Congreso del Estado de Veracruz, **fechada el 15 de agosto de 2018**, aunque está guardada en una carpeta denominada «Cotizaciones 2019». Su alcance comercial abarca pólizas de noviembre de 2016 a agosto de 2018. Se incorpora como **antecedente funcional de otra institución**, sin atribuirle valor normativo ni aprobación institucional del PJEV. El [contraste del antecedente](REFERENCIA_ARCHIVO_DIGITAL_CONGRESO_2018.md) conserva procedencia, observaciones y datos económicos históricos.

Sus ideas de preparación física, consulta, enlace financiero y capacitación se conservan cuando son compatibles con los instrumentos del PJEV. La clasificación por recopilador o código de póliza del Congreso no rige el piloto.

## 3. Conceptos que deben permanecer separados

| Concepto | Identidad y relación |
|---|---|
| Expediente | Unidad lógica de un asunto. Identificador interno estable, folio institucional, unidad productora, ámbito operativo, nodo y versión de clasificación y regla de disposición. Puede abarcar varias carpetas o tomos. |
| Documento | Pieza documental vinculada al expediente. Tipo, fecha, emisor, soporte, orden documental y versiones. Un PDF de varias páginas no implica varios documentos. |
| Archivo digital | Binario de una versión documental, con ruta privada, tamaño, MIME y hash; puede ser original electrónico, digitalización o derivado de consulta. |
| Carpeta, tomo y caja | Unidades físicas con identidad propia. Una caja puede contener unidades de varios expedientes. No se modifica el expediente al cambiar de caja. |
| Marbete | Identificador visible de un expediente o unidad física; el tipo de objeto debe ser explícito. Mantiene historial y equivalencias anteriores. |
| Ubicación | Archivo, depósito, zona, archivero/anaquel, nivel y posición. Es distinta del identificador y puede cambiar. |
| Instrumento y versión | CGCA/CADIDO/PADA/Guía u otro instrumento, fuente, periodo, fecha, acto y validación. Un expediente conserva la versión aplicada aunque exista otra posterior. |
| Préstamo / transferencia | Eventos con solicitud, autorización y recepción. La salida en préstamo muestra custodio temporal; una transferencia cambia custodia y fase sólo al confirmarse, conservando productor e inventario. |

Un marbete de expediente que abarque varias unidades físicas devolverá todas sus localizaciones. Un marbete de caja permitirá consultar su contenido según permisos. La unidad física raíz ocupa capacidad; sus unidades contenidas heredan ubicación efectiva para evitar contar el mismo espacio dos veces. La ocupación física no se calcula con el tamaño de los archivos digitales.

### Diagramas de base del analista

Se incorporan dos vistas complementarias estudiadas por el analista: ciclo archivístico y relación entre soporte físico, expediente, documentos y metadatos. Se conserva su estructura conceptual; la [validación y relación de ajustes](VALIDACION_DIAGRAMAS_ARCHIVO_PJEV.md) identifica cada cambio y conserva las imágenes recibidas.

La primera vista se particulariza para 2530 con 2/8 años de referencia y destino histórico. La segunda distingue muebles, posiciones y contenedores del expediente lógico, mantiene los cinco tipos documentales como ejemplos y separa metadatos comunes, específicos y técnicos. UUID fiscal y timbrado sólo aplican a los tipos que los contienen; los soportes de proveedor, empleados u obra se exigen según el procedimiento, conservando sus áreas productoras.

## 4. Ocho opciones del módulo

### CA-01. Enlace Digital de Documentos

**Finalidad:** escanear o incorporar documentos, etiquetarlos, ordenarlos y vincularlos con el expediente correcto.

- Entrada: expediente existente o alta previa; tipo documental, fecha, soporte, orden, folios físicos cuando existan y archivo o lote de digitalización.
- Para lotes físicos: registrar entrega, periodo/área, contenedores, inventario de hojas/documentos y condición de recepción. Preparar y ordenar antes del escaneo, dejando constancia de incidencias. El retiro de grapas o el desmontaje de carpetas se realiza conforme al tratamiento autorizado; después se rearma y devuelve el acervo con acuse.
- Flujo: identificar expediente → capturar metadatos → escanear/importar → revisar orientación, legibilidad, integridad y orden → subsanar incidencias → validar e incorporar.
- El índice documental se define por serie y procedimiento; una plantilla puede marcar tipos esperados, secuencia y excepciones justificadas. No se impone un orden universal a todas las series.
- En el piloto, elegir serie/subserie 2530 y versión desde el expediente. El estado de digitalización es independiente de subseries «Tramitada» y «Liquidada». Una carpeta física o un código financiero no reemplaza la clasificación archivística.
- Conservar por separado orden documental, folio físico y número de página digital. Los anexos no renumeran silenciosamente folios ya asentados.
- El escaneo directo requiere integrar un dispositivo o agente compatible; el navegador por sí solo no garantiza control del escáner. La importación de PDF/imágenes es una ruta alternativa.
- Validar tipo y tamaño reales, permisos y contenido malicioso antes de incorporar. Calcular hash en servidor; un duplicado genera advertencia contextual, sin eliminar documentos de otros expedientes.
- OCR opcional como índice de búsqueda sujeto a los mismos permisos; no sustituye el original ni corrige automáticamente metadatos. Rotaciones, OCR y PDF de consulta son derivados con procedencia identificable.
- Salida: documento/versiones incorporadas, índice actualizado, resultado de calidad, responsable y bitácora. Un reescaneo crea versión y conserva la anterior.
- La entrega del lote incluirá manifiesto de documentos/versiones, conteos conciliados, incidencias aceptadas o pendientes, validación de consulta por el área receptora y devolución del soporte físico. Se propone capacitación y guía de operación para que el personal institucional continúe con el acervo posterior.

**Aceptación:** un lote incompleto o rechazado no marca el expediente como digitalizado validado; reintentar el lote no duplica documentos.

### CA-02. Impresión de Marbetes

**Finalidad:** identificar expedientes, carpetas, tomos y cajas mediante número legible y código de barras.

- Seleccionar tipo de unidad, cantidad y plantilla de impresión; generar un número único por institución, sin reutilizar números cancelados.
- Imprimir identificador, tipo de unidad, área o serie cuando proceda y número de tomo/caja. Evitar datos personales o asuntos sensibles en la etiqueta visible.
- Propuesta: Code 128 para lectores láser compatibles; validar simbología, impresora y tamaño físico con el equipo real. La maqueta gráfica del manual no es una etiqueta lista para lectura.
- Registrar emisión y reimpresión con usuario, fecha, motivo y plantilla. Reimprimir conserva el número; reemplazarlo crea una equivalencia auditable.

**Aceptación:** el número escrito y el leído llevan al mismo objeto. Un marbete antiguo informa su sustitución sin crear otro expediente.

### CA-03. Ubicación Física de los Documentos

**Finalidad:** asignar o sugerir un espacio físico disponible para una unidad de archivo.

- Mantener catálogo de ubicaciones, condiciones de uso, capacidad total, ocupada y reservada, unidad de medida y restricciones de conservación/acceso.
- Distinguir archivo de trámite, concentración e histórico de depósito/anaquel/posición. Trasladar una caja dentro del mismo depósito es reubicación; una transferencia archivística exige inventario y recepción, no se acredita cambiando sólo su posición.
- Filtrar espacios activos, compatibles, autorizados y con capacidad suficiente. Ordenar candidatos por continuidad de la serie/área, cercanía y menor espacio remanente compatible, según parámetros institucionales.
- La sugerencia requiere confirmación del custodio. La asignación manual pasa por las mismas validaciones y registra motivo.
- En una transacción: bloquear/revalidar capacidad, reservar destino y registrar movimiento. Confirmada la colocación física, actualizar ubicación vigente y liberar origen. Cancelar una reserva libera destino sin alterar origen.
- Si no hay espacio compatible, mostrar «Sin ubicación disponible». No sobreasignar ni inventar una ubicación.
- La propuesta admite capacidad en posiciones de caja o centímetros lineales, pero una asignación compara cantidades de la misma unidad y perfil. No mezclar unidades ni omitir dimensiones/peso cuando restrinjan el espacio.

**Aceptación:** dos usuarios compitiendo por el último espacio no pueden confirmar dos ocupaciones; antes de confirmar la colocación se distingue ubicación actual de destino reservado.

### CA-04. Ubicación Física de los Documentos Anteriores

**Finalidad:** aplicar el mismo control a acervo capturado mediante Registro de Archivo Inicial.

- Dependencia explícita: Registro de Archivo Inicial, mencionado en el requerimiento pero aún no definido como módulo completo. Se prepara su contrato de entrada sin inventar sus reglas.
- Capturar procedencia, lote, área, folio y marbete anterior, descripción, fechas disponibles, contenedor y ubicación declarada; separar datos declarados de datos verificados.
- Detectar posibles duplicados; conservar identificadores históricos y correspondencias. Una colisión de marbetes históricos queda en conciliación y requiere contexto; nunca se resuelve escogiendo un expediente arbitrario.
- Para archivo contable anterior, conservar recopilador de origen y referencia financiera. La vista «recopilador → tipo de póliza → documento» es una agrupación de consulta; no sustituye el expediente, el CGCA ni la jerarquía de ubicaciones. Los códigos históricos se homologan con el catálogo real antes de vincularlos a pólizas actuales.
- Aplicar CA-03 después de verificar físicamente. El acervo sin corroborar se marca «Ubicación no verificada»; tampoco se presume digitalizado ni se fabrican fechas o folios faltantes.
- Conservar la clasificación y versión históricas y proponer equivalencia con las actuales. No aplicar retrospectivamente una regla de conservación ni una fecha de cierre inventadas.

**Aceptación:** consultar un marbete histórico conciliado encuentra el expediente actual y su procedencia. Reimportar un mismo lote no genera duplicados.

### CA-05. Registro de Anexos

**Finalidad:** incorporar nuevas piezas a un expediente, carpeta o caja ya archivados, preservando su contexto.

- Identificar destino por marbete, resolver expediente y unidad física; una caja con varios expedientes requiere seleccionar el expediente receptor.
- Registrar folio de anexo, fecha documental y de incorporación, remitente, motivo, tipo, número de hojas, orden, soporte y vínculo con el documento al que complementa, si procede.
- Asociar archivos, validar calidad y emitir constancia de incorporación. Conservar el índice previo; toda corrección queda versionada.
- Un expediente cerrado requiere autorización de adición o reapertura conforme a su procedimiento; no se abre automáticamente. Recalcular capacidad si el anexo aumenta el volumen físico.
- Conservar el cómputo anterior y el efecto autorizado del anexo. No reiniciar plazos de guarda por una nueva carga o reescaneo.

**Aceptación:** el anexo aparece en el índice y la bitácora sin sobrescribir documentos ni perder el orden previamente validado.

### CA-06. Buscar Documentos en Archivo

**Finalidad:** localizar por marbete vigente o anterior, captura manual o lector de código de barras.

- Mostrar tipo de objeto, folio, área, disponibilidad, unidades contenidas, ubicación actual verificada y calidad de digitalización, según autorización.
- Un documento hereda la ubicación de su unidad física; un expediente puede devolver varias ubicaciones. Marbetes históricos ambiguos requieren contexto de procedencia.
- Filtros complementarios propuestos: asunto, serie, fechas, tipo documental y contenido OCR autorizado.
- Para Contabilidad: serie/subserie 2530, versión, periodo del expediente, unidad productora, fase de archivo, disponibilidad y préstamo vigente. Un expediente prestado informa ubicación habitual y custodio temporal a usuarios autorizados.
- Para soporte contable, consultar también por institución/sistema de origen, ejercicio, tipo y número de póliza, más periodo cuando sea necesario para distinguir registros. Conservar vínculo al ID persistente de la póliza confirmada y resolver datos en su sistema de origen. Si el folio es ambiguo, mostrar candidatos autorizados y conciliar; si la póliza histórica aún no está en SIAF, permitir registro documental con vínculo pendiente, sin crear una póliza ficticia.
- Consultar o leer un código nunca mueve, presta ni elimina una unidad. No se revelan ubicación o metadatos de expedientes fuera del permiso del usuario.

**Aceptación:** una búsqueda autorizada distingue «pendiente de localizar», «no verificada» y «ubicada». El buscador y el OCR respetan el mismo alcance de acceso que el visor.

### CA-07. Eliminar Documentos del Archivo

**Finalidad:** atender el requerimiento mediante rutas controladas, distinguiendo errores de captura y disposición documental.

- **Corrección de captura:** cancelación lógica justificada de registros erróneos, conservando identificación, evidencia y auditoría; no equivale a baja documental ni destruye soportes. Una desvinculación errónea conserva el documento y sus demás relaciones.
- **Baja documental:** solicitud a 09.3.3 con inventario, valoración, revisión de conservación e impedimentos, dictamen y autorización competente. Este módulo registra y consulta la solicitud; no ejecuta una eliminación inmediata por marbete.
- La clasificación de acceso, litigios, auditorías, observaciones, obligaciones pendientes y vínculo patrimonial se verifican antes de promover la baja, conforme a las disposiciones aplicables. No bastan fecha vencida, escaneo completo ni un rol administrador.
- Las 16 entradas de referencia 2530 señalan destino Archivo Histórico y bloquean la baja ordinaria por vencimiento. Corresponde evaluar transferencia secundaria conforme al procedimiento aplicable, sin ejecutar traslado o disposición de forma automática.
- Conservar prueba del resultado y trazabilidad. Una baja autorizada tampoco se interpreta como autorización técnica indiscriminada para borrar copias o respaldos.

**Aceptación:** escanear un marbete no habilita un borrado directo; cancelar una captura no altera el estado archivístico ni una póliza o trámite asociado.

### CA-08. Cambio de Marbetes

**Finalidad:** conservar la opción solicitada, separando las dos operaciones que su descripción mezcla.

- **Reubicar:** mantener identificador y marbete, aplicar CA-03 y registrar origen, destino, motivo y confirmación de custodia. Si la etiqueta contiene ubicación, reimprimirla con el mismo identificador.
- **Sustituir marbete:** emitir nuevo código por deterioro o corrección autorizada, conservar el anterior como alias y registrar causa, responsable y fecha. No cambia ubicación por sí solo.
- Si ambas acciones son necesarias, registrar eventos separados relacionados. Mover una caja actualiza la ubicación efectiva de su contenido, conserva la trazabilidad de sus integrantes y no duplica ocupación.

**Aceptación:** tras una reubicación funciona el mismo marbete; tras una sustitución ambos números resuelven la misma identidad e informan cuál está vigente.

## 5. Datos y estados propuestos

Reutilizar el diseño existente `archivos.documento`, `documento_version`, `documento_relacion`, `documento_bitacora`, `cgca_catalogo` y `cadido_catalogo`, previa revisión de su implementación real. Los SQL del manual son antecedentes de diseño y no prueban que existan en producción.

El modelo debe incorporar nodos e instrumentos versionados. La referencia nueva no puede cargarse en una estructura que sólo admita clave global única, omita Subsección o mezcle valores contable/fiscal. Se conservan reglas por serie/subserie y versión, nunca valores universales de 1/5 años o destino de baja.

| Entidad propuesta | Datos y restricciones mínimas |
|---|---|
| expediente | UUID, folio único institucional, asunto, área, serie y versión de instrumentos, fechas de apertura/cierre, acceso, procedencia y estados separados. |
| expediente_documento | Expediente, documento y versión, orden documental único por expediente, folio físico si existe y motivo de incorporación. |
| unidad_fisica | UUID, tipo CAJA/CARPETA/TOMO, padre físico permitido, expediente cuando corresponda, dimensiones/ocupación; sin ciclos. Caja puede contener carpetas/tomos de diferentes expedientes. |
| documento_unidad_fisica | Documento y unidad física contenedora; controlar cambios y ausencia de soporte físico para documentos nacidos electrónicos. |
| marbete / marbete_alias | Número institucional no reutilizable, objeto expediente o unidad física (una sola referencia), vigencia, historial y procedencia de códigos anteriores. Alias histórico ambiguo exige contexto. |
| ubicacion_fisica | Jerarquía, responsable, capacidad total/ocupada/reservada, unidad de medida, perfil físico y restricciones. |
| movimiento_ubicacion | Unidad raíz, origen, destino reservado, estado, motivo, solicitante, confirmante y fechas. Un solo movimiento abierto por unidad; historial de contención. |
| lote_digitalizacion / control_calidad | Identificador de reintento, periodo, área, contenedores, recepción/preparación/devolución, hojas físicas, imágenes esperadas/generadas/aceptadas, documentos y expedientes; operador, revisor, incidencias, manifiesto y aceptación de entrega. No equiparar hojas con imágenes ni inventar cantidades esperadas. |
| anexo / lote_archivo_inicial | Procedencia, fecha de incorporación, objetos afectados, evidencia, conciliación y autorización cuando aplique. |
| referencia_financiera_documental | Documento, sistema e institución de origen, ejercicio, tipo y número de póliza, periodo si distingue registros, ID de origen confirmado, estado de conciliación y recopilador histórico. Reutilizar documento_relacion para el vínculo validado; esta referencia no crea una segunda póliza. |
| instrumento / instrumento_version / nodo_clasificacion | Tipo de instrumento, fuente y hash, fechas, estado de validación, nodo padre, nivel, código fuente y literal; claves únicas dentro de versión, sin reescribir versiones aplicadas. |
| regla_disposicion / equivalencia | Nodo y versión, valores administrativo/legal/contable/fiscal separados, marcas originales de información, plazos por fase, destino, disparador y resolución de equivalencia con fuente/responsable. |
| ambito_operativo / responsable_archivo | Institución, unidad orgánica, subsección archivística relacionada, proceso, series habilitadas y perfiles por vigencia. Contabilidad no recibe todos los permisos de 2530 por defecto. |
| inventario / transferencia / prestamo | Finalidad, expedientes y unidades, origen/destino, solicitante, autorizaciones, recepción, fechas, custodia temporal y devolución; eventos distintos de marbetes. |
| programa_archivistico / actividad / riesgo | Ejercicio, responsable, calendario programado, evidencia ejecutada, avance verificable e incidencias de conservación/espacio. El PADA 2025 se conserva como programa fuente. |

Todas las entidades de mantenimiento contemplarán `estatus_registro`, `usuario_c`, `fecha_c`, `usuario_m`, `fecha_m`. Eventos históricos se agregan sin sobrescribir su contenido; el usuario se obtiene de la sesión autenticada. El registro lógico no sustituye los estados de negocio.

| Dimensión | Estados propuestos |
|---|---|
| Trámite del expediente | ABIERTO, CERRADO; reapertura como evento autorizado. |
| Ciclo archivístico | TRAMITE, CONCENTRACION, HISTORICO, BAJA_EJECUTADA cuando proceda legalmente; autorización y ejecución son eventos distintos. El referente 2530 tiene destino histórico. |
| Digitalización | PENDIENTE, EN_PROCESO, EN_REVISION, OBSERVADA, VALIDADA; completitud sustentada por inventario. |
| Localización física | PENDIENTE, DECLARADA_NO_VERIFICADA, UBICADA_VERIFICADA, NO_APLICA para soporte exclusivamente electrónico. |
| Movimiento físico | RESERVADO, CONFIRMADO, CANCELADO. El destino reservado nunca suplanta la ubicación actual. |
| Vinculación financiera | PENDIENTE, PROPUESTA, VALIDADA, RECHAZADA; independiente de la calidad del escaneo. La confirmación exige identificar una póliza del sistema de origen de forma inequívoca. |
| Transferencia | PROPUESTA, EN_REVISION, AUTORIZADA, ENTREGADA, RECIBIDA, RECHAZADA/CANCELADA, según procedimiento aprobado. La autorización no prueba recepción. |
| Préstamo | SOLICITADO, AUTORIZADO, ENTREGADO, DEVUELTO, CANCELADO; vencimiento e incidencias se registran sin cambiar fase archivística. |

El vencimiento se muestra pendiente mientras falte cierre formal, disparador de cómputo o validación aplicable. Las fechas de escaneo y carga no sustituyen esos datos.

Estos nombres son propuesta inicial: deberán mapearse a los catálogos definitivos sin cambiar silenciosamente el diseño anterior.

## 6. Contratos técnicos propuestos, todavía sin implementación

Los contratos se sitúan después del modelo de datos, conforme al orden del manual. Antes de crear migraciones se cotejará el esquema real y se resolverán las autoridades y los catálogos pendientes.

**PostgreSQL:** familias `archivos.fn_leer_expediente` / `fn_crud_expediente`, `fn_leer_marbete` / `fn_crud_marbete` y `fn_leer_movimiento_ubicacion` / `fn_crud_movimiento_ubicacion`. Retorno estándar `{ "error": 0, "mensaje": "OK", "data": {} }`; `-1` validación de negocio y `-2` error técnico. Las firmas exactas se definirán al cotejar el esquema. Funciones de escritura con autorización, transacción, auditoría e idempotencia; `SECURITY DEFINER` con `search_path` fijo, privilegios mínimos y actor de un contexto de sesión confiable.

**REST / NestJS:** autenticación y alcance de expediente en cada endpoint; roles propuestos de captura, digitalización, revisión, custodia y consulta. Auditoría de bajas según autoridad institucional, sin asumir que TI o un administrador puede autorizarlas.

| Método | Ruta propuesta | Resultado |
|---|---|---|
| GET / POST | `/api/v1/archivo-control/expedientes` | Consulta paginada / registro previo del expediente. |
| POST | `/api/v1/archivo-control/expedientes/:id/lotes-digitalizacion` | Inicia lote; carga e integridad se apoyan en el servicio transversal de archivos. |
| POST | `/api/v1/archivo-control/lotes-digitalizacion/:id/revision` | Acepta u observa calidad, sin sustituir versiones anteriores. |
| POST | `/api/v1/archivo-control/marbetes/emisiones` | Emite o reimprime, diferenciando ambas acciones. |
| GET | `/api/v1/archivo-control/marbetes/:codigo` | Resuelve objeto, equivalencias y ubicación autorizada; procedencia si es ambigua. |
| GET / POST | `/api/v1/archivo-control/unidades/:id/ubicaciones-sugeridas` / `.../movimientos` | Consulta candidatos / reserva destino con revalidación de capacidad. |
| POST | `/api/v1/archivo-control/movimientos/:id/confirmacion` | Confirma colocación y libera origen de forma atómica. |
| POST | `/api/v1/archivo-control/movimientos/:id/cancelacion` | Cancela reserva; conserva origen e historial. |
| POST | `/api/v1/archivo-control/lotes-archivo-inicial` | Importa acervo y conserva procedencia; reintentos idempotentes. |
| POST | `/api/v1/archivo-control/expedientes/:id/anexos` | Incorpora pieza con controles de cierre, índice y capacidad. |
| POST | `/api/v1/archivo-control/documentos/:id/cancelacion-captura` | Cancelación lógica justificada y auditada. |
| POST | `/api/v1/archivo-control/expedientes/:id/solicitudes-baja` | Remite al procedimiento 09.3.3; no ejecuta destrucción. |
| POST | `/api/v1/archivo-control/marbetes/:id/sustitucion` | Nuevo número y alias del anterior; mantiene identidad y ubicación. |

Ninguna ruta anterior se declara disponible. La integración documental reutilizará el servicio transversal; no debe crearse un segundo repositorio de binarios por módulo.

La recalibración añade contratos de lectura de instrumentos/versiones/nodos por ámbito y de solicitud/recepción de transferencias y préstamos/devoluciones. Requieren validación de alcance en servidor, idempotencia e inventarios trazables; las firmas se detallan en la etapa de implementación. El selector de la maqueta consulta la referencia embebida y no llama a un backend.

## 7. Actores e interfaces

El área productora identifica el asunto y aporta documentación; captura registra; digitalización procesa; revisión valida calidad; custodia confirma ubicación; consulta accede según permisos. La aprobación de disposición documental se identifica mediante su fundamento institucional antes de habilitarla. La segregación entre captura, revisión y autorización se propone para validación.

| Interfaz | Evidencias a relacionar, sin sustituir sus procesos |
|---|---|
| Presupuesto | Suficiencia, adecuaciones y soporte de compromiso mediante identificadores de origen. |
| Contabilidad | Pólizas, comprobantes y libros; referencia financiera compuesta e ID persistente confirmado, con versiones y vínculos auditables. Consultar información del registro de origen sin alterar importes o asientos al archivar. |
| Cuentas por Pagar | Expediente de pago y requisitos; conservar XML original y representación PDF como objetos relacionados distintos. |
| Tesorería | Orden de pago, comprobante de transferencia/cheque y acuses; acceso restringido a información bancaria. |
| Recursos Materiales y control patrimonial | Contrato, recepción, inventario y resguardo; conservación del soporte de adquisición mientras corresponda al bien. El marbete documental no sustituye el número de inventario patrimonial. |
| Gestión Documental existente | 09.2.1 consulta transversal; 09.2.2 ingreso de archivos; 09.2.3 visor; 09.3.2 transferencias; 09.3.3 bajas; 09.4.3 bitácora. Reutilizar estas capacidades sin atribuirles desarrollo ya terminado. |

Archivar, reubicar o reimprimir no genera momentos presupuestarios, pólizas, obligaciones de pago ni movimientos patrimoniales por sí solo.

## 8. Criterios de aceptación y construcción incremental

| Caso | Resultado verificable |
|---|---|
| Archivo Inicial sin datos completos | Conserva faltantes y procedencia; no presume ubicación ni digitalización validada. |
| Caja con tres expedientes | Buscar su marbete lista únicamente contenido autorizado y ubicación efectiva. |
| Expediente repartido en dos tomos | Devuelve ambos tomos y ubicaciones, sin elegir una arbitrariamente. |
| Reescaneo o anexo | Conserva versión/índice anterior y registra calidad, motivo y responsable. |
| Marbete emitido dos veces por reintento | Una sola emisión, sin duplicar identidad ni consumir códigos indebidamente. |
| Último espacio solicitado simultáneamente | Solo una reserva válida; la otra recibe conflicto de capacidad. |
| Cancelación de reubicación | Libera destino y conserva origen; deja evento de cancelación. |
| Sustitución de marbete | Código anterior y vigente resuelven el mismo objeto y muestran historial. |
| Baja con auditoría pendiente o soporte de bien vigente | Detiene la solicitud y documenta el impedimento; no destruye soportes. |
| Usuario sin acceso consulta o usa OCR | No obtiene metadatos, texto ni ubicación fuera de su autorización. |
| Dos pólizas con igual número en ejercicios o sistemas distintos | La búsqueda distingue las referencias; no confirma el vínculo por el número aislado. |
| Póliza histórica ausente del sistema financiero actual | Conserva documento y procedencia con vínculo pendiente; no genera registros contables. |
| Diez hojas a doble cara y un documento de varias hojas | Registra por separado hojas, imágenes, documentos y expedientes; no presenta esas cantidades como equivalentes. |
| Lote entregado para digitalización | Concilia recepción, preparación, manifiesto digital e incidencias; acredita devolución física y aceptación del área receptora. |
| Selección de una entrada 2530 | Consulta clave, literal, fuente, 2/8 años y Archivo Histórico; no ofrece baja por transcurso del tiempo. |
| Dos copias idénticas del CADIDO | Una versión lógica y una sola carga de las 16 entradas, con ambas procedencias. |
| Nueva versión de instrumento | Conserva versiones y equivalencias previas; la transición funcional no reescribe historia. |
| Información marcada Pública y Reservada en CADIDO | Conserva las marcas fuente y exige clasificación real/permisos antes de dar acceso. |
| Préstamo y devolución de una unidad | Registra acuses y custodio temporal; conserva ubicación habitual e identidad del expediente. |

La cobertura se reportará por unidad: imágenes aceptadas sobre imágenes esperadas verificadas, documentos validados sobre documentos inventariados y expedientes completos sobre expedientes del alcance. Cuando un denominador no esté validado, se informará «por determinar». No se usará el máximo de hojas de una cotización histórica como inventario real ni como meta automática del PJEV.

**Secuencia recalibrada:** (1) fuentes/versiones, ámbito DGA–2530–Contabilidad y catálogo de referencia; (2) expediente, inventario inicial, responsables y ubicaciones; (3) marbetes, consulta y enlace financiero; (4) digitalización/calidad/anexos; (5) préstamos, transferencias y seguimiento de conservación/actividades. La disposición respeta el destino histórico de la referencia 2530. Las ocho funciones originales se mantienen integradas a este modelo general.

Los instrumentos recibidos ya sustentan esta recalibración. Para puesta en operación se ratificará su versión aplicable y acto de aprobación, y se completarán el inventario real de espacios, formatos de transferencia/préstamo, muestras de marbetes/lectores y el procedimiento de Archivo Inicial. La Guía y el Informe de cumplimiento están enlazados en el XLS, pero su contenido no se ha dado por conocido.

## 9. Fuentes y antecedentes

- [Ley General de Archivos, texto legislativo alojado por IMSS](https://www.imss.gob.mx/sites/all/statics/pdf/leyes/4536_LGA.pdf), reforma indicada 14-11-2025; consulta 29-10-2026.
- [LGCG, Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/pdf/LGCG.pdf), reforma indicada 14-05-2026; consulta 29-10-2026.
- [Acuerdo CONAC: Disposiciones Generales para el Archivo Contable Gubernamental](https://sidof.segob.gob.mx/notas/docFuente/5710974), publicación 11-12-2023, apartados IV a VI; [índice de normatividad CONAC](https://www.conac.gob.mx/es/CONAC/Normatividad_Vigente).
- Fuente institucional local: `Documentación Normatividad/Manuales de PJE/03_MANUAL.ESPECIFICO.PROCEDIMIENTOS.SUBDIRECCION_DE_RECURSOS_MATERIALES_FEB_2023.pdf`, páginas PDF 10 a 12, revisadas directamente. Su vigencia operativa debe ratificarse para la puesta en servicio.
- Antecedentes de diseño, sin valor de norma ni prueba de despliegue: `PLAN_GESTION_DOCUMENTAL_Y_ARCHIVOS_SIAF_PJEV.md`, `FILE_BACKEND_ARCHITECTURE.md`, `FILE_COMPONENTS_AND_INTEGRATION_GUIDE.md`, `FILE_ADMIN_AND_SECURITY.md`, `archivos_schema.sql`.
- [Antecedente comercial del Congreso de Veracruz, 15-08-2018](REFERENCIA_ARCHIVO_DIGITAL_CONGRESO_2018.md): cotización DOCX proporcionada por el usuario el 29-10-2026. Aporta preparación física, organización por recopilador/tipo/documento, enlace financiero, entrega y capacitación; no establece reglas institucionales del PJEV.
- Fuentes institucionales recibidas en Downloads: `CUADRO_DE_CLASIFICACION_ARCHIVISTICA_2024.pdf` (pp. 31–32 y nota p. 34); `CATALOGO__DE_DISPOSICION_DOCUMENTAL_2024.pdf` (pp. 36–37 y nota p. 39), con copia idéntica «(1)»; `PROGRAMA_ANUAL_DE_DESARROLLO_ARCHIVISTICO_2025.pdf` (pp. 12–20); `XLV_c.xls`, Informacion A1:L14 y tabla relacionada de responsables. [Procedencia, contraste y decisiones](RECALIBRACION_ARCHIVISTICA_DGA_PJEV.md).

## 10. Historial

| Fecha | Cambio | Estado |
|---|---|---|
| 29-10-2026 | Alta del alcance 4.1; ocho opciones, modelo conceptual, contratos propuestos, interfaces y criterios de aceptación. | Especificación inicial; validación institucional y desarrollo pendientes. |
| 29-10-2026 | Integración del antecedente del Congreso fechado 15-08-2018: preparación y entrega por lote, recopiladores, vínculo financiero inequívoco, conteos y capacitación. | Propuesta funcional incorporada; sin trasladar precios, catálogo ni condiciones comerciales históricas. |
| 29-10-2026 | Recalibración con instrumentos institucionales PJEV y alcance DGA–2530–Contabilidad confirmado. Se incorporan cuatro series/doce subseries, plazos por fase, destino histórico, versiones, inventarios, préstamos y transferencias. | Especificación y maqueta recalibradas; sin despliegue de base de datos o servicios. |
| 29-10-2026 | Incorporación de los dos diagramas de base del analista y versiones SVG ajustadas: ciclo 2530, identidad/ubicación, documentos por procedimiento y metadatos aplicables por tipo. | Revisión documentada sobre la base existente; fuentes gráficas conservadas. |
