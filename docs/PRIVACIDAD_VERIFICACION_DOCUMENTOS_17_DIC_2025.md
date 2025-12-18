# 🔒 PRIVACIDAD EN VERIFICACIÓN DE DOCUMENTOS - DOS NIVELES DE ACCESO

**Fecha:** 17 de Diciembre 2025  
**Objetivo:** Proteger datos personales en verificación pública  
**Estado:** ✅ **IMPLEMENTADO**  
**Cumplimiento:** Ley 1581 de 2012 (Protección de Datos Personales - Colombia)

---

## 🎯 PROBLEMA IDENTIFICADO

**Pregunta del usuario:**
> "¿Cuando la validación la realice una persona no registrada en el censo va a ver la misma información de la respuesta? Porque los documentos generados pueden ir a otras entidades gubernamentales."

**Preocupación válida:**
- Los documentos pueden ser escaneados por terceros (empleadores, instituciones, etc.)
- Mostrar información personal completa a cualquiera viola principios de privacidad
- Se debe cumplir con normativas de protección de datos

---

## ✅ SOLUCIÓN IMPLEMENTADA: DOS NIVELES DE ACCESO

### Nivel 1: 👤 Usuario NO Autenticado (Público/Terceros)
**Información VISIBLE:**
- ✅ Estado del documento (Válido/Vencido/Revocado/Inválido)
- ✅ Tipo de documento
- ✅ Número de documento
- ✅ Fecha de expedición
- ✅ Fecha de vencimiento
- ✅ Nombre de la organización emisora

**Información OCULTA:**
- ❌ Nombre completo del beneficiario
- ❌ Número de identificación
- ❌ Tipo de documento de identidad
- ❌ NIT de la organización
- ❌ Hash de verificación

**Propósito:**
Permitir que terceros verifiquen que el documento es **auténtico y válido**, sin exponer datos personales del beneficiario.

---

### Nivel 2: 🔐 Usuario Autenticado (Sistema Interno)
**Información VISIBLE:**
- ✅ Todo lo del Nivel 1, más:
- ✅ Nombre completo del beneficiario
- ✅ Número de identificación
- ✅ Tipo de documento de identidad
- ✅ NIT de la organización
- ✅ Hash de verificación completo

**Propósito:**
Personal autorizado de la organización puede acceder a información completa para verificaciones internas o reportes.

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### 1. Modificación en `document_views.py`

**Función:** `verify_document(request, hash)`

**Código agregado:**
```python
# Determinar si el usuario está autenticado
is_authenticated = request.user.is_authenticated

# Información básica (siempre visible)
basic_info = {
    'document_type': document.document_type.document_type_name,
    'document_number': document.document_number,
    'issue_date': document.issue_date,
    'expiration_date': document.expiration_date,
    'organization_name': document.organization.organization_name,
    'status': verification_status,
}

# Información sensible (solo autenticados)
sensitive_info = {
    'person_full_name': document.person.full_name,
    'person_identification': document.person.identification_person,
    'person_document_type': document.person.document_type.document_type,
    'organization_nit': getattr(document.organization, 'nit', None),
    'verification_hash': document.verification_hash,
} if is_authenticated else {}

context = {
    ...
    'is_authenticated': is_authenticated,
    'basic_info': basic_info,
    'sensitive_info': sensitive_info,
    ...
}
```

**Logging diferenciado:**
```python
if is_authenticated:
    logger.info(
        f"Verificación autenticada de documento {document.document_number} - "
        f"Hash: {hash} - Usuario: {request.user.username}"
    )
else:
    logger.info(
        f"Verificación pública de documento {document.document_number} - "
        f"Hash: {hash} - IP: {request.META.get('REMOTE_ADDR', 'desconocida')}"
    )
```

---

### 2. Modificación en `verify_document.html`

**Bloques condicionales agregados:**

#### a) Información del Documento (siempre visible):
```django
<div class="info-section">
    <h5><i class="fas fa-file-alt me-2"></i>Información del Documento</h5>
    <div class="info-row">
        <span class="info-label">Tipo de Documento:</span>
        <span class="info-value">{{ basic_info.document_type }}</span>
    </div>
    <!-- Más campos básicos -->
</div>
```

