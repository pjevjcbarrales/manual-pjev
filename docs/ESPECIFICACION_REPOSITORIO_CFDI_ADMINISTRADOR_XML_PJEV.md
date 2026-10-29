# Especificación Funcional y Técnica: 07 · Repositorio CFDI y Administrador de XML (SIAF-PJEV)

**Fecha de actualización:** 29 de octubre de 2026  
**Sistema:** `07 · Repositorio CFDI` (Administrador Institucional de XML y Servicios SAT)  
**Responsable técnico asignado en tablero:** Cristian  
**Estado de implementación:** Especificación funcional y técnica completa (Fase 2 / Segunda etapa); pendiente de desarrollo e integración con servicios web del SAT.  
**Módulos que comprende:**
- [`07.1.1` Bóveda CFDI, Almacén y Descarga SAT (Administrador de XML)](../07_repositorio_cfdi/07.1.1-boveda-cfdi.html)
- [`07.2.1` Validación y Vinculación Fiscal (SAT, EFOS 69-B, Buzón y Expedientes)](../07_repositorio_cfdi/07.2.1-validacion-vinculacion-fiscal.html)
- [`07.3.1` Control y Auditoría CFDI (Conciliación Metadata, Sabana Excel y DIOT)](../07_repositorio_cfdi/07.3.1-control-auditoria-cfdi.html)

---

## 1. Propósito y Distinción Expresa de Fuentes (Regla de Contraste Normativo)

El sistema **07 · Repositorio CFDI (Administrador de XML)** constituye el concentrador fiscal único del SIAF-PJEV para la descarga automatizada de comprobantes y metadata desde el Servicio de Administración Tributaria (SAT), la ingesta manual, el almacenamiento inmutable en bóveda, la relación automática de UUIDs, la validación masiva de vigencia, el monitoreo de listas negras (EFOS Art. 69-B CFF), la conversión de Metadata `.txt` y la vinculación transversal sin duplicidad con Presupuesto, Recursos Materiales, Cuentas por Pagar, Tesorería/Pagos, Ingresos, Contabilidad y Archivo.

En cumplimiento estricto de las reglas de arquitectura del entorno SIAF-PJEV (`AGENTS.md`), se distingue expresamente el origen de cada determinación de diseño:

