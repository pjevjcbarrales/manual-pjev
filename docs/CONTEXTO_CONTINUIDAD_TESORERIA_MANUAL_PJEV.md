# Contexto de continuidad — Tesorería en el manual SIAF-PJEV

Fecha de corte: 31 de agosto de 2026.

## Propósito

Este documento permite continuar en el proyecto `sitio_web` la actualización del manual y de su dashboard, después de la revisión funcional realizada en el repositorio SIAF-PJEV.

La decisión principal fue dejar de representar Tesorería como un solo sistema. Para efectos del manual y del tablero de seguimiento se dividió en cuatro sistemas independientes:

1. Ingresos.
2. Cuentas por Pagar.
3. Pagos.
4. Repositorio CFDI.

La estructura aún es una propuesta funcional de trabajo. No debe interpretarse como certificación normativa ni como definición definitiva de reglas contables o presupuestarias.

## Responsables acordados

| Sistema | Responsable |
| --- | --- |
| 04 Ingresos | Daryl |
| 05 Cuentas por Pagar | Eunice |
| 06 Pagos | Eunice |
| 07 Repositorio CFDI | Cristian |

La asignación se aplica a todos los módulos que pertenecen a cada sistema.

## Relación vigente: sistema, subsistema y módulos

### 04 Ingresos

Responsable: Daryl.

#### 04.1 Catálogos

- `04.1.1` Conceptos de ingreso.
- `04.1.2` Tipos de movimiento de ingreso.

Las fuentes de financiamiento ya se consideran en Configuración Inicial. Las cuentas recaudadoras deben validarse contra la matriz de conversión antes de crear otro catálogo. Los conceptos de reintegro pueden resolverse como subtipo de concepto de ingreso.

#### 04.2 Registro

- `04.2.1` Registro y seguimiento de ingresos.

La propuesta concentra los distintos tipos de registro en un solo módulo parametrizado por tipo y subtipo, evitando opciones separadas cuando comparten captura, reglas y ciclo de vida.

#### 04.3 Procesos

- `04.3.1` Conciliación de ministraciones.
- `04.3.2` Cierre mensual de ingresos.

La solicitud y recepción de ministración, su aplicación presupuestaria, cancelación y corrección deben convivir dentro del registro y seguimiento mediante acciones y estados. No se plantean como módulos independientes mientras no exista una diferencia funcional que lo justifique.

#### 04.4 Informes

- `04.4.1` Informes y control de ingresos.

La integración mensual para Contabilidad quedó pendiente de validar, porque puede existir ya una integración o fuente equivalente en otros componentes.

### 05 Cuentas por Pagar

Responsable: Eunice.

#### 05.1 Catálogos

- `05.1.1` Requisitos documentales.
- `05.1.2` Tarifas y zonas de viáticos.
- `05.1.3` Conceptos de retención y deducción.

Los tipos y subtipos de afectación del gasto deben reutilizar las matrices de conversión si ya son su fuente de verdad. Los conceptos de retención y deducción deben validarse contra la implementación existente antes de duplicar catálogo o lógica.

#### 05.2 Registro

- `05.2.1` Afectación del gasto.
- `05.2.2` Orden de pago.
- `05.2.3` Gastos a comprobar.
- `05.2.4` Comprobación y revisión de gastos.
- `05.2.5` Pre-pólizas.

La comprobación del gasto y la recepción/revisión de gastos se consolidaron en un solo módulo. Debe contemplar comprobaciones, peajes, recibos y demás evidencias, con captura apoyada por el Repositorio CFDI/XML y prevención de facturas duplicadas. Está relacionado con Gastos a comprobar y con el expediente documental.

La reposición de gastos se entiende vinculada al fondo rotatorio y no quedó como módulo separado en esta estructura. Las obligaciones de terceros institucionales deben validarse para evitar duplicidad con Afectación del gasto y con el control de retenciones.

#### 05.3 Procesos

- `05.3.1` Programación de pagos.
- `05.3.2` Control y entero de retenciones.
- `05.3.3` DIOT.
- `05.3.4` Movimientos de fideicomisos.

#### 05.4 Informes

- `05.4.1` Informes de Cuentas por Pagar.

### 06 Pagos

Responsable: Eunice.

#### 06.1 Catálogos

- `06.1.1` Medios de pago.

Los conceptos bancarios se conservan como referencia funcional, pero no se crearon como opción separada en el tablero actual. Las cuentas pagadoras deben validarse contra la matriz correspondiente y las chequeras contra Configuración Inicial. Los estados del pago son estados internos del flujo, no un catálogo navegable. Los instrumentos de inversión pueden modelarse como tipo de concepto bancario si el análisis funcional lo confirma.

#### 06.2 Registro

- `06.2.1` Bandeja de pagos.
- `06.2.2` Registro y control de pagos.
- `06.2.3` Traspasos entre cuentas.
- `06.2.4` Inversiones y rendimientos — segunda etapa.

Cheque y transferencia electrónica se definen dentro del registro del pago, incluyendo los datos bancarios aplicables como la CLABE. Autorización, liberación y aplicación del pago forman parte del flujo y de sus estados, no de opciones independientes. El pago a terceros institucionales debe resolverse dentro del registro cuando no requiera reglas propias.

