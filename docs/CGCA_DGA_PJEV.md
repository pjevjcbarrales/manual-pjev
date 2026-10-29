# Cuadro de Clasificación Archivística

**09.1.1 · Referencia institucional recalibrada el 29-10-2026.**  
**Alcance inicial:** DGA2500 → 2530, Subdirección de Recursos Financieros, con foco operativo en Contabilidad confirmado por el usuario. El modelo conserva estructura y configuración para otras unidades.

## 1. Fuente y jerarquía

El CGCA recibido, denominado 2024, publica en las páginas 31–32 la ruta `FOPJ01 → PLENOCJP → DGA2500 → 2530`, con cuatro series y doce subseries. La nota de la página 34, fechada 09-03-2025, informa una transición hacia clasificación funcional. Estos códigos sustituyen los ejemplos inventados `PJEV-DGA-RF-1S.*` del diseño anterior como referencia para este piloto.

La subsección archivística 2530 es distinta de la unidad orgánica operativa de Contabilidad y de su conjunto de permisos. El fondo aparece como `FOPJO1` en el CADIDO; se mantiene la diferencia de grafía y su conciliación pendiente, sin alterar el original. La confirmación del alcance por el usuario no equivale a aprobar una modificación de los instrumentos.

## 2. Entradas de referencia del piloto

<!-- TABLA_REFERENCIA -->

Las cuatro series son nodos; las doce subseries son sus subdivisiones publicadas. La serie 2530.4 no presenta subserie en el bloque recibido. «Tramitada» y «Liquidada» son nombres archivísticos del instrumento: no ejecutan estados del pago ni equivalen a calidad del escaneo.

## 3. Modelo de datos propuesto

Separar fuente, instrumento, versión, nodo jerárquico y equivalencia. Cada nodo tendrá identificador estable, padre dentro de su versión, nivel, código y literal de fuente, procedencia/página y estado de validación. Subsección y Subserie son niveles opcionales según el instrumento. La unicidad se controla por versión y código; una revisión futura no reemplaza las claves aplicadas a expedientes históricos.

El expediente relaciona `clasificacion_nodo_id`, `instrumento_version_id`, unidad productora y ámbito operativo. El ID de un nodo no sustituye el folio del expediente, su marbete, su ubicación ni el tipo de póliza financiero. El catálogo admite ramas de otras áreas con activación posterior por permisos.

## 4. Contratos técnicos propuestos

Las funciones de lectura/crud del CGCA del diseño anterior requieren adaptación a nodos/versiones, actor autenticado y permisos por ámbito. La lectura debe filtrar por versión, nivel, padre y unidad. La escritura crea versiones o equivalencias con fundamento; no modifica el histórico aplicado. Retorno estándar propuesto: `{ "error": 0, "mensaje": "OK", "data": [] }`.

La API de catálogo entregará nodos con versión y procedencia; la asignación al expediente validará en servidor ámbito, vigencia aplicable y coherencia con CADIDO. El retiro de una versión de uso nuevo no elimina sus relaciones históricas. No se incluyen funciones ejecutables ni se afirma que estas rutas estén implementadas.

## 5. Reglas y aceptación

- Un expediente nuevo selecciona la versión aplicable y una serie/subserie coherente; los documentos heredan esa clasificación sin duplicar binarios.
- Reimportar cualquiera de las dos copias idénticas del CADIDO no duplica nodos ni versiones.
- Una reclasificación requiere motivo, responsable, equivalencia y evidencia; conserva el valor previo.
- El literal CADIDO `TRANFERENCIAS PRESUPUESTALES` de 2530.3d y el literal CGCA `TRANSFERENCIAS PRESUPUESTALES` se conservan por fuente.
- La vista general admite Fondo, Subfondo, Sección, Subsección, Serie y Subserie. La activación inicial en Contabilidad no habilita automáticamente Recursos Humanos, Materiales o TI.

## 6. Fuentes y continuidad

Fuente primaria local: `C:\Users\jcbar\Downloads\CUADRO_DE_CLASIFICACION_ARCHIVISTICA_2024.pdf`, páginas 31–32 y 34. Los valores y huellas se conservan en la [referencia JSON](datos_archivisticos_dga_2530_2024.json); el derivado no sustituye al PDF.

Consultar la [recalibración y sus pendientes de validación](RECALIBRACION_ARCHIVISTICA_DGA_PJEV.md), el [CADIDO](../09_gestion_documental/09.1.2-cadido.html) y [Control de Archivo](../09_gestion_documental/09.2.4-control-archivo.html). La cotización histórica del Congreso permanece como antecedente comercial.
