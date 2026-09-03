# Benchmark y Modelo de Referencia: DocuWare aplicado al SIAF-PJEV
## Arquitectura de Gestión Documental y Archivo de Trámite Digital

**Entidad:** Poder Judicial del Estado de Veracruz (PJEV)  
**Proyecto:** Sistema Integral de Administración y Finanzas (SIAF-PJEV)  
**Referente de Industria:** DocuWare (DMS / Enterprise Content Management)  
**Marco Normativo de Cumplimiento:** Ley General de Archivos (LGA), NOM-151-SCFI-2016, Lineamientos AGN, LGCG/CONAC, LGTAIP/IVAI  
**Fecha de Publicación:** Septiembre de 2026

---

## 1. Justificación del Modelo de Referencia (DocuWare)

**DocuWare** es el estándar de oro a nivel global en sistemas de gestión documental empresarial (*Enterprise Content Management - ECM*), automatización de cuentas por pagar (*Processing Incoming Invoices*) y preservación segura de documentos.

Tomar a DocuWare como **ejemplo a seguir** permite dotar al SIAF-PJEV de una experiencia de usuario madura, intuitiva y sumamente potente, elevando el módulo transversal de archivos más allá de un simple "subidor de ficheros" para convertirlo en una **plataforma integral de gestión de expedientes digitales, sellado, flujos de trabajo e indexación inteligente**.

---

## 2. Mapeo Conceptual: DocuWare vs. SIAF-PJEV

A continuación se detalla la traducción de los conceptos nucleares de DocuWare a la arquitectura canónica de base de datos, backend y frontend del SIAF-PJEV:

```text
┌───────────────────────────────────────┐         ┌──────────────────────────────────────────────┐
│        CONCEPTO EN DOCUWARE           │         │         IMPLEMENTACIÓN EN SIAF-PJEV          │
├───────────────────────────────────────┤         ├──────────────────────────────────────────────┤
│ 1. Document Trays (Bandejas)          │ ──────► │ Buzón de Entrada y Documentos Temporales     │
│ 2. File Cabinets (Archivadores)       │ ──────► │ Repositorio Institucional (CGCA + CADIDO)    │
│ 3. Index Fields (Campos de Índice)    │ ──────► │ Metadatos Archivísticos, Fiscales y Contables│
│ 4. Intelligent Indexing / Autoindex   │ ──────► │ Lector CFDI 4.0 XML y Auto-indexación ERP    │
│ 5. Digital Stamps (Sellos Digitales)  │ ──────► │ Sellos Administrativos con Firma y Auditoría │
│ 6. Document Stapling (Grapado/Unión)  │ ──────► │ Agrupación de Paquetes (XML + PDF + Anexos)  │
│ 7. Task Lists (Listas de Tareas)      │ ──────► │ Bandejas de Trabajo por Rol y Faltantes      │
│ 8. Workflow Manager (Gestor Flujos)   │ ──────► │ Ciclo de Revisión, Aprobación y Suplencias   │
│ 9. Universal Viewer (Visor y Redact)  │ ──────► │ Visor Web Seguro y Testado para Transparencia│
│ 10. Smart Connect                     │ ──────► │ Componente Reutilizable <EntityFiles />      │
└───────────────────────────────────────┘         └──────────────────────────────────────────────┘
```

---

## 3. Detalle de Componentes Adaptados

### 3.1 Document Trays (Bandeja de Entrada y Archivos Temporales)
* **DocuWare:** Espacio de trabajo personal donde aterrizan los documentos escaneados, arrastrados o importados antes de ser archivados formalmente. Permite rotar páginas, ordenarlas, desglosarlas o graparlas.
* **En SIAF-PJEV (`<DocumentTray />`):**
  * Zona interactiva de pre-carga donde el usuario sube sus comprobantes mientras llena un trámite o expediente.
  * Los documentos residen transitoriamente con `es_temporal = TRUE` asociados a un `ticket_temporal`.
  * **Función de Grapado (*Stapling*):** Permite vincular automáticamente un archivo XML del SAT con su representación impresa PDF, tratándolos como un binomio indisoluble de comprobación fiscal.
  * **Acción de Archivar:** Al guardar el formulario de negocio (ej. Afectación de Gasto, Registro de Ingreso), los documentos pasan de la bandeja temporal al archivador formal con un solo clic transaccional.

