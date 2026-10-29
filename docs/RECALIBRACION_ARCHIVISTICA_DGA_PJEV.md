# Recalibración del Sistema de Control de Archivo del PJEV

**Fecha de revisión:** 29 de octubre de 2026.  
**Alcance operativo confirmado por el usuario:** Dirección General de Administración, subsección documental **2530 — Subdirección de Recursos Financieros**, con foco en **Contabilidad**.  
**Estado:** especificación y maqueta del manual recalibradas; implementación operativa pendiente. La revisión de las fuentes no equivale a certificar su vigencia actual ni a autorizar transferencias o bajas.

El sistema se diseña como un control archivístico institucional configurable. La implantación inicial atiende Contabilidad dentro de la DGA; su estructura conserva la posibilidad de incorporar otras áreas mediante catálogos, versiones y permisos. La cotización del Congreso de 2018 queda como antecedente histórico subordinado: los instrumentos del PJEV aportados por el usuario pasan a ser la referencia institucional del diseño.

## 1. Fuentes recibidas y lectura de su alcance

| Fuente | Contenido observado | Uso en el sistema |
|---|---|---|
| PADA 2025, 20 páginas | Diagnóstico y planeación; responsables, organización, inventarios, transferencias, consulta/préstamo, capacitación, espacios y riesgos; objetivos y proyectos en pp. 12–17, programación en pp. 18–20. | Orienta procesos y seguimiento de actividades. Es un programa del ejercicio 2025: no acredita ejecución de sus metas ni constituye automáticamente el programa de 2026. |
| CGCA denominado 2024, 34 páginas | Jerarquía institucional; DGA en pp. 27–33; subsección 2530 en pp. 31–32. La nota final, p. 34, está fechada 09-03-2025 e informa transición a clasificación funcional. | Claves y denominaciones con versión y procedencia. No sustituirlas por códigos inventados del diseño anterior. |
| CADIDO denominado 2024, 39 páginas | Para 2530, pp. 36–37: valores/marcas, información, plazos por fase y destino. La nota de p. 39 está fechada 09-04-2025 e informa transición a clasificación funcional. | Reglas documentadas de referencia, preservando literalmente columnas y excepciones que deban validarse. |
| Segunda copia del CADIDO, terminada en «(1)» | Igual tamaño y SHA-256 que la otra copia. | Una sola versión lógica de instrumento, con dos rutas de origen; no dos catálogos ni dos cargas de series. |
| XLV_c.xls, hoja Informacion, A1:L14 | Registro de publicación de ocho instrumentos/tipos para 01-01-2025 a 31-03-2025; actualización declarada 31-03-2025 y creación/modificación de registros 24-04-2025. El campo Periodos dice Anual. | Evidencia de publicación y enlaces. No es inventario de expedientes ni una medición del volumen documental. No confundir periodicidad del formato con periodo efectivamente informado. |

El XLS incluye enlaces al CGCA, CADIDO, PADA, Guía de Archivo Documental e Informe Anual de Cumplimiento. Los dos últimos documentos no fueron aportados y su contenido no se presupone. Para dictamen, acta de baja y acta de transferencia secundaria, el archivo no proporciona enlace y contiene notas sobre valoración del Grupo Interdisciplinario. Esas celdas no prueban la autorización de un caso concreto ni ausencia de documentos fuera de ese corte.

La hoja TABLA587183 relaciona responsables publicados por ID; se conserva como evidencia del corte de 2025. Los permisos actuales se asignan a cargos y usuarios con vigencia, sin fijar a esas personas como autoridades permanentes.

## 2. Requisito normativo, regla institucional y propuesta tecnológica

**Requisito normativo.** Se mantiene la conservación, integridad, organización y trazabilidad exigibles conforme a LGA, LGCG y las disposiciones CONAC de archivo contable. El acuerdo CONAC publicado el 11-12-2023 establece una guarda general y excepciones patrimoniales, de procedimientos pendientes y de cuentas por cobrar/pagar. Su referencia general de seis años no sustituye los plazos específicos ni el destino histórico consignado por el instrumento institucional.

