# Diagnóstico: Manejo Actual de Archivos y Documentos en SIAF-PJEV

**Fecha de emisión:** Septiembre de 2026  
**Documento:** `ANALISIS_MANEJO_ARCHIVOS_ACTUAL.md`  
**Objetivo:** Identificar el estado del arte sobre almacenamiento, referencias y requerimientos de archivos en la base de datos, módulos backend y frontend del SIAF-PJEV, catalogando cada hallazgo conforme a las directrices de migración técnica.

---

## 1. Resumen Ejecutivo del Diagnóstico

Tras la inspección profunda del esquema de base de datos (`schema_supabase_2026-05-26.sql`), los módulos funcionales (`01_cfg`, `02_presupuesto`, `03_contabilidad`, `04_ingresos`, `05_cuentas_por_pagar`, `07_recursos_materiales`) y la base de conocimiento (`knowledge_base.txt`, `chat_manual_dev_siaf.md`), se determinan las siguientes conclusiones críticas:

1. **Inexistencia de un esquema o tablas de archivos en PostgreSQL:**  
   Actualmente la base de datos contiene esquemas para `auditoria`, `config`, `contabilidad`, `cxc`, `cxp`, `nav`, `pbr`, `pm` y `presupuesto`. **No existe ninguna tabla centralizada ni esquema (`archivos` o `doc`)** que administre binarios, metadatos documentales, hashes SHA-256 o relaciones.
2. **Estrategia provisional desacoplada (Campos alfanuméricos de referencia):**  
   En los módulos de `04 · Ingresos` y `02 · Presupuesto`, ante la ausencia de un subsistema transversal de archivos, se adoptó como regla canónica provisional el uso de un campo simple `referencia_externa VARCHAR(100)` para anotar números de oficios o contratos sin permitir la subida de binarios.
3. **Catálogos de Requisitos Documentales Desconectados:**  
   En `05.1.1 Requisitos Documentales` y `07.1.6 Matriz de Checklist` existen catálogos analíticos que tipifican qué documentos son requeridos (ej. `DOC-CON-TRA`, `DOC-ENT-ALM`, `DOC-OFI-COM`), tamaño máximo permitido (`tamano_max_mb`) y obligatoriedad. Sin embargo, no cuentan con un servicio de almacenamiento ni API de vinculación real detrás.
4. **Mockups de interfaz visual (Wireframes) con controles de adjuntos aislados:**  
   En formularios como `05.2.1 Afectación del Gasto` y `07.2.1 Requerimientos de Adquisiciones` se diseñaron botones visuales (`+ Adjuntar Doc`) y tablas de adjuntos en SVG nativo, pero carecen de una biblioteca de componentes reusable (`<EntityFiles />`) en React/Next.js.

---

## 2. Inventario de Hallazgos y Clasificación Técnica

Conforme al estándar del plan de trabajo, cada implementación encontrada se clasifica en:
* `CANÓNICA`: Estándar formal vigente que debe adoptarse y respetarse.
* `REUTILIZABLE`: Componente o lógica que se aprovechará en el nuevo módulo transversal.
* `LEGACY`: Código o estructura antigua desarrollada de manera aislada.
* `DUPLICADA`: Implementación redundante que debe consolidarse.
* `A MIGRAR`: Componente que debe adaptarse al nuevo servicio transversal de archivos.
* `A ELIMINAR`: Código o tablas provisionales que se sustituyen definitivamente.

| Elemento Identificado | Ubicación / Archivo | Clasificación | Diagnóstico y Acción de Migración |
| :--- | :--- | :--- | :--- |
| **Esquema `archivos` en PostgreSQL** | Base de datos | **CANÓNICA** | Inexistente actualmente. Se creará como el nuevo estándar transversal para todo el SIAF-PJEV. |
| **Catálogo de Requisitos Documentales** | `05.1.1` (`cxp.requisito_documental`) | **REUTILIZABLE** | Excelente tipificación de tipos documentales (`DOC-*`), reglas de obligatoriedad y tamaños máximos. Se integrará como catálogo alimentador de `tipo_documento` en `archivos.documento_relacion`. |
| **Matriz de Checklist de Adquisiciones** | `07.1.6` (`rm.matriz_checklist`) | **REUTILIZABLE** | Lógica de matriz de requisitos según modalidad de compra (Licitación, Adjudicación Directa). Se consumirá por el componente `<EntityFiles />` para determinar documentos obligatorios. |
| **Campo `referencia_externa`** | `04.2.1` (`ingresos.ingreso_registro`), `02.2.4` (`presupuesto.ampliacion_reduccion`) | **A MIGRAR** | Actualmente almacena cadenas como `OFI-SEFIPLAN-2026-114` sin adjunto. Se mantendrá el campo para búsqueda rápida, pero se habilitará la relación polimórfica en `archivos.documento_relacion`. |
| **Validación `fn_validar_checklist_afectacion`** | `05.2.1` (`cxp.afectacion_gastos`) | **A MIGRAR** | Modificar el SP para que no consulte banderas booleanas locales sino que consulte `archivos.fn_leer_documento_relacion(p_filtros)` para certificar que todos los documentos marcados como `es_obligatorio = TRUE` estén cargados y validados. |
| **Botón y Tabla SVG "+ Adjuntar Doc"** | `05.2.1-afectacion-gastos.html`, `07.2.1-requerimientos-adquisiciones.html` | **A MIGRAR** | Sustituir las representaciones aisladas por el componente canónico frontend `<EntityFiles />`. |
| **Manejo de rutas directas en disco/URL local** | Scripts auxiliares legacy | **A ELIMINAR** | Prohibir expresamente almacenar URLs hardcodeadas en tablas de negocio. La persistencia física se abstrae mediante `IFileStorageDriver` con identificadores neutrales UUID. |
| **Subida directa sin validación de Magic Bytes** | Prácticas preliminares | **A ELIMINAR** | Se sustituye por el pipeline estricto de NestJS con validación binaria (`file-type`), rechazo de extensiones dobles y cálculo de hash SHA-256 en stream. |

---

## 3. Conclusión del Diagnóstico

El SIAF-PJEV se encuentra en un **punto óptimo de intervención arquitectónica**:  
Al no existir esquemas legacy de archivos fragmentados o viciados en la base de datos, es posible desplegar el **Subsistema Transversal de Gestión Documental y Archivos Digitales** de forma 100% canónica, limpia y homologada, cumpliendo desde el día cero con la **Ley General de Archivos (LGA)**, la **NOM-151-SCFI-2016** y los estándares de desarrollo del PJEV.
