# Módulo de Manejo de Archivos y Gestión Documental Digital (SIAF-PJEV)
## Plan de Trabajo y Marco Normativo Institucional

**Entidad:** Poder Judicial del Estado de Veracruz (PJEV)  
**Proyecto:** Sistema Integral de Administración y Finanzas (SIAF-PJEV)  
**Componente:** Subsistema Transversal de Gestión Documental y Archivos  
**Fecha:** Septiembre de 2026  
**Marco Legal y Normativo de Referencia:**
* **Ley General de Archivos (LGA)** (Publicada en DOF 15-06-2018; última reforma aplicable).
* **Ley de Archivos del Estado de Veracruz de Ignacio de la Llave**.
* **Norma Oficial Mexicana NOM-151-SCFI-2016** (Requisitos para la conservación de mensajes de datos y digitalización de documentos).
* **Lineamientos Técnicos del Archivo General de la Nación (AGN)** para la Creación y Uso de Sistemas Automatizados de Gestión Documental y Archivos Electrónicos.
* **Ley General de Contabilidad Gubernamental (LGCG)** y Criterios del **Consejo Nacional de Armonización Contable (CONAC)** sobre guarda y custodia de comprobación del gasto e ingreso público.
* **Código Fiscal de la Federación (CFF - Art. 30)** sobre plazos de conservación de contabilidad y documentación comprobatoria.
* **Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (LGPDPPSO)** y **Ley 316 del Estado de Veracruz**.
* **Ley General de Transparencia y Acceso a la Información Pública (LGTAIP)** y Criterios del SNT / IVAI para la emisión de Versiones Públicas Testadas.
* **Normas Internacionales Adoptadas:** ISO 15489-1 (Gestión de Documentos), ISO 23081 (Metadatos de Gestión Documental), ISO 14721 (OAIS - Preservación Digital) e ISO 19005 (Formato PDF/A).

---

## 1. Fundamentación Jurídica y Normativa Oficial

El Poder Judicial del Estado de Veracruz, en su calidad de Sujeto Obligado de acuerdo con la **Ley General de Archivos (LGA)** y la **Ley de Archivos del Estado de Veracruz**, no puede limitar la gestión de archivos a un mero repositorio físico o disco virtual (*file storage*) desvinculado. Cada documento incorporado o producido en el SIAF-PJEV forma parte del patrimonio documental del Poder Judicial y constituye el **Archivo de Trámite Digital**.

A continuación se detalla la correspondencia normativa obligatoria que rige el diseño del módulo:

### 1.1 Ley General de Archivos (LGA)
1. **Sistema Institucional de Archivos (Arts. 10 al 14):**
   * El SIAF-PJEV opera como el soporte tecnológico del **Archivo de Trámite** para las unidades operativas y administrativas (Presupuesto, Contabilidad, Tesorería, Cuentas por Pagar, Recursos Materiales, etc.).
   * Todo documento debe vincularse a un expediente y clasificarse conforme a los instrumentos de control archivístico:
     * **Cuadro General de Clasificación Archivística (CGCA):** Codificación jerárquica: Fondo (PJEV) → Subfondo → Sección → Serie → Subserie.
     * **Catálogo de Disposición Documental (CADIDO):** Asignación obligatoria de los valores documentales (Administrativo, Legal, Fiscal/Contable), plazos de retención en trámite y concentración, y destino final (Baja Documental o Transferencia Histórica).
     * **Inventarios Documentales:** Generación de inventarios generales por transferencia o baja conforme al formato estándar del AGN.
