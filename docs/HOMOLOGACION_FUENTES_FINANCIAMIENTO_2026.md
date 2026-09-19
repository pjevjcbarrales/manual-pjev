# Homologación del Catálogo de Fuentes de Financiamiento (SEFIPLAN / CONAC / SAFPOJ)

> **Documento de Continuidad Técnica y Arquitectura**  
> **Conversación de Referencia:** [c49c8248-d02a-4904-88b7-2ffd84bae2d0](conversation://c49c8248-d02a-4904-88b7-2ffd84bae2d0)  
> **Proyecto:** SIAF-PJEV & Manual de Desarrollo  
> **Módulo:** `01.2.4 Fuentes de Financiamiento` (`cfg/cpp/fuentesf`)  
> **Fecha de Consolidación:** Septiembre 2026  

---

## 1. Resumen Ejecutivo
Se implementó la homologación transversal del **Catálogo de Fuentes de Financiamiento** en toda la arquitectura del SIAF-PJEV (Base de Datos PostgreSQL, Servicios Backend NestJS, Frontend Next.js y Manual Web de Desarrollo), alineándolo con la estructura oficial de **SEFIPLAN Veracruz**, el marco de armonización **CONAC**, la **Ley de Disciplina Financiera (LDF)** y el sistema legado **SAFPOJ** del Poder Judicial del Estado de Veracruz.

---

## 2. Definición Canónica de Fuentes de Financiamiento 2026

La clave presupuestal oficial de la fuente de financiamiento se compone de **6 dígitos**:
`[CONAC 2 dígitos] + [Fondo / Origen 2 dígitos] + [Año Fiscal 2 dígitos]`

| Clave (`cff_clave`) | Abrev (`cff_abrev`) | Denominación Oficial | Ejercicio (`eje_id`) | Tipo (`cff_tipo`) | Régimen LDF | Subcuenta SAFPOJ |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **`160126`** | `EST` | PRESUPUESTO AUTORIZADO 2026 (Subsidio Estatal) | 2026 (`1`) | Estatal (`1`) | No Etiquetado | `1182002-160126` |
| **`160926`** | `CONV` | PRESUPUESTO AUTORIZADO 2026 (CONVENIOS) | 2026 (`1`) | Estatal (`1`) | No Etiquetado | `1182002-160926` |
| **`170126`** | `PROP` | OTROS INGRESOS 2026 (Recursos Propios) | 2026 (`1`) | Propios (`3`) | No Etiquetado | `1182002-170126` |
| **`170226`** | `FAUX` | FONDO AUXILIAR PARA LA IMPARTICIÓN DE JUSTICIA 2026 | 2026 (`1`) | Propios (`3`) | No Etiquetado | `1182002-170226` |
| **`250126`** | `FASP` | APORTACIÓN FEDERAL FASP 2026 | 2026 (`1`) | Federal (`2`) | Etiquetado Federal | `1182001-250126` |
| **`250226`** | `JLAB` | JUZGADOS LABORALES 2026 | 2026 (`1`) | Federal (`2`) | Etiquetado Federal | `1182001-250226` |

---

## 3. Jerarquía y Árbol Presupuestal SAFPOJ (Cuenta 1180000)

En los estados analíticos e informes del Poder Judicial, las fuentes de financiamiento se subordinan a la cuenta mayor de Ingresos:

```text
📁 1180000 TRANSFERENCIAS, ASIGNACIONES Y DONATIVOS CORRIENTES RECIBIDOS
  ├── 📁 1182000 DEL SECTOR PÚBLICO
  │     ├── 📁 1182001 PROVENIENTES DEL GOBIERNO FEDERAL (Etiquetado)
  │     │     └── 🏷️ 1182001-250126 APORTACIÓN FEDERAL FASP 2026
  │     │     └── 🏷️ 1182001-250226 JUZGADOS LABORALES 2026
  │     └── 📁 1182002 PROVENIENTES DEL GOBIERNO ESTATAL (No Etiquetado)
  │           ├── 🏷️ 1182002-160126 PRESUPUESTO AUTORIZADO 2026 (Subsidio Estatal)
  │           ├── 🏷️ 1182002-160926 PRESUPUESTO AUTORIZADO 2026 (CONVENIOS)
  │           ├── 🏷️ 1182002-170126 OTROS INGRESOS 2026 (Recursos Propios)
  │           └── 🏷️ 1182002-170226 FONDO AUXILIAR PARA LA IMPARTICIÓN DE JUSTICIA 2026
```

---

## 4. Cambios Realizados por Capa Técnica

### A. Base de Datos (PostgreSQL)
* **Script:** `packages/database/sql/20260918_1930_fuentes_financiamiento_canonico_2026.sql`
* **Acciones:**
  - Limpieza de espacios residuales (`TRIM`) en `cff_clave`, `cff_abrev` y `cff_nombre`.
  - Asignación formal de fuentes 2025 al ejercicio fiscal `eje_id = 5`.
  - Inserción y actualización idempotente de las 6 fuentes canónicas del ejercicio 2026 (`eje_id = 1`).
  - Validación de unicidad de clave por ejercicio fiscal (`cff_ejercicio`, `cff_clave`).

### B. Backend (NestJS)
* **Archivo:** `apps/backend/src/configuracion/fuentesf/fuentesf.service.ts`
* **Acciones:**
  - Validación de formato alfanumérico/numérico de 6 caracteres (`^[0-9]{6}$`).
  - Métodos `findAll`, `findOne` y `mapRow` enriquecidos con campos de metadatos computados:
    - `regimenLdf`: *Etiquetado Federal* (para prefijo 25) vs *No Etiquetado* (para prefijos 16, 17).
    - `conacClasificacion`: Etiqueta normativa CONAC.
  - Generación de reportes analíticos con desglose de la cuenta mayor `1180000`.

### C. Frontend (Next.js / PJEV-UI)
* **Bandeja Principal:** `apps/frontend/app/(dashboard)/cfg/cpp/fuentesf/page.tsx`
  - Switch interactivo para alternar entre **Vista Tabla Grid** y **Vista en Árbol SAFPOJ**.
  - Insignias de régimen LDF con paleta oficial PJEV.
* **Formulario ABC:** `apps/frontend/app/(dashboard)/cfg/cpp/fuentesf/[id]/page.tsx`
  - Validación Zod para claves de 6 dígitos.
  - Sincronización automática de sufijo anual conforme al ejercicio seleccionado.

### D. Manual Web de Desarrollo
* **Página Canónica:** `sitio_web/01_cfg/01.2.4-fuentes-financiamiento.html`
  - Secciones 1 a 15 con el marco normativo LDF/CONAC/SEFIPLAN.
  - SPs `fn_leer_fuentesf` y `fn_crud_fuentesf`.
  - Wireframes SVG con pestañas interactivas, diagrama de árbol y controles PJEV.

---

## 5. Estado de Pruebas y Certificación
* **NestJS Backend:** `nest build` ejecutado exitosamente con 0 errores.
* **Next.js Frontend:** `npx tsc --noEmit` completado exitosamente con 0 errores.
* **PostgreSQL:** Verificación de 12 registros (6 de 2025 y 6 de 2026) normalizados y activos.