**Regla institucional documentada.** Se toman del CGCA y CADIDO recibidos las claves, jerarquía y celdas de 2530. El PADA aporta los procesos y actores que el programa de 2025 describe. Estas fuentes se registran con sus fechas, páginas y estado de validación; el aviso de transición impide afirmar que su estructura sea una versión definitiva para toda operación de 2026.

**Propuesta tecnológica.** Se propone versionar instrumentos y nodos, mantener equivalencias, configurar alcance por área/proceso, relacionar expedientes con documentos y operaciones financieras, y separar los estados de digitalización, ubicación, préstamo y ciclo archivístico. El formato JSON, OCR, hashes y marbetes son decisiones de implementación.

## 3. Alcance inicial y modelo general

La ruta del **CGCA** para el piloto es:

`FOPJ01 → PLENOCJP → DGA2500 → 2530 → serie → subserie, cuando exista`.

En el **CADIDO** la grafía de fondo es `FOPJO1`, con letra O donde el CGCA usa cero. Se preservan ambos códigos fuente y una incidencia de equivalencia pendiente de validación archivística. El vínculo de diseño entre los renglones 2530 se fundamenta en la coincidencia de subsección, series y denominaciones; no se convierte esa inferencia en una normalización autorizada del fondo.

La denominación «subdirección de administración y contabilidad» del diálogo fue confirmada por el usuario como referencia a 2530 con foco en Contabilidad. La denominación documental de los instrumentos permanece como **Subdirección de Recursos Financieros**. Un catálogo orgánico vigente podrá distinguir la unidad operativa de Contabilidad de la subsección archivística, sin cambiar retrospectivamente los códigos de los documentos.

El modelo general admite Fondo, Subfondo, Sección, Subsección, Serie y Subserie. Algunos niveles serán opcionales según la versión del instrumento. Se mantiene contexto de las subsecciones DGA 2510, 2520 y 2540 para futuras etapas; no se habilita su captura por pertenecer a la misma DGA.

Las cuatro series de 2530 se cargan como referencia. El piloto prioriza estados contables, pólizas y conciliación. La información presupuestaria/programática conserva su productor y su interfaz con Presupuesto; la pertenencia a 2530 no otorga a Contabilidad facultades de producción o autorización sobre todos sus procesos. El alcance efectivo combina unidad productora, proceso, serie, clasificación de acceso y permiso.

## 4. Clasificación y disposición verificadas en 2530

| Serie | Denominación CGCA | Subseries del instrumento | Trámite | Concentración | Columna de destino marcada |
|---|---|---|---|---|---|
| 2530.1 | Estados contables | 2530.1a Mensual; 2530.1b Trimestral; 2530.1c Anual. | 2 años | 8 años | Archivo Histórico |
| 2530.2 | Información presupuestaria y programática | 2530.2a Mensual; 2530.2b Trimestral; 2530.2c Anual. | 2 años | 8 años | Archivo Histórico |
| 2530.3 | Pólizas | 2530.3a Ingresos; 2530.3b Tramitada; 2530.3c Liquidada; 2530.3d Transferencias presupuestales; 2530.3e Traspasos bancarios; 2530.3f Manuales. | 2 años | 8 años | Archivo Histórico |
| 2530.4 | Conciliación contable/presupuestal | Sin subserie publicada en el bloque revisado. | 2 años | 8 años | Archivo Histórico |

Son **4 series y 12 subseries**, es decir, 16 entradas de referencia; no 16 expedientes ni documentos. Las marcas del CADIDO se comprobaron por columnas en las pp. 36–37: **Archivo Histórico tiene X y Baja está sin marca** en las 16 entradas.

La extracción de diseño se conserva en [datos_archivisticos_dga_2530_2024.json](datos_archivisticos_dga_2530_2024.json), con claves, literales, marcas, páginas, huellas y observaciones. Ese JSON es un derivado verificable; no sustituye a los PDF oficiales ni prueba carga en producción.

«Tramitada» y «Liquidada» son denominaciones de subseries del instrumento, no estados del flujo de pago ni de digitalización. El cambio de estado de un trámite no reclasifica automáticamente el expediente ni duplica los archivos. Del mismo modo, Mensual/Trimestral/Anual clasifica la documentación; no equivale a la fecha de carga.

## 5. Conservación y disposición