2. **Gestión Documental Electrónica y Preservación Digital (Título Cuarto, Arts. 43 al 50):**
   * **Art. 43 (SIGDA):** Los sujetos obligados deben desarrollar e implementar sistemas automatizados de gestión documental que permitan la administración de documentos de archivo a lo largo de su ciclo de vida.
   * **Art. 44 y 45 (Atributos Esenciales):** El sistema debe garantizar incondicionalmente cinco atributos:
     * **Autenticidad:** Certeza de que el documento es lo que afirma ser, producido por el autor o entidad facultada.
     * **Integridad:** Certeza de que el documento se encuentra completo e inalterado en su estructura y contenido.
     * **Fiabilidad:** Su contenido puede ser creído como una representación fidedigna de las transacciones o actos que atestigua.
     * **Disponibilidad:** Localizable, recuperable, presentable e interpretable en cualquier momento por usuarios autorizados.
     * **Trazabilidad:** Registro continuo de todas las acciones efectuadas sobre el documento desde su ingreso hasta su destino final.
   * **Art. 46 (Metadatos Obligatorios):** Todo documento electrónico debe contar con metadatos de identificación, contexto, estructura, relaciones, procedencia, derechos de acceso, eventos de gestión y firmas aplicadas.
   * **Art. 47 (Formatos Abiertos y No Propietarios):** Para evitar la obsolescencia técnica, los documentos definitivos deben almacenarse en formatos estandarizados independientes de software comercial (PDF/A, XML, CSV, PNG, TIFF).
   * **Art. 48 e Interoperabilidad:** Capacidad de compartir e intercambiar documentos y metadatos con otros sistemas jurisdiccionales y de fiscalización (ORFIS, SEFIPLAN, ASF).
   * **Art. 49 (Firma Electrónica y Sellado de Tiempo):** Validez probatoria de firmas electrónicas avanzadas (e.firma/FIEL) y sellado de tiempo para asegurar la inalterabilidad jurídica.

### 1.2 Norma Oficial Mexicana NOM-151-SCFI-2016
* Establece los requisitos que deben cumplirse para la **conservación de mensajes de datos y digitalización de documentos**:
  * **Digitalización con Valor Probatorio:** Los documentos físicos escaneados (ej. oficios recibidos en oficialía de partes, facturas históricas impresas) adquieren validez probatoria equivalente al original si se sujetan a un proceso de digitalización certificada.
  * **Constancia de Conservación de Mensajes de Datos:** Emisión de constancias de conservación otorgadas por un Prestador de Servicios de Certificación (PSC) acreditado por la Secretaría de Economía.
  * **Sello Digital de Tiempo (*Timestamp*):** Emisión de marcas de tiempo conforme a la norma ISO/IEC 18014.
  * **Resumen Criptográfico (Hash):** Generación obligatoria de firmas criptográficas basadas en algoritmos **SHA-256** o superior para garantizar que no exista manipulación posterior.

### 1.3 Plazos Fiscales, Contables y de Auditoría (LGCG, CONAC y CFF Art. 30)
* La documentación soporte de operaciones presupuestales, contables y financieras (pólizas, facturas CFDI 4.0 con XML/PDF, estados bancarios, transferencias, contratos, órdenes de compra y nóminas) tiene un plazo de conservación forzosa de:
  * **Mínimo 5 años:** Plazo general de extinción de facultades de comprobación fiscal.
  * **Hasta 10 años:** Para operaciones que trasciendan ejercicios, afectaciones de pasivos de largo plazo, juicios en trámite o auditorías iniciadas por el ORFIS o la Auditoría Superior de la Federación (ASF).
  * **Permanente / Histórica:** Aquella documentación fundacional, decretos de presupuesto aprobados, convenios marco o actas constitutivas que el CADIDO determine con valor secundario.

### 1.4 Transparencia y Protección de Datos Personales (LGTAIP, LGPDPPSO e IVAI)
* **Clasificación de Seguridad:**
  1. **Pública:** Documentos que deben ser accesibles en obligaciones de transparencia (ej. contratos públicos, padrón de proveedores).
  2. **Reservada:** Documentación cuya difusión pueda comprometer procedimientos jurisdiccionales en curso o estrategias legales del Poder Judicial (requiere acuerdo formal fundado y motivado del Comité de Transparencia por plazo delimitado).
  3. **Confidencial:** Datos personales sensibles (nóminas con datos médicos o deducciones personales, cuentas bancarias particulares, identificaciones oficiales de personas físicas).
* **Versiones Públicas:** Obligatoriedad de generar versiones públicas con testado de campos sensibles aprobadas por el Comité de Transparencia, conservando inalterada la versión matriz para uso judicial/administrativo interno.