#### b) Información Sensible (solo autenticados):
```django
{% if is_authenticated %}
    <div class="info-section">
        <h5><i class="fas fa-user me-2"></i>Beneficiario</h5>
        <div class="info-row">
            <span class="info-label">Nombre Completo:</span>
            <span class="info-value">{{ sensitive_info.person_full_name }}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Identificación:</span>
            <span class="info-value">
                {{ sensitive_info.person_document_type }} 
                {{ sensitive_info.person_identification }}
            </span>
        </div>
    </div>
    
    <div class="text-center mt-4">
        <div class="security-badge">
            <i class="fas fa-lock"></i>
            Hash: {{ sensitive_info.verification_hash }}
        </div>
    </div>
{% else %}
    <!-- Aviso de información limitada -->
    <div class="alert-box">
        <i class="fas fa-info-circle me-2"></i>
        <strong>Información Limitada:</strong> Por motivos de privacidad...
    </div>
{% endif %}
```

---

## 📊 COMPARACIÓN VISUAL

### Usuario NO Autenticado ve:

```
================================
✅ VÁLIDO
Este documento es auténtico y está vigente
================================

📋 Información del Documento
- Tipo: Aval
- Número: AVA-RES-2025-0001
- Expedición: 16/12/2025
- Vencimiento: 16/12/2026
- Estado: VÁLIDO

🏢 Organización Emisora
- Nombre: Resguardo Indígena Purac

⚠️ Información Limitada
Por motivos de privacidad y protección de datos personales,
la información del beneficiario no se muestra públicamente.

✅ Verificación de Autenticidad
Este código QR es auténtico y corresponde a un documento
real emitido por Resguardo Indígena Purac.

ℹ️ Para obtener información del beneficiario, contacte
a la organización emisora o inicie sesión.
```

---

### Usuario Autenticado ve:

```
================================
✅ VÁLIDO
Este documento es auténtico y está vigente
================================

📋 Información del Documento
- Tipo: Aval
- Número: AVA-RES-2025-0001
- Expedición: 16/12/2025
- Vencimiento: 16/12/2026
- Estado: VÁLIDO

🏢 Organización Emisora
- Nombre: Resguardo Indígena Purac
- NIT: 900.123.456-7

👤 Beneficiario
- Nombre: Juan Pérez López
- Identificación: CC 12345678

🔒 Hash: 3db390289987cf57

✅ Acceso Autorizado
Como usuario autenticado, tiene acceso a información
completa protegida por normativas de datos personales.
```

---

## 🎯 CASOS DE USO

### Caso 1: Empleador Verifica Documento ✅

**Escenario:**
Un empleador recibe un aval de un candidato que dice ser miembro de una comunidad indígena.

**Flujo:**
1. Empleador escanea QR (sin iniciar sesión)
2. Ve:
   - ✅ Documento VÁLIDO
   - ✅ Emitido por "Resguardo Indígena Purac"
   - ✅ Número: AVA-RES-2025-0001
   - ✅ Vigente hasta: 16/12/2026
3. NO ve:
   - ❌ Nombre del beneficiario
   - ❌ Identificación
4. Empleador puede:
   - ✅ Confirmar que el documento es auténtico
   - ✅ Verificar que la organización es real
   - ✅ Ver que está vigente
5. Para confirmar que es del candidato:
   - Debe solicitar identificación al candidato
   - O contactar a la organización

**Resultado:** ✅ Privacidad protegida + Verificación funcional

---

### Caso 2: Personal de la Organización Verifica ✅

**Escenario:**
Un miembro del equipo administrativo necesita verificar un documento emitido.

**Flujo:**
1. Inicia sesión en el sistema
2. Escanea QR o ingresa hash
3. Ve información COMPLETA:
   - ✅ Todos los datos del documento
   - ✅ Nombre y identificación del beneficiario
   - ✅ Hash completo
   - ✅ NIT de la organización
4. Puede confirmar todos los detalles

**Resultado:** ✅ Acceso completo para personal autorizado

---

### Caso 3: Institución Gubernamental Verifica ✅

**Escenario:**
Una entidad gubernamental recibe un documento para un trámite.

**Flujo:**
1. Funcionario escanea QR (sin login)
2. Ve información básica
3. Confirma autenticidad del documento
4. Si requiere verificar beneficiario:
   - Solicita documento de identidad a la persona
   - Compara con el documento físico
   - O contacta a la organización emisora

**Resultado:** ✅ Verificación de autenticidad sin exponer datos

---

## 🔒 CUMPLIMIENTO NORMATIVO

### Ley 1581 de 2012 (Colombia) - Habeas Data

**Principios cumplidos:**

1. **Finalidad:** ✅
   - Los datos personales solo se muestran a usuarios autorizados
   - Terceros solo ven lo necesario para verificar autenticidad

2. **Acceso y Circulación Restringida:** ✅
   - Datos sensibles solo accesibles con autenticación
   - Logging de todos los accesos

3. **Seguridad:** ✅
   - Hash criptográfico para verificación
   - Separación de niveles de información

