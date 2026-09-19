# Sesión de trabajo: Manual de Desarrollo SIAF-PJEV
**Fecha:** 26 de mayo de 2026  
**Participantes:** Julio Barrales (Director de Proyecto) · Claude (Asistente PMP)  
**Proyecto:** SIAF-PJEV · Dix Consultoría · OAJ-DGA · Poder Judicial del Estado de Veracruz

---

## Contexto inicial

Julio propone crear un **Manual de Desarrollo del SIAF-PJEV** para el equipo técnico (Cristian, Eunice, Daryl). El punto de partida es estudiar los análisis funcionales producidos y el código existente en el repositorio local.

**Equipo de desarrollo confirmado:**
- Cristian Arcos Fernández — Backend / full-stack / Configuración Inicial y Contabilidad
- Eunice Hernández Cruz — Analista UX / Presupuesto y CxC / levantamiento de requerimientos
- Daryl Olazarán Gómez — UX-UI / Cuentas por Pagar / también programa

---

## Decisión de formato: GitHub Wiki → Sitio web estilo UI-PJEV

Después de evaluar opciones (Word, Markdown, GitHub Wiki), se resuelve que el formato más adecuado es un **sitio web estático** al estilo del manual UI-PJEV ya producido, por las siguientes razones:

- Los SVGs de wireframes se renderizan nativamente en HTML
- Control total del estilo con la paleta institucional PJEV
- Navegación más rica que Markdown
- Fácil de compartir con la DGA o el OAJ sin cuenta GitHub

---

## Inventario de archivos acordado

**Total: 62 archivos** (3 navegación + 3 fundamentos + 56 módulos)

### Criterios de clasificación por módulo

| Criterio | Valores | Descripción |
|---|---|---|
| **Modo** | A / B | A = existe en código · B = por desarrollar |
| **Tipo** | Simple / Compuesto | Simple = solo encabezado · Compuesto = encabezado + líneas de movimiento |

---

## Estructura del sistema (Sistema → Subsistema → Módulo)

Derivada del código real en `C:\dixsys\siaf_pjev\apps\`:

```
📁 00. Fundamentos del Sistema
📁 01. Configuración Inicial  [cfg]
    ├── Subsistema: Entidad [ent]
    │   └── Entidad | Ejercicios Fiscales | Períodos Contables
    ├── Subsistema: Clasificadores Presupuestales [cpp]
    │   └── Centros de Costo | COG | CRI | CUCOP | Fuentes FF | Programas | Subprogramas | Proyectos
    ├── Subsistema: Catálogos [cat]
    │   └── Bancos | Chequeras | Cuentas Bancarias | Tipos Cuenta | Empleados | Proveedores | ...
    └── Subsistema: Seguridad [seg]
        └── Sistemas | Subsistemas | Módulos | Roles | Grupos | Usuarios
📁 02. Presupuesto  [ppto]
📁 03. Contabilidad  [conta]
📁 04. Cuentas por Cobrar  [ing]
📁 05. Cuentas por Pagar  [fin]
📁 06. Tesorería  (renombrado desde Bancos — confirmado por Eunice en carpeta 07_Tesorería)
📁 07. Adquisiciones  [adq]
    ├── Subsistema: Compras → Adjudicación Directa | Invitación a Tres | Licitación Pública
    ├── Subsistema: Instrumentos Jurídicos → Contratos | Pedidos
    └── Subsistema: Afectaciones Contables → Afectación de Gasto Adquisiciones
```

---

## Estándar oficial de Stored Procedures (funciones PostgreSQL)

Derivado del análisis del código real de pólizas contables:

### Nomenclatura

```sql
-- Pantalla principal (grid)
[esquema].fn_leer_[entidad](...)

-- Formulario encabezado
[esquema].fn_leer_[entidad](...)
[esquema].fn_crud_[entidad](...)

-- Formulario con líneas de detalle
[esquema].fn_leer_[entidad]_movtos(...)
[esquema].fn_crud_[entidad]_movtos(...)

-- Funciones auxiliares
[esquema].fn_lista_[entidad]_[contexto](...)
[esquema].fn_folio_siguiente_[entidad](...)
```

### Parámetros siempre presentes

```sql
@usuario    VARCHAR   -- usuario activo de sesión
@ejercicio  INTEGER   -- ejercicio fiscal activo de sesión

-- Control en fn_leer:
@id         [tipo]    -- NULL o > 0 → lee con filtros
                      -- < 0        → devuelve objeto con valores por defecto

-- Control en fn_crud:
@accion     SMALLINT  -- 0 = Leer
                      -- 1 = Alta
                      -- 2 = Cambio
                      -- 3 = Baja (softdelete)