---

## 2. Principio Arquitectónico del Módulo

La gestión de archivos en el SIAF-PJEV se estructura como un **servicio transversal desacoplado**, donde los módulos funcionales aportan el contexto institucional y la clasificación archivística, mientras que el subsistema de archivos resuelve la persistencia, seguridad, integridad, trazabilidad y ciclo de vida documental.

```text
       ┌────────────────────────────────────────────────────────┐
       │             MÓDULOS DE NEGOCIO SIAF-PJEV               │
       │ Presupuesto · Contabilidad · CxP · Tesorería · Ingresos│
       └──────────────────────────┬─────────────────────────────┘
                                  │ Provee contexto:
                                  │ { modulo, entidad, registroId, tipoDoc,
                                  │   cgca_serie, valor_doc, clasificacion }
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │     SUBSISTEMA TRANSVERSAL DE GESTIÓN DOCUMENTAL       │
       ├────────────────────────────────────────────────────────┤
       │ 1. Frontend Reutilizable: <EntityFiles />, <Upload />  │
       │ 2. API NestJS: FilesController, ValidationPipe, Auth   │
       │ 3. Storage Layer: Abstracción (Local, S3, MinIO, NAS)  │
       │ 4. Motor Criptográfico: SHA-256, Magic Bytes, NOM-151  │
       │ 5. Motor Archivístico: CGCA, CADIDO, Ciclo Vital (LGA) │
       │ 6. Motor de Seguridad: Matriz ACL, Transparencia, IVAI │
       │ 7. Auditoría Inmutable: Bitácora y Cadena de Custodia  │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
                  ┌───────────────────────────────┐
                  │      PostgreSQL (Esquema      │
                  │   archivos / SPs Canónicos)   │
                  └───────────────────────────────┘
```

---

## 3. Modelo de Datos Gubernamental y Archivístico (PostgreSQL)

El modelo se implementará bajo el esquema dedicado `archivos` con convenciones estrictas de auditoría (`usuario_c`, `fecha_c`, `usuario_m`, `fecha_m`) y soft-delete (`estatus_registro = 0/1`):

### 3.1 Tabla: `archivos.documento` (Entidad Maestra)
Almacena la ficha técnica, metadatos archivísticos e información física del binario:

| Campo | Tipo | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `uuid` | PK, Default `gen_random_uuid()` | Identificador único universal del documento. |
| `nombre_original` | `varchar(255)` | NOT NULL | Nombre original proporcionado en la carga. |
| `nombre_almacenamiento` | `varchar(500)` | NOT NULL, UNIQUE | Ruta física interna neutral (ej. `2026/09/uuid.pdf`). |
| `extension` | `varchar(10)` | NOT NULL | Extensión normalizada en minúsculas (`pdf`, `xml`, `xlsx`). |
| `mime_type` | `varchar(100)` | NOT NULL | Tipo MIME real verificado por firma de bytes (magic bytes). |
| `tamanio_bytes` | `bigint` | NOT NULL | Tamaño exacto en bytes. |
| `hash_sha256` | `char(64)` | NOT NULL | Resumen criptográfico SHA-256 para control de integridad y duplicados. |
| `ruta_storage` | `text` | NOT NULL | URI o clave de localización en el driver de almacenamiento. |
| `descripcion` | `text` | NULL | Breve síntesis o resumen descriptivo del documento. |
| **Metadatos Archivísticos (LGA / AGN)** | | | |
| `cgca_codigo` | `varchar(50)` | NULL | Clave del Cuadro General de Clasificación Archivística (ej. `PJEV-DGA-RF-02.01`). |
| `valor_documental` | `varchar(20)` | NOT NULL | `'ADMINISTRATIVO'`, `'LEGAL'`, `'FISCAL_CONTABLE'`, `'TECNICO'`. |
| `vigencia_tramite_anios`| `int` | NOT NULL DEFAULT 1 | Años de guarda en Archivo de Trámite (según CADIDO). |
| `vigencia_concentracion_anios`| `int` | NOT NULL DEFAULT 5 | Años de custodia en Archivo de Concentración. |
| `fecha_cierre_tramite`| `date` | NULL | Fecha en que concluye la vigencia activa en trámite. |
| `destino_final` | `varchar(25)` | NOT NULL DEFAULT `'BAJA_DOCUMENTAL'` | `'BAJA_DOCUMENTAL'` o `'TRANSFERENCIA_HISTORICA'`. |
| `estado_archivistico` | `varchar(20)` | NOT NULL DEFAULT `'TRAMITE'` | `'TRAMITE'`, `'CONCENTRACION'`, `'HISTORICO'`, `'BAJA'`. |
| **Seguridad y Transparencia (IVAI / LGPDPPSO)** | | | |
| `clasificacion_acceso` | `varchar(20)` | NOT NULL DEFAULT `'CONFIDENCIAL'` | `'PUBLICO'`, `'RESERVADO'`, `'CONFIDENCIAL'`. |
| `acuerdo_reserva_id` | `varchar(100)` | NULL | Folio del Acuerdo de Reserva emitido por el Comité de Transparencia. |
| `posee_version_publica`| `boolean` | NOT NULL DEFAULT FALSE | Indica si cuenta con versión con datos personales testados. |
| **Certificación Legal (NOM-151 / e.firma)** | | | |
| `es_digitalizado` | `boolean` | NOT NULL DEFAULT FALSE | `TRUE` si proviene de escaneo de soporte físico en papel. |
| `folio_constancia_nom151`| `varchar(150)` | NULL | Folio de la constancia de conservación emitida por PSC acreditado. |
| `posee_firma_electronica`| `boolean` | NOT NULL DEFAULT FALSE | Indicador de firma electrónica avanzada vinculada. |
| **Auditoría Estándar SIAF** | | | |
| `estatus_registro` | `smallint` | NOT NULL DEFAULT 1 | `1` = Activo, `0` = Inactivo / Baja lógica. |
| `usuario_c` | `varchar(50)` | NOT NULL | Usuario institucional que creó el registro. |
| `fecha_c` | `timestamp with time zone` | NOT NULL DEFAULT clock_timestamp() | Fecha y hora de creación. |
| `usuario_m` | `varchar(50)` | NULL | Último usuario que modificó metadatos. |
| `fecha_m` | `timestamp with time zone` | NULL | Fecha y hora de modificación. |

### 3.2 Tabla: `archivos.documento_relacion` (Asociación Polimórfica)
Gobernará la vinculación con cualquier entidad del SIAF sin crear tablas redundantes:

| Campo | Tipo | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `uuid` | PK | Clave única de la relación. |
| `documento_id` | `uuid` | FK -> `archivos.documento.id` | Documento vinculado. |
| `modulo_siaf` | `varchar(30)` | NOT NULL | Módulo funcional (`presupuesto`, `contabilidad`, `ingresos`, `cxp`, `tesoreria`). |
| `entidad_origen` | `varchar(60)` | NOT NULL | Nombre canónico de la tabla padre (ej. `afectacion_gasto`, `orden_pago`, `poliza_maestro`). |
| `registro_id` | `varchar(100)` | NOT NULL | ID del registro padre (soporta IDs enteros o UUIDs). |
| `tipo_documento` | `varchar(50)` | NOT NULL | Subtipo documental funcional (`OFICIO_SOLICITUD`, `CFDI_XML`, `CFDI_PDF`, `CONTRATO`, `POLIZA_CHEQUE`). |
| `descripcion` | `varchar(300)` | NULL | Observación contextual de la vinculación. |
| `es_obligatorio` | `boolean` | NOT NULL DEFAULT FALSE | Define si la relación es requisito indispensable para aprobar el trámite. |
| `orden` | `int` | NOT NULL DEFAULT 1 | Secuencia visual en los formularios. |
| `estatus_registro` | `smallint` | NOT NULL DEFAULT 1 | `1` = Relación activa, `0` = Desvinculado. |
| `usuario_c`, `fecha_c`, `usuario_m`, `fecha_m` | Estándar | | Auditoría del vínculo. |

