# Sistema Simple de Generación de Documentos con jsPDF

**Fecha:** 21 de Diciembre de 2024  
**Implementación:** Sistema simple de 3 documentos sin dependencia del administrador de plantillas  
**Tecnología:** jsPDF (generación en el navegador)  

---

## 📋 Documentos Implementados

### 1. **AVAL GENERAL**
**URL:** `/documento/aval-general/<person_id>/`  
**Campos del formulario:**
- Entidad que Requiere (requerido)
- Motivo (requerido): Trabajar, Practicar Deporte, Voluntariado, Otro
- Cargo / Actividad (requerido)

**Contenido del documento:**
- Encabezado con logo y datos de la organización
- Título: "AVAL GENERAL"
- Certifica que la persona pertenece al resguardo
- Especifica la entidad, motivo y cargo
- Firmas de la junta directiva

### 2. **AVAL DE ESTUDIO**
**URL:** `/documento/aval-estudio/<person_id>/`  
**Campos del formulario:**
- Institución Educativa (requerido)
- Programa Académico (requerido)
- Semestre (requerido): 1° a 10°
- Proyecto / Práctica (opcional)
- Horas por Semestre (opcional)

**Contenido del documento:**
- Encabezado con logo y datos de la organización
- Título: "AVAL DE ESTUDIO"
- Certifica que la persona pertenece al resguardo
- Especifica la institución, programa, semestre
- Incluye proyecto y horas si se proporcionan
- Firmas de la junta directiva

### 3. **CONSTANCIA DE PERTENENCIA**
**URL:** `/documento/constancia/<person_id>/`  
**Campos del formulario:**
- Ninguno (documento automático)

**Contenido del documento:**
- Encabezado con logo y datos de la organización
- Título: "CONSTANCIA DE PERTENENCIA"
- Hace constar que la persona está registrada en el censo
- Detalla que reside en el territorio y participa en actividades
- Menciona derechos y deberes como miembro
- Firmas de la junta directiva
- **Se genera automáticamente al cargar la página**

---

## 🎯 Flujo de Usuario

### Paso 1: Seleccionar Tipo de Documento

Usuario accede desde el detalle de una persona → Click en "Generar Documento"

**Pantalla de selección:**
```
┌─────────────────────────────────────────────────┐
│  Seleccione el Tipo de Documento               │
├─────────────────────────────────────────────────┤
│                                                  │
│  [📄 Aval General]  [🎓 Aval Estudio]  [📜 Constancia] │
│                                                  │
│  Para trabajar      Para estudiantes   Certifica │
│  o actividades      académicas         pertenencia│
└─────────────────────────────────────────────────┘
```

### Paso 2: Completar Formulario (si aplica)

**Para Aval General y Aval de Estudio:**
- Formulario a la izquierda
- Preview del PDF a la derecha
- Click en "Generar PDF"
- PDF se muestra en iframe
- Click en "Descargar" para guardar

**Para Constancia de Pertenencia:**
- Se genera automáticamente al cargar
- Sin formulario
- Preview inmediato
- Click en "Descargar" para guardar

---

## 🚀 Archivos Creados

### Vistas (Backend)

**`censoapp/simple_document_views.py`**
- `select_document_type(request, person_id)` - Selector de tipo
- `generate_aval_general(request, person_id)` - Aval General
- `generate_aval_estudio(request, person_id)` - Aval de Estudio
- `generate_constancia_pertenencia(request, person_id)` - Constancia

Todas las vistas:
- ✅ Verifican permisos por organización
- ✅ Validan junta directiva vigente
- ✅ Pasan datos de persona, organización y firmantes al template

### Templates (Frontend)

**`templates/censo/documentos/select_document_type.html`**
- Pantalla de selección con 3 cards
- Diseño responsive
- Hover effects
- Iconos Font Awesome

**`templates/censo/documentos/aval_general.html`**
- Formulario con 3 campos
- Validación HTML5
- Generación de PDF con jsPDF
- Preview en iframe
- Botón de descarga

**`templates/censo/documentos/aval_estudio.html`**
- Formulario con 5 campos (3 requeridos, 2 opcionales)
- Validación HTML5
- Generación de PDF con jsPDF
- Preview en iframe
- Botón de descarga

