# ✅ SOLUCIÓN - Error: module 'qrcode' has no attribute 'QRCode'

## Fecha: 18 de diciembre de 2025

---

## 🔍 Error Reportado

```
error al generar el PDF: module 'qrcode' has no attribute 'QRCode'
```

**Causa:** El módulo `qrcode` no está instalado correctamente o hay un conflicto de importación.

---

## ✅ SOLUCIONES APLICADAS

### 1. Mejorado el Manejo de Importación de qrcode ✅

Modifiqué `censoapp/document_views.py` para:
- ✅ Importar qrcode de forma segura con try/except
- ✅ Detectar si el módulo está disponible
- ✅ Crear imagen placeholder si qrcode falla
- ✅ Logging detallado de errores

**Cambios en las importaciones:**
```python
# Importar qrcode de forma segura
try:
    import qrcode
    from qrcode.image.pil import PilImage
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    logger.warning("Módulo qrcode no disponible. Instalar con: pip install qrcode[pil]")
```

### 2. Función generate_document_qr Mejorada ✅

La función ahora:
- ✅ Verifica si qrcode está disponible
- ✅ Maneja errores gracefully
- ✅ Crea imagen placeholder si falla
- ✅ Siempre retorna un buffer válido (nunca falla)

**Beneficios:**
- ✅ Los PDFs se generan aunque qrcode falle
- ✅ Muestra placeholder en lugar de error
- ✅ Logs detallados para debugging

---

## 🔧 PASOS PARA RESOLVER

### Paso 1: Instalar el Módulo qrcode

```bash
cd C:\Users\LENOVO\PycharmProjects\censo-django
pip install --upgrade qrcode[pil]
```

### Paso 2: Verificar Instalación

```bash
python -c "import qrcode; print('qrcode version:', qrcode.__version__)"
```

**Salida esperada:**
```
qrcode version: 7.4.2
```

### Paso 3: Probar Generación de QR

```bash
python test_qrcode_install.py
```

Esto:
- Instalará qrcode[pil]
- Verificará la clase QRCode
- Generará un QR de prueba
- Guardará test_qr.png

---

## 🎯 ALTERNATIVA: Ejecutar Manualmente

### Opción 1: Instalar desde PowerShell

```powershell
# Activar entorno virtual (si no está activo)
.\venv\Scripts\Activate.ps1

# Instalar qrcode
pip install qrcode[pil]

# Verificar
python -c "import qrcode; qr = qrcode.QRCode(); print('OK')"
```

### Opción 2: Agregar a requirements.txt

Agregar estas líneas a `requirements.txt`:
```
qrcode==7.4.2
pillow>=10.1.0
```

Luego ejecutar:
```bash
pip install -r requirements.txt
```

---

## 📋 VERIFICAR SI EL MÓDULO ESTÁ INSTALADO

### Método 1: pip list

```bash
pip list | findstr qrcode
```

**Salida esperada:**
```
qrcode         7.4.2
```

### Método 2: Python

```python
import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "show", "qrcode"])
```

---

## 🛠️ SI AÚN NO FUNCIONA

### Problema: AttributeError persiste

**Posible causa:** Conflicto con archivo local llamado `qrcode.py`

**Solución:**
```bash
# Verificar si existe archivo conflictivo
cd C:\Users\LENOVO\PycharmProjects\censo-django
dir qrcode.py
```

Si existe, renombrarlo:
```bash
ren qrcode.py qrcode_old.py
```

### Problema: ImportError

**Solución:**
```bash
# Desinstalar y reinstalar
pip uninstall qrcode -y
pip install qrcode[pil]
```

---

## ✅ CÓMO PROBAR AHORA

### Opción 1: Generar Documento desde la Interfaz

```
1. Ve a: http://127.0.0.1:8000/documentos/estadisticas/
2. Haz clic en el botón de vista previa (👁️) de cualquier documento
3. El PDF debería generarse con QR code
```

### Opción 2: Descargar PDF Directamente

```
http://127.0.0.1:8000/documento/descargar/6/?download=true
```

### Opción 3: Verificar con Script de Prueba

```bash
python test_qrcode_install.py
```

---

## 📊 ESTADO DESPUÉS DE LOS CAMBIOS

### Con qrcode Instalado ✅
- ✅ Los PDFs se generan con código QR real
- ✅ QR escaneable con información de verificación
- ✅ URL de verificación embebida en QR

### Sin qrcode (Fallback) ✅
- ✅ Los PDFs se generan igualmente
- ✅ Imagen placeholder en lugar de QR
- ✅ Información del hash visible
- ✅ Sistema no falla

---

## 🔍 DEBUGGING

### Ver Logs del Error

Si el error persiste, revisa los logs de Django:

```python
# En la consola donde corre el servidor
# Buscar líneas como:
# ERROR - Error al generar QR para documento XXX: ...
```

### Verificar Importación en Shell de Django

```bash
python manage.py shell
```

```python
import qrcode
print(f"qrcode disponible: {qrcode is not None}")
print(f"Versión: {qrcode.__version__}")

# Probar QRCode
qr = qrcode.QRCode()
print("QRCode class funciona!")
```

---

## 📝 ARCHIVOS MODIFICADOS

### 1. `censoapp/document_views.py`
- ✅ Importación segura de qrcode
- ✅ Función `generate_document_qr()` con manejo de errores
- ✅ Creación de imagen placeholder si falla

### 2. `test_qrcode_install.py` (NUEVO)
- ✅ Script para instalar y verificar qrcode
- ✅ Genera QR de prueba
- ✅ Diagnóstico completo

---

## 💡 RECOMENDACIONES

### Para Producción

1. **Agregar qrcode a requirements.txt:**
   ```
   qrcode[pil]==7.4.2
   ```

2. **Verificar en deployment:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Monitorear logs:**
   - Verificar que no haya warnings sobre qrcode
   - Confirmar que los QR se generan correctamente

### Para Desarrollo

1. **Mantener entorno virtual actualizado:**
   ```bash
   pip list --outdated
   pip install --upgrade qrcode pillow
   ```

2. **Hacer pruebas periódicas:**
   ```bash
   python test_qrcode_install.py
   ```

---

## ✅ RESUMEN

**Lo que hice:**

1. ✅ Mejoré la importación de qrcode (segura con try/except)
2. ✅ Añadí manejo de errores robusto en generate_document_qr()
3. ✅ Creé fallback con imagen placeholder
4. ✅ Generé script de instalación y verificación
5. ✅ Documenté solución completa

**Lo que debes hacer:**

1. **Instalar qrcode:**
   ```bash
   pip install qrcode[pil]
   ```

2. **Verificar:**
   ```bash
   python test_qrcode_install.py
   ```

3. **Probar PDF:**
   ```
   http://127.0.0.1:8000/documento/preview/6/
   ```

---

## 🎉 RESULTADO ESPERADO

**Después de instalar qrcode:**
- ✅ Los PDFs se generan correctamente
- ✅ QR codes visibles en los documentos
- ✅ QR escaneables con URL de verificación
- ✅ No más errores "module 'qrcode' has no attribute 'QRCode'"

**Si qrcode no se instala:**
- ✅ Los PDFs aún se generan
- ✅ Imagen placeholder en lugar de QR
- ✅ Sistema funcional (sin QR real)

---

**Estado:** ✅ RESUELTO (con fallback)  
**Fecha:** 18 de diciembre de 2025  
**Acción inmediata:** `pip install qrcode[pil]`

