# Diagnóstico y Solución - Error al Cargar PDF

## Fecha
18 de diciembre de 2025

## Error Reportado
```
Error al cargar el documento
No se pudo cargar el PDF para visualización.
Error: Invalid PDF structure.
```

## Diagnóstico Realizado

### 1. Verificación del Documento ✅
- El documento ID 3 existe en la base de datos
- Tiene contenido válido (458 caracteres)
- Tiene firmantes asignados (2 firmantes)
- Tiene número de documento: `CON-RES-2025-0002`

### 2. Verificación de la Generación de PDF ✅
- Script de prueba generó PDF exitosamente
- PDF de prueba: 1736 bytes
- Guardado como `test_documento.pdf`

### 3. Posibles Causas del Error

1. **Problema de Autenticación/Permisos**
   - El usuario no tiene permisos para ver el documento
   - PDF.js no puede cargar el PDF debido a problemas de sesión/cookies

2. **Problema con el Hash de Verificación**
   - El documento no tiene `verification_hash` generado
   - El QR y el hash se generan al acceder al PDF, pero si falla antes...

3. **Problema de CORS**
   - PDF.js no puede cargar el PDF debido a restricciones CORS
   - Las cabeceras CORS están configuradas pero pueden no estar funcionando

4. **Problema con el Navegador**
   - El navegador está bloqueando la carga del PDF
   - Cache corrupto del navegador

## Solución Implementada

### Paso 1: Verificar y Generar Hash de Verificación

El hash de verificación se genera automáticamente al cargar el PDF por primera vez, pero podemos asegurarnos de que exista:

```python
# Ejecutar en Django shell
from censoapp.models import GeneratedDocument
import hashlib

doc = GeneratedDocument.objects.get(id=3)

if not doc.verification_hash:
    verification_data = f"{doc.id}|{doc.document_number}|{doc.issue_date.isoformat()}"
    doc.verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]
    doc.save(update_fields=['verification_hash'])
    print(f"Hash generado: {doc.verification_hash}")
else:
    print(f"Hash existente: {doc.verification_hash}")
```

### Paso 2: Acceder Directamente al PDF

Intenta acceder directamente a la URL del PDF sin pasar por PDF.js:

```
http://127.0.0.1:8000/documento/descargar/3/
```

Esto debería:
- Descargar el PDF directamente
- O mostrarlo en el navegador (inline)
- Permitir verificar si el PDF se genera correctamente

### Paso 3: Forzar Descarga

Si la vista previa no funciona, puedes forzar la descarga agregando el parámetro `?download=true`:

```
http://127.0.0.1:8000/documento/descargar/3/?download=true
```

### Paso 4: Limpiar Cache del Navegador

1. Abre las Herramientas de Desarrollador (F12)
2. Ve a la pestaña "Red" (Network)
3. Marca "Disable cache"
4. Recarga la página (Ctrl+F5)
5. Verifica los errores en la consola

### Paso 5: Verificar Permisos del Usuario

Asegúrate de que el usuario tiene permisos para ver documentos de la organización:

```python
# En Django shell
from django.contrib.auth.models import User
from censoapp.models import GeneratedDocument

user = User.objects.get(username='tu_usuario')
doc = GeneratedDocument.objects.get(id=3)

# Verificar organización
if hasattr(user, 'userprofile'):
    user_org = user.userprofile.organization
    doc_org = doc.organization
    print(f"Usuario org: {user_org}")
    print(f"Doc org: {doc_org}")
    print(f"Tiene permiso: {user_org == doc_org or user.is_superuser}")
else:
    print("Usuario no tiene perfil")
```

## Alternativa: Descargar en Lugar de Vista Previa

Si la vista previa continúa fallando, puedes modificar temporalmente el botón para que descargue directamente:

### Modificar organization_stats.html

En lugar de abrir en nueva pestaña, forzar descarga directa:

```html
<!-- Cambiar esto -->
<a href="{% url 'preview-document-pdf' doc.id %}"
   class="btn btn-action-view"
   title="Vista Previa PDF"
   target="_blank">
    <i class="fas fa-eye"></i>
</a>

<!-- Por esto (temporalmente) -->
<a href="{% url 'download-document-pdf' doc.id %}?download=true"
   class="btn btn-action-view"
   title="Descargar PDF">
    <i class="fas fa-download"></i>
</a>
```

## Script de Verificación Rápida

Ejecuta este script para verificar todos los documentos:

```bash
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import GeneratedDocument
import hashlib

docs = GeneratedDocument.objects.all()
for doc in docs:
    has_content = bool(doc.document_content)
    has_hash = bool(doc.verification_hash)
    has_number = bool(doc.document_number)
    signers_count = doc.signers.count()
    
    print(f'Doc {doc.id}: {doc.document_number}')
    print(f'  Contenido: {'✓' if has_content else '✗'}')
    print(f'  Hash: {'✓' if has_hash else '✗'}')
    print(f'  Número: {'✓' if has_number else '✗'}')
    print(f'  Firmantes: {signers_count}')
    
    # Generar hash si no existe
    if not has_hash:
        verification_data = f'{doc.id}|{doc.document_number}|{doc.issue_date.isoformat()}'
        doc.verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]
        doc.save(update_fields=['verification_hash'])
        print(f'  Hash generado: {doc.verification_hash}')
    print()
"
```

## Solución Definitiva

La causa más probable es que el navegador no puede cargar el PDF debido a:
1. Problemas de sesión/autenticación con PDF.js
2. El documento no tiene hash de verificación

### Acción Inmediata

1. Ejecutar el script de verificación para generar hashes faltantes
2. Limpiar cache del navegador
3. Intentar acceder directamente a la URL del PDF
4. Si falla, usar descarga directa en lugar de vista previa

### Para Desarrollo Futuro

Considerar implementar:
1. Generación de hash al crear el documento (en el método `save`)
2. Validación de permisos más robusta
3. Mejor manejo de errores en el frontend
4. Logging detallado de errores de PDF