Se eliminan como reglas del diseño los valores universales de un año de trámite, cinco de concentración y baja documental predeterminada. Para la referencia 2530 se muestran **dos fases de 2 y 8 años**. La suma de diez años es informativa: no constituye un contador automático desde la fecha de escaneo, de apertura o de carga.

El expediente requiere cierre formal, evento de inicio del cómputo, fundamento, versión aplicable, fechas de recepción/transferencia y suspensiones. Hasta validar el disparador y el calendario aplicable, la fecha de vencimiento se presenta **pendiente de determinar**, conservando los plazos de referencia. El cierre del expediente es un acto del procedimiento, no un dato que el CADIDO calcula por sí solo.

La transferencia primaria requiere inventario y entrega/recepción; la secundaria exige el procedimiento y la valoración competentes. El destino histórico de 2530 bloquea la ruta ordinaria de baja por vencimiento y propone evaluación de transferencia secundaria; ni el transcurso del tiempo ni la clasificación histórica ejecutan el movimiento físico automáticamente.

Los soportes de bienes aún vigentes, litigios, observaciones de auditoría y otras obligaciones de conservación se mantienen como impedimentos o ampliaciones según su fundamento. Una discrepancia entre disposiciones se documenta y se somete al área competente; el sistema conserva el instrumento fuente y la resolución aplicable. No se reduce un plazo institucional mediante un parámetro tecnológico genérico.

La cancelación lógica por error de captura mantiene su ruta separada y no destruye documentos ni equivale a disposición final. Una desactivación de catálogo tampoco borra los expedientes relacionados.

## 6. Procesos que el PADA añade al bloque de digitalización

| Proceso | Comportamiento propuesto | Evidencia mínima y referencia |
|---|---|---|
| Inventario documental | Registro por expediente, serie, área, fechas extremas, soporte, volumen, ubicación y estado; distinguir inventario general, transferencia y baja. | Inventario versionado, responsable y conciliación; PADA pp. 12–16. |
| Directorio de responsables | Responsables de trámite, custodia y enlace por área, cargo y vigencia; validación del alcance de acceso. | Nombramiento/designación cuando corresponda y periodos de responsabilidad; PADA pp. 13 y 18. |
| Transferencia primaria | Propuesta, revisión de inventario, entrega y recepción; conservar productor y cambiar custodia sólo al confirmar. | Inventario, acuses y fechas; PADA pp. 12–13 y 18–19; integración con 09.3.2. |
| Préstamo y devolución | Solicitud, autorización, salida, vencimiento previsto, renovación, devolución e incidencia; distinguir consulta digital de salida física. | Solicitante y autorización, unidad y ubicación habitual, receptor, fechas, acuses e incidencias; PADA pp. 12, 14 y 19. |
| Preservación y espacios | Capacidad, condiciones de resguardo, incidencias y acciones; control de acceso y seguimiento de riesgos. | Registro de condición, responsable y seguimiento; PADA pp. 13–14, 17 y 20. |
| Planeación y seguimiento | Programa por ejercicio, actividades, responsables, calendario previsto, evidencia realizada y resultado. | Plan y evidencia separados; no marcar metas de 2025 cumplidas por haberlas importado; PADA pp. 18–20. |
| Consulta y versiones públicas | Acceso según expediente y finalidad; versión pública como derivado ligado al original. | Autorización y bitácora; las marcas del CADIDO son referencia, no permisos automáticos. |

Estos procesos complementan las ocho opciones del requerimiento 4.1 y se integran con los módulos documentales ya previstos. La implementación inicial puede ser gradual, pero los datos y contratos deben contemplar custodia, préstamos y transferencias desde el diseño para evitar reconstruir la historia después.

## 7. Datos y estados a recalibrar

Se propone separar **fuente documental**, **versión de instrumento**, **nodo de clasificación**, **regla de disposición**, **unidad orgánica**, **ámbito de operación**, **expediente** y **evento de custodia**. Un cambio de instrumento crea una nueva versión; no reescribe la que sustentó un expediente anterior. La equivalencia entre versiones conserva autor, fundamento, fecha y resolución.