### 3.3 Tabla: `archivos.documento_version` (Control de Versiones y Sustituciones)
| Campo | Tipo | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `uuid` | PK | Identificador de la versión. |
| `documento_id` | `uuid` | FK -> `archivos.documento.id` | Documento padre. |
| `numero_version` | `int` | NOT NULL | Versión secuencial (1, 2, 3...). |
| `hash_sha256` | `char(64)` | NOT NULL | Hash criptográfico del binario de esta versión. |
| `ruta_storage` | `text` | NOT NULL | Ubicación física del archivo en el storage. |
| `tamanio_bytes` | `bigint` | NOT NULL | Tamaño de esta versión. |
| `motivo_cambio` | `text` | NOT NULL | Justificación obligatoria del reemplazo o actualización. |
| `es_version_actual` | `boolean` | NOT NULL DEFAULT FALSE | Bandera de versión vigente. |
| `usuario_c`, `fecha_c` | Estándar | | Responsable de la carga de la versión. |

### 3.4 Tabla: `archivos.documento_bitacora` (Cadena de Custodia y Auditoría Inmutable)
Garantiza el cumplimiento estricto del principio de **Trazabilidad** exigido por el Art. 45 de la LGA:

| Campo | Tipo | Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `bigserial` | PK | Identificador incremental. |
| `documento_id` | `uuid` | FK -> `archivos.documento.id` | Documento auditado. |
| `evento` | `varchar(40)` | NOT NULL | `'CARGA'`, `'DESCARGA'`, `'VISUALIZACION'`, `'REEMPLAZO'`, `'VERSION'`, `'DESVINCULACION'`, `'BAJA_LOGICA'`, `'RESERVA'`. |
| `usuario` | `varchar(50)` | NOT NULL | Usuario ejecutor de la acción. |
| `ip_cliente` | `varchar(45)` | NULL | Dirección IP de origen. |
| `user_agent` | `text` | NULL | Navegador o cliente HTTP utilizado. |
| `detalles_json` | `jsonb` | NULL | Contexto adicional del evento (entidad vinculada, hash previo, motivo). |
| `fecha_evento` | `timestamp with time zone` | NOT NULL DEFAULT clock_timestamp() | Marca temporal inmutable. |

---

## 4. Ciclo de Vida Archivístico Automatizado (LGA / CADIDO)

El sistema administra de forma automática el tránsito documental por las tres edades del archivo:

```text
               [ GENERACIÓN / RADICACIÓN EN SIAF-PJEV ]
       (Factura XML/PDF, Oficio de Ministración, Contrato, Póliza)
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │                  ARCHIVO DE TRÁMITE                    │
       │  * Acceso continuo y operativo por las áreas.          │
       │  * Vigencia: 1 a 3 años según CADIDO.                  │
       │  * Modificaciones controladas vía versionamiento.      │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Cierre de ejercicio y término de trámite
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │               ARCHIVO DE CONCENTRACIÓN                 │
       │  * Guarda precautoria para auditorías (ORFIS / ASF).   │
       │  * Plazo obligatorio: 5 años (hasta 10 años contables).│
       │  * Estado de solo lectura inmutable (WORM lógico).     │
       │  * Integridad garantizada con Hash SHA-256 / NOM-151.  │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Dictamen del CADIDO y Comité de Archivos
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
   ┌───────────────────────────┐     ┌───────────────────────────┐
   │      BAJA DOCUMENTAL      │     │  TRANSFERENCIA HISTÓRICA  │
   │  * Aplica a documentos sin│     │  * Documentos con valor   │
   │    valores secundarios.   │     │    evidencial, testimonial│
   │  * Acta formal de baja    │     │    o histórico (PJEV).    │
   │    autorizada por el AGN/ │     │  * Custodia perpetua en   │
   │    Archivo General del Edo│     │    Archivo Histórico.     │
   │  * Destrucción física y   │     │  * Formato abierto PDF/A. │
   │    desactivación lógica.  │     │  * Acceso público general.│
   └───────────────────────────┘     └───────────────────────────┘
```

