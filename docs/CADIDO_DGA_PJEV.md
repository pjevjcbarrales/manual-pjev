# Catálogo de Disposición Documental

**09.1.2 · Referencia institucional recalibrada el 29-10-2026.**  
**Piloto:** DGA2500 → 2530, Subdirección de Recursos Financieros, con foco en Contabilidad. Los parámetros del resto de la institución se definirán por sus instrumentos y versiones.

## 1. Regla de referencia recibida

El CADIDO denominado 2024, páginas 36–37, señala **2 años en Archivo de Trámite, 8 años en Archivo de Concentración y destino Archivo Histórico** para las cuatro series y doce subseries de 2530. La columna Baja no tiene marca en esas entradas. La nota de la página 39, de 09-04-2025, informa transición hacia clasificación funcional.

Esto corrige los ejemplos anteriores de 1/5 años, la baja predeterminada y el cierre calculado automáticamente. La selección de CADIDO no cierra el expediente ni autoriza su destrucción. Se preservan los valores publicados y se ratifica su aplicabilidad antes de la puesta en operación.

## 2. Entradas de referencia del piloto

<!-- TABLA_REFERENCIA -->

Las dos copias recibidas del CADIDO tienen el mismo SHA-256 y constituyen una única versión lógica. La suma de diez años describe las dos fases de referencia, sin ser una fecha automática de disposición desde la carga o el escaneo.

## 3. Modelo de datos propuesto

La regla de disposición referencia nodo y versión de instrumento. Conserva valores administrativo, legal, contable y fiscal por separado, las marcas originales de información Pública/Reservada/Confidencial, plazos por fase, destino, fuente/página, disparador de cómputo, validación y fundamento. No se usa un único valor fiscal/contable ni una combinación de valores por defecto universal.

Se distingue la marca fuente del acto real de clasificación de acceso. Para pólizas, el CADIDO marca Pública y Reservada simultáneamente; estas marcas no generan acceso público ni una reserva automática. El documento/expediente conserva la determinación y el permiso que corresponda al caso.

El expediente guarda cierre formal, fecha/evento de inicio del cómputo, regla/versiones aplicadas, suspensiones y referencias de transferencias. Si falta un dato validado para el cómputo, la fecha objetivo permanece pendiente, aunque se muestren 2/8 años como referencia.

## 4. Contratos técnicos propuestos

La lectura debe devolver la regla de la versión aplicable y su procedencia. Las operaciones de mantenimiento crean nueva versión o resolución autorizada, sin reescribir expedientes previos. El actor procede de la sesión; el backend comprueba ámbito, autoridad, coherencia de fuente y campos obligatorios. Retorno estándar propuesto: `{ "error": 0, "mensaje": "OK", "data": [] }`.

La evaluación de disposición es una consulta de elegibilidad con impedimentos y datos faltantes. Para 2530, el destino histórico de referencia bloquea la ruta de baja ordinaria por vencimiento y conduce a evaluar transferencia secundaria. No ejecuta traslado, destrucción ni borrado. Los SQL y endpoints del diseño anterior requieren adaptación al esquema versionado y no se presentan aquí como implementación vigente.

## 5. Reglas y aceptación

- No existen valores universales de 1 año de trámite, 5 de concentración o baja automática. Se exige una regla documentada por nodo/versión.
- El cierre y el evento de inicio del cómputo se registran conforme al procedimiento; no se derivan de la fecha de escaneo.
- La transferencia primaria y la secundaria conservan inventario, valoración/autorización aplicable y acuse de recepción. La autorización no cambia por sí sola custodia ni fase.
- Las excepciones patrimoniales, obligaciones, auditorías y procedimientos pendientes se verifican con su fundamento. Una norma general no reduce silenciosamente el plazo o destino del instrumento institucional.
- La cancelación lógica por error de captura no equivale a disposición documental ni destruye el soporte.
- Cumplir los plazos en una entrada 2530 no muestra una acción de baja por vencimiento. Una nueva versión conserva las reglas previamente aplicadas y sus equivalencias.

## 6. Fuentes y continuidad

Fuentes primarias: `C:\Users\jcbar\Downloads\CATALOGO__DE_DISPOSICION_DOCUMENTAL_2024.pdf`, páginas 36–37 y 39, y su copia idéntica «(1)». Se conservan rutas y huellas en la [referencia JSON](datos_archivisticos_dga_2530_2024.json). El PDF prevalece sobre cualquier transcripción.

Contraste normativo: [Disposiciones Generales para el Archivo Contable Gubernamental, CONAC](https://sidof.segob.gob.mx/notas/docFuente/5710974), con su régimen general y excepciones. La regla institucional del piloto no se reemplaza por un mínimo genérico.

Consultar la [recalibración y sus validaciones de puesta en operación](RECALIBRACION_ARCHIVISTICA_DGA_PJEV.md), el [CGCA](../09_gestion_documental/09.1.1-cgca.html) y [Control de Archivo](../09_gestion_documental/09.2.4-control-archivo.html).