### 3.2 File Cabinets (Archivadores Digitales Seguros)
* **DocuWare:** Repositorio central estructurado con permisos granulares por perfil y grupos de usuarios sincronizados con Active Directory.
* **En SIAF-PJEV (`archivos.documento` + CGCA / CADIDO):**
  * La estructura del archivador responde estrictamente al **Cuadro General de Clasificación Archivística (CGCA)** de la Ley General de Archivos:
    * *Fondo:* Poder Judicial del Estado de Veracruz.
    * *Sección:* Recursos Financieros / Recursos Materiales / Recursos Humanos.
    * *Serie / Subserie:* Pólizas de Egresos, Afectaciones Presupuestales, Facturas, Contratos.
  * Los plazos de guarda en **Archivo de Trámite** y **Archivo de Concentración** se gobiernan automáticamente mediante el Catálogo de Disposición Documental (CADIDO).

### 3.3 Intelligent Indexing y Autoindex (Extracción Automática sin Recaptura)
* **DocuWare:** Reconoce automáticamente campos clave (emisor, fecha, total, número de factura) y los asocia a los campos de índice; cruza datos con bases de datos SQL externas vía ODBC/Autoindex.
* **En SIAF-PJEV:**
  1. **Parser CFDI 4.0 Nativo:** Al cargar un comprobante fiscal digital, el sistema extrae en milisegundos:
     * Folio Fiscal (UUID SAT).
     * RFC y Razón Social del Emisor (Proveedor).
     * Fecha de Timbrado.
     * Importe Subtotal, IVA, Retenciones (ISR/IVA) y Total.
     * Uso de CFDI y Método de Pago.
  2. **Auto-Indexación Presupuestal / Contable:** Al asociar el documento al trámite de gasto o ingreso, el backend hereda e indexa automáticamente:
     * Centro Gestor y Unidad Responsable.
     * Clave Presupuestal y Objeto del Gasto (COG).
     * Cuenta Contable de Pasivo / Activo.
     * Ejercicio Fiscal y Mes Contable.
  * **Beneficio:** Cero errores de transcripción y cotejo instantáneo contra el Padrón de Proveedores.

### 3.4 Digital Stamps (Sellos Digitales de Trámite y Auditoría)
* **DocuWare:** Sellos visuales ("APPROVED", "REJECTED", "PAID") aplicados directamente sobre el documento en el visor. Al estampar, el sistema puede solicitar notas o campos obligatorios, actualiza los índices y detona el siguiente paso del flujo.
* **En SIAF-PJEV (`archivos.documento_sello`):**
  * Se implementa una paleta de **Sellos Oficiales Institucionales**:
    * 🟩 **REVISIÓN CONFORME:** Aplicado por el analista de Cuentas por Pagar tras verificar la documentación soporte.
    * 🟦 **AUTORIZADO PARA PAGO:** Aplicado por el Director General de Administración o titular facultado.
    * 🟨 **PAGADO / DISPERSADO:** Estampado por Tesorería junto con la clave de rastreo SPEI o número de cheque.
    * 🟪 **CONTABILIZADO:** Estampado por Contabilidad al emitir la póliza en firme (con número de póliza y fecha).
    * 🟥 **OBSERVADO / RECHAZADO:** Devuelve el expediente al usuario de origen indicando el motivo de rechazo.
    * 🏛️ **COTEJADO CON EL ORIGINAL:** Sello para documentos digitalizados conforme a la NOM-151-SCFI-2016.
  * **Efectos del Sello:**
    * Imprime un distintivo visual estilizado en el visor web.
    * Registra en la bitácora inmutable (`archivos.documento_bitacora`): Usuario, IP, Certificado/e.firma, Sello Digital de Tiempo (*Timestamping* ISO/IEC 18014).
    * Actualiza el estado del trámite en la base de datos PostgreSQL.

### 3.5 Universal Viewer y Herramienta de Testado (Transparencia / IVAI)
* **DocuWare:** Visor web interactivo sin necesidad de plugins locales, con miniaturas, herramientas de medición, rotación, zoom y marcas de agua.
* **En SIAF-PJEV (`<FileViewer />`):**
  * Visor en línea que renderiza PDFs, XML estructurado formateado visualmente, imágenes y hojas de cálculo.
  * **Módulo de Testado de Datos Personales (Generador de Versiones Públicas):**
    * Inspirado en la herramienta de *Redaction* de DocuWare y en estricto cumplimiento de los Lineamientos del SNT y el IVAI.
    * Permite al personal de la Unidad de Transparencia dibujar rectángulos negros sobre datos sensibles (firmas autógrafas de particulares, cuentas bancarias personales, RFC de personas físicas, domicilios).
    * Genera un nuevo documento derivado catalogado como **Versión Pública**, resguardando de forma inalterable e inviolable el documento matriz original.