| Naturaleza | Fuente de Referencia | Alcance e Impacto en el Diseño del SIAF-PJEV |
| :--- | :--- | :--- |
| **Requisito Normativo** | **Código Fiscal de la Federación (CFF)** Arts. 29, 29-A, 30, 32-D y 69-B; **Anexo 20 de la RMF** (CFDI 4.0, Complemento de Recepción de Pagos 2.0, Nómina 1.2, Retenciones 2.0 y los 29 complementos vigentes del SAT); **Lineamientos Técnicos del Web Service de Descarga Masiva de CFDI y Retenciones del SAT (v1.5)**; **LGCG** Arts. 4, fracc. XIV–XVII, 42 y 43; **Acuerdos CONAC** (Momentos Contables de los Egresos e Ingresos y Disposiciones para el Archivo Contable Gubernamental). | Obligación de conservar el archivo electrónico `.xml` como único soporte fiscalmente válido; verificar su autenticidad, vigencia ante el SAT y que el RFC emisor no se encuentre publicado en los listados del Art. 69-B del CFF (EFOS); verificar el cumplimiento fiscal (Art. 32-D); gestionar la aceptación o rechazo de solicitudes de cancelación en el Buzón Tributario (Art. 29-A); y vincular el `UUID` a las pólizas contables. **Regla CONAC obligatoria:** la descarga o carga de un CFDI en la bóveda **no genera por sí sola el momento contable del Devengado**, el cual exige la recepción conforme del bien, servicio u obra o el reconocimiento jurídico de la obligación. |
| **Regla Institucional PJEV** | **Manual Específico de Procedimientos de la Subdirección de Recursos Financieros** (Feb 2023: *Recepción y revisión de gastos*, pág. 124; *Pago a contratistas de obra*, pág. 155; *Comprobación de viáticos*, pág. 159; *Integración de documentación soporte*, pág. 186) y **Manual Específico de Procedimientos de la Subdirección de Recursos Materiales** (Feb 2023: *Adquisiciones*, *Almacén* y *Control de Inventarios*). | Todo trámite de afectación presupuestal y pago exige integrar la factura (XML y representación impresa PDF) validada, cotejada contra el pedido, contrato, entrada de almacén, resguardo patrimonial o estimación de obra, y vinculada al expediente único sin permitir que un mismo comprobante ampare dos pagos distintos. |
| **Propuesta Tecnológica y Referente Funcional Externo** | **Referente visual y operativo proporcionado por el usuario:** Tutorial y 9 capturas de pantalla de la plataforma **Onefacture v4.0.9** (`https://www.youtube.com/watch?v=Vl4qRXLMxmM`), conservadas en [`07_repositorio_cfdi/referencias/`](../07_repositorio_cfdi/referencias/) (`01-descarga-fechas.png` a `09-alcance-funcional-modulos.png`). | Se adopta como **referencia de experiencia de usuario (UX) y arquitectura de descarga/almacén** la separación en tres pestañas (**1. Fechas**, **2. Retenciones**, **3. Folio Fiscal UUID**), el contraste entre **Descarga Directa (límite de 2,000 XMLs)** y **SAT Web Service con FIEL (hasta 200,000 XMLs o 1,000,000 de registros de Metadata)**, el panel de **Almacén CFDI** con sus acciones de **Relacionar UUIDs**, **Exportar a Excel**, **Verificar estatus (cambios de vigente a cancelado)** y **Consultar**, así como las **Herramientas Plus** (Lector XML local, Conversor de Metadata `.txt`, Pre-armado DIOT, Solicitudes de Cancelación, Compatibilidad decimal, Buzón Tributario y Monitoreo EFOS 69-B). Este referente externo orienta el diseño de pantallas sin sustituir los procedimientos oficiales del PJEV ni las reglas de CONAC. |

---

## 2. Contraste Técnico con los Servicios Oficiales del SAT (`sat.gob.mx`)

El diseño del Administrador de XML del SIAF-PJEV se alinea con las especificaciones técnicas vigentes de los dos canales oficiales del Servicio de Administración Tributaria:

| Característica Técnica | Canal 1: Portal del SAT / Consulta Directa (Descarga Básica) | Canal 2: SAT Web Service de Descarga Masiva (SOAP v1.5) |
| :--- | :--- | :--- |
| **Autenticación soportada** | RFC + Contraseña (CIEC) o e.firma (FIEL), con resolución de reto captcha. | **Exclusivamente e.firma (FIEL) vigente** (`.cer`, `.key` y clave privada) para firma XML-DSig del token SOAP. |
| **Límite de volumen por consulta** | **Máximo 2,000 archivos XML por consulta/día** (con tope visual de 500 registros en portal). | **Hasta 200,000 CFDI (XML)** por petición, y **hasta 1,000,000 de registros** cuando se solicita **Metadata (`.txt`)**. |
| **Umbral recomendado de uso** | Consultas operativas diarias, por folio fiscal (`UUID`) o periodos acotados (< 2,000 XMLs). | Volúmenes mayores a **20,000 XMLs**, cierres mensuales/anuales de nómina timbrada o cuando existen **más de 500 CFDI en un mismo segundo**. |
| **Naturaleza del procesamiento** | **Síncrono / En línea:** descarga inmediata con contador en vivo de Vigentes (`V`) y Cancelados (`C`). | **Asíncrono en 3 etapas:** 1) `Solicitar` (genera `IdSolicitud`), 2) `Verificar` (consulta estatus cada 2 horas; el SAT tarda desde minutos hasta **72 horas / 3 días**), 3) `Descargar` paquetes `.zip` (disponibles por 72 horas con límite de 2 descargas por paquete). |
| **Tipos de entrega** | Archivos `.xml` individuales, representación `.pdf` y archivo `.txt` de Metadata. | Paquetes comprimidos `.zip` de archivos `.xml` (CFDI o Retenciones) y paquetes `.zip` de archivos `.txt` de **Metadata**. |