---

## 5. Servicio de Almacenamiento Criptográfico y Formatos

### 5.1 Capa de Abstracción de Storage (`FileStorageService`)
Para garantizar la soberanía tecnológica del PJEV y evitar el bloqueo por proveedor (*vendor lock-in*), el backend implementa una interfaz genérica:

```typescript
export interface IFileStorageDriver {
  upload(fileStream: NodeJS.ReadableStream, path: string, metadata: FileMetadata): Promise<UploadResult>;
  download(path: string): Promise<NodeJS.ReadableStream>;
  delete(path: string): Promise<boolean>;
  exists(path: string): Promise<boolean>;
  getSignedUrl(path: string, expiresInSeconds: number): Promise<string>;
}
```

Drivers soportados intercambiables mediante variables de entorno:
1. `LocalFileSystemDriver`: Almacenamiento directo en volúmenes locales o montajes NAS del PJEV.
2. `MinioStorageDriver`: Almacenamiento de objetos S3 compatible auto-hospedado en la infraestructura del Poder Judicial.
3. `S3StorageDriver` / `SupabaseStorageDriver`: Para nubes autorizadas si así lo requiere la alta dirección.

### 5.2 Estructura Jerárquica Física
El almacenamiento físico se estructura temporalmente y por módulo:
```text
storage/
  └── siaf/
      └── {modulo}/           (ej. cxp, presupuesto, ingresos)
          └── {ejercicio}/    (ej. 2026)
              └── {mes}/      (ej. 09)
                  └── {uuid}.{ext}
```
* **Nunca** se almacena físicamente con el nombre original provisto por el usuario para prevenir colisiones, caracteres ilegales y vulnerabilidades de *Path Traversal*.

### 5.3 Validación Binaria (Magic Bytes) y Sanitización
* No se confía en la extensión ni en el `Content-Type` enviado por el navegador.
* Se inspeccionan los **Magic Bytes** de la cabecera binaria mediante librerías especializadas (`file-type`).
* Formatos oficialmente permitidos:
  * **Documentos:** `PDF` (PDF/A ISO-19005 preferente).
  * **Datos y Comprobantes Fiscales:** `XML` (validación de esquema XSD de CFDI 4.0).
  * **Hojas auxiliares:** `XLSX`, `CSV`.
  * **Imágenes probatorias:** `PNG`, `JPEG`, `TIFF`.
* **Bloqueo Total:** Archivos ejecutables o que admitan scripts (`.exe`, `.bat`, `.cmd`, `.sh`, `.vbs`, `.js`, `.py`, `.php`, `.html`, macros `.xlsm` sin certificado digital).

---

## 6. Arquitectura Backend (NestJS + Stored Procedures PostgreSQL)

Siguiendo la regla canónica del SIAF-PJEV: **las reglas de negocio pesadas y auditorías viven en PostgreSQL, expuestas vía Stored Procedures con retorno JSONB**, mientras que NestJS gestiona el streaming, la autenticación y los contratos REST.

### 6.1 Stored Procedures de Base de Datos
* `archivos.fn_leer_documento(p_filtros jsonb)`:
  * Permite consultar y filtrar por UUID, módulo, entidad, registro, CGCA, vigencia, clasificación y estatus.
* `archivos.fn_crud_documento(p_operacion varchar, p_datos jsonb)`:
  * Maneja operaciones: `'INSERT'`, `'UPDATE'`, `'VERSIONAR'`, `'DESACTIVAR'`.
  * Verifica hash SHA-256 para evitar duplicados accidentales o intencionales.
  * Registra automáticamente en la bitácora inmutable.
* `archivos.fn_crud_documento_relacion(p_operacion varchar, p_datos jsonb)`:
  * Gestiona las asociaciones polimórficas entre el documento y los trámites de negocio.
* `archivos.fn_registrar_evento_bitacora(p_evento varchar, p_documento_id uuid, p_usuario varchar, p_ip varchar, p_detalles jsonb)`:
  * Inserción protegida de auditoría documental.

