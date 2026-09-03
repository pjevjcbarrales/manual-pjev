# Arquitectura Backend: Servicio de Archivos y Storage en NestJS (SIAF-PJEV)

**Proyecto:** Sistema Integral de Administración y Finanzas (SIAF-PJEV)  
**Módulo:** Subsistema Transversal de Gestión Documental y Archivos  
**Backend:** NestJS + Prisma ORM + PostgreSQL (`archivos.*`)  
**Estándar de Arquitectura:** `00-estandares-rest.html` y `00-estandares-prisma.html`

---

## 1. Abstracción del Proveedor de Almacenamiento (Storage Driver)

Para cumplir con la independencia tecnológica del PJEV y permitir almacenamiento tanto en servidores *on-premise* (NAS local) como en buckets de objetos (MinIO institucional / S3), se implementa el patrón **Strategy**:

```typescript
// src/files/storage/file-storage.interface.ts
import { Readable } from 'stream';

export interface FileMetadata {
  originalName: string;
  mimeType: string;
  sizeBytes: number;
  hashSha256: string;
  modulo: string;
  ejercicio: number;
  mes: number;
}

export interface UploadResult {
  storagePath: string;     // ej. 'siaf/cxp/2026/09/uuid.pdf'
  storageUrl?: string;
  driverName: 'local' | 'minio' | 's3';
}

export interface IFileStorageDriver {
  upload(stream: Readable, path: string, metadata: FileMetadata): Promise<UploadResult>;
  download(path: string): Promise<Readable>;
  delete(path: string): Promise<boolean>;
  exists(path: string): Promise<boolean>;
  getSignedUrl(path: string, expiresInSeconds: number): Promise<string>;
}
```

### 1.1 Implementaciones Soportadas
* **`LocalStorageDriver`**: Escribe en un volumen montado institucional (ej. `/var/siaf/storage/` o carpeta compartida NAS CIFS/NFS), organizando las carpetas por `{modulo}/{ejercicio}/{mes}/`.
* **`MinioStorageDriver` / `S3StorageDriver`**: Utiliza el cliente oficial `@aws-sdk/client-s3` para comunicarse con la instancia MinIO auto-hospedada del Poder Judicial.

---

## 2. Pipeline de Validación de Seguridad e Integridad

No se confía en los datos declarados por el navegador web:
1. **Magic Bytes (Firma Binaria Real):** Se inspecciona el encabezado de los primeros 4100 bytes mediante la librería `file-type` antes de procesar el archivo. Si el binario real no coincide con los tipos permitidos, la petición es abortada de inmediato (`400 Bad Request`).
2. **Cálculo de Hash Criptográfico SHA-256:** Se calcula el hash mediante `crypto.createHash('sha256')` a lo largo del stream de subida, evitando guardar archivos corruptos o incompletos.
3. **Control de Duplicados:** Se coteja el hash calculado contra la base de datos para alertar oportunamente si el archivo ya existe.

```typescript
// src/files/pipes/file-validation.pipe.ts
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';
import { fromBuffer } from 'file-type';

const ALLOWED_MIME_TYPES = [
  'application/pdf',
  'text/xml',
  'application/xml',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // xlsx
  'text/csv',
  'image/png',
  'image/jpeg',
  'image/tiff',
];

const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25 MB

@Injectable()
export class FileValidationPipe implements PipeTransform {
  async transform(file: Express.Multer.File) {
    if (!file) {
      throw new BadRequestException('No se ha proporcionado ningún archivo.');
    }

    if (file.size > MAX_FILE_SIZE) {
      throw new BadRequestException(`El archivo excede el tamaño máximo permitido de 25 MB.`);
    }

    // Inspección de magic bytes
    const type = await fromBuffer(file.buffer);
    if (!type || !ALLOWED_MIME_TYPES.includes(type.mime)) {
      throw new BadRequestException(`Tipo de archivo no permitido o firma binaria inválida (${type?.mime || 'desconocido'}).`);
    }

    return file;
  }
}
```

---

## 3. Data Transfer Objects (DTOs) con Decoradores Swagger

