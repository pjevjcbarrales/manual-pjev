# Historial de Conversaciones y Estado de Avance — SIAF-PJEV

> **ESTADO ACTUAL DEL PROYECTO — ¿DÓNDE TE QUEDASTE?**
> 📍 **Punto exacto:** **Homologación Integral y Reconstrucción Canónica de Fuentes de Financiamiento (`01.2.4-fuentes-financiamiento.html`)**.
> 🔗 **Conversación integrada:** [c49c8248-d02a-4904-88b7-2ffd84bae2d0](conversation://c49c8248-d02a-4904-88b7-2ffd84bae2d0) (del repositorio `siaf_pjev`).
> 📅 **Última sesión:** Septiembre 2026.
> 🎯 **Foco consolidado:** Homologación transversal del catálogo de Fuentes de Financiamiento en toda la arquitectura del sistema:
> 1. **Base de Datos PostgreSQL**: Limpieza de espacios con `TRIM`, migración SQL de fuentes históricas 2025 (`eje_id = 5`) e inserción de las 6 fuentes canónicas 2026 (`eje_id = 1`): `160126`, `160926`, `170126`, `170226`, `250126`, `250226`.
> 2. **Backend NestJS**: Validación de clave de 6 dígitos numéricos (`^[0-9]{6}$`), inyección de metadatos `regimenLdf` (*Etiquetado Federal* vs *No Etiquetado*) y clasificación CONAC.
> 3. **Frontend Next.js**: Switch vista dual (Grid vs Árbol SAFPOJ bajo cuenta `1180000`), insignias LDF y validación Zod.
> 4. **Manual de Desarrollo**: Página `01.2.4-fuentes-financiamiento.html` con marco normativo, SPs, Swagger y wireframes interactivos.
> 5. **Documento Técnico de Referencia**: [`sitio_web/docs/HOMOLOGACION_FUENTES_FINANCIAMIENTO_2026.md`](file:///c:/dixsys/manual_pjev/sitio_web/docs/HOMOLOGACION_FUENTES_FINANCIAMIENTO_2026.md).

---

## Índice Rápido de Conversaciones / Sesiones

1. [Sesión 1 — Fundamentos, Estándares de Arquitectura y Configuración Base](#sesión-1--fundamentos-estándares-de-arquitectura-y-configuración-base)
2. [Sesión 2 — Clasificadores Presupuestales y Catálogos Generales](#sesión-2--clasificadores-presupuestales-y-catálogos-generales)
3. [Sesión 3 — Módulo de Presupuesto (02 · Ppto) y Reportes CONAC/LDF](#sesión-3--módulo-de-presupuesto-02--ppto-y-reportes-conacldf)
4. [Sesión 4 — Módulo de Contabilidad (03 · Conta) y Matriz de Conversión (03.1.2)](#sesión-4--módulo-de-contabilidad-03--conta-y-matriz-de-conversión-0312)
5. [Sesión 5 — Módulo de Ingresos / Cuentas por Cobrar (04 · Ing)](#sesión-5--módulo-de-ingresos--cuentas-por-cobrar-04--ing)
6. [Sesión 6 — Arquitectura de Gestión Documental y Manejo de Archivos (DocuWare vs SIAF)](#sesión-6--arquitectura-de-gestión-documental-y-manejo-de-archivos-docuware-vs-siaf)
7. [Sesión 7 (ÚLTIMA) — Homologación Transversal de Fuentes de Financiamiento (01.2.4) [PUNTO DE CORTE]](#sesión-7-última--homologación-transversal-de-fuentes-de-financiamiento-0124-punto-de-corte)

---

## Detalle Cronológico de Conversaciones

### Sesión 1 — Fundamentos, Estándares de Arquitectura y Configuración Base
* **Participantes:** Julio Barrales (Director) · Asistente IA.
* **Objetivo:** Definición de arquitectura del manual y módulos iniciales de configuración.
* **Acuerdos clave:**
  - Formato del manual: Sitio web estático institucional con tokens de diseño PJEV (`shared.css`) y wireframes SVG nativos.
  - Estándar DOC-08 y estructura de páginas canónicas (10 a 15 secciones).
  - Estándar de base de datos PostgreSQL: esquemas lógicos, soft-delete obligatorio (`estatus_registro = 0`), auditoría (`usuario_c`, `fecha_c`, `usuario_m`, `fecha_m`), SPs `fn_leer_[entidad]` y `fn_crud_[entidad]` con retorno JSONB `{ error, mensaje, data }`.
  - Módulos documentados: `01.1.1 Entidad`, `01.1.2 Ejercicios Fiscales`, `01.1.3 Períodos Contables`.

---

### Sesión 2 — Clasificadores Presupuestales y Catálogos Generales
* **Participantes:** Julio Barrales · Asistente IA · Equipo técnico (Cristian, Eunice, Daryl).
* **Módulos procesados:**
  - Clasificadores: `01.2.1 Unidades Administrativas`, `01.2.2 COG`, `01.2.3 Programas`, `01.2.5 CUCOP`, `01.2.6 Subprogramas`, `01.2.7 CRI`, `01.2.8 Proyectos`, `01.2.9 Centros de Costo`.
  - Catálogos: Proveedores, Subtipo de Proveedor, Empleados, Terceros Institucionales, Terceros, Bancos, Chequeras, Conceptos Bancarios, Seguridad (Sistemas, Subsistemas, Módulos, Roles).

---

### Sesión 3 — Módulo de Presupuesto (02 · Ppto) y Reportes CONAC/LDF
* **Participantes:** Julio Barrales · Eunice Hernández · Asistente IA.
* **Módulos procesados:**
  - Clave presupuestal integrada (28 dígitos), Presupuesto Autorizado, Bienes Inmuebles, Registro de Contratos.
  - Calendarización, Recalendarización, Transferencias, Ampliaciones/Reducciones, Compromiso de Arrendamientos, Operaciones Especiales, Cierre Presupuestal Mensual.
  - Suficiencias Presupuestales, Bitácora de Adecuaciones, Gastos de Operación y Consola Central de Reportes (EAEPE por Clasificación Administrativa, Económica, Objeto del Gasto, Funcional, Estado Analítico de Ingresos).

---

### Sesión 4 — Módulo de Contabilidad (03 · Conta) y Matriz de Conversión (03.1.2)
* **Participantes:** Julio Barrales · Cristian Arcos · Asistente IA.
* **Módulos procesados:**
  - Plan de Cuentas Armonizado CONAC, Pólizas Contables (Ingresos, Egresos, Diario), Cierre Contable.
  - **Matriz de Conversión CONAC (`03.1.2`)**:
    - Asignado a **Julio Barrales** como responsable técnico y desarrollador.
    - Homologado con arquitectura real (10 tablas del ecosistema de matrices en PostgreSQL, servicios REST en NestJS y frontend Next.js).
    - Modelo funcional basado en el esquema **Etiqueta:Caja** con 4 dimensiones y trazabilidad de origen CxP / CxC.
    - Wireframes interactivos con vista dual: **Mosaico** y **Detalles** (con columnas de Cargo Contable `C` y Abono Contable `C`).
    - Estado de 03.1.2: **Terminado y canónico**.

---

### Sesión 5 — Módulo de Ingresos / Cuentas por Cobrar (04 · Ing)
* **Participantes:** Julio Barrales · Daryl Olazarán · Eunice Hernández · Asistente IA.
* **Módulos procesados y acuerdos:**
  - Asignado formalmente a **Daryl Olazarán Gómez** como responsable técnico de Ingresos.
  - `04.1.1 Conceptos de Ingreso`: 17 conceptos institucionales, CRI, 10 banderas de validación, tratamiento de arrendamientos, reintegros de personal (`ING-REI-*`) y aclaraciones bancarias.
  - `04.1.2 Tipos de Movimiento de Ingreso`: devengado, recaudado, simultáneo y ajuste; clarificación de roles para autorización en `CAP_INCORRECTO` y comportamiento de contramovimientos en `OTRO_AUTORIZ`.
  - `04.1.3 Claves SEFIPLAN` y `04.1.4 Cuentas Recaudadoras`.
  - `04.2.1 Registro de Ingresos (Devengo)`: formulario compuesto, doble archivo físico firmado (comprobante fiscal/bancario + oficio/acuerdo), grid PJEV-UI y barra de cuadre en vivo.
  - `04.2.2 Validación de Depósitos`: precarga bancaria y cotejo.
  - `04.3.1 Conciliación de Ingresos`, `04.3.2 Cierre Mensual de Ingresos` (13 validaciones V-01 a V-13), `04.4.1 Informes y Control de Ingresos`.

---

### Sesión 6 — Arquitectura de Gestión Documental y Manejo de Archivos (DocuWare vs SIAF)
* **Participantes:** Julio Barrales · Asistente IA.
* **Entregables generados:**
  - `BENCHMARK_DOCUWARE_VS_SIAF_PJEV.md` (Comparativo funcional y técnico).
  - `PLAN_GESTION_DOCUMENTAL_Y_ARCHIVOS_SIAF_PJEV.md` (Estrategia institucional).
  - `FILE_BACKEND_ARCHITECTURE.md`, `FILE_COMPONENTS_AND_INTEGRATION_GUIDE.md`, `FILE_ADMIN_AND_SECURITY.md`.
  - Especificación de almacenamiento S3/MinIO/FileSystem, hash SHA-256 de integridad, metadatos JSONB y visores integrados.

---

### Sesión 7 (ÚLTIMA) — Homologación Transversal de Fuentes de Financiamiento (01.2.4) [PUNTO DE CORTE]
* **Conversación Origen:** [c49c8248-d02a-4904-88b7-2ffd84bae2d0](conversation://c49c8248-d02a-4904-88b7-2ffd84bae2d0) (Proyecto `siaf_pjev`).
* **Participantes:** Julio Barrales · Asistente IA.
* **Tema tratado:** **Homologación transversal y canónica del catálogo `01.2.4 Fuentes de Financiamiento` (SEFIPLAN / CONAC / SAFPOJ)**.
* **Detalle técnico de lo ejecutado y consolidado:**
  1. **Base de Datos (PostgreSQL)**:
     - Script SQL idempotente: `packages/database/sql/20260918_1930_fuentes_financiamiento_canonico_2026.sql`.
     - Normalización de cadenas (`TRIM`) en `cff_clave`, `cff_abrev` y `cff_nombre`.
     - Mapeo de fuentes históricas 2025 al ejercicio fiscal `eje_id = 5`.
     - Creación/actualización de las 6 fuentes canónicas del ejercicio 2026 (`eje_id = 1`):
       * `160126` (EST - Presupuesto Autorizado Subsidio Estatal - No Etiquetado).
       * `160926` (CONV - Convenios / Ampliaciones - No Etiquetado).
       * `170126` (PROP - Otros Ingresos / Recursos Propios - No Etiquetado).
       * `170226` (FAUX - Fondo Auxiliar para la Impartición de Justicia - No Etiquetado).
       * `250126` (FASP - Aportación Federal FASP 2026 - Etiquetado Federal).
       * `250226` (JLAB - Juzgados Laborales 2026 - Etiquetado Federal).
  2. **Backend (NestJS)**:
     - Servicio `apps/backend/src/configuracion/fuentesf/fuentesf.service.ts` actualizado.
     - Validación de estructura de 6 dígitos (`^[0-9]{6}$`).
     - Inyección de metadatos automáticos `regimenLdf` y `conacClasificacion` en `mapRow`.
     - Reportes analíticos con agrupación por la cuenta mayor institucional `1180000`.
  3. **Frontend (Next.js / PJEV-UI)**:
     - Bandeja `apps/frontend/app/(dashboard)/cfg/cpp/fuentesf/page.tsx`: Switch interactivo para vista de Grid y vista en Árbol SAFPOJ (`1180000 -> 1182000 -> 1182001 / 1182002`).
     - Formulario `apps/frontend/app/(dashboard)/cfg/cpp/fuentesf/[id]/page.tsx`: Validación Zod de 6 dígitos y sincronización de sufijo del año.
  4. **Manual Web de Desarrollo**:
     - Actualizado canónicamente `sitio_web/01_cfg/01.2.4-fuentes-financiamiento.html` con marco normativo, SPs `fn_leer_fuentesf` / `fn_crud_fuentesf`, Swagger y wireframes SVG interactivos.
     - Creado documento de arquitectura [`sitio_web/docs/HOMOLOGACION_FUENTES_FINANCIAMIENTO_2026.md`](file:///c:/dixsys/manual_pjev/sitio_web/docs/HOMOLOGACION_FUENTES_FINANCIAMIENTO_2026.md).
  5. **Verificación de Calidad**:
     - `nest build` en backend: 0 errores.
     - `npx tsc --noEmit` en frontend: 0 errores.
     - BD PostgreSQL: 12 registros normalizados y verificados.
* **Commits consolidados:**
  - `0ec58c8 docs(cfg): actualizar 01.2.4 con representacion visual del arbol SAFPOJ y fuentes canonicas 2026`
  - `88c0cb3 docs(cfg): reconstruir canónicamente página 01.2.4 de Fuentes de Financiamiento conforme a estándar y reglas PJEV`

---

## 📌 Resumen para responder: "¿Dónde me quedé?"

Cuando preguntes **"¿Dónde me quedé?"**, la respuesta es:

> **Te quedaste en la homologación e integración canónica de 01.2.4 Fuentes de Financiamiento** (referencia: conversación [c49c8248-d02a-4904-88b7-2ffd84bae2d0](conversation://c49c8248-d02a-4904-88b7-2ffd84bae2d0)), donde se consolidó la arquitectura completa en BD PostgreSQL (script 2026 con 6 fuentes canónicas), Backend NestJS (validación 6 dígitos y metadatos LDF), Frontend Next.js (vista dual Grid / Árbol SAFPOJ cuenta `1180000`), y el Manual Web en `01_cfg/01.2.4-fuentes-financiamiento.html`.
> 
> **Lo que sigue en la ruta de trabajo:**
> 1. Continuar con la fase de **05 · Cuentas por Pagar (CxP)** asignada a **Cristian Arcos** (`05.1.1 Requisitos Documentales`, `05.1.2 Tarifas y Zonas de Viáticos`, `05.1.3 Retenciones y Deducciones`, `05.2.1 Afectación del Gasto`, `05.2.2 Orden de Pago`, `05.2.3 Gastos a Comprobar`, etc.) y su enlace con la Matriz de Conversión A.1/A.2.
> 2. O bien abordar los catálogos/procesos complementarios que priorices.
