# Contexto y Marco de Diseño: Sistema 04 · Ingresos (SIAF-PJEV)

**Fecha de consolidación:** Septiembre de 2026  
**Subsistema:** `04 Ingresos`  
**Responsable Técnico:** Eunice  
**Analista / Dirección:** Julio César  

---

## 1. Fundamentación Normativa y Documental

El análisis, modelado y diseño funcional del sistema de Ingresos se sustenta en:
1. **Marco Jurídico y Contable Gubernamental:**
   - Ley General de Contabilidad Gubernamental (LGCG).
   - Normatividad y Postulados Básicos del CONAC.
   - Manual de Contabilidad Gubernamental (CONAC).
   - Clasificador por Rubros de Ingresos (CRI) y momentos contables de los ingresos: *Estimado*, *Modificado*, *Devengado* y *Recaudado*.
2. **Normatividad Institucional PJEV:**
   - Manual Específico de Procedimientos de Recursos Financieros del Poder Judicial del Estado de Veracruz.
   - Procedimientos de Cuentas por Cobrar, Caja Central, Contabilidad y Conciliación de Ministraciones.
3. **Evidencia Documental Observada (Fuentes Primarias):**
   - Oficios y comunicaciones oficiales de ministraciones de SEFIPLAN.
   - Solicitudes y comprobaciones de radicación de recursos.
   - Órdenes o números de trámite presupuestal.
   - Fichas, avisos y extractos de depósitos bancarios institucionales.
   - Referencias bancarias (claves de rastreo SPEI, autorizaciones).
   - Fechas de operación y fechas valor de disponibilidad de fondos.
   - Sellos y acuses de recepción institucional.
   - Distribuciones programáticas por órgano, capítulo y fuente de financiamiento.
   - Otros ingresos: contratos de arrendamiento (rentas), reintegros de viáticos y rendimientos de cuentas productivas.

---

## 2. Decisión de Alcance Arquitectónico

> **Regla de Alcance Estricta (Fase Actual):**  
> En esta etapa **no se administrarán oficios, expedientes documentales, archivos digitales (PDF/XML), firmas electrónicas ni sellos/acuses digitales**.  
> Para efectos de trazabilidad administrativa, el sistema provee exclusivamente un campo alfanumérico opcional de **Referencia externa** (ej. número de oficio, contrato o solicitud). Toda la operación se enfoca en el control financiero y presupuestario.

---

## 3. Catálogos Propios de Ingresos

Los tres catálogos que residen en `04.1 Catálogos` cuentan con plena justificación funcional y técnica:

### 3.1 `04.1.1 Conceptos de ingreso`
Clasificador maestro que categoriza el rubro o motivo por el que ingresa dinero a la institución:
- **Conceptos cubiertos:** Ministraciones, Rentas, Reintegros de trabajadores, Rendimientos financieros, Cheques caducos, Pagos rechazados, Reposición de credenciales, y Otros ingresos institucionales.
- **Relaciones y atributos que debe gobernar:**
  - Código CRI correspondiente.
  - Matriz contable asociada (cuentas 4.x de ingreso patrimonial y cuentas de orden 8.1.x).
  - Reglas de reconocimiento contable.
  - Bandera: *Permite devengado previo* (esperado).
  - Bandera: *Permite devengado y recaudado simultáneo* (en firme).
  - Bandera: *Permite recepción parcial* (cobro en parcialidades).
  - Bandera: *Requiere distribución por capítulo y fuente* (obligatoria para techos de gasto).
  - Vigencia y estatus de registro.

### 3.2 `04.1.2 Tipos de movimiento de ingreso`
Gobierna los momentos operativos y transaccionales del ciclo de captación:
- `Devengado`: Nace el derecho de cobro formal.
- `Recaudado`: Percepción efectiva en cuentas bancarias.
- `Devengado y recaudado simultáneo`: Registro directo de ingresos en firme (ej. rendimientos bancarios).
- `Ajuste`: Corrección autorizada sobre importes o atributos sin anulación total.
- `Cancelación`: Anulación lógica del registro por improcedencia.
- `Reverso`: Cancelación o contrasiento de una afectación contable/presupuestaria previa.
- `Reclasificación`: Reasignación de concepto, fuente o destino sin modificar el importe líquido percibido.

### 3.3 `04.1.3 Motivos de ajuste o cancelación`
Catálogo estandarizado de auditoría y control institucional para justificar cualquier cambio o anulación:
- *Error de captura*.
- *Registro duplicado*.
- *Importe incorrecto*.
- *Cuenta bancaria incorrecta*.
- *Concepto o CRI incorrecto*.
- *Fuente de financiamiento incorrecta*.
- *Depósito no identificado*.
- *Corrección contable*.

---

## 4. Catálogos Transversales Reutilizados

Para evitar duplicidad y mantener una única fuente de la verdad, el sistema de Ingresos **reutiliza directamente** los catálogos administrados por `01 · Configuración Inicial` y el subsistema contable:

| Catálogo Transversal | Ubicación Canónica | Uso en Ingresos |
| :--- | :--- | :--- |
| **Clasificador por Rubros de Ingresos (CRI)** | `01.2.7` / Configuración | Define la naturaleza económica del recurso ingresado. |
| **Clasificador por Objeto del Gasto (COG) y Capítulos** | `01.2.2` / Configuración | Asigna el destino presupuestal del gasto (1000, 2000, 3000, 5000). |
| **Fuentes de Financiamiento** | `01.2.4` / Configuración | Identifica el origen legal del recurso (Fiscales, Propios, Federales). |
| **Fondos o Recursos Específicos** | `01.2.4` / Configuración | Bolsas y fondos etiquetados asociados a la fuente. |
| **Plan de Cuentas Institucional (COA)** | `03.1.1` / Contabilidad | Cuentas de orden de ingresos (8.1.x) y activo circulante (1.1.x). |
| **Matrices Contables de Conversión** | `03.1.2` / Contabilidad | Reglas automáticas para generar los asientos de devengo y recaudo. |
| **Bancos** | `01.4.1` / Bancarios | Instituciones financieras pagadoras o receptoras. |
| **Cuentas Bancarias Institucionales** | `01.4.2` / Bancarios | Cuentas recaudadoras y concentradoras del PJEV. |
| **Órganos del PJEV y Unidades Administrativas** | `01.2.1` / Configuración | Unidades ejecutoras receptoras de la asignación presupuestal. |
| **Ejercicios Fiscales y Periodos** | `01.1.2` / `01.1.3` | Ejercicio activo (año) y mes contable/presupuestal (1 a 12). |
| **Usuarios, Roles y Permisos** | `01.5.4` / `01.5.5` | Control de accesos, perfiles de captura, revisión y auditoría. |

---

## 5. Módulo de Operación: `04.2.1 Registro de ingresos`

### 5.1 Las Dos Puertas de Entrada

1. **A. Ingreso Esperado:**  
   Se detona cuando el área recibe aviso formal previo de que llegará un recurso (ej. oficio de SEFIPLAN de ministración, contrato de renta o solicitud de reintegro).  
   *Flujo:*  
   $$\text{Registro Esperado} \longrightarrow \text{Espera del Depósito} \longrightarrow \text{Recepción Total o Parcial} \longrightarrow \text{Aplicación} \longrightarrow \text{Contabilización} \longrightarrow \text{Conciliación}$$

2. **B. Ingreso Recibido:**  
   Se detona cuando primero se detecta y valida el depósito bancario en firme en el estado de cuenta institucional, exista o no un aviso previo.  
   *Flujo:*  
   $$\text{Depósito Recibido} \longrightarrow \text{Identificación} \longrightarrow \text{Clasificación y Distribución} \longrightarrow \text{Aplicación} \longrightarrow \text{Contabilización} \longrightarrow \text{Conciliación}$$

### 5.2 Distribución Presupuestaria Obligatoria
Cada ingreso debe desglosarse en una o varias líneas de destino con:
- **Capítulo de Gasto:** destino presupuestario del recurso.
- **Fuente de Financiamiento:** procedencia y condición financiera.
- **Fondo o Recurso Específico:** cuando aplique según la fuente.
- **Órgano o Unidad Administrativa:** ejecutora que recibe el techo.
- **Importe Distribuido:** valor monetario de la línea.

$$\sum \text{Importe Distribuido} = \text{Importe Total}$$

### 5.3 Cuadrilátero de Distinciones Conceptuales

```
┌─────────────────────────────────────────────────────────────┐
│ CRI               → Naturaleza u origen del ingreso         │
│ Capítulo de Gasto → Destino presupuestario del recurso       │
│ Fuente de Finan.  → Procedencia y condición financiera       │
│ Cuenta Bancaria   → Ubicación física/financiera del dinero   │
└─────────────────────────────────────────────────────────────┘
```
*Ninguno de estos cuatro conceptos debe confundirse, fusionarse ni sustituirse entre sí.*

---

## 6. Principios Rectores de Diseño de Interfaces y Procesos

1. **Enfoque Centrado en el Usuario Operativo:** Las interfaces deben guiar el flujo natural de trabajo de Tesorería; el usuario no debe navegar conceptos contables abstractos.
2. **Generación Automática de Momentos Contables:** El devengo y la recaudación presupuestaria y contable deben generarse como consecuencia del registro administrativo validado.
3. **Soporte de Depósitos Parciales:** Un ingreso esperado puede recibirse en varias exhibiciones; el sistema debe actualizar el saldo pendiente acumulativo.
4. **Relación 1 a N:** Un solo ingreso esperado puede vincularse a múltiples depósitos bancarios individuales.
5. **Depósitos Transitorios No Identificados:** Los abonos bancarios cuya procedencia no esté aclarada deben poder registrarse en un estado especial sin detener la operación diaria de caja.
6. **Consistencia de Catálogos:** Cero duplicidad de catálogos transversales.
7. **Trazabilidad Total:** Todo ajuste o cancelación debe exigir el motivo institucional tipificado (catálogo `04.1.3`) y registrar usuario y fecha de modificación.
8. **Diferenciación Expresa de Fuentes:** Toda documentación técnica debe clasificar sin ambigüedad si un requisito es:
   - *Requerimiento normativo*.
   - *Evidencia del Manual del PJEV*.
   - *Evidencia de documentos fuente*.
   - *Propuesta de diseño del nuevo sistema*.