### 3.6 Task Lists (Listas de Tareas por Rol)
* **DocuWare:** Consultas predefinidas mostradas como pestañas en la bandeja del usuario (ej. "Mis facturas pendientes de revisar", "Facturas mayores a $50,000 esperando firma").
* **En SIAF-PJEV:**
  * Bandejas dinámicas en el dashboard del usuario:
    * *Bandeja de Afectaciones Incompletas:* Trámites que no pueden avanzar por faltar documentos obligatorios del catálogo `05.1.1`.
    * *Bandeja de Validación Fiscal:* Documentos XML pendientes de validar estatus en el Web Service del SAT.
    * *Bandeja de Transferencias Documentales:* Expedientes que han cumplido su vigencia activa en Archivo de Trámite y deben remitirse al Archivo de Concentración.

### 3.7 Workflow Manager y Reglas de Suplencia (Out-of-Office)
* **DocuWare:** Motor gráfico de procesos con delegación por ausencia (*Substitution Rules*).
* **En SIAF-PJEV:**
  * Motor de flujo de autorizaciones documentales alineado a la Ley Orgánica del Poder Judicial del Estado de Veracruz:
    * Cuando un Magistrado Presidente, Director de Administración o Jefe de Departamento activa su estado de ausencia / comisión oficial, sus tareas documentales de aprobación y sellado se reasignan automáticamente al **Encargado de Despacho** legalmente habilitado, dejando constancia en la bitácora de auditoría.

---

## 4. Flujo Modelo de Referencia: "Procesamiento de Facturas y Comprobaciones"

Inspirado en el caso de estudio de DocuWare (*Incoming Invoices Processing*):

```text
  [ 1. CAPTACIÓN EN BANDEJA ]
  El proveedor o el área administrativa sube factura (XML + PDF).
  El sistema grapa ambos archivos automáticamente.
                 │
                 ▼
  [ 2. INDEXACIÓN INTELIGENTE ]
  El parser XML extrae Folio, RFC, Total y Conceptos.
  El sistema valida vigencia ante el SAT y coteja en Padrón de Proveedores.
                 │
                 ▼
  [ 3. ASOCIACIÓN AL TRÁMITE SIAF ]
  El analista de CxP enlaza el comprobante a la Afectación de Gasto.
  El sistema hereda automáticamente Centro Gestor, Partida COG y Ejercicio.
                 │
                 ▼
  [ 4. REVISIÓN Y SELLADO DIGITAL ]
  El analista aplica sello digital "REVISIÓN CONFORME".
  El sistema valida checklist documental (Contrato, Remisión de Almacén, etc.).
                 │
                 ▼
  [ 5. AUTORIZACIÓN PRESUPUESTAL ]
  El Director aprueba y estampa sello "AUTORIZADO PARA PAGO".
  Se genera la Orden de Pago en firme.
                 │
                 ▼
  [ 6. DISPERSIÓN BANCARIA ]
  Tesorería dispersa el recurso vía SPEI y estampa sello "PAGADO".
                 │
                 ▼
  [ 7. ARCHIVO DE TRÁMITE E INMUTABILIDAD ]
  El expediente queda congelado (WORM lógico).
  Se calcula Hash SHA-256 definitivo y se programa vigencia de 5 años según CADIDO.
```

---

## 5. Próximos Pasos para Cristian, Eunice y Daryl

1. **Frontend (`@/components/files/`):**
   * Adoptar el componente `<EntityFiles />` enriquecido con la metáfora de **Bandeja de Carga**, **Grapado XML+PDF** y **Ficha de Sellos Digitales**.
2. **Backend (NestJS + Prisma):**
   * Incorporar el servicio extractor de XML CFDI 4.0 para alimentar los metadatos de `archivos.documento`.
   * Habilitar el endpoint para la aplicación de sellos digitales auditados (`/api/v1/archivos/:id/estampar`).
3. **Base de Datos (PostgreSQL):**
   * Aplicar el DDL canónico `archivos_schema.sql` y los Stored Procedures `archivos_stored_procedures.sql`.
