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

La fuente de financiamiento se almacena atómicamente homologada con `presupuesto.clave_presupuestal`:
* **`cff_tipo_fondo`**: 1 dígito (`1` = Estatal / No Etiquetado / Propios, `2` = Etiquetado / Federal)
* **`cff_fondo_especifico`**: 3 dígitos (`601`, `609`, `701`, `702`, `501`, `502`)
* **`cff_anio`**: 2 dígitos (calculado automáticamente a partir de `cff_ejercicio` $\rightarrow$ `eje_anio % 100`, ej. `26`)
* **`cff_tipo_gasto`**: 1 dígito (`1` = Gasto Corriente, `2` = Gasto de Capital)
* **`cff_clave`**: Clave concatenada resultante (`[tipo_fondo][fondo_especifico][anio]`, 6 dígitos)

| Tipo Fondo | Fondo Esp. | Año | Clave Concatenada (`cff_clave`) | Abrev (`cff_abrev`) | Denominación Oficial | Ejercicio (`eje_id`) | Régimen LDF | Subcuenta SAFPOJ |
| :---: | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| `1` | `601` | `26` | **`160126`** | `EST` | PRESUPUESTO AUTORIZADO 2026 (Subsidio Estatal) | 2026 (`1`) | No Etiquetado | `1182002-160126` |
| `1` | `609` | `26` | **`160926`** | `CONV` | PRESUPUESTO AUTORIZADO 2026 (CONVENIOS) | 2026 (`1`) | No Etiquetado | `1182002-160926` |
| `1` | `701` | `26` | **`170126`** | `PROP` | OTROS INGRESOS 2026 (Recursos Propios) | 2026 (`1`) | No Etiquetado | `1182002-170126` |
| `1` | `702` | `26` | **`170226`** | `FAUX` | FONDO AUXILIAR PARA LA IMPARTICIÓN DE JUSTICIA 2026 | 2026 (`1`) | No Etiquetado | `1182002-170226` |
| `2` | `501` | `26` | **`250126`** | `FASP` | APORTACIÓN FEDERAL FASP 2026 | 2026 (`1`) | Etiquetado Federal | `1182001-250126` |
| `2` | `502` | `26` | **`250226`** | `JLAB` | JUZGADOS LABORALES 2026 | 2026 (`1`) | Etiquetado Federal | `1182001-250226` |

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
* **Script:** `packages/database/prisma/migrations/010_homologacion_campos_fuentesf.sql`
* **Acciones:**
  - Adición de columnas `cff_tipo_fondo`, `cff_fondo_especifico`, `cff_anio`, `cff_tipo_gasto` en `config.catalogo_fuentes_fin`.
  - Poblado automático de registros históricos a partir de `cff_clave` y de `config.catalogo_ejercicios`.
  - Creación de índices dedicados para optimización de reportes cruzados con `presupuesto.clave_presupuestal`.

### B. Backend (NestJS)
* **Archivo:** `apps/backend/src/configuracion/fuentesf/fuentesf.service.ts`
* **Acciones:**
  - Soporte de DTO con campos atómicos (`tipoFondo`, `fondoEspecifico`, `tipoGasto`) y cálculo automático de `cff_anio` y `cff_clave`.
  - Enriquecimiento de `mapRow` con los valores atómicos y calculados para el frontend.

### C. Frontend (Next.js / PJEV-UI)
* **Bandeja Principal:** `apps/frontend/app/(dashboard)/cfg/cpp/fuentesf/page.tsx`
  - Grid con soporte de claves de 6 dígitos y enlaces a edición.
* **Formulario ABC:** `apps/frontend/app/(dashboard)/cfg/cpp/fuentesf/[id]/page.tsx`
  - Control compuesto con selector de tipo de fondo, fondo específico (3 chars), año calculado en tiempo real y barra de previsualización en vivo de la clave concatenada (`160126`).

### D. Manual Web de Desarrollo
* **Página Canónica:** `sitio_web/01_cfg/01.2.4-fuentes-financiamiento.html`
  - Homologación formal con `presupuesto.clave_presupuestal` (`02.1.1`).
  - Wireframe SVG actualizado mostrando los controles atómicos y la clave concatenada.

---

## 5. Estado de Pruebas y Certificación
* **NestJS Backend:** `nest build` ejecutado exitosamente con 0 errores.
* **Next.js Frontend:** `npx tsc --noEmit` completado exitosamente con 0 errores.
* **PostgreSQL:** Verificación de 12 registros (6 de 2025 y 6 de 2026) normalizados y activos.