Las reglas de disposición guardan valores administrativo, legal, contable y fiscal de forma independiente; el diseño anterior que mezclaba fiscal/contable pierde información del CADIDO. Se preservan también las marcas crudas de información Pública, Reservada y Confidencial y el acto de clasificación real por documento/expediente. El CADIDO marca simultáneamente Pública y Reservada para pólizas: no procede convertirlo en un único valor ni habilitar acceso público de modo automático.

El estado archivístico (Trámite, Concentración, Histórico, Baja ejecutada cuando legalmente proceda) permanece separado del estado de transferencia, la autorización de destino, la calidad del escaneo y la disponibilidad física. Un expediente prestado conserva su ubicación habitual y muestra al custodio temporal; no ocupa un nuevo anaquel por el hecho de salir en préstamo.

Los contratos propuestos deben aceptar `instrumento_version_id`, `clasificacion_nodo_id`, `regla_disposicion_id`, `unidad_productora_id`, `ambito_operativo_id`, `fecha_cierre`, `evento_inicio_computo`, `suspensiones` y referencias de transferencia/préstamo. Los IDs son propuesta técnica; sus firmas y tablas se cotejarán con el sistema real antes de migrar.

## 8. Cambios a las ocho opciones originales

CA-01 hereda la clasificación validada del expediente y conserva el índice; CA-02 imprime una identidad estable con clasificación/versiones según formato autorizado; CA-03 diferencia depósito de trámite/concentración/histórico de ubicación dentro del depósito; CA-04 conserva clasificación y fechas históricas sin forzar la versión más reciente; CA-05 registra anexos sin reiniciar plazos silenciosamente; CA-06 busca por serie/subserie, unidad productora, ejercicio y referencia financiera; CA-07 separa corrección de captura y disposición, bloqueando baja por vencimiento de las entradas históricas 2530; CA-08 distingue sustitución de marbete, reubicación y transferencia archivística.

## 9. Criterios de aceptación de la recalibración

- Las 16 entradas 2530 coinciden con las páginas fuente y conservan 2/8 años y destino histórico. La carga de ambas copias del CADIDO produce una sola versión.
- La selección de 2530.3b o 2530.3c no modifica el estado financiero del trámite. Un código contable de operación se homologa con la subserie mediante una regla aprobada, sin inferirla por letras heredadas del Congreso.
- Un expediente de 2530 no puede solicitar baja ordinaria sólo por sumar diez años. Sin cierre/disparador validado, el vencimiento permanece pendiente; un anexo tampoco lo reinicia sin fundamento.
- Un cambio de CGCA conserva la clasificación anterior y su equivalencia; `FOPJ01` y `FOPJO1` no se fusionan silenciosamente.
- Contabilidad opera su ámbito autorizado; otras subsecciones de la DGA permanecen como contexto configurable. El filtro visual no sustituye la autorización del backend.
- Un préstamo registra salida y devolución con custodio temporal; la transferencia conserva inventario y recepción. Ninguno se registra como simple cambio de marbete.
- Las marcas Pública/Reservada del CADIDO no conceden acceso al documento. Se aplican clasificación real, datos personales y permisos vigentes.
- La importación de XLV genera referencias de publicación, no expedientes, metas ejecutadas, nombramientos vigentes ni actas de disposición aprobadas.

## 10. Fuentes y validaciones restantes

Los cinco archivos originales permanecen en sus ubicaciones de Downloads; las huellas y rutas se registran en el JSON derivado. El CGCA y CADIDO proporcionados son la base institucional identificada; sus propias notas requieren gestionar vigencia, actualización y equivalencias. No se presume que una descarga realizada en 2026 sea un instrumento expedido en 2026.

Se requiere ratificar con el área archivística competente la versión vigente y su acto de aprobación, la equivalencia del código de fondo, los eventos de cómputo, formatos de inventario y los actos necesarios para transferencias y disposición. Estas validaciones se dejan como requisitos de puesta en operación y no impiden desarrollar la especificación y la maqueta.

Referencia legal consultada el 29-10-2026: [Disposiciones Generales para el Archivo Contable Gubernamental, CONAC](https://sidof.segob.gob.mx/notas/docFuente/5710974). Los enlaces publicados en el XLS se conservan como procedencia; la revisión sustantiva de CGCA, CADIDO y PADA se efectuó sobre los archivos locales aportados.