**`templates/censo/documentos/constancia_pertenencia.html`**
- Sin formulario
- Generación automática al cargar
- Preview en iframe
- Botón de descarga

### URLs

**`censoapp/urls.py`**
```python
# Sistema simple con jsPDF
path('documento/seleccionar/<int:person_id>/', select_document_type, name='select-document-type'),
path('documento/aval-general/<int:person_id>/', generate_aval_general, name='generate-aval-general'),
path('documento/aval-estudio/<int:person_id>/', generate_aval_estudio, name='generate-aval-estudio'),
path('documento/constancia/<int:person_id>/', generate_constancia_pertenencia, name='generate-constancia'),
```

---

## 💻 Tecnología Utilizada

### jsPDF
**CDN:** `https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js`

**Ventajas:**
- ✅ Generación en el navegador (no consume servidor)
- ✅ Preview instantáneo en iframe
- ✅ Descarga directa sin peticiones adicionales
- ✅ No requiere base de datos para guardar templates
- ✅ Fácil de mantener y modificar

**Funciones principales:**
```javascript
const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'letter'
});

// Agregar texto
doc.text('Texto', x, y, { align: 'center' });

// Agregar imagen (logo)
doc.addImage(logoImg, 'PNG', x, y, width, height);

// Líneas
doc.line(x1, y1, x2, y2);

// Texto multilinea automático
const lines = doc.splitTextToSize(text, maxWidth);
doc.text(lines, x, y);

// Generar blob para preview
const pdfBlob = doc.output('blob');
const pdfUrl = URL.createObjectURL(pdfBlob);
iframe.src = pdfUrl;

// Descargar
doc.save('archivo.pdf');
```

---

## 🎨 Estructura del PDF

### Encabezado (Todos los documentos)
```
┌─────────────────────────────────────────────┐
│ [Logo]              Nombre Organización     │
│                     NIT: xxxxx              │
│                     Dirección               │
│                     Tel: xxxxx              │
├─────────────────────────────────────────────┤ Línea azul
```

### Cuerpo
```
            TÍTULO DEL DOCUMENTO (azul)

La Autoridad Tradicional del [organización]...

CERTIFICA QUE: / HACE CONSTAR QUE:

Párrafo con datos de la persona...

Párrafo con datos específicos del documento...

Párrafo final...

Fecha...
```

### Firmas
```
         FIRMAS AUTORIZADAS

_______________    _______________
Nombre Firmante    Nombre Firmante
C.C. xxxxx         C.C. xxxxx
Cargo              Cargo
```

---

## 📊 Datos Dinámicos

### Desde Django (Backend)

**Datos de la persona:**
```python
person = {
    'fullName': person.full_name,
    'identification': person.identification_person,
    'documentType': person.document_type.document_type,
    'vereda': person.family_card.sidewalk_home.sidewalk_name
}
```

**Datos de la organización:**
```python
organization = {
    'name': organization.organization_name,
    'nit': organization.organization_identification,
    'address': organization.organization_address,
    'phone': organization.organization_mobile_phone,
    'logoUrl': organization.organization_logo.url
}
```

**Firmantes (Junta Directiva):**
```python
signers = [
    {
        'name': signer.holder_person.full_name,
        'position': signer.get_position_name_display(),
        'id': signer.holder_person.identification_person
    }
]
```

### Desde Formulario (Usuario)

**Aval General:**
- `entidad` - Texto libre
- `motivo` - Select (trabajar, practicar, voluntariado, otro)
- `cargo` - Texto libre

**Aval de Estudio:**
- `entidad` - Texto libre
- `programa` - Texto libre
- `semestre` - Select (1° a 10°)
- `proyecto` - Texto libre (opcional)
- `horas` - Número (opcional)

**Constancia de Pertenencia:**
- Ninguno (se genera automáticamente)

---

## ✅ Validaciones Implementadas

### Permisos
- ✅ Usuario debe estar autenticado
- ✅ Usuario solo puede generar documentos de su organización
- ✅ Superusuario puede generar para cualquier organización

### Junta Directiva
- ✅ Debe existir junta directiva vigente
- ✅ Mínimo 1 firmante activo
- ✅ Se muestran todos los firmantes en el documento