---

## 3. Catálogo de las 9 Pantallas de Referencia Incorporadas

Las capturas proporcionadas por el usuario se encuentran resguardadas en `sitio_web/07_repositorio_cfdi/referencias/` y documentan el flujo integral:

1. `01-descarga-fechas.png`: **Descarga de CFDIs — Pestaña 1 (`Fechas`)**, con banner preventivo del límite de 2,000 XMLs, filtros de Inicio, Fin, Complemento, RFC receptor opcional, Estatus, radio Emitidos/Recibidos y consola en vivo (`Tiempo: 00:11:15`, `Total vigentes (V)`, `Total cancelados (C)`).
2. `02-descarga-retenciones.png`: **Descarga de CFDIs — Pestaña 2 (`Retenciones`)**, especializada en CFDI de Retenciones e Información de Pagos.
3. `03-descarga-folio-fiscal-uuid.png`: **Descarga de CFDIs — Pestaña 3 (`Folio fiscal UUID`)**, con selector `Solo uno` o `Varios`, indicador `¿Son retenciones?` y radio Emitidos/Recibidos.
4. `04-resultado-almacen-cfdi.png`: **Confirmación de fin de descarga** (*"Se descargaron 13 de 13 CFDIs — Los XML se guardaron correctamente en almacén"*).
5. `05-sat-web-service-200k.png`: **Referencia de capacidad del módulo SAT Web Service** (recuperación de hasta 200,000 XML por consulta y ruta de almacenamiento).
6. `06-almacen-cfdi-relacionar-uuids.png`: **Consola de Almacén CFDI**, con banner superior **`[Relacionar UUIDs]`**, filtros por los **29 complementos del SAT**, casilla **`Solo Egresos`** y la tríada de acciones: **`[Exportar a excel]`**, **`[Verificar estatus]`** (detecta CFDIs que cambiaron de vigentes a cancelados) y **`[Consultar]`**.
7. `07-herramientas-xml-metadata-diot.png`: **Panel de Herramientas Plus**, que agrupa:
   - **`XMLs`**: Importador local de archivos XML para visualización y exportación a Excel o PDF.
   - **`Metadata`**: Conversor a Excel y conciliador de los archivos `.txt` de metadata descargados del SAT.
   - **`DIOT`**: Generador automático de la DIOT desde los CFDI sin captura manual proveedor por proveedor.
   - **`Solicitudes de cancelación`**: Gestión masiva de solicitudes de cancelación ante el SAT.
   - **`AntiCaptchas`**: Resolución automatizada de captchas del SAT en descargas, almacén y consultas.
   - **`Compatibilidad CFDI`**: Ajuste y validación de precisión decimal para sistemas contables.
   - **`Buzón Tributario`**: Consulta centralizada de avisos y notificaciones del SAT.
8. `08-sat-web-service-solicitudes.png`: **Consola de SAT Web Service**, con aviso de procesamiento de hasta 3 días para volúmenes mayores a 20,000 XMLs, selector de entidad configurada con FIEL, rango de fecha/hora, tipo Emitidos/Recibidos, checkbox `¿Son retenciones?`, botón **`[Solicitar CFDI y Metadata]`** y tabla de seguimiento de peticiones (`Solicitado`, `Tipo`, `Fechas de solicitud`, `Estatus`, `Acciones`).
9. `09-alcance-funcional-modulos.png`: **Matriz integral de capacidades**, incluyendo **Constancias y Opiniones del SAT (CSF, CIF, Opinión 32-D)**, **Monitoreo de EFOS (Cruce 69-B)** y **Multi-acciones**.

---

## 4. Arquitectura de Datos del Esquema `cfdi` (PostgreSQL)