```

### Envelope de retorno estándar

```json
{
  "error":   0,
  "mensaje": "OK",
  "data":    { ... }
}
```

| Valor de `error` | Tipo | Toast en UI |
|---|---|---|
| `0` o mayor | Éxito | ✅ Verde |
| `-1` | Warning | ⚠️ Amarillo |
| `-2` | Danger / Error técnico | 🔴 Rojo |

### Reglas adicionales

- **Softdelete** siempre: `estatus_registro = 0`, nunca `DELETE`
- **Auditoría** obligatoria: `usuario_c`, `fecha_c`, `usuario_m`, `fecha_m`
- **Alias camelCase** en SELECT: `p.p_id AS "pId"`, `p.usuario_c AS "usuarioC"`
- **`SECURITY DEFINER`** + `SET search_path` en todas las funciones
- **Retorno `jsonb`**, no `JSON`

### Deuda técnica CxP

Los SPs actuales de CxP (`sp_CxpAfectacionesGasto_*`) no siguen el estándar. Correcciones pendientes para Cristian:

1. Renombrar a `fn_leer_afectaciones_gasto` y `fn_crud_afectaciones_gasto`
2. Cambiar retorno de `JSON` a `jsonb`
3. Homologar envelope: `{ error, mensaje, data }` con códigos `0 / -1 / -2`
4. Cambiar acciones de `2/3/4` a `0/1/2/3`
5. Cambiar alias de `MAYUSCULAS_GUION` a `camelCase`
6. Agregar `SECURITY DEFINER` y `SET search_path`
7. Implementar `@id < 0` para retorno de defaults

---

## Plantilla de documentación por módulo

Cada página del sitio tiene 10 secciones fijas:

| # | Sección | Responsable principal |
|---|---|---|
| 1 | Descripción General | Julio / Eunice |
| 2 | Marco Normativo | Julio |
| 3 | Roles que intervienen | Eunice |
| 4 | Modelo de Datos | Cristian / Daryl |
| 5 | Stored Procedures | Cristian / Daryl |
| 6 | Servicios REST | Cristian / Daryl |
| 7 | Pantallas de Referencia (4 SVGs) | Daryl / Eunice |
| 8 | Reglas de Negocio Críticas | Julio / Eunice |
| 9 | Flujos de Integración | Julio |
| 10 | Historial de Cambios | Todo el equipo |

### Wireframes — 4 SVGs por módulo

| SVG | Contenido |
|---|---|
| P1 | Grid con filtros `@parametro` y columnas `{campo}` — notación técnica |
| P2 | Grid con datos reales de ejemplo |
| P3 | Formulario ABC con campos `@parametro` y sección OUT `{campo}` |
| P4 | Formulario con valores reales, SP call bar, envelope JSON OK/Error |

---

## Archivos producidos en esta sesión

### Sitio web manual-dev-siaf (ZIP)

```
manual-dev-siaf/
├── index.html              ← Portada con índice navegable completo (7 módulos)
├── shared.css              ← Tokens y estilos del shell UI-PJEV (reutilizado)
├── shared.js               ← copy-code + active sidebar link
├── 01.1.1-entidad.html     ← Módulo Entidad (Modo A, Simple)
├── 01.1.2-ejercicios.html  ← Módulo Ejercicios Fiscales (Modo A, Simple)
└── 01.1.3-periodos.html    ← Módulo Períodos Contables (Modo A, Simple)
```

### Tokens de diseño (heredados de UI-PJEV)

```css
--pjev-verde-oscuro:  #183125;
--pjev-verde-medio:   #254a37;
--pjev-verde-claro:   #33614a;
--pjev-dorado:        #DEAC50;
--pjev-dorado-dim:    #b58c3a;
--pjev-rojo-vino:     #5e111a;
--pjev-crema:         #F5F0E8;
--pjev-blanco:        #FFFFFF;
--pjev-texto:         #1A1A1A;
--pjev-texto-muted:   #5A5A5A;
--pjev-borde:         #D4C9B5;
```

---

## Módulos documentados hasta ahora

### 01.1.1 Entidad

**Modo A · Tipo Simple**  
Ruta: `cfg / ent / entidad`

- Tabla: `configuracion.entidad`
- SPs: `fn_leer_entidad` · `fn_crud_entidad`
- RN-01: Solo 1 entidad activa por sistema
- RN-02: RFC = 12 caracteres (persona moral)
- RN-03: `ent_folio_inicial_pd` mínimo = 4 (folios 1–3 reservados)
- RN-04: Softdelete — no existe eliminación física
- Integración: provee ejercicio activo, folio inicial PD y logo a todos los módulos

### 01.1.2 Ejercicios Fiscales

**Modo A · Tipo Simple**  
Ruta: `cfg / ent / ejercicios`

- Tabla: `configuracion.ejercicio`
- SPs: `fn_leer_ejercicios` · `fn_crud_ejercicio` · `fn_activar_ejercicio`
- RN-01: Solo 1 ejercicio activo a la vez
- RN-02: Activación irreversible — no existe desactivación manual
- RN-03: Ejercicio cerrado no acepta transacciones
- Integración: provee contexto de ejercicio a todos los módulos; genera los períodos

### 01.1.3 Períodos Contables

**Modo A · Tipo Simple**  
Ruta: `cfg / ent / periodos`

- Tabla: `configuracion.periodo`
- SPs: `fn_leer_periodos` · `fn_generar_periodos` · `fn_crud_periodo`
- Diferencia clave: los períodos se generan en lote (12 a la vez), nunca individualmente
- RN-01: Solo 1 período abierto a la vez
- RN-02: No se puede enviar a contabilidad si está abierto
- RN-03: Solo generación masiva — no existe POST individual
- RN-04: No duplicar períodos por ejercicio
- Los toggles Abierto/Enviado operan directamente en el grid sin abrir formulario

---

## Pendientes para próximas sesiones

- [ ] Agregar sección de nombre de SP/función en la sección 5 (ya corregido con patch)
- [ ] Continuar con subsistema Clasificadores Presupuestales (01.2.x) — 8 módulos
- [ ] Continuar con subsistema Catálogos (01.3.x) — 9 módulos
- [ ] Continuar con subsistema Seguridad (01.4.x) — 6 módulos
- [ ] Completar módulos de Presupuesto (02.x) — 7 módulos
- [ ] Completar módulos de Contabilidad (03.x) — 5 módulos
- [ ] Completar módulos de CxC (04.x) — 4 módulos
- [ ] Refactorizar SPs de CxP (Cristian) antes de documentar (05.x)
- [ ] Diseñar módulos Modo B: Tesorería (06.x) y Adquisiciones (07.x)

---

*Generado automáticamente al cierre de sesión · 2026-05-26 · SIAF-PJEV · Dix Consultoría*