### Formularios
- ✅ Campos requeridos marcados con asterisco (*)
- ✅ Validación HTML5 (`required` attribute)
- ✅ Validación antes de generar PDF
- ✅ Mensajes de error si faltan datos

---

## 🔧 Cómo Usar

### Para el Usuario Final

1. **Ir al detalle de una persona**
   - Menú: Personas → Listado
   - Click en una persona

2. **Click en "Generar Documento"**
   - Botón verde en la parte superior

3. **Seleccionar tipo de documento**
   - Click en el card del documento deseado

4. **Completar formulario (si aplica)**
   - Llenar los campos requeridos
   - Click en "Generar PDF"

5. **Descargar**
   - Preview se muestra automáticamente
   - Click en "Descargar" para guardar el archivo

### Para el Desarrollador

**Modificar contenido de un documento:**
1. Abrir el archivo HTML correspondiente
2. Buscar la sección de contenido en JavaScript
3. Modificar los textos de los párrafos
4. Guardar y recargar

**Agregar un nuevo documento:**
1. Crear vista en `simple_document_views.py`
2. Agregar URL en `urls.py`
3. Crear template HTML con jsPDF
4. Agregar card en `select_document_type.html`

---

## 📝 Ejemplo de Contenido

### Aval General (Ejemplo)

**Formulario:**
- Entidad: `Universidad del Cauca`
- Motivo: `Trabajar`
- Cargo: `Auxiliar Administrativo`

**PDF Generado:**
```
La Autoridad Tradicional del Resguardo Indígena Puracé...

CERTIFICA QUE:

Que Elena Sofia Martínez López, identificado con Cedula Ciudadania 
No. 58269788, actualmente se encuentra inscrito en el censo del 
Resguardo Indígena Puracé — Vereda Purace, reside de manera integral, 
comparte los usos y costumbres en nuestro territorio.

Se expide el presente AVAL para que Elena Sofia Martínez López pueda 
trabajar en Universidad del Cauca, desempeñando el cargo de Auxiliar 
Administrativo.

El presente certificado se expide a solicitud del interesado para los 
fines que considere conveniente.

Dado en el Resguardo Indígena Puracé, a los 21 días del mes de 
diciembre de 2024.
```

---

## 🎯 Ventajas de Esta Implementación

### Simplicidad
- ✅ No requiere configuración en el admin
- ✅ No depende de base de datos para templates
- ✅ Código fácil de entender y mantener
- ✅ Modificaciones rápidas editando HTML

### Rendimiento
- ✅ Generación instantánea en el navegador
- ✅ No consume recursos del servidor
- ✅ Preview inmediato sin cargas adicionales
- ✅ Descarga directa sin peticiones al servidor

### Usabilidad
- ✅ Interfaz intuitiva
- ✅ Preview en tiempo real
- ✅ Formularios simples
- ✅ Un solo click para descargar

### Mantenibilidad
- ✅ Todo en un solo archivo por documento
- ✅ Sin dependencias complejas
- ✅ Fácil de depurar (todo en JavaScript del navegador)
- ✅ Cambios sin necesidad de reiniciar servidor

---

## 🚀 Próximos Pasos

### Recomendaciones

1. **Probar cada tipo de documento:**
   - Aval General con diferentes motivos
   - Aval de Estudio con y sin campos opcionales
   - Constancia de Pertenencia

2. **Verificar en diferentes navegadores:**
   - Chrome ✅
   - Firefox
   - Edge
   - Safari

3. **Ajustar contenido según necesidad:**
   - Modificar textos de los párrafos
   - Ajustar espaciado si es necesario
   - Personalizar según feedback de usuarios

### Posibles Mejoras Futuras

- [ ] Agregar código QR de verificación
- [ ] Guardar historial de documentos generados
- [ ] Enviar por correo electrónico
- [ ] Agregar más tipos de documentos
- [ ] Personalizar colores por organización

---

**Estado:** ✅ IMPLEMENTADO Y LISTO PARA USAR  
**Fecha:** 21 de Diciembre de 2024  
**Archivos creados:** 5 (1 vista Python + 4 templates HTML)  
**Dependencias:** jsPDF (CDN)

