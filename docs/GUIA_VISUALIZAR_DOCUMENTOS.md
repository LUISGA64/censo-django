# 📄 Guía Completa: Cómo Visualizar Documentos Generados

**Fecha:** 2025-12-15  
**Sistema:** Censo Django - Generación de Documentos

---

## 🎯 Documentos Disponibles en tu Sistema

Actualmente tienes **2 documentos generados**:

| ID | Tipo | Número | Persona | URL |
|----|------|--------|---------|-----|
| 1 | Aval | AVA-RES-2025-0001 | Andrés Sánchez | [Ver →](http://127.0.0.1:8000/documento/ver/1/) |
| 2 | Certificado | CER-RES-2025-0001 | Andrés Sánchez | [Ver →](http://127.0.0.1:8000/documento/ver/2/) |

---

## 🔍 MÉTODOS PARA VISUALIZAR DOCUMENTOS

### ✅ Método 1: URL Directa (Más Rápido)

Simplemente accede a la URL del documento:

```
http://127.0.0.1:8000/documento/ver/<ID_DOCUMENTO>/
```

**Ejemplos con tus documentos:**
- Documento #1 (Aval): http://127.0.0.1:8000/documento/ver/1/
- Documento #2 (Certificado): http://127.0.0.1:8000/documento/ver/2/

**Pasos:**
1. Copia la URL
2. Pégala en tu navegador
3. ¡Listo! Verás el documento completo

---

### ✅ Método 2: Desde el Detalle de Persona

**Ruta:** Personas → Detalle → Generar Documento

```
Flujo completo:
1. http://127.0.0.1:8000/personas/
2. Click en la persona deseada
3. En la página de detalle, click en "Generar Documento"
4. Después de generar, serás redirigido automáticamente a la vista del documento
```

**Ejemplo práctico:**
```
1. Ir a: http://127.0.0.1:8000/personas/detail/32/
   (Andrés Sánchez López - RC4504603)

2. Click en botón verde "Generar Documento"

3. Seleccionar tipo de documento (Aval, Constancia, etc.)

4. Click en "Generar Documento"

5. → Redirige automáticamente a: /documento/ver/<ID>/
```

---

### ✅ Método 3: Ver Todos los Documentos de una Persona

Si quieres ver **todos** los documentos generados para una persona específica:

```
http://127.0.0.1:8000/documento/persona/<ID_PERSONA>/
```

**Ejemplo:**
```
Ver todos los documentos de Andrés Sánchez (ID 32):
http://127.0.0.1:8000/documento/persona/32/
```

---

## 📋 Lo Que Verás en la Vista de Documento

### Secciones del Documento

```
┌────────────────────────────────────────────┐
│         [Volver] [Imprimir] [Descargar]    │ ← Botones de acción
├────────────────────────────────────────────┤
│                                            │
│    RESGUARDO INDÍGENA PURACÉ               │ ← Header
│              AVAL                          │
│       No. AVA-RES-2025-0001                │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  LA JUNTA DIRECTIVA CERTIFICA QUE:         │ ← Contenido
│                                            │
│  Andrés Sánchez López, identificado(a)     │
│  con Registro Civil No. RC4504603...       │
│                                            │
├────────────────────────────────────────────┤
│  Fecha de Expedición: 15 de diciembre...  │ ← Fechas
│  Válido hasta: 15 de diciembre de 2026     │
├────────────────────────────────────────────┤
│                                            │
│  _________________  ___________________    │ ← Firmas
│  Luis Gabriel Q.    Luz Torres            │
│  Gobernador         Alcalde               │
│                                            │
└────────────────────────────────────────────┘
```

---

## 🖨️ Acciones Disponibles en la Vista

### 1. Imprimir Documento
- **Botón:** "Imprimir" (icono de impresora)
- **Función:** Abre el diálogo de impresión del navegador
- **Resultado:** Documento optimizado para impresión (sin botones ni elementos de navegación)

### 2. Descargar Documento
- **Botón:** "Descargar" (azul)
- **Función:** Descarga el documento
- **Formato actual:** Texto plano (.txt)
- **Futuro:** PDF con formato profesional

### 3. Volver
- **Botón:** "Volver" (gris)
- **Función:** Regresa al detalle de la persona

---

## 🧪 Prueba Rápida - Paso a Paso

### Generar y Ver un Nuevo Documento

**Paso 1: Accede a generar documento**
```
http://127.0.0.1:8000/documento/generar/24/
(Luz Torres - CC 58262324)
```

**Paso 2: Selecciona tipo de documento**
- Click en la tarjeta "Constancia de Pertenencia"
- Selecciona vigencia: 365 días (1 año)

**Paso 3: Genera el documento**
- Click en botón verde "Generar Documento"
- Espera el spinner "Generando..."

**Paso 4: Vista automática**
- Serás redirigido automáticamente a: `/documento/ver/3/`
- Verás el documento completo con:
  - Contenido personalizado
  - Datos de Luz Torres
  - Firmas de la junta directiva
  - Número de documento: CON-RES-2025-0001

**Paso 5: Acciones**
- Imprimir: Click en "Imprimir"
- Descargar: Click en "Descargar"
- Ver en el futuro: Guarda la URL `/documento/ver/3/`

---

## 🔗 URLs Útiles

### Documentos Existentes
```bash
# Ver documento #1 (Aval)
http://127.0.0.1:8000/documento/ver/1/

# Ver documento #2 (Certificado)
http://127.0.0.1:8000/documento/ver/2/
```

### Generar Nuevos Documentos
```bash
# Para Luis Gabriel Quira (ID 23)
http://127.0.0.1:8000/documento/generar/23/

# Para Luz Torres (ID 24)
http://127.0.0.1:8000/documento/generar/24/

# Para Juan González (ID 27)
http://127.0.0.1:8000/documento/generar/27/

# Para Carlos Sánchez (ID 30)
http://127.0.0.1:8000/documento/generar/30/

# Para Luz Elena Rodríguez (ID 33)
http://127.0.0.1:8000/documento/generar/33/
```

### Ver Todos los Documentos de una Persona
```bash
# Documentos de Andrés Sánchez (ID 32)
http://127.0.0.1:8000/documento/persona/32/

# Documentos de Luz Torres (ID 24)
http://127.0.0.1:8000/documento/persona/24/
```

---

## 📊 Estado Actual del Sistema

### Documentos Generados
- **Total:** 2 documentos
- **Tipos:**
  - 1 Aval
  - 1 Certificado
- **Organización:** Resguardo Indígena Puracé
- **Estado:** Todos expedidos ✅

### Junta Directiva Vigente
- ✅ 3 firmantes autorizados
- ✅ Período vigente hasta 2027
- ✅ Sistema operativo para generar documentos

---

## ❓ Preguntas Frecuentes

### ¿Cómo sé el ID de un documento?
**Opción 1:** Ejecución del script `ver_documentos.py`
```bash
python ver_documentos.py
```

**Opción 2:** Desde la base de datos
```bash
python manage.py shell
>>> from censoapp.models import GeneratedDocument
>>> for d in GeneratedDocument.objects.all():
...     print(f"ID: {d.id}, Número: {d.document_number}")
```

### ¿Por qué no veo mis documentos?
**Verificaciones:**
1. ✅ ¿El documento fue generado exitosamente? (mensaje de éxito verde)
2. ✅ ¿Estás usando el ID correcto?
3. ✅ ¿Tienes permisos para ver documentos de esa organización?

### ¿Puedo editar un documento generado?
**No.** Los documentos generados son **inmutables** por seguridad.
- Una vez expedidos, no se pueden modificar
- Si necesitas cambios, genera un nuevo documento
- Los documentos antiguos se pueden marcar como "Revocados"

### ¿Cómo imprimo sin botones?
El sistema ya está optimizado:
- Click en "Imprimir"
- Los botones y navegación se ocultan automáticamente
- Solo se imprime el contenido del documento

---

## 🎯 Resumen Rápido

### Para Ver un Documento Existente:
```
http://127.0.0.1:8000/documento/ver/<ID>/

Ejemplos:
- Documento #1: /documento/ver/1/
- Documento #2: /documento/ver/2/
```

### Para Generar un Nuevo Documento:
```
1. http://127.0.0.1:8000/documento/generar/<ID_PERSONA>/
2. Seleccionar tipo
3. Click "Generar Documento"
4. → Automáticamente redirige a /documento/ver/<ID_NUEVO>/
```

### Para Ver Todos los Documentos de una Persona:
```
http://127.0.0.1:8000/documento/persona/<ID_PERSONA>/
```

---

## 🚀 Siguiente Paso Recomendado

**Prueba inmediata:** Abre tu navegador y accede a:
```
http://127.0.0.1:8000/documento/ver/1/
```

Deberías ver el documento de Aval para Andrés Sánchez con:
- ✅ Contenido completo
- ✅ Firmas de la junta directiva
- ✅ Número de documento
- ✅ Fechas de expedición y vencimiento
- ✅ Botones de imprimir y descargar

---

## 📞 Comandos Útiles

### Ver documentos desde terminal
```bash
python ver_documentos.py
```

### Limpiar documentos de prueba
```bash
python manage.py shell
>>> from censoapp.models import GeneratedDocument
>>> GeneratedDocument.objects.filter(status='DRAFT').delete()
```

### Contar documentos
```bash
python manage.py shell
>>> from censoapp.models import GeneratedDocument
>>> print(f"Total: {GeneratedDocument.objects.count()}")
```

---

**Última actualización:** 2025-12-15  
**Estado del sistema:** ✅ Operativo  
**Documentos disponibles:** 2

