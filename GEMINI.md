# Contexto del Proyecto: Manual de Desarrollo SIAF-PJEV

Este archivo (`GEMINI.md`) sirve como base de conocimiento y contexto para el agente de IA que retome el trabajo en este proyecto tras su migración a un nuevo equipo. Lee detenidamente estas instrucciones antes de realizar modificaciones.

## 1. Resumen del Proyecto
Este proyecto pertenece a **Dix Consultoría** (para OAJ-DGA del Poder Judicial del Estado de Veracruz). Su propósito es construir y mantener el **Manual de Desarrollo del SIAF-PJEV**, un sitio web estático detallado que sirve como guía técnica (arquitectura, base de datos, frontend, backend) para el equipo de desarrollo interno (Cristian, Eunice, Daryl).

## 2. Estructura del Directorio
* **Raíz (`/`)**: Contiene múltiples scripts de Python (`add_sec*.py`, `append*.py`, `update_wf*.py`, etc.) que hemos utilizado para procesar, limpiar y extraer datos de manuales en texto plano, PDFs y Excels (`anexo_9.xlsx`, `rf_manual.txt`, `rm_manual.txt`, `procesos_presupuesto.json`) para automatizar la inyección de código y contenido en los HTMLs.
* **`sitio_web/`**: Contiene el código fuente del manual. Es un sitio web estático (HTML, CSS, JS puro) para facilitar su distribución sin depender de entornos complejos. Incluye carpetas para los distintos subsistemas (cfg, presupuesto, contabilidad, ingresos, etc.) y un subdirectorio `inicio/` con los estándares de arquitectura.
* **Base de conocimiento**: Archivos clave como `knowledge_base.txt` y `chat_manual_dev_siaf.md` contienen el historial de sesiones de trabajo, prompts y decisiones arquitectónicas tomadas con el director del proyecto (Julio).

## 3. Reglas Arquitectónicas y de Desarrollo (SIAF-PJEV)
Cuando se documente un nuevo módulo, se deben respetar las siguientes reglas técnicas del ecosistema del SIAF:

* **Base de Datos (PostgreSQL)**:
  * Dividida en esquemas lógicos (`nav`, `config`, `contabilidad`, `presupuesto`, etc.).
  * **Soft-delete obligatorio**: `estatus_registro = 0`, nunca hacer `DELETE`.
  * **Auditoría obligatoria**: Todas las tablas tienen `usuario_c`, `fecha_c`, `usuario_m`, `fecha_m`.
* **Stored Procedures (SPs)**:
  * Convención de nombres estricta: `fn_leer_[entidad]` y `fn_crud_[entidad]`.
  * Estructura de retorno (JSONB): `{ "error": 0, "mensaje": "OK", "data": {...} }`. (`0` = Éxito, `-1` = Warning de negocio, `-2` = Error técnico).
  * Todos los SPs usan `SECURITY DEFINER` y `SET search_path`.
* **Backend (Nest.js + Prisma)**:
  * Las reglas de negocio pesadas viven en Postgres, no en Node.js.
  * Prisma ORM se usa como puente tipado, principalmente consumiendo `$queryRaw` para llamar a los SPs.
* **Frontend (Next.js)**:
  * Los módulos se dividen en **Catálogos Simples** (Grid de lectura + Modal de alta/edición) y **Formularios Compuestos** (Maestro-Detalle, donde el encabezado se guarda antes de poder añadir partidas).

