# Administrador General de Archivos, Seguridad y Preservación Digital (SIAF-PJEV)

**Proyecto:** Sistema Integral de Administración y Finanzas (SIAF-PJEV)  
**Módulo:** Gestión Documental y Archivo de Trámite Digital  
**Normatividad:** Ley General de Archivos (LGA), NOM-151-SCFI-2016, LGTAIP y LGPDPPSO

---

## 1. Administrador General de Archivos (Backoffice PJEV)

El Administrador General de Archivos se ubica en el menú principal:  
`Administración → Gestión Documental y Archivos`

Está concebido para la **Unidad de Archivos Institucionales del PJEV**, la **Contraloría Interna** y auditores autorizados.

### 1.1 Funcionalidades Principales
1. **Buscador Transversal:**
   * Búsqueda en tiempo real por: Nombre original, UUID, Hash SHA-256, Módulo emisor, Entidad relacionada, Folio de trámite, Serie del CGCA, Rango de fechas y Usuario creador.
2. **Tablero de Control de Vigencias Documentales (CADIDO):**
   * Indicador de expedientes en **Archivo de Trámite** activos.
   * Indicador de expedientes en plazo de **Archivo de Concentración** (guarda precautoria de 5 a 10 años).
   * Alertas automáticas de documentos que han cumplido su vigencia para dictaminar su **Baja Documental** o **Transferencia Histórica**.
3. **Ficha Integral de Control Documental:**
   * **Pestaña 1 (Ficha y Previsualización):** Metadatos generales, tamaño, extensión, hash SHA-256 y visor integrado.
   * **Pestaña 2 (Trazabilidad y Relaciones):** Árbol de relaciones polimórficas (a qué pólizas, órdenes de pago o contratos está asociado).
   * **Pestaña 3 (Historial de Versiones):** Línea de tiempo de sustituciones con motivos de cambio y hashes comparativos.
   * **Pestaña 4 (Cadena de Custodia Inmutable):** Registro de cada consulta, descarga, previsualización o baja lógica con fecha, IP y usuario.
   * **Pestaña 5 (Certificación y Cumplimiento NOM-151):** Folio de constancia de conservación emitida por PSC y validez de firmas electrónicas.

---

## 2. Matriz de Seguridad, Roles y Permisos (ACL)

El acceso al subsistema de archivos se rige por un **principio de doble capa**:

```text
               PETICIÓN DE ACCESO A DOCUMENTO
                             │
                             ▼
   ┌────────────────────────────────────────────────────────┐
   │ CAPA 1: Permiso Funcional sobre el Trámite Padre       │
   │ ¿El usuario tiene permiso para consultar la póliza o   │
   │  afectación de gasto asociada a este documento?        │
   └──────────────────────────┬─────────────────────────────┘
                              │ SÍ
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │ CAPA 2: Permisos Específicos del Módulo de Archivos    │
   │ ¿Qué operaciones documentales tiene autorizadas?       │
   └──────────────────────────┬─────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
        VER/PREVIEW       DESCARGAR        MODIFICAR/SUBIR
```

### 2.1 Permisos del Módulo:
* `ARCHIVOS_VER`: Permite visualizar el documento en el visor en línea y consultar metadatos.
* `ARCHIVOS_DESCARGAR`: Permite descargar el binario físico.
* `ARCHIVOS_SUBIR`: Permite adjuntar nuevos documentos a expedientes abiertos.
* `ARCHIVOS_VERSIONAR`: Permite cargar sustituciones o nuevas versiones justificadas.
* `ARCHIVOS_DESVINCULAR`: Permite retirar un documento de un trámite en borrador.
* `ARCHIVOS_DESACTIVAR`: Soft-delete de documentos.
* `ARCHIVOS_CLASIFICAR`: Reservado a la Unidad de Transparencia para clasificar documentos como Reservados o Confidenciales.
* `ARCHIVOS_ADMIN`: Acceso irrestricto al Administrador General y dictaminación de bajas documentales.

---

## 3. Preservación Digital a Largo Plazo y NOM-151-SCFI-2016

Conforme al Título Cuarto de la Ley General de Archivos y la NOM-151:

1. **Inmutabilidad y No Repudio:**
   * Una vez que un trámite pasa de estado borrador a **Aprobado / Contabilizado**, sus documentos asociados adquieren estatus de **Solo Lectura Inmutable (WORM lógico)**.
   * No se permite la alteración directa del binario. Cualquier actualización exige registrar una nueva versión con justificación auditada.
2. **Digitalización Certificada:**
   * Los documentos en soporte papel escaneados se asocian con su **Constancia de Conservación NOM-151** emitida por un Prestador de Servicios de Certificación (PSC) acreditado por la Secretaría de Economía, garantizando validez probatoria plena ante tribunales y entes fiscalizadores (ORFIS / ASF).
3. **Formatos Abiertos para Preservación (Art. 47 LGA):**
   * Se promueve el estándar internacional **PDF/A** (ISO 19005) para documentos definitivos, garantizando que el documento se pueda visualizar fielmente en el futuro sin depender de fuentes instaladas o software de terceros.

---

## 4. Destino Final y Dictamen de Baja Documental

De acuerdo con los Arts. 11, 13 y 14 de la LGA:

* Ningún documento de archivo del PJEV puede ser destruido arbitrariamente.
* Cuando un documento cumple su vigencia en el Archivo de Concentración (ej. 5 años para facturas de gasto ordinario):
  1. El Administrador de Archivos genera la **Cédula de Valoración Documental**.
  2. Si carece de valores históricos o testimoniales, se formula el **Acta de Baja Documental**.
  3. Una vez aprobada por el Comité de Archivos del PJEV y con la autorización correspondiente del Consejo Estatal de Archivos / AGN, se procede a la deshabilitación formal y purga controlada, conservando a perpetuidad la ficha técnica de metadatos y el acta de baja en la bitácora inmutable.
  4. Si posee valores históricos, se transfiere de forma definitiva al **Archivo Histórico del PJEV** en formato abierto para su custodia permanente.
