# ✅ Documento de Prueba Generado - Certificado de Pertenencia

## Fecha
18 de diciembre de 2025

## Resumen

Se ha generado exitosamente un **Certificado de Pertenencia a la Comunidad** como documento de prueba para el sistema de censo web.

---

## 📄 Información del Documento Generado

### Detalles del Certificado

| Campo | Valor |
|-------|-------|
| **Tipo de Documento** | Constancia de Pertenencia |
| **Número de Documento** | CON-RES-2025-0002 |
| **ID en la Base de Datos** | 3 |
| **Estado** | Expedido (ISSUED) |
| **Fecha de Expedición** | 18 de diciembre de 2025 |
| **Fecha de Vencimiento** | 18 de marzo de 2026 |
| **Días de Vigencia** | 90 días |

### Organización Emisora

- **Nombre**: Resguardo Indígena Prueba 1
- **NIT**: 78912333

### Persona Beneficiaria

- **Nombre Completo**: Juan Ruiz
- **Tipo de Documento**: Cédula de Ciudadanía
- **Número de Identificación**: 5623124
- **Fecha de Nacimiento**: 01 de enero de 1980
- **Edad**: 45 años
- **Vereda**: Puraré
- **Zona**: Urbana

### Firmantes Autorizados

1. **Gobernador**: Lucía Verónica Mendoza Castillo
2. **Secretario**: Paola Rodríguez Ruiz

---

## 📋 Contenido del Certificado

```
LA JUNTA DIRECTIVA DE Resguardo Indígena Prueba 1

HACE CONSTAR QUE:

Juan Ruiz, identificado(a) con Cedula Ciudadania No. 5623124,
nacido(a) el 01 de January de 1980, con 45 años de edad, es miembro perteneciente 
a nuestra comunidad indígena.

La persona reside en la vereda Puraré, zona Urbana, y se encuentra registrada 
en nuestro censo comunitario.

Se expide la presente CONSTANCIA DE PERTENENCIA a solicitud del interesado(a) 
para los fines que estime conveniente.

Expedido en Puraré, a los 18 días del mes de diciembre de 2025.

Válido hasta: 18 de March de 2026
```

---

## 🔗 URLs del Sistema

### URLs de Acceso al Documento

- **Descarga PDF**: `/documents/pdf/3/`
- **Vista Previa**: `/documents/preview/3/`
- **Verificación QR**: (Por implementar - requiere hash de verificación)

---

## 📊 Estadísticas Actuales

Después de generar este documento, el sistema tiene:

| Métrica | Cantidad |
|---------|----------|
| Total de documentos de la organización | 3 |
| Certificados de pertenencia | 2 |
| Documentos en estado "Expedido" (ISSUED) | 3 |
| Documentos anulados | 0 |

---

## 🎯 Características Implementadas

### ✅ Sistema de Generación de Documentos

1. **Tipos de Documentos Configurables**
   - Aval
   - Constancia de Pertenencia ✓ (Usado en este ejemplo)
   - Certificado de Residencia

2. **Plantillas Dinámicas**
   - Uso de variables personalizables: `{organizacion}`, `{nombre_completo}`, etc.
   - Reemplazo automático de datos de la persona y organización

3. **Numeración Automática**
   - Formato: `CON-RES-2025-0002`
   - Patrón: `[TIPO]-[ORG]-[AÑO]-[CONSECUTIVO]`

4. **Junta Directiva**
   - Firmantes autorizados configurables
   - Validación de vigencia de cargos
   - Asociación de firmantes a cada documento

5. **Control de Vigencia**
   - Fecha de expedición
   - Fecha de vencimiento (configurable según tipo de documento)
   - Cálculo automático de días de vigencia

6. **Auditoría**
   - Registro de creación (created_at)
   - Registro de última actualización (updated_at)
   - Historial de cambios (django-simple-history)

---

## 🛠️ Scripts Creados

