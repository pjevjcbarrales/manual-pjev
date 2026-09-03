# Guía de Continuidad Técnica y Arquitectónica: 05 · Cuentas por Pagar (CxP)

Este documento condensa el conocimiento metodológico, funcional y técnico adquirido durante la construcción de los módulos de Configuración (01), Presupuesto (02), Contabilidad (03) e Ingresos (04), sirviendo de base para la apertura de la nueva conversación de trabajo enfocada en **05 · Cuentas por Pagar**.

---

## 1. Contexto y Ecosistema de Desarrollo
* **Cliente / Ente:** Dirección General de Administración (DGA) / Órgano Auxiliar de la Junta (OAJ) del Poder Judicial del Estado de Veracruz (PJEV).
* **Consultora:** Dix Consultoría (Liderazgo de Proyecto: Julio César Barrales).
* **Equipo de Desarrollo Interno:**
  * **Cristian:** Responsable técnico asignado al subsistema de Cuentas por Pagar (CxP).
  * **Eunice:** Responsable del subsistema de Ingresos (04).
  * **Daryl:** Seguridad y control de acceso.
* **Repositorio Git:** `c:\dixsys\manual_pjev\sitio_web` (`origin master` en `https://github.com/pjevjcbarrales/manual-pjev.git`).
* **Despliegue Continuo:** [https://manual-pjev.vercel.app/](https://manual-pjev.vercel.app/) (sincronizado automáticamente con `master`).

---

## 2. Convenciones Técnicas Obligatorias (Reglas de Oro)

1. **Ubicación Estricta de SPs y Swagger**:
   En todos los documentos HTML de análisis funcional (estándar DOC-08), los **Stored Procedures PostgreSQL** (`fn_leer_*` y `fn_crud_*`) y los **Servicios API REST (Swagger / NestJS)** deben colocarse **inmediatamente después del Modelo de Datos / Diccionario de Campos**, antes de las Reglas de Negocio y Wireframes. Las secciones subsecuentes deben quedar numeradas secuencialmente (1 a 14/15) sin duplicidades.
2. **Estándar de Base de Datos (PostgreSQL)**:
   * Esquema para CxP: `cxc` (o `cxp` según la definición del esquema relacional vigente).
   * Parámetros de sesión obligatorios en cada función: `p_usuario VARCHAR`, `p_ejercicio INTEGER`.
   * Formato de retorno unificado en JSONB:
     ```json
     { "error": 0, "mensaje": "OK", "data": { ... } }
     ```
     (`0` = Operación exitosa, `-1` = Validación de negocio / Warning, `-2` = Error técnico / Excepción).
   * Parámetros de seguridad: `SECURITY DEFINER` y `SET search_path = cxc, public;`.
   * **Soft-delete obligatorio**: `estatus_registro = 0` (nunca ejecutar `DELETE` físico).
   * **Auditoría obligatoria**: Columnas `usuario_c`, `fecha_c`, `usuario_m`, `fecha_m`.
3. **Backend (NestJS + Prisma)**:
   * La lógica contable y de afectación presupuestal pesada reside en los Stored Procedures de PostgreSQL, no en JavaScript/TypeScript.
   * NestJS expone controladores REST decorados con Swagger (`@ApiTags`, `@ApiOperation`, `@ApiResponse`, `@UseGuards(JwtAuthGuard, RolesGuard)`).
4. **Diseño Visual**:
   * Reutilización de estilos de `sitio_web/shared.css`, clases `.code-wrap` y `.method.*` (`.method.get`, `.method.post`, `.method.put`, `.method.delete`).
   * Bocetos de interfaz (Wireframes) implementados como **SVGs nativos embebidos**, interactivos mediante pestañas JavaScript (`showWF`).

---

## 3. Mapa del Subsistema: 05 · Cuentas por Pagar

El subsistema se encuentra estructurado en el menú principal (`sitio_web/index.html`) con las siguientes opciones:

### 05.1 · Catálogos
* **05.1.1 Requisitos documentales**: Matriz de checklist de soportes fiscales, contratos y actas de entrega requeridas según el tipo de gasto o proveedor.
* **05.1.2 Tarifas y zonas de viáticos**: Tabulador oficial de viáticos por zona geográfica, jerarquía del servidor público y límites de comprobación sin comprobante.
* **05.1.3 Conceptos de retención y deducción**: Catálogo de deducciones legales (ISR 1.25% / 10%, IVA retenido 2/3 o 10.667%, 5 al millar de obra, cuotas sindicales, pensiones alimenticias, etc.).

### 05.2 · Registro
* **05.2.1 Afectación del gasto**: Registro del compromiso y devengo del gasto basado en factura XML validada en Bóveda CFDI o solicitud interna. *(Nota: existe antecedente funcional en `05_cuentas_por_pagar/05.2.3-afectacion-gastos.html` que debe homologarse como 05.2.1)*.
* **05.2.2 Orden de pago**: Generación del documento formal de trámite de pago para remitir a Tesorería.
* **05.2.3 Gastos a comprobar**: Emisión de solicitudes y dispersión de recursos a servidores públicos bajo fondo fijo o comisión oficial.
* **05.2.4 Comprobación y revisión de gastos**: Cotejo de CFDI y facturas entregadas por el comisionado contra los viáticos otorgados, determinando saldo a favor o saldo a reintegrar.

### 05.3 · Procesos
* **05.3.1 Pre-pólizas**: Generación preliminar y revisión del asiento contable-presupuestal previo a su aplicación definitiva en el libro diario.
* **05.3.2 Programación de pagos**: Calendario y priorización de compromisos de pago según disponibilidad de flujo de efectivo en bancos.
* **05.3.3 Control y entero de retenciones**: Consolidación mensual de retenciones impositivas y de terceros para su pago ante el SAT, SEFIPLAN o juzgados.
* **05.3.4 DIOT**: Generación de la Declaración Informativa de Operaciones con Terceros (A-29).
* **05.3.5 Movimientos de fideicomisos**: Registro de afectaciones presupuestarias y compromisos derivados de fondos fiduciarios institucionales.

### 05.4 · Informes
* **05.4.1 Informes de Cuentas por Pagar**: Concentrador de reportes analíticos (Antigüedad de saldos, Estado de pasivos, Relación de retenciones por enterar, Auxiliar de órdenes de pago, etc.).

---

## 4. Convergencia con la Matriz de Conversión CONAC (Egresos)

Así como en Ingresos convergieron las matrices B.1, B.2 y B.3, en Cuentas por Pagar convergen las **Matrices de Egresos**:

1. **Matriz A.1: Devengado de Gastos**:
   * Cruza el **COG (Clasificador por Objeto del Gasto - `01.2.6`)** con las cuentas del Plan de Cuentas:
     * *Patrimonial:* Cargo a cuentas de **Gasto (`5.x`)** o **Activo (`1.2.x` Bienes muebles/inmuebles)** / Abono a **Pasivo Circulante (`2.1.1.x Cuentas por Pagar a Corto Plazo`)**.
     * *Presupuestal:* Cargo a `8.2.4 Presupuesto de Egresos Comprometido` / Abono a `8.2.5 Presupuesto de Egresos Devengado`.
2. **Matriz A.2: Pagado de Gastos**:
   * Se detona al formalizar el pago hacia Tesorería (06):
     * *Patrimonial:* Cargo a **Pasivo Circulante (`2.1.1.x`)** / Abono a **Bancos (`1.1.1.2`)**.
     * *Presupuestal:* Cargo a `8.2.5 Devengado` / Abono a `8.2.7 Presupuesto de Egresos Pagado`.
3. **Conexión con el Subsistema de Ingresos (04)**:
   * Cuando en `05.2.4 Comprobación de viáticos` un servidor público no ejerce la totalidad del anticipo, se genera un **Saldo a Reintegrar**.
   * Ese reintegro viaja al subsistema de Ingresos y se captura en `04.2.1` bajo los conceptos `ING-REI-VIA` o `ING-REI-GAC`, vinculando el folio de la Orden de Gasto de CxP para restaurar el saldo presupuestal en el capítulo correspondiente (Capítulo 3000).

---

## 5. Puntos de Contacto con Otros Subsistemas
* **Adquisiciones (07)**: Recibe contratos (`02.1.4`), suficiencias presupuestarias (`07.2.2`) y actas de entrega/recepción de almacén.
* **Bóveda CFDI (03.2.5)**: Valida la autenticidad del UUID ante el SAT, estatus de cancelación y coherencia de RFC antes de autorizar cualquier devengo.
* **Tesorería / Pagos (06)**: Envía las órdenes de pago debidamente autorizadas y validadas presupuestalmente para su dispersión por transferencia SPEI o cheque.
* **Contabilidad (03)**: Alimenta el libro diario con las pólizas de egresos y reportes de pasivos para la Cuenta Pública.