El sistema `07 · Repositorio CFDI` persiste su información en el esquema lógico `cfdi`, manteniendo integridad referencial con `archivos.documento` (almacenamiento binario y hash `SHA-256`), `cfg` (entidad, proveedores, empleados), `cxp` (afectaciones de gasto, órdenes de pago, viáticos, retenciones, DIOT), `rm` (contratos, recepciones, entradas de almacén, activo fijo), `ing` (ingresos) y `contabilidad` (pólizas).

### Tablas Principales del Esquema `cfdi`

1. **`cfdi.boveda_comprobantes`**: Tabla maestra de comprobantes fiscales (1 registro único por `uuid`). Contiene los atributos de `cfdi:Comprobante`, `cfdi:Emisor`, `cfdi:Receptor` y `tfd:TimbreFiscalDigital`, código de complemento (entre los 29 del SAT), estatus SAT (`VIGENTE`, `CANCELADO`), fecha de última verificación de estatus, estatus EFOS 69-B y semáforo de disponibilidad para vinculación.
2. **`cfdi.boveda_comprobantes_conceptos`**: Desglose de partidas del XML (`cfdi:Concepto`), incluyendo `ClaveProdServ`, `NoIdentificacion`, `Cantidad`, `ClaveUnidad`, `Descripcion`, `ValorUnitario`, `Importe`, `Descuento` y `ObjetoImp`, más diferencia de precisión decimal detectada, para cruce con **CUCOP / COG**, entradas de almacén y altas de activo fijo.
3. **`cfdi.boveda_comprobantes_impuestos`**: Desglose de impuestos trasladados y retenidos (`IVA`, `ISR`, `IEPS`, impuestos locales como 5 al millar) a nivel comprobante y concepto, utilizado para validar retenciones en `05.1.3` y armar automáticamente la **DIOT (`05.3.4`)**.
4. **`cfdi.boveda_comprobantes_relaciones`**: Grafo de relaciones generado por la acción **`[Relacionar UUIDs]`** y por la lectura de nodos `cfdi:CfdiRelacionados` (`TipoRelacion`: `01` Nota de crédito, `02` Nota de débito, `04` Sustitución de CFDI previos, `07` Aplicación de anticipo) y enlace entre facturas `PPD` y sus **Complementos de Recepción de Pagos (`TipoDeComprobante = 'P'`)**.
5. **`cfdi.peticiones_descarga_sat`**: Bitácora y cola de trabajo tanto de descargas básicas (Fechas, Retenciones, UUID) como de solicitudes asíncronas al **SAT Web Service** (`id_solicitud_sat`, modalidad `CFDI_XML` o `METADATA_TXT`, indicador `es_retencion`, rango fecha-hora, estatus SAT `ACEPTADA`/`EN_PROCESO`/`TERMINADA`/`RECHAZADA`, paquetes `.zip`, conteo de vigentes/cancelados y bitácora de ejecución).
6. **`cfdi.metadata_sat_registros`**: Almacén de registros importados desde archivos `.txt` de Metadata del SAT (hasta 1,000,000 de filas por petición), utilizado para conciliar contra `cfdi.boveda_comprobantes` y detectar XMLs faltantes o cambios de estatus a `Cancelado`.
7. **`cfdi.vinculos_expediente`**: Tabla puente polimórfica que asocia un CFDI (`cfdi_id` / `uuid`) con los actos administrativos y financieros del SIAF-PJEV (`RECEPCION_RM`, `ENTRADA_ALMACEN`, `ALTA_ACTIVO_FIJO`, `AFECTACION_GASTO`, `ORDEN_PAGO`, `COMPROBACION_VIATICOS`, `PAGO_TESORERIA`, `REGISTRO_INGRESO`, `POLIZA_CONTABLE`).
8. **`cfdi.padron_efos_69b`** y **`cfdi.solicitudes_cancelacion_buzon`**: Catálogo sincronizado con las listas del Art. 69-B del CFF (*Presunto*, *Desvirtuado*, *Definitivo*, *Sentencia Favorable*) y bandeja de control de solicitudes de cancelación recibidas en el Buzón Tributario.