```typescript
// src/files/dto/file-operations.dto.ts
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsString, IsNotEmpty, IsUUID, IsOptional, IsBoolean, IsInt, IsIn } from 'class-validator';

export class SubirArchivoDto {
  @ApiProperty({ description: 'Módulo funcional emisor', example: 'cxp' })
  @IsString()
  @IsNotEmpty()
  modulo_siaf: string;

  @ApiPropertyOptional({ description: 'Código del CGCA según LGA', example: 'PJEV-DGA-RF-01.01' })
  @IsString()
  @IsOptional()
  cgca_codigo?: string;

  @ApiPropertyOptional({ description: 'Valor documental según CADIDO', enum: ['ADMINISTRATIVO', 'LEGAL', 'FISCAL_CONTABLE', 'TECNICO'] })
  @IsIn(['ADMINISTRATIVO', 'LEGAL', 'FISCAL_CONTABLE', 'TECNICO'])
  @IsOptional()
  valor_documental?: string;

  @ApiPropertyOptional({ description: 'Nivel de clasificación de acceso', enum: ['PUBLICO', 'RESERVADO', 'CONFIDENCIAL'] })
  @IsIn(['PUBLICO', 'RESERVADO', 'CONFIDENCIAL'])
  @IsOptional()
  clasificacion_acceso?: string;

  @ApiPropertyOptional({ description: 'Descripción o extracto del archivo' })
  @IsString()
  @IsOptional()
  descripcion?: string;

  @ApiPropertyOptional({ description: 'Indica si es una carga temporal previa a guardar registro padre' })
  @IsBoolean()
  @IsOptional()
  es_temporal?: boolean;

  @ApiPropertyOptional({ description: 'Token de sesión temporal del formulario' })
  @IsUUID()
  @IsOptional()
  ticket_temporal?: string;
}

export class VincularDocumentoDto {
  @ApiProperty({ description: 'UUID del documento ya almacenado' })
  @IsUUID()
  @IsNotEmpty()
  documento_id: string;

  @ApiProperty({ description: 'Módulo del SIAF', example: 'cxp' })
  @IsString()
  @IsNotEmpty()
  modulo_siaf: string;

  @ApiProperty({ description: 'Tabla o entidad padre', example: 'afectacion_gasto' })
  @IsString()
  @IsNotEmpty()
  entidad_origen: string;

  @ApiProperty({ description: 'ID del registro padre en su tabla', example: '852' })
  @IsString()
  @IsNotEmpty()
  registro_id: string;

  @ApiProperty({ description: 'Clave del tipo documental del catálogo', example: 'DOC-CON-TRA' })
  @IsString()
  @IsNotEmpty()
  tipo_documento: string;

  @ApiPropertyOptional({ description: 'Define si el trámite exige forzosamente este archivo' })
  @IsBoolean()
  @IsOptional()
  es_obligatorio?: boolean;

  @ApiPropertyOptional({ description: 'Descripción u observación' })
  @IsString()
  @IsOptional()
  descripcion?: string;
}

export class NuevaVersionDto {
  @ApiProperty({ description: 'Motivo fundado y motivado del cambio o sustitución (LGA Art. 45)' })
  @IsString()
  @IsNotEmpty()
  motivo_cambio: string;
}
```

---

## 4. Controlador REST Canónico (`FilesController`)