Los movimientos de inversión se consolidaron bajo Inversiones y rendimientos, marcado para segunda etapa. La cuantificación de disponibilidad financiera y la programación bancaria siguen pendientes de validación funcional antes de convertirse en módulos.

#### 06.3 Procesos

- `06.3.1` Conciliación bancaria.

Las cancelaciones y devoluciones deben contemplarse como acciones controladas del flujo de pagos.

#### 06.4 Informes

- `06.4.1` Informes de pagos y bancos.

Este módulo agrupa pagos diarios; programados, aplicados y cancelados; libro de bancos; disponibilidad financiera; cheques y transferencias; inversiones y rendimientos; y gastos de operación y liberación de recursos.

### 07 Repositorio CFDI

Responsable: Cristian. Todo el sistema está marcado para segunda etapa.

#### 07.1 Registro

- `07.1.1` Bóveda CFDI.

Debe contemplar carga de XML y PDF, recepción de complementos de pago y documentos no fiscales. Los tipos de CFDI, tipos de relación, estados de validación, motivos de rechazo y tipos de expediente son clasificaciones internas o catálogos de soporte, no necesariamente opciones independientes del menú.

#### 07.2 Procesos

- `07.2.1` Validación y vinculación fiscal.

Alcance previsto: validación ante el SAT, detección de duplicados, vinculación con gasto, orden y pago, relación con viáticos y sujetos a comprobar, control de complementos e integración del expediente digital.

#### 07.3 Informes

- `07.3.1` Control y auditoría CFDI.

Debe informar CFDI inválidos o duplicados, comprobantes sin vincular, complementos pendientes, expedientes incompletos y trazabilidad documental.

## Cambios realizados en el dashboard

El archivo modificado es `pm_actualizacion_2026_08_31.js`. Es una capa de actualización cargada después de `pm_data.js` por `dashboard_pm.html`.

Cambios aplicados:

- Se eliminó del tablero la antigua reasignación de Bóveda CFDI dentro de Contabilidad (`03.2.5`).
- Se sustituyó el sistema único `04 Tesorería` por los cuatro sistemas descritos en este documento.
- Materiales se renumeró de `05` a `08` para liberar la numeración de los nuevos sistemas.
- Se agregó el reconocimiento del estado `Segunda etapa` en la normalización visual.
- Se asignaron responsables de forma transversal por sistema.

Estado comprobado del tablero después de la reorganización:

| Indicador | Total |
| --- | ---: |
| Sistemas | 8 |
| Subsistemas | 38 |
| Módulos | 132 |

Distribución verificada:

| Sistema | Módulos |
| --- | ---: |
| 01 Configuración Inicial | 34 |
| 02 Presupuesto | 21 |
| 03 Contabilidad | 36 |
| 04 Ingresos | 6 |
| 05 Cuentas por Pagar | 13 |
| 06 Pagos | 7 |
| 07 Repositorio CFDI | 3 |
| 08 Materiales | 12 |

No se detectaron identificadores de módulo duplicados.

## Verificaciones realizadas

- `node --check pm_actualizacion_2026_08_31.js` sin errores.
- Evaluación conjunta de `pm_data.js` y la capa de actualización.
- Comprobación de responsables: seis módulos de Ingresos asignados a Daryl; trece de Cuentas por Pagar y siete de Pagos asignados a Eunice; tres de Repositorio CFDI asignados a Cristian.
- Revisión visual local de `dashboard_pm.html`: indicadores, filtros y acordeones correctos, sin errores en consola.
- `git diff --check` sin errores de espacios; Git sólo advirtió la conversión futura de LF a CRLF en Windows.

## Consideraciones para continuar

1. Leer primero este archivo y revisar el estado de Git antes de editar. El repositorio contenía archivos no rastreados ajenos a este cambio; deben preservarse.
2. Mantener `pm_data.js` como base histórica y concentrar esta reorganización en `pm_actualizacion_2026_08_31.js`, salvo que se acuerde consolidar ambas fuentes.
3. Crear o actualizar las páginas del manual de los sistemas 04 a 07 sólo después de confirmar el alcance de cada módulo.
4. Validar en el sistema SIAF las fuentes de verdad pendientes: matrices de conversión, cuentas recaudadoras y pagadoras, chequeras, retenciones y estados internos.
5. Evitar duplicar catálogos o reglas ya implementados. Cuando una operación sea una acción o transición del mismo expediente, conservarla dentro del módulo principal.
6. Para el Repositorio CFDI, diseñar la integración con comprobaciones y gastos a comprobar, incluyendo unicidad de comprobantes, validación fiscal, vínculos y trazabilidad de expediente.
7. Después de cualquier cambio, ejecutar validación sintáctica y revisar visualmente `dashboard_pm.html`.

## Documentos de origen consultados

En el repositorio SIAF-PJEV se consultaron como antecedentes:

- `docs/CONTEXTO_CONTINUIDAD_SIAF_PJEV.md`.
- `docs/REVISION_CUMPLIMIENTO_SIAF_PJEV.md`.

Estos documentos contienen contexto general del sistema y revisión de cumplimiento; el presente archivo concentra únicamente la continuidad necesaria para el manual y la reorganización de Tesorería.
