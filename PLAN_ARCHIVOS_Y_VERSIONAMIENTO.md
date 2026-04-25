# 📋 Análisis de Archivos Sin Seguimiento y Plan de Acción

## ✅ Archivos a INCLUIR en el Repositorio

### 1. **package.json** ✅ SUBIR
**Razón:** Define dependencias de frontend (Tailwind CSS, Alpine.js, Chart.js)
**Propósito:** Otros desarrolladores necesitan saber qué instalar
**Comando:** `git add package.json`

### 2. **tailwind.config.js** ✅ SUBIR
**Razón:** Configuración de Tailwind CSS personalizada para el proyecto
**Propósito:** Define colores, breakpoints, plugins del proyecto
**Comando:** `git add tailwind.config.js`

### 3. **postcss.config.js** ✅ SUBIR
**Razón:** Configuración de PostCSS (procesador CSS)
**Propósito:** Necesario para compilar Tailwind correctamente
**Comando:** `git add postcss.config.js`

### 4. **pyproject.toml** ✅ SUBIR
**Razón:** Configuración de herramientas Python (Black, isort, pytest)
**Propósito:** Mantener consistencia de código entre desarrolladores
**Comando:** `git add pyproject.toml`

### 5. **setup.cfg** ✅ SUBIR
**Razón:** Configuración adicional de herramientas de linting
**Propósito:** Reglas de Flake8, coverage, etc.
**Comando:** `git add setup.cfg`

### 6. **VERSION** ✅ SUBIR (recién creado)
**Razón:** Archivo de versión del proyecto
**Propósito:** Semantic versioning
**Comando:** `git add VERSION`

### 7. **CHANGELOG.md** ✅ SUBIR (recién creado)
**Razón:** Historial de cambios del proyecto
**Propósito:** Documentar todas las versiones y cambios
**Comando:** `git add CHANGELOG.md`

---

## ❌ Archivos a NO INCLUIR en el Repositorio

### 1. **node_modules/** ❌ NO SUBIR (Ya en .gitignore)
**Razón:** Carpeta de dependencias npm (puede pesar 100+ MB)
**Solución:** Ya agregado a .gitignore
**Los desarrolladores ejecutan:** `npm install` para obtenerlas

### 2. **package-lock.json** ❌ NO SUBIR (Ya en .gitignore)
**Razón:** Archivo de lock de npm (genera conflictos)
**Solución:** Ya agregado a .gitignore
**Se regenera automáticamente con:** `npm install`

### 3. **.pre-commit-config.yaml** ⚠️ OPCIONAL
**Razón:** Configuración de pre-commit hooks
**Problema actual:** Está causando errores (python3.11 not found)
**Recomendación:** NO subir hasta corregir errores
**O deshabilitarlo temporalmente**

### 4. **.idea/censo-django.iml** ❌ NO SUBIR
**Razón:** Archivo de configuración de PyCharm (específico del usuario)
**Solución:** Ya debería estar en .gitignore por la carpeta `.idea/`

---

## 📊 Estado Actual vs Recomendado

### Estado Actual:
```
Untracked files:
  ✅ package.json              → ✅ SUBIR
  ✅ tailwind.config.js        → ✅ SUBIR
  ✅ postcss.config.js         → ✅ SUBIR
  ✅ pyproject.toml            → ✅ SUBIR
  ✅ setup.cfg                 → ✅ SUBIR
  ❌ node_modules/             → ❌ YA en .gitignore
  ❌ package-lock.json         → ❌ YA en .gitignore
  ⚠️ .pre-commit-config.yaml  → ⚠️ OMITIR (errores)
  ❌ .idea/                    → ❌ YA en .gitignore
```

---

## 🚀 Plan de Acción Completo

### FASE 1: Actualizar .gitignore ✅ COMPLETADO

```bash
# Ya se agregó a .gitignore:
node_modules/
package-lock.json
static/css/output.css
static/css/output.css.map
```

### FASE 2: Agregar Archivos Necesarios

```bash
cd C:\Users\luisg\PycharmProjects\censo-django

# Agregar archivos de configuración frontend
git add package.json
git add tailwind.config.js
git add postcss.config.js

# Agregar archivos de configuración Python
git add pyproject.toml
git add setup.cfg

# Agregar sistema de versionamiento
git add VERSION
git add CHANGELOG.md

# Agregar .gitignore actualizado
git add .gitignore

# Verificar qué se va a subir
git status
```

### FASE 3: Commit en Development

```bash
git commit -m "build: Agregar configuración de Tailwind CSS y sistema de versionamiento

- Agregado package.json con dependencias de frontend
- Agregado tailwind.config.js y postcss.config.js
- Agregado pyproject.toml y setup.cfg para tooling
- Implementado sistema de versionamiento semántico (VERSION + CHANGELOG.md)
- Actualizado .gitignore para excluir node_modules y archivos generados
- Versión: 2.1.0"
```

### FASE 4: Merge a Main (Producción)