### 1. `crear_datos_documentos.py`

Script para crear los datos básicos necesarios:
- Tipos de documentos (Aval, Constancia de Pertenencia, Certificado de Residencia)
- Junta directiva con firmantes autorizados

### 2. `generar_certificado_pertenencia.py` ✨

Script principal que:
1. ✅ Verifica organización
2. ✅ Verifica tipo de documento
3. ✅ Busca persona en la organización
4. ✅ Verifica junta directiva vigente
5. ✅ Genera el certificado con plantilla dinámica
6. ✅ Asigna firmantes
7. ✅ Muestra información completa del documento

---

## 📝 Próximos Pasos Sugeridos

### En el Sistema Web

1. **Acceder a Estadísticas de Documentos**
   - Ver la tabla con todos los documentos generados
   - Filtrar por tipo, organización, persona, fechas

2. **Descargar PDF del Certificado**
   - Generar PDF con formato profesional
   - Incluir código QR de verificación
   - Firmas digitales de la junta directiva

3. **Verificar Documento**
   - Escanear código QR
   - Verificar autenticidad del documento
   - Consultar estado y vigencia

### Mejoras Pendientes

1. **Generación de Hash de Verificación**
   - Implementar generación automática de `verification_hash`
   - Crear código QR con el hash

2. **Generación de PDF**
   - Template profesional con logo de la organización
   - Código QR embebido
   - Firmas digitales de los firmantes

3. **Sistema de Verificación en Línea**
   - Página pública para verificar documentos
   - Escaneo de QR redirige a verificación
   - Mostrar estado y validez del documento

4. **Notificaciones**
   - Alertas de documentos próximos a vencer
   - Notificación a la persona cuando se genera su documento

---

## 🔍 Verificación del Sistema

### ✅ Pruebas Realizadas

- [x] Creación de tipos de documentos
- [x] Creación de junta directiva
- [x] Generación de certificado de pertenencia
- [x] Asignación de firmantes
- [x] Cálculo de vigencia
- [x] Numeración automática
- [x] Almacenamiento en base de datos
- [x] Generación de contenido con plantilla

### ⏳ Pruebas Pendientes

- [ ] Generación de PDF
- [ ] Generación de código QR
- [ ] Verificación en línea
- [ ] Descarga desde la interfaz web
- [ ] Vista previa en navegador
- [ ] Anulación de documentos
- [ ] Edición de documentos en borrador

---

## 💡 Comandos Útiles

### Ejecutar Scripts

```bash
# Crear tipos de documentos y junta directiva
python crear_datos_documentos.py

# Generar certificado de pertenencia de prueba
python generar_certificado_pertenencia.py
```

### Consultas en Django Shell

```python
# Ver todos los documentos
from censoapp.models import GeneratedDocument
docs = GeneratedDocument.objects.all()
for doc in docs:
    print(f"{doc.document_number} - {doc.person.full_name}")

# Ver documentos de una organización
org_docs = GeneratedDocument.objects.filter(organization_id=1)

# Ver documentos vigentes
from datetime import date
vigentes = GeneratedDocument.objects.filter(
    status='ISSUED',
    expiration_date__gte=date.today()
)
```

---

## 📚 Referencias

- **Documentación del modelo**: `censoapp/models.py` - Línea 921 (GeneratedDocument)
- **Script de creación**: `crear_datos_documentos.py`
- **Script de generación**: `generar_certificado_pertenencia.py`
- **Plantillas de documentos**: Almacenadas en `DocumentType.template_content`

---

## ✨ Conclusión

El sistema de generación de documentos está funcionando correctamente:

✅ **Certificado de Pertenencia generado exitosamente**  
✅ **Numeración automática funcionando**  
✅ **Plantillas dinámicas operativas**  
✅ **Junta directiva y firmantes configurados**  
✅ **Control de vigencia implementado**

El documento generado está listo para ser visualizado en la interfaz web de estadísticas de documentos.

