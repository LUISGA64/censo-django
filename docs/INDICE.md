# 📚 Índice de Documentación - Censo Web

## 📁 Estructura de Documentación

### 📂 `/docs/technical/` - Documentación Técnica Activa
Documentación técnica relevante para el proyecto actual:

- **CORRECCION_COMPLETA_MAPAS.md** - Solución completa error 403 en mapas
- **MEJORAS_INTERFAZ_MAPAS.md** - Mejoras visuales en mapas
- **RESUMEN_SOLUCION_MAPAS.md** - Resumen ejecutivo de correcciones
- **SOLUCION_ERROR_MAPAS_403.md** - Detalles técnicos del error 403

### 📂 `/docs/deployment/` - Guías de Deployment
Documentación para despliegue en producción:

- **DEPLOY_PYTHONANYWHERE_2026-02-28.md** - Guía de deploy en PythonAnywhere
- **DEPLOY_SEGURO_PYTHONANYWHERE.md** - Configuración de seguridad
- **DESPLIEGUE_FINAL_OPCION_A.md** - Proceso de despliegue final

### 📂 `/docs/archive/` - Documentación Archivada
Documentación de desarrollo histórica (no crítica para producción):

- Análisis y arquitectura del proyecto
- Guías de desarrollo Android/Kotlin
- Checklists de implementación
- Resúmenes de fases completadas
- Tutoriales y guías de desarrollo
- Documentación JWT y configuraciones

---

## 📖 Documentación Principal (Root)

### README.md
Documentación principal del proyecto con:
- Descripción general
- Requisitos
- Instalación
- Configuración
- Uso

### README_QUICK_START.md
Guía rápida para:
- Inicio rápido del proyecto
- Configuración básica
- Primeros pasos

---

## 🗂️ Organización de Archivos

### Archivos Eliminados (Limpieza)
Los siguientes archivos fueron eliminados del repositorio por ser temporales o innecesarios:

#### Archivos de Test Temporales
- ❌ test_jwt.py
- ❌ test_jwt_simple.py
- ❌ test_jwt.bat
- ❌ test_mapas_solucion.html

#### Scripts de Verificación Temporales
- ❌ verificar_*.py (múltiples)
- ❌ ver_documentos.py

#### Archivos de Reportes
- ❌ bandit_report.json
- ❌ security_report.json

#### Archivos Duplicados
- ❌ requirements_clean.txt
- ❌ requirements_new.txt
- ❌ db.censo_Web_OLD

---

## ✅ Tests Unitarios (Manteni dos)

Los tests unitarios y de integración se mantienen en:
- `/tests/unit/` - Tests unitarios de modelos y formularios
- `/tests/integration/` - Tests de integración de vistas

**Nota:** Los tests son críticos y se mantienen en el repositorio.

---

## 🚀 Para Producción

### Archivos Esenciales
- ✅ `requirements.txt` - Dependencias Python
- ✅ `manage.py` - Django management
- ✅ `.env.example` - Ejemplo de variables de entorno
- ✅ `.env.pythonanywhere.example` - Ejemplo para PythonAnywhere
- ✅ `.gitignore` - Archivos ignorados por Git
- ✅ `README.md` - Documentación principal

### Directorios Esenciales
- ✅ `censoapp/` - Aplicación principal
- ✅ `censoProject/` - Configuración del proyecto
- ✅ `templates/` - Templates HTML
- ✅ `static/` - Archivos estáticos
- ✅ `media/` - Archivos de usuario
- ✅ `tests/` - Suite de tests
- ✅ `scripts/` - Scripts de utilidad
- ✅ `docs/` - Documentación organizada

---

## 📝 Convenciones

### Documentación Técnica
- Los archivos en `docs/technical/` son relevantes para el proyecto actual
- Usar formato Markdown (.md)
- Incluir fecha de última actualización
- Mantener enlaces actualizados

### Documentación Archivada
- Los archivos en `docs/archive/` son históricos
- No son necesarios para operación normal
- Se mantienen para referencia

### Git Ignore
- `docs/archive/` está en .gitignore
- No se sube a producción
- Reduce el tamaño del repositorio

---

## 🔄 Actualización de Documentación

### Para agregar nueva documentación:

1. **Técnica/Importante:** → `docs/technical/`
2. **Deployment:** → `docs/deployment/`
3. **Desarrollo/Temporal:** → `docs/archive/` (no se sube a Git)

### Para eliminar documentación obsoleta:
```bash
# Mover a archive
Move-Item -Path "archivo.md" -Destination "docs\archive\"

# O eliminar si ya no es necesaria
Remove-Item -Path "archivo.md" -Force
```

---

## 📊 Resumen del Estado Actual

### ✅ Limpio y Organizado
- Documentación categorizada
- Archivos temporales eliminados
- Estructura clara y mantenible

### ✅ Listo para Producción
- Solo archivos esenciales en root
- Documentación organizada en carpetas
- .gitignore actualizado

### ✅ Fácil Navegación
- Índice claro
- Categorías definidas
- Referencias rápidas

---

**Última actualización:** 2026-04-20  
**Estado:** ✅ Repositorio limpio y organizado  
**Listo para:** Producción