### 6.2 Endpoints REST Canónicos (NestJS Controller)

| Método | Endpoint | Decoradores | Propósito |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/archivos/subir` | `@UseInterceptors(FileInterceptor)`, `@JwtAuthGuard` | Carga de archivo, cálculo de hash SHA-256, verificación de magic bytes y registro de metadatos. |
| `GET` | `/api/v1/archivos/:id` | `@JwtAuthGuard` | Obtiene la ficha técnica completa y metadatos archivísticos del documento. |
| `GET` | `/api/v1/archivos/:id/descargar` | `@JwtAuthGuard`, `@AuditLog` | Descarga segura por stream, registrando usuario e IP en la bitácora. |
| `GET` | `/api/v1/archivos/:id/previsualizar` | `@JwtAuthGuard` | Visualización en línea (`Content-Disposition: inline`) para PDF e imágenes. |
| `POST` | `/api/v1/archivos/vincular` | `@Body() VincularDocumentoDto` | Asocia un documento a una entidad y registro específico de un formulario SIAF. |
| `DELETE` | `/api/v1/archivos/:id/desvincular/:relacionId` | `@JwtAuthGuard` | Desvincula lógicamente el documento de un trámite concreto. |
| `POST` | `/api/v1/archivos/:id/versionar` | `@UseInterceptors(FileInterceptor)` | Registra una nueva versión del archivo sustentada en un motivo justificado. |
| `GET` | `/api/v1/archivos/entidad/:modulo/:entidad/:registroId` | `@JwtAuthGuard` | Consulta todos los documentos adjuntos a un trámite institucional. |
| `PATCH` | `/api/v1/archivos/:id/clasificacion` | `@Roles('ADMIN_ARCHIVOS')` | Actualiza nivel de clasificación (Público/Reservado/Confidencial) o CGCA. |
| `POST` | `/api/v1/archivos/temporales/depurar` | `@Cron('0 2 * * *')` | Tarea programada nocturna para purga de archivos temporales huérfanos (> 24 h). |

---

## 7. Componentes Frontend Reutilizables (Next.js)

Para que ningún desarrollador vuelva a programar lógica de carga, validación o descarga dentro de formularios de negocio, se diseñan los siguientes componentes en `@/components/files/`:

1. **`<EntityFiles />` (Componente Integral Maestro):**
   * Se incrusta en cualquier formulario compuesto (ej. Afectación de Gasto, Registro de Ingreso, Orden de Pago).
   * **Propiedades:**
     ```typescript
     interface EntityFilesProps {
       modulo: string;
       entidad: string;
       registroId: string | number;
       tiposPermitidos?: string[]; // ej. ['OFICIO_SOLICITUD', 'CFDI_XML', 'CFDI_PDF']
       soloLectura?: boolean;
       requiereVersionamiento?: boolean;
       permitirDescarga?: boolean;
       permitirPrevisualizacion?: boolean;
     }
     ```
   * Despliega la tabla de documentos vinculados, estado de cumplimiento (obligatorios cubiertos), botones de acción y visor integrado.
2. **`<SingleFileField />`:** Control compacto para un único archivo obligatorio o complementario (ej. "Comprobante de Transferencia SPEI").
3. **`<MultiFileField />`:** Zona interactiva Drag & Drop para adjuntar paquetes documentales con barras de progreso y cálculo de hash local previo.
4. **`<FilePreviewModal />`:** Modal seguro para previsualización nativa de archivos PDF e imágenes sin exponer la URL física del almacenamiento. Incluye ficha lateral con los metadatos archivísticos (CGCA, vigencia, autor, hash).
5. **`<ArchivalBadge />`:** Etiqueta visual de clasificación (Verde: *Público*, Amarillo: *Reservado*, Rojo: *Confidencial*, Azul: *Vigencia Contable 5A*).

---

## 8. Administrador General de Gestión Documental y Archivos

Ubicado en el menú principal: **Administración → Gestión Documental y Archivos**.

Permite a la Unidad Central de Archivos del PJEV, a la Contraloría Interna y a los administradores del sistema:
1. **Búsqueda Global y Filtros Avanzados:**
   * Localización de cualquier documento en el sistema por: Nombre, Hash SHA-256, Folio de registro, Módulo emisor, Serie archivística del CGCA, Rango de fechas, Usuario responsable y Nivel de reserva.
2. **Panel de Estadísticas y Semáforos de Vigencia:**
   * Métricas de espacio consumido por módulo y ejercicio fiscal.
   * Semáforo de vigencias documentales: alertas de documentos próximos a cumplir su periodo de trámite para solicitar su transferencia primaria al Archivo de Concentración.
3. **Ficha Integral de Detalle del Documento:**
   * **Vista Previa:** Visualización inmediata del contenido.
   * **Relaciones Activas:** Muestra en qué transacciones del SIAF está involucrado (ej. vinculado a la Transferencia Presupuestal 458 y a la Póliza de Egresos 1204).
   * **Historial de Versiones:** Comparativa de versiones 1, 2 y actual con detalle de modificaciones y usuarios responsables.
   * **Cadena de Custodia (Bitácora):** Listado inmutable de cada consulta, descarga, previsualización o cambio de estado con marca de tiempo e IP.
   * **Ficha Técnica Archivística:** Código CGCA, valores asignados en CADIDO, plazo de custodia y estatus ante la NOM-151.

---

## 9. Estrategia de Archivos Temporales y Registros Nuevos

Para resolver la concurrencia en formularios nuevos donde **aún no existe el `registro_id` de la entidad**:
1. **Estrategia Canónica (Token de Operación Temporal):**
   * Al abrir un formulario de alta, el frontend genera un `ticket_temporal` (UUID).
   * Los archivos se cargan con `modulo_siaf = 'temporal'`, asociados a dicho ticket.
   * Tienen vigencia máxima de **24 horas** en estado `'TEMPORAL'`.
2. **Confirmación Transaccional:**
   * Al guardar exitosamente el encabezado del registro principal (ej. se genera el ID de Afectación de Gasto `852`), el backend invoca en la misma transacción la asociación de los archivos temporales vinculados al ticket, actualizando la relación a definitiva (`registro_id = 852`, `modulo_siaf = 'cxp'`).
3. **Depuración Automática (Garbage Collector):**
   * Un proceso batch diario (`@Cron('0 2 * * *')`) elimina física y lógicamente todos los archivos en estado `'TEMPORAL'` con más de 24 horas de antigüedad que nunca fueron consolidados por el usuario.

---

## 10. Fases de Implementación y Cronograma Técnico

| Fase | Título | Entregables Principales |
| :--- | :--- | :--- |
| **Fase 1** | Diagnóstico y Auditoría Actual | Documento `ANALISIS_MANEJO_ARCHIVOS_ACTUAL.md` clasificando implementaciones previas. |
| **Fase 2** | DDL y Esquema PostgreSQL | Script SQL de creación del esquema `archivos.*`, tablas, índices por hash y constraints. |
| **Fase 3** | Stored Procedures Canónicos | SPs `fn_leer_documento`, `fn_crud_documento`, `fn_crud_documento_relacion` y bitácora. |
| **Fase 4** | Servicio de Almacenamiento | Interfaz `IFileStorageDriver` y adaptadores para Local/NAS y MinIO/S3. |
| **Fase 5** | API REST y Validaciones | FilesController en NestJS con magic bytes, SHA-256 y documentación OpenAPI / Swagger. |
| **Fase 6** | Componentes Frontend | `<EntityFiles />`, `<SingleFileField />`, `<MultiFileField />` y visor `<FilePreviewModal />`. |
| **Fase 7** | Administrador General | Módulo administrativo de consulta transversal, búsqueda y ficha documental en el front. |
| **Fase 8** | Integración Piloto | Integración en un formulario real del sistema (ej. `05.2.1 Afectación del Gasto` y `04.2.1 Registro de Ingreso`). |
| **Fase 9** | Endurecimiento y Pruebas | Pruebas de seguridad (path traversal, falsificación MIME, inyección) y manual técnico de integración. |
