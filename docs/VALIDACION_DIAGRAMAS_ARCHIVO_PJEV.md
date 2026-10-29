# Validación y ajuste de los diagramas del analista

**Revisión:** 29 de octubre de 2026.  
**Base de trabajo:** dos diagramas aportados por el usuario, previamente estudiados por el analista. Se conserva su estructura conceptual y se documentan los ajustes realizados para el piloto **DGA–2530–Contabilidad**. Esta revisión técnica no sustituye la aprobación o vigencia de los instrumentos archivísticos.

El primer diagrama explica cómo CGCA y CADIDO orientan los expedientes, inventarios y ciclo de vida. El segundo describe la relación del archivo físico con el expediente, sus documentos indexados y los metadatos. Son vistas complementarias del mismo sistema; sus cajas y flechas no se convierten automáticamente en tablas, requisitos normativos o permisos.

## 1. Ciclo archivístico

Se conservan CGCA y CADIDO como entradas, Expedientes e Inventarios como núcleo, las fases de Trámite y Concentración y la determinación del destino final.

| Elemento de la base | Validación y ajuste | Naturaleza |
|---|---|---|
| CGCA define «en qué carpeta va cada papel». | Precisar que clasifica el asunto por serie/subserie y versión. El contenedor y el anaquel se registran de forma independiente. | Precisión conceptual y propuesta de implementación. |
| Rangos 1–3 años y 5–10 años. | Mantener el concepto de plazos por fase; mostrar para el piloto los 2 años de trámite y 8 de concentración del CADIDO recibido, pp. 36–37. Otras series conservarán su regla aplicable. | Regla institucional documentada de referencia. |
| Flechas directas entre fases. | Hacer explícitas transferencia primaria, inventario, entrega y recepción; para el destino histórico, evaluación y transferencia secundaria conforme al procedimiento aplicable. | Proceso institucional previsto; detalle tecnológico propuesto. |
| Documento «de rutina» conduce a baja/destrucción. | La condición no basta para determinar disposición. La versión del piloto muestra destino histórico para las entradas 2530 revisadas. La eventual baja de otras series dependerá del instrumento, valoración, impedimentos y autorización aplicables. | Contraste institucional; sin automatizar destrucción. |
| Paso del tiempo como progresión del dibujo. | Añadir cierre, evento de inicio de cómputo y validaciones. El vencimiento no se deduce de escanear ni sumar diez años desde la carga. | Control de diseño y validación institucional pendiente del disparador. |

Versión ajustada: [Clasificación y ciclo archivístico 2530](../09_gestion_documental/diagramas/01-ciclo-archivistico-2530.svg). Base conservada: [primer diagrama del analista](referencias_diagramas_analista/01-original-ciclo.png).

## 2. Archivo físico, expediente, documentos y metadatos

Se conservan las cuatro ideas del analista: localización del soporte físico, expediente, índice de documentos y metadatos. Se mantienen los cinco tipos documentales como ejemplos de soportes, sujetos a la plantilla del procedimiento.

| Elemento de la base | Validación y ajuste | Naturaleza |
|---|---|---|
| Archivero de 2 × 4 gavetas y Anaquel A-02. | Son ejemplos de muebles distintos. El catálogo admite archivero/anaquel y niveles/gavetas/posiciones según el tipo de mueble, sin fijar ocho gavetas para toda ubicación. | Propuesta tecnológica configurable. |
| Ubicación y recopilador en una misma caja del diagrama. | Distinguir ubicación física de contenedor identificado. El recopilador se modela como unidad física o agrupación validada, no como serie archivística. | Precisión conceptual y regla de modelado. |
| «Expediente / carpeta». | Separar identidad lógica del expediente de carpeta/tomo físico. El expediente puede abarcar varias unidades físicas; uno nacido electrónico puede carecer de soporte físico. Conservar un folio estable de ejemplo sin hacerlo depender del anaquel. | Propuesta tecnológica; continuidad de identidad. |
| Póliza PD-001058. | Conservar el ejemplo de referencia financiera sin imponer PD como código del CGCA ni homologarlo automáticamente. El vínculo usa sistema, ejercicio, tipo, folio e ID confirmado. | Dato de ejemplo del analista; homologación por validar. |
| CFDI «XML + PDF timbrado». | Distinguir XML fiscal y representación PDF como objetos relacionados con procedencia. UUID y FechaTimbrado se toman del XML cuando corresponda, conservando datos y validación. | Precisión técnica apoyada en el esquema del SAT. |
| Cédulas de proveedor, empleados y obra. | Mantenerlas como soportes vinculados cuando el procedimiento los requiera. Conservar productor, fecha de referencia y versión; consultarlas desde Contabilidad no otorga administración de los catálogos de origen. | Regla de alcance del piloto y propuesta tecnológica. |
| Todos los campos bajo «Metadatos obligatorios». | Separar metadatos comunes de control, específicos por tipo y técnicos de cada archivo. No exigir UUID fiscal, RFC de proveedor o fecha de timbrado a una conciliación o un oficio. | Propuesta de validación por plantilla. |
| Fecha de emisión / timbrado. | Mantener fechas distintas: documental/emisión, timbrado cuando aplique, incorporación y escaneo. Un dato ausente o no aplicable no se rellena con una fecha inventada. | Regla de integridad de datos propuesta. |
| Palabras clave y descripción. | Mantenerlas como herramientas de consulta con controles de acceso; su obligatoriedad se define por plantilla. El OCR no modifica el original ni sus metadatos sin revisión. | Propuesta tecnológica. |