```typescript
// src/files/files.controller.ts
import {
  Controller, Post, Get, Delete, Patch, Param, Body, Query,
  UseInterceptors, UploadedFile, UseGuards, Res, Req, HttpStatus
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth, ApiConsumes } from '@nestjs/swagger';
import { Response, Request } from 'express';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { FilesService } from './files.service';
import { FileValidationPipe } from './pipes/file-validation.pipe';
import { SubirArchivoDto, VincularDocumentoDto, NuevaVersionDto } from './dto/file-operations.dto';

@ApiTags('Transversal - Gestión Documental y Archivos')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('archivos')
export class FilesController {
  constructor(private readonly filesService: FilesService) {}

  @Post('subir')
  @ApiOperation({ summary: 'Subir archivo y registrar metadatos archivísticos conforme a LGA y NOM-151' })
  @ApiConsumes('multipart/form-data')
  @UseInterceptors(FileInterceptor('file'))
  async subirArchivo(
    @UploadedFile(FileValidationPipe) file: Express.Multer.File,
    @Body() dto: SubirArchivoDto,
    @Req() req: Request,
  ) {
    const usuario = (req.user as any)?.username || 'SISTEMA';
    const ip = req.ip || req.socket.remoteAddress;
    const userAgent = req.headers['user-agent'] || '';

    return this.filesService.subirArchivo(file, dto, usuario, ip, userAgent);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Obtener metadatos completos y clasificación de un archivo' })
  async obtenerMetadatos(@Param('id') id: string) {
    return this.filesService.obtenerPorId(id);
  }

  @Get(':id/descargar')
  @ApiOperation({ summary: 'Descargar archivo por stream registrando evento en auditoría' })
  async descargarArchivo(
    @Param('id') id: string,
    @Req() req: Request,
    @Res() res: Response,
  ) {
    const usuario = (req.user as any)?.username || 'SISTEMA';
    const ip = req.ip;
    const { stream, documento } = await this.filesService.obtenerStreamDescarga(id, usuario, ip, 'DESCARGA');

    res.setHeader('Content-Type', documento.mime_type);
    res.setHeader('Content-Disposition', `attachment; filename="${encodeURIComponent(documento.nombre_original)}"`);
    res.setHeader('Content-Length', documento.tamanio_bytes);

    stream.pipe(res);
  }

  @Get(':id/previsualizar')
  @ApiOperation({ summary: 'Visualizar archivo en línea (PDF / Imágenes)' })
  async previsualizarArchivo(
    @Param('id') id: string,
    @Req() req: Request,
    @Res() res: Response,
  ) {
    const usuario = (req.user as any)?.username || 'SISTEMA';
    const ip = req.ip;
    const { stream, documento } = await this.filesService.obtenerStreamDescarga(id, usuario, ip, 'VISUALIZACION');

    res.setHeader('Content-Type', documento.mime_type);
    res.setHeader('Content-Disposition', `inline; filename="${encodeURIComponent(documento.nombre_original)}"`);
    stream.pipe(res);
  }

  @Post('vincular')
  @ApiOperation({ summary: 'Vincular documento con un registro de trámite de cualquier módulo' })
  async vincularDocumento(@Body() dto: VincularDocumentoDto, @Req() req: Request) {
    const usuario = (req.user as any)?.username || 'SISTEMA';
    const ip = req.ip;
    return this.filesService.vincularRegistro(dto, usuario, ip);
  }

  @Delete(':id/desvincular/:relacionId')
  @ApiOperation({ summary: 'Desvincular documento de un registro del SIAF' })
  async desvincularDocumento(
    @Param('id') id: string,
    @Param('relacionId') relacionId: string,
    @Query('motivo') motivo: string,
    @Req() req: Request,
  ) {
    const usuario = (req.user as any)?.username || 'SISTEMA';
    const ip = req.ip;
    return this.filesService.desvincularRegistro(relacionId, motivo, usuario, ip);
  }

  @Post(':id/versionar')
  @ApiOperation({ summary: 'Registrar una nueva versión de un documento existente' })
  @ApiConsumes('multipart/form-data')
  @UseInterceptors(FileInterceptor('file'))
  async nuevaVersion(
    @Param('id') id: string,
    @UploadedFile(FileValidationPipe) file: Express.Multer.File,
    @Body() dto: NuevaVersionDto,
    @Req() req: Request,
  ) {
    const usuario = (req.user as any)?.username || 'SISTEMA';
    const ip = req.ip;
    const userAgent = req.headers['user-agent'] || '';
    return this.filesService.crearNuevaVersion(id, file, dto.motivo_cambio, usuario, ip, userAgent);
  }

  @Get('entidad/:modulo/:entidad/:registroId')
  @ApiOperation({ summary: 'Listar todos los documentos asociados a un trámite del SIAF' })
  async listarPorEntidad(
    @Param('modulo') modulo: string,
    @Param('entidad') entidad: string,
    @Param('registroId') registroId: string,
  ) {
    return this.filesService.listarPorEntidad(modulo, entidad, registroId);
  }
}
```

---

## 5. Servicio NestJS (`FilesService`) consumiendo Stored Procedures vía Prisma

En apego a `00-estandares-prisma.html`: **la lógica y la auditoría se ejecutan llamando a los Stored Procedures con `$queryRaw`**:

```typescript
// src/files/files.service.ts
import { Injectable, NotFoundException, BadRequestException, Inject } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { IFileStorageDriver } from './storage/file-storage.interface';
import { createHash } from 'crypto';
import { Readable } from 'stream';
import { SubirArchivoDto, VincularDocumentoDto } from './dto/file-operations.dto';

@Injectable()
export class FilesService {
  constructor(
    private readonly prisma: PrismaService,
    @Inject('FILE_STORAGE_DRIVER') private readonly storageDriver: IFileStorageDriver,
  ) {}

  async subirArchivo(
    file: Express.Multer.File,
    dto: SubirArchivoDto,
    usuario: string,
    ip: string,
    userAgent: string,
  ) {
    // 1. Calcular Hash SHA-256
    const hash = createHash('sha256').update(file.buffer).digest('hex');
    const now = new Date();
    const ejercicio = now.getFullYear();
    const mes = String(now.getMonth() + 1).padStart(2, '0');
    const extension = file.originalname.split('.').pop()?.toLowerCase() || 'bin';

    // 2. Definir ruta física neutral
    const uuid = crypto.randomUUID();
    const storagePath = `siaf/${dto.modulo_siaf}/${ejercicio}/${mes}/${uuid}.${extension}`;

    // 3. Subir al Storage Driver
    const stream = Readable.from(file.buffer);
    await this.storageDriver.upload(stream, storagePath, {
      originalName: file.originalname,
      mimeType: file.mimetype,
      sizeBytes: file.size,
      hashSha256: hash,
      modulo: dto.modulo_siaf,
      ejercicio,
      mes: now.getMonth() + 1,
    });

    // 4. Invocar Stored Procedure Canónico
    const datosSp = {
      id: uuid,
      nombre_original: file.originalname,
      nombre_almacenamiento: storagePath,
      extension,
      mime_type: file.mimetype,
      tamanio_bytes: file.size,
      hash_sha256: hash,
      ruta_storage: storagePath,
      descripcion: dto.descripcion,
      cgca_codigo: dto.cgca_codigo,
      valor_documental: dto.valor_documental,
      clasificacion_acceso: dto.clasificacion_acceso,
      es_temporal: dto.es_temporal || false,
      ticket_temporal: dto.ticket_temporal || null,
      usuario,
      ip_cliente: ip,
      user_agent: userAgent,
    };

    const resultado: any = await this.prisma.$queryRaw`
      SELECT archivos.fn_crud_documento('INSERT', ${JSON.stringify(datosSp)}::jsonb) AS res
    `;

    const resJson = resultado[0]?.res;
    if (resJson?.error !== 0) {
      // Reversar archivo físico si falla BD
      await this.storageDriver.delete(storagePath);
      throw new BadRequestException(resJson?.mensaje || 'Error al persistir documento.');
    }

    return resJson;
  }

  async obtenerPorId(id: string) {
    const resultado: any = await this.prisma.$queryRaw`
      SELECT archivos.fn_leer_documento(${JSON.stringify({ id })}::jsonb) AS res
    `;
    const doc = resultado[0]?.res?.data?.[0];
    if (!doc) {
      throw new NotFoundException(`Documento con ID ${id} no encontrado.`);
    }
    return doc;
  }

  async obtenerStreamDescarga(id: string, usuario: string, ip: string, evento: 'DESCARGA' | 'VISUALIZACION') {
    const doc = await this.obtenerPorId(id);
    const stream = await this.storageDriver.download(doc.ruta_storage);

    // Auditoría automática en segundo plano
    this.prisma.$queryRaw`
      SELECT archivos.fn_registrar_evento_bitacora(${JSON.stringify({
        documento_id: id,
        evento,
        usuario,
        ip_cliente: ip,
      })}::jsonb)
    `.catch(err => console.error('Error al registrar auditoría:', err));

    return { stream, documento: doc };
  }

  async vincularRegistro(dto: VincularDocumentoDto, usuario: string, ip: string) {
    const resultado: any = await this.prisma.$queryRaw`
      SELECT archivos.fn_crud_documento_relacion('VINCULAR', ${JSON.stringify({
        ...dto,
        usuario,
        ip_cliente: ip,
      })}::jsonb) AS res
    `;
    return resultado[0]?.res;
  }

  async desvincularRegistro(relacionId: string, motivo: string, usuario: string, ip: string) {
    const resultado: any = await this.prisma.$queryRaw`
      SELECT archivos.fn_crud_documento_relacion('DESVINCULAR', ${JSON.stringify({
        relacion_id: relacionId,
        motivo,
        usuario,
        ip_cliente: ip,
      })}::jsonb) AS res
    `;
    return resultado[0]?.res;
  }

  async listarPorEntidad(modulo: string, entidad: string, registroId: string) {
    const filtros = {
      modulo_siaf: modulo,
      entidad_origen: entidad,
      registro_id: registroId,
    };
    const resultado: any = await this.prisma.$queryRaw`
      SELECT archivos.fn_leer_documento(${JSON.stringify(filtros)}::jsonb) AS res
    `;
    return resultado[0]?.res?.data || [];
  }
}
```
