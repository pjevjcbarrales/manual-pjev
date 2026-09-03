# Guía de Componentes Frontend e Integración: Manejo de Archivos en SIAF-PJEV

**Proyecto:** Sistema Integral de Administración y Finanzas (SIAF-PJEV)  
**Módulo:** Componentes Frontend Reutilizables para Gestión Documental  
**Frontend:** Next.js / React + Tailwind CSS / Shared CSS institucional PJEV  
**Destinatarios:** Equipo de desarrollo (Cristian, Eunice, Daryl)

---

## 1. Principio de Reutilización

Ningún formulario del SIAF-PJEV debe volver a implementar lógica de subida, barra de progreso, validación de extensiones, previsualización o llamadas directas a APIs de almacenamiento.

El frontend dispone de una suite de **componentes autocontenidos** ubicados en `@/components/files/` que se conectan automáticamente con la API transversal `/api/v1/archivos/`.

---

## 2. Catálogo de Componentes Reutilizables

### 2.1 `<EntityFiles />` (Componente Maestro Transversal)
Es el control principal para vincular expedientes documentales en formularios compuestos (Maestro-Detalle), como `05.2.1 Afectación del Gasto`, `04.2.1 Registro de Ingreso` u `05.2.2 Orden de Pago`.

#### Propiedades (Props):
```typescript
export interface EntityFilesProps {
  modulo: 'presupuesto' | 'contabilidad' | 'cxp' | 'ingresos' | 'rm';
  entidad: string;                  // ej. 'afectacion_gasto'
  registroId: string | number;      // ID en firme o ticket temporal
  esTemporal?: boolean;             // TRUE si el formulario padre aún no guarda
  tiposPermitidos?: string[];       // Filtro de tipos del catálogo DOC-* (opcional)
  soloLectura?: boolean;            // Desactiva acciones de carga y desvinculación
  permitirVersionamiento?: boolean; // Habilita botón de 'Nueva Versión'
  permitirDescarga?: boolean;       // Habilita descarga (default: true)
  permitirPreview?: boolean;        // Habilita modal de vista previa (default: true)
  onCambio?: () => void;            // Callback cuando se añade/remueve un documento
}
```

#### Ejemplo de Uso en Formulario:
```tsx
import { EntityFiles } from '@/components/files/EntityFiles';

export function FormularioAfectacionGasto({ idAfectacion, estadoTramite }) {
  const esSoloLectura = estadoTramite === 'AUTORIZADO' || estadoTramite === 'CANCELADO';

  return (
    <div className="card-seccion">
      <h3 className="titulo-seccion">Expediente Documental y Soporte Legal</h3>
      <p className="texto-ayuda">
        Adjunte los documentos obligatorios conforme a la normativa de gasto y catálogo CADIDO.
      </p>

      <EntityFiles
        modulo="cxp"
        entidad="afectacion_gasto"
        registroId={idAfectacion}
        soloLectura={esSoloLectura}
        permitirVersionamiento={true}
      />
    </div>
  );
}
```

---

### 2.2 `<SingleFileField />` (Campo para Archivo Único)
Diseñado para formularios simples o campos puntuales dentro de un formulario (ej. "Comprobante de Transferencia SPEI", "Oficio de Solicitud").

#### Propiedades:
```typescript
export interface SingleFileFieldProps {
  label: string;
  tipoDocumento: string;            // ej. 'DOC-OFI-SEF'
  documentoActualId?: string;
  nombreArchivoActual?: string;
  requerido?: boolean;
  tamanoMaxMb?: number;             // Default: 15 MB
  formatosAceptados?: string[];     // Default: ['.pdf', '.xml']
  onChange: (documentoId: string | null) => void;
  disabled?: boolean;
}
```

---

### 2.3 `<MultiFileField />` (Área Drag & Drop Masiva)
Permite arrastrar paquetes de comprobantes (ej. 10 facturas XML + PDF simultáneas en una comprobación de viáticos).
* Valida tamaño y extensión en el cliente antes del envío.
* Muestra barras individuales de progreso de subida.
* Calcula el hash SHA-256 preliminar en el navegador (Web Crypto API) para alertar sobre duplicados antes de saturar el ancho de banda.