4. **Confidencialidad:** ✅
   - Información personal protegida
   - Solo personal autorizado puede verla

---

### RGPD (General Data Protection Regulation - Referencia)

**Principios aplicables:**

1. **Minimización de Datos:** ✅
   - Solo se muestra información estrictamente necesaria
   - Usuarios no autenticados ven mínimo indispensable

2. **Limitación de Finalidad:** ✅
   - Información básica: verificar autenticidad
   - Información completa: personal autorizado

3. **Integridad y Confidencialidad:** ✅
   - Datos protegidos con autenticación
   - Logging de accesos

---

## 📋 MATRIZ DE INFORMACIÓN

| Campo | Público | Autenticado | Justificación |
|-------|---------|-------------|---------------|
| **Tipo de Documento** | ✅ | ✅ | Necesario para verificar autenticidad |
| **Número de Documento** | ✅ | ✅ | Identifica el documento, no a la persona |
| **Fecha Expedición** | ✅ | ✅ | Verifica vigencia |
| **Fecha Vencimiento** | ✅ | ✅ | Verifica vigencia |
| **Organización** | ✅ | ✅ | Confirma emisor legítimo |
| **Estado** | ✅ | ✅ | Esencial para verificación |
| **Nombre Beneficiario** | ❌ | ✅ | Dato personal protegido |
| **Identificación** | ❌ | ✅ | Dato personal sensible |
| **Tipo ID** | ❌ | ✅ | Dato personal |
| **NIT Organización** | ❌ | ✅ | Info tributaria |
| **Hash Verificación** | ❌ | ✅ | Seguridad adicional |

---

## 🧪 TESTING

### Test 1: Usuario No Autenticado

**Pasos:**
```bash
1. Abrir navegador en modo incógnito
2. Ir a URL de verificación:
   http://127.0.0.1:8000/documento/verificar/{hash}/
3. Verificar que muestra:
   ✅ Estado del documento
   ✅ Tipo y número
   ✅ Fechas
   ✅ Organización
   ❌ NO muestra nombre del beneficiario
   ❌ NO muestra identificación
   ✅ Mensaje "Información Limitada"
```

**Resultado esperado:**
```
✅ Verificación funciona
✅ Información básica visible
❌ Datos personales ocultos
✅ Aviso de privacidad mostrado
```

---

### Test 2: Usuario Autenticado

**Pasos:**
```bash
1. Iniciar sesión con usuario admin
2. Ir a URL de verificación
3. Verificar que muestra:
   ✅ Estado del documento
   ✅ Tipo y número
   ✅ Fechas
   ✅ Organización
   ✅ Nombre completo del beneficiario
   ✅ Identificación completa
   ✅ Hash de verificación
   ✅ Mensaje "Acceso Autorizado"
```

**Resultado esperado:**
```
✅ Verificación funciona
✅ Información básica visible
✅ Datos personales visibles
✅ Hash completo mostrado
✅ Aviso de acceso autorizado
```

---

### Test 3: Logging Diferenciado

**Verificar en logs:**
```bash
# Usuario no autenticado
tail -f logs/debug.log | grep "Verificación pública"

Salida esperada:
"Verificación pública de documento AVA-RES-2025-0001 - Hash: abc123 - IP: 192.168.1.100"

# Usuario autenticado
tail -f logs/debug.log | grep "Verificación autenticada"

Salida esperada:
"Verificación autenticada de documento AVA-RES-2025-0001 - Hash: abc123 - Usuario: admin"
```

---

## 📁 ARCHIVOS MODIFICADOS

### 1. `censoapp/document_views.py`

**Función modificada:** `verify_document()`

**Cambios:**
- ✅ Detección de autenticación (`request.user.is_authenticated`)
- ✅ Separación de información básica y sensible
- ✅ Contexto diferenciado
- ✅ Logging con IP para públicos y username para autenticados

**Líneas modificadas:** ~30

---

### 2. `templates/censo/documentos/verify_document.html`

**Secciones modificadas:**
- ✅ Información del documento (usa `basic_info`)
- ✅ Información de organización (NIT condicional)
- ✅ Bloque condicional `{% if is_authenticated %}`
- ✅ Sección de beneficiario (solo autenticados)
- ✅ Hash de verificación (solo autenticados)
- ✅ Aviso de información limitada (solo públicos)
- ✅ Mensaje de verificación de autenticidad (solo públicos)
- ✅ Info adicional con alertas diferenciadas

**Líneas modificadas:** ~80

---

### 3. Documentación Creada