Versión ajustada: [Expediente, documentos y metadatos](../09_gestion_documental/diagramas/02-expediente-documentos-metadatos.svg). Base conservada: [segundo diagrama del analista](referencias_diagramas_analista/02-original-expediente-metadatos.png).

## 3. Diccionario inicial de aplicabilidad

| Nivel | Datos propuestos | Criterio de validación |
|---|---|---|
| Expediente | ID y folio, asunto, unidad productora, serie/subserie y versión, regla de disposición, fechas documentadas, índice, clasificación real de acceso. | Mantener los datos archivísticos separados de la referencia de una operación financiera y de la ubicación. Registrar faltantes y excepciones justificadas. |
| Documento | ID, expediente, título, tipo, fecha documental cuando exista, soporte, emisor/receptor según tipo, orden y procedencia. | Aplicar plantilla por tipo y procedimiento. El título no constituye identidad única. |
| Archivo digital | Objeto, versión, MIME, tamaño, hash, origen, relación con original/derivado y bitácora. | Integridad y trazabilidad por objeto; no equiparar XML y PDF como un solo binario. |
| CFDI con timbre | UUID fiscal, RFC emisor/receptor y fechas de emisión/timbrado extraídas cuando correspondan, versión XML y resultado de validación. | UUID fiscal no sustituye al ID interno. La longitud de 36 caracteres es un dato del esquema del Timbre Fiscal Digital, no una obligación para todos los documentos. |
| Póliza | Institución/sistema, ejercicio, tipo, número/folio e ID de origen confirmado. | Resolver homónimos por referencia compuesta. La clase de operación financiera no es un estado de digitalización. |
| Cédula de proveedor | Identificación del tercero, tipo de soporte, fecha/corte y versión archivada de sus documentos. | Mantener evidencia histórica; una actualización del padrón no reescribe la cédula incorporada. La opinión 32-D no se impone a todo expediente desde este dibujo. |
| Empleados / obra | Periodo/lote de dispersión o contrato/estimación, área productora y documentos soporte que correspondan. | Aplicabilidad por trámite y permisos. El piloto no habilita la producción de nómina ni la gestión operativa de obra. |

Los campos exactos y su obligatoriedad se validarán por procedimiento antes de implementar formularios. No se transforma la etiqueta gráfica «obligatorio» en una exigencia normativa sin fundamento.

## 4. Alcance de la revisión y continuidad

Las dos versiones SVG son editables y se incorporan al manual como ajustes sobre la base del analista. Los PNG recibidos se conservan como fuente de contraste. Se mantienen las ocho opciones CA-01 a CA-08, la referencia institucional 2530 y la separación entre requisitos normativos, reglas institucionales y propuestas tecnológicas.

Fuentes de contraste: CGCA recibido, pp. 31–32; CADIDO recibido, pp. 36–37; [recalibración institucional](RECALIBRACION_ARCHIVISTICA_DGA_PJEV.md). Precisión técnica del CFDI: [Timbre Fiscal Digital, SAT](https://www.gob.mx/sat/acciones-y-programas/timbre-fiscal-digital) y [esquema publicado por SAT](https://wwwmat.sat.gob.mx/cs/Satellite?blobcol=urldata&blobkey=id&blobtable=MungoBlobs&blobwhere=1461176205015&ssbinary=true), consulta 29-10-2026.