---

### 2.4 `<FilePreviewModal />` (Visor Documental Seguro)
Renderiza modales flotantes para visualizar archivos sin exponer URLs directas de almacenamiento:
* Soporta visualización en línea para **PDF** (renderizador PDF nativo o PDF.js) e **Imágenes** (PNG, JPEG).
* Panel lateral integrado que exhibe la **Ficha Técnica Archivística**:
  * Código CGCA (Serie / Subserie).
  * Valor documental (Administrativo, Fiscal/Contable, Legal).
  * Plazos de vigencia en Trámite y Concentración según CADIDO.
  * Resumen criptográfico Hash SHA-256.
  * Usuario emisor, fecha y estatus de constancia NOM-151.

---

### 2.5 `<ArchivalBadge />` (Insignia Visual de Clasificación)
Muestra insignias normalizadas de clasificación archivística y reserva:

```tsx
<ArchivalBadge tipo="PUBLICO" />       {/* Insignia Verde: 'Información Pública' */}
<ArchivalBadge tipo="RESERVADO" />     {/* Insignia Amarilla: 'Reserva Transparencia' */}
<ArchivalBadge tipo="CONFIDENCIAL" />  {/* Insignia Roja: 'Datos Personales Confidenciales' */}
<ArchivalBadge tipo="FISCAL_5A" />     {/* Insignia Azul: 'Guarda Contable 5 Años' */}
```

---

## 3. Integración en Flujo de Alta: Registros Nuevos (Manejo de Temporales)

Un reto recurrente es cómo adjuntar archivos cuando el usuario está capturando un nuevo registro que **todavía no tiene un ID asignado en la base de datos**.

### Estrategia Canónica de 3 Pasos:

```text
  PASO 1: Generar Ticket Temporal en el Frontend
          const [ticketTemporal] = useState(() => crypto.randomUUID());
          <EntityFiles esTemporal={true} registroId={ticketTemporal} ... />
                                │
                                ▼
  PASO 2: Guardar Encabezado Principal en Backend
          const res = await api.post('/afectacion-gasto', payload);
          const nuevoId = res.data.id_afectacion;
                                │
                                ▼
  PASO 3: Consolidar Archivos Temporales
          await api.post('/archivos/consolidar', {
            ticket_temporal: ticketTemporal,
            modulo_siaf: 'cxp',
            entidad_origen: 'afectacion_gasto',
            registro_id: nuevoId
          });
```

* Si el usuario cancela la captura o cierra la ventana, los archivos temporales quedarán en estado `es_temporal = TRUE` y serán eliminados automáticamente por el proceso batch de limpieza nocturna (`fn_depurar_archivos_temporales`).

---

## 4. Matriz de Errores y Mensajes al Usuario

El frontend debe presentar mensajes institucionales amigables y pedagógicos, evitando tecnicismos opacos:

| Código Backend | Causa Real | Mensaje UI para el Usuario |
| :--- | :--- | :--- |
| `400 Bad Request` | Archivo excede límite | *"El archivo seleccionado excede el tamaño máximo permitido de 25 MB. Por favor comprima el documento."* |
| `400 Bad Request` | Magic Bytes inválidos | *"Formato no autorizado. El archivo contiene un formato binario no permitido o una extensión alterada."* |
| `409 Conflict` | Hash SHA-256 duplicado | *"Este documento ya existe previamente en el expediente institucional (mismo contenido e integridad). Verifique si intenta adjuntar un duplicado."* |
| `403 Forbidden` | Sin permiso de descarga | *"No cuenta con atribuciones de seguridad para consultar o descargar documentos de este expediente."* |
| `404 Not Found` | Archivo no encontrado | *"El documento solicitado no se encuentra disponible en el almacenamiento institucional o fue deshabilitado."* |