## 4. Estado Actual del Proyecto
* **Logros Fundacionales**: Paleta de colores institucional PJEV (`shared.css`), plantilla canónica de análisis funcional (estándar DOC-08), módulos de Configuración (`01.1.1 Entidad`, `01.1.2 Ejercicios`, `01.1.3 Periodos`) y documentos de estándares de arquitectura (`inicio/`).
* **Logros Recientes (04 · Ingresos - Completo)**:
  * Documentado funcional y técnicamente el subsistema completo de **04 · Ingresos** (7 módulos):
    * `04.1.1 Conceptos de ingreso` (17 conceptos institucionales, CRI y 10 banderas).
    * `04.1.2 Tipos de movimiento de ingreso` (devengado, recaudado, simultáneo, ajuste).
    * `04.1.3 Motivos de ajuste o cancelación` (catálogo tipificado obligatorio para bajas).
    * `04.2.1 Registro de ingresos` (maestro-detalle, 9 estados, distribución multilínea).
    * `04.3.1 Conciliación de ingresos` (cotejo cuádruple: expectativa, banco, distribución y póliza 8.1.5).
    * `04.3.2 Cierre mensual de ingresos` (batería de 13 validaciones V-01 a V-13, bitácora de reapertura).
    * `04.4.1 Informes y control de ingresos` (concentrador de 10 reportes analíticos y enlace CONAC).
  * En **todos** estos módulos se integraron:
    * **Stored Procedures PostgreSQL**: `fn_leer_[entidad]` y `fn_crud_[entidad]` bajo `SECURITY DEFINER`, `SET search_path`, soft-delete y retorno JSONB `{ error: 0, mensaje: "OK", data: [...] }`.
    * **Servicios API REST (Swagger / NestJS)**: Tabla de endpoints HTTP y controlador NestJS con decoradores (`@ApiTags`, `@ApiOperation`, `@UseGuards`).
    * **Regla de Ubicación Mandatoria**: Los SPs y Swagger deben situarse **inmediatamente después del modelo de datos / diccionario de campos**, reenumerando secuencialmente las secciones siguientes (1 a 14/15).
    * **Convergencia con la Matriz de Conversión CONAC (`03.1.2`)**: Los conceptos operan desacoplados; mapean hacia CRI y disparan automáticamente las Matrices B.1 (Devengado), B.2 (Recaudado), B.3 (Simultáneo) o Pasivos/Reversos sin captura manual de cuentas contables.
* **Próximo Objetivo (05 · Cuentas por Pagar - CxP)**:
  * Responsable técnico de desarrollo: Cristian.
  * Catálogos: `05.1.1 Requisitos documentales`, `05.1.2 Tarifas y zonas de viáticos`, `05.1.3 Conceptos de retención y deducción`.
  * Registro: `05.2.1 Afectación del gasto` (existe base en `05.2.3-afectacion-gastos.html`), `05.2.2 Orden de pago`, `05.2.3 Gastos a comprobar`, `05.2.4 Comprobación y revisión de gastos`.
  * Procesos: `05.3.1 Pre-pólizas`, `05.3.2 Programación de pagos`, `05.3.3 Control y entero de retenciones`, `05.3.4 DIOT`, `05.3.5 Fideicomisos`.
  * Informes: `05.4.1 Informes de Cuentas por Pagar`.
  * Integración clave: Conexión con Matriz de Conversión de Egresos (**A.1 Devengado de Gastos** [COG vs Pasivo 2.1.1] y **A.2 Pagado de Gastos** [Pasivo vs Bancos 1.1.1.2]) y con los Reintegros de Personal que retornan por Ingresos (`ING-REI-*`).

## 5. Instrucciones de Continuación para la IA
1. Al crear nuevos HTMLs en `sitio_web/`, respeta la estructura de plantillas con sus secciones obligatorias (Descripción, Marco Normativo, Actores, Flujo, Modelo de Datos, **SPs LEER y ABC**, **Swagger / NestJS**, Reglas de Negocio, Wireframes SVG nativos, Integraciones, Casos de Prueba e Historial).
2. Emplea la misma paleta visual y clases CSS ya definidas en `sitio_web/shared.css`, incluyendo `.code-wrap` y `.method.*` para endpoints.
3. Ubica siempre los SPs y Swagger inmediatamente después del modelo de datos / diccionario de campos.
4. Para los diagramas (Wireframes), usa y adapta los SVGs nativos embebidos tal como se documentó en las primeras sesiones y en Ingresos.
5. Mantén sincronizado `sitio_web/index.html` y el dashboard `sitio_web/pm_actualizacion_2026_08_31.js` con las nuevas opciones documentadas.
6. El repositorio Git vive dentro de `sitio_web/` (remoto `origin master` en `pjevjcbarrales/manual-pjev`). Toda actualización debe consolidarse y commitearse allí.