```bash
# 1. Asegurarse de estar en development con todo commiteado
git status  # Debe decir "working tree clean"

# 2. Cambiar a main
git checkout main

# 3. Pull de cambios remotos (si los hay)
git pull origin main

# 4. Merge desde development
git merge development

# 5. Crear tag de versión
git tag -a v2.1.0 -m "Release v2.1.0 - Sistema de versionamiento y configuración Tailwind

Added:
- Sistema de versionamiento semántico
- Configuración de Tailwind CSS
- Documentación consolidada de deploy
- Script helper para producción

Fixed:
- Configuración de variables de entorno en producción
- Error de tabla loginattempt
- Configuración WSGI

Changed:
- Consolidada documentación en README.md
- Optimizado proceso de deploy"

# 6. Push main y tags
git push origin main
git push origin v2.1.0

# 7. Volver a development
git checkout development
```

### FASE 5: Actualizar Producción (PythonAnywhere)

```bash
# En PythonAnywhere Bash Console

# 1. Ir al proyecto
cd /home/luisga64/censo-django

# 2. Activar virtualenv
source /home/luisga64/.virtualenvs/venv/bin/activate

# 3. Cambiar a rama main
git checkout main

# 4. Pull de cambios
git pull origin main

# 5. Instalar dependencias frontend (si se usa Tailwind)
# NOTA: Verificar primero si npm está disponible
npm install

# 6. Compilar Tailwind (si se usa)
npm run build

# 7. Configurar Django settings
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere

# 8. Migrar BD (si hay cambios)
python manage.py migrate

# 9. Collectstatic
python manage.py collectstatic --noinput

# 10. Recargar aplicación
# Web tab → Reload button
```

---

## ⚠️ Sobre .

pre-commit-config.yaml

### Problema Actual:
```
Error: python3.11 not found
```

### Soluciones:

**Opción 1: Deshabilitarlo temporalmente**
```bash
# Renombrar para que no se ejecute
mv .pre-commit-config.yaml .pre-commit-config.yaml.disabled
```

**Opción 2: Corregirlo**
```bash
# Editar .pre-commit-config.yaml
# Cambiar: python3.11 → python3.12 (tu versión actual)
```

**Opción 3: Desinstalarlo**
```bash
pre-commit uninstall
rm .pre-commit-config.yaml
```

**Recomendación:** Por ahora, deshabilitarlo (Opción 1) o eliminarlo (Opción 3)

---

## 🎯 Resumen de Impacto

### ¿Afectarán estos archivos al proyecto?

✅ **package.json, tailwind.config.js, postcss.config.js**
- **NO afectan** si no usas npm/Tailwind activamente
- **SÍ necesarios** si quieres usar Tailwind en el futuro
- **Recomendación:** Subirlos para que el proyecto esté completo

✅ **pyproject.toml, setup.cfg**
- **NO afectan** el funcionamiento de la app
- **SÍ útiles** para mantener calidad de código
- **Recomendación:** Subirlos (son buenas prácticas)

✅ **VERSION, CHANGELOG.md**
- **NO afectan** el funcionamiento
- **SÍ esenciales** para versionamiento profesional
- **Recomendación:** Subirlos definitivamente

❌ **node_modules/, package-lock.json**
- **SÍ afectarían** (negativamente) si se suben
- Harían el repo muy pesado (100+ MB)
- **Recomendación:** Mantener en .gitignore

---

## 📝 Checklist Final

### Antes de Continuar:

- [ ] .gitignore actualizado con node_modules y archivos generados
- [ ] Archivos a subir identificados (package.json, tailwind.config.js, etc.)
- [ ] VERSION y CHANGELOG.md creados
- [ ] README.md actualizado con sección de deploy
- [ ] Pre-commit deshabilitado o corregido
- [ ] Git working tree limpio

### Después de Merge a Main:

- [ ] Tag de versión creado (v2.1.0)
- [ ] Main pusheado a GitHub
- [ ] Tag pusheado a GitHub
- [ ] Producción actualizada desde main
- [ ] WSGI configurado: `settings_pythonanywhere`
- [ ] Aplicación web recargada
- [ ] Sitio verificado funcionando
- [ ] Error log revisado

---

## 🔄 Workflow Futuro Recomendado

```
┌──────────────┐
│ Development  │  ← Desarrollo diario, features, fixes
└──────┬───────┘
       │ (cuando está estable)
       ↓
┌──────────────┐
│     Main     │  ← Solo código probado y estable
└──────┬───────┘
       │ (crear tag)
       ↓
┌──────────────┐
│     Tag      │  ← v2.1.0, v2.2.0, etc.
└──────┬───────┘
       │ (deploy)
       ↓
┌──────────────┐
│  Producción  │  ← PythonAnywhere usa main
└──────────────┘
```

### Proceso:
1. Trabajar en `development`
2. Cuando esté listo: merge a `main`
3. Crear tag con versión
4. Deploy desde `main` en producción
5. Volver a `development` para siguiente feature

---

**Próximo paso recomendado:** Ejecutar FASE 2 y FASE 3 para commitear los archivos necesarios.