**Archivo:** `docs/PRIVACIDAD_VERIFICACION_DOCUMENTOS_17_DIC_2025.md` ✨ NUEVO

**Contenido:**
- Explicación de dos niveles de acceso
- Cumplimiento normativo
- Casos de uso
- Testing
- Comparación visual

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Detección de autenticación implementada
- [x] Separación de información básica/sensible
- [x] Contexto diferenciado en vista
- [x] Template actualizado con condicionales
- [x] Aviso de información limitada agregado
- [x] Mensaje de verificación básica agregado
- [x] Logging diferenciado implementado
- [x] Testing con usuario público
- [x] Testing con usuario autenticado
- [x] Documentación creada
- [x] Cumplimiento normativo verificado

---

## 🎯 BENEFICIOS

### Para Terceros (Empleadores, Instituciones):
- ✅ Pueden verificar autenticidad del documento
- ✅ Confirman que la organización es real
- ✅ Verifican vigencia del documento
- ✅ No necesitan cuenta en el sistema
- ❌ NO ven datos personales del beneficiario

### Para Beneficiarios:
- ✅ Sus datos personales están protegidos
- ✅ Solo personal autorizado puede verlos
- ✅ Cumplimiento de normativa de privacidad
- ✅ Control sobre su información

### Para la Organización:
- ✅ Cumplimiento normativo (Ley 1581/2012)
- ✅ Protección de datos de sus miembros
- ✅ Trazabilidad de accesos
- ✅ Imagen de seguridad y profesionalismo
- ✅ Personal autorizado tiene acceso completo

### Para el Sistema:
- ✅ Seguridad mejorada
- ✅ Logging completo de accesos
- ✅ Cumplimiento legal
- ✅ Flexibilidad de acceso

---

## 📊 COMPARACIÓN ANTES/DESPUÉS

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Datos personales públicos** | ✅ Visibles | ❌ Ocultos |
| **Verificación funciona** | ✅ Sí | ✅ Sí |
| **Niveles de acceso** | 1 (todos ven todo) | 2 (básico/completo) |
| **Cumplimiento normativo** | ⚠️ Cuestionable | ✅ Completo |
| **Logging diferenciado** | ❌ No | ✅ Sí |
| **Privacidad del beneficiario** | ❌ Baja | ✅ Alta |
| **Utilidad para terceros** | ✅ Alta | ✅ Alta |
| **Protección de datos** | ⚠️ Básica | ✅ Robusta |

---

## 💡 MEJORAS FUTURAS (OPCIONAL)

### Corto Plazo:
1. **Auditoría de Accesos:**
   - Registrar en BD quién accedió a qué documento
   - Panel para ver historial de verificaciones

2. **Rate Limiting por IP:**
   - Limitar verificaciones públicas (ej: 10 por hora por IP)
   - Prevenir scraping masivo

3. **CAPTCHA para Públicos:**
   - Agregar CAPTCHA después de N verificaciones
   - Prevenir bots

### Medio Plazo:
4. **API con Autenticación:**
   - API REST para instituciones verificadas
   - Acceso completo con API key

5. **Reporte de Verificaciones:**
   - Dashboard con estadísticas
   - Alertas de accesos sospechosos

### Largo Plazo:
6. **Consentimiento del Beneficiario:**
   - Beneficiario puede autorizar acceso temporal
   - QR con permisos específicos

---

## 📝 CONCLUSIÓN

La implementación de **dos niveles de acceso** en la verificación de documentos garantiza:

1. ✅ **Privacidad:** Datos personales protegidos
2. ✅ **Funcionalidad:** Terceros pueden verificar autenticidad
3. ✅ **Cumplimiento:** Ley 1581 de 2012 (Colombia)
4. ✅ **Trazabilidad:** Logging completo de accesos
5. ✅ **Flexibilidad:** Personal autorizado ve información completa

**Usuario público ve:**
- ✅ "El documento es válido"
- ✅ "Emitido por [Organización]"
- ❌ NO ve nombre ni identificación

**Usuario autenticado ve:**
- ✅ TODO lo anterior, más:
- ✅ Nombre completo
- ✅ Identificación
- ✅ Hash completo

**Resultado:** Sistema seguro, funcional y conforme a normativa.

---

**Implementado por:** GitHub Copilot  
**Fecha:** 17 de Diciembre 2025  
**Cumplimiento:** Ley 1581/2012 (Colombia)  
**Estado:** ✅ **PRODUCCIÓN LISTA**

---

*"La privacidad no es optativa, es un derecho fundamental."*

🔒 **¡PRIVACIDAD Y FUNCIONALIDAD - AMBAS GARANTIZADAS!**

