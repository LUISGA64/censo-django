# 🏠 GUÍA DE TRABAJO REMOTO Y SINCRONIZACIÓN

**Sistema de Gestión de Censo para Resguardos Indígenas**  
**Versión:** 1.0  
**Fecha:** 21 de Diciembre de 2024  
**Objetivo:** Trabajar desde casa y oficina manteniendo sincronización

---

## 🎯 PROBLEMA A RESOLVER

**Situación:**
- Trabajo desde casa 🏠
- Trabajo desde oficina 🏢
- Necesito mantener el código sincronizado
- Seguir el roadmap ordenadamente
- No perder progreso

---

## ✅ SOLUCIÓN COMPLETA

### 1. Git y GitHub (Ya lo tienes ✅)

**Ya está funcionando:**
- Repositorio en GitHub: `https://github.com/LUISGA64/censo-django`
- Rama `development` para desarrollo
- Commits organizados

**Flujo de trabajo:**

```bash
# 🏠 EN CASA - Al empezar a trabajar
git pull origin development          # Descargar últimos cambios

# Trabajas en tu código...

git add -A                           # Agregar cambios
git commit -m "feat: descripción"    # Guardar cambios
git push origin development          # Subir a GitHub

# 🏢 EN LA OFICINA - Al empezar a trabajar
git pull origin development          # Descargar cambios de casa

# Trabajas en tu código...

git add -A
git commit -m "feat: descripción"
git push origin development

# 🏠 DE REGRESO A CASA
git pull origin development          # Descargar cambios de oficina
```

**✅ Resultado:** Código siempre sincronizado

---

### 2. Sistema de Tareas con GitHub Projects

**Crear en GitHub:**

```
GitHub → Tu Repositorio → Projects → New Project

Nombre: "Roadmap censo-django v2.0"
Template: Board

Columnas:
📋 Backlog       → Tareas por hacer
🚀 To Do         → Próximas a hacer
⏳ In Progress   → Trabajando ahora
✅ Done          → Completadas
```

**Beneficios:**
- ✅ Visualización clara de tareas
- ✅ Accesible desde cualquier lugar
- ✅ Sincronizado automáticamente
- ✅ Historial de trabajo

**Alternativa Simple (Sin GitHub):**
- Usa el archivo `ROADMAP_TRACKER.md` que voy a crear

---

### 3. Base de Datos Sincronizada

**Opciones:**

#### A. Git con Base de Datos SQLite (Actual)
```bash
# Incluir BD en git (NO RECOMENDADO para producción)
git add db.censo_Web
git commit -m "backup: BD actualizada"
git push
```

**❌ Problema:** Archivo grande, conflictos

#### B. Backup Manual (RECOMENDADO)
```bash
# 🏠 EN CASA - Antes de terminar
python manage.py dumpdata > backup_casa_2024_12_21.json
git add backup_casa_2024_12_21.json
git commit -m "backup: datos casa 21/12"
git push

# 🏢 EN OFICINA - Al llegar
git pull
python manage.py loaddata backup_casa_2024_12_21.json
```

#### C. Base de Datos en la Nube (MEJOR)
```
Opciones:
1. PostgreSQL en Heroku (Gratis hasta 10k filas)
2. PostgreSQL en Railway (Gratis)
3. PostgreSQL en Supabase (Gratis)
4. MySQL en PlanetScale (Gratis)

Ventaja:
- Misma BD desde casa y oficina
- Siempre sincronizada
- No hay que hacer backup manual
```

**Recomendación:** Usa PostgreSQL en Railway (gratis y fácil)

---

### 4. Entorno Virtual Sincronizado

**Problema:** Diferentes versiones de paquetes

**Solución:**

```bash
# Mantener requirements.txt actualizado

# 🏠 EN CASA - Si instalas algo nuevo
pip install nueva-libreria
pip freeze > requirements.txt
git add requirements.txt
git commit -m "deps: agregada nueva-libreria"
git push

# 🏢 EN OFICINA - Al actualizar
git pull
pip install -r requirements.txt
```

---

## 📋 SISTEMA DE SEGUIMIENTO DE ROADMAP

He creado archivos para hacer seguimiento:

### 1. ROADMAP_TRACKER.md
- Lista de tareas del roadmap
- Estado de cada tarea
- Notas de progreso
- Tiempo estimado vs real

### 2. DAILY_LOG.md
- Log diario de trabajo
- Qué hiciste hoy
- Problemas encontrados
- Siguiente paso

### 3. CHECKLIST_SEMANAL.md
- Objetivos de la semana
- Progreso diario
- Revisión de fin de semana

---

## 🔄 FLUJO DE TRABAJO DIARIO RECOMENDADO

### 🌅 AL EMPEZAR EL DÍA (Casa u Oficina)

```bash
# 1. Abrir PowerShell en la carpeta del proyecto
cd C:\Users\luisg\PycharmProjects\censo-django

# 2. Actualizar código
git pull origin development

# 3. Activar entorno virtual
.\venv\Scripts\activate

# 4. Actualizar dependencias (si hay cambios)
pip install -r requirements.txt

# 5. Ver qué tarea sigue
code docs/ROADMAP_TRACKER.md

# 6. Iniciar servidor
python manage.py runserver
```

### 💼 DURANTE EL DÍA

```bash
# Cada hora o al completar una funcionalidad
git add -A
git commit -m "feat: descripción de lo que hiciste"
git push origin development

# Actualizar DAILY_LOG.md con tu progreso
```

### 🌙 AL TERMINAR EL DÍA

```bash
# 1. Guardar TODO
git add -A
git commit -m "wip: trabajo del día DD/MM - descripción"
git push origin development

# 2. Actualizar DAILY_LOG.md
# 3. Actualizar ROADMAP_TRACKER.md con progreso
# 4. Hacer backup de BD (opcional)
python manage.py dumpdata > backup_DD_MM_YYYY.json
git add backup_DD_MM_YYYY.json
git commit -m "backup: BD del día DD/MM"
git push
```

---

## 📱 HERRAMIENTAS ÚTILES

### 1. GitHub Desktop (Recomendado para Windows)

**Descargar:** https://desktop.github.com/

**Ventajas:**
- ✅ Interfaz gráfica fácil
- ✅ Ver cambios visualmente
- ✅ Commits simples
- ✅ Push/Pull con un click
- ✅ No necesitas comandos git

**Uso:**
1. Abre GitHub Desktop
2. Selecciona el repositorio
3. Click "Fetch origin" → Actualiza
4. Haz cambios en el código
5. GitHub Desktop los detecta automáticamente
6. Escribe mensaje de commit
7. Click "Commit to development"
8. Click "Push origin"

---

### 2. Visual Studio Code con Sincronización

**Extensiones útiles:**
- GitLens (visualizar historial git)
- GitHub Pull Requests
- Settings Sync (sincroniza configuración de VSCode)

**Activar Settings Sync:**
1. VSCode → Cuenta → Turn on Settings Sync
2. Login con GitHub
3. Tus configuraciones se sincronizan automáticamente

---

### 3. Notion o Trello (Gestión de Tareas)

**Notion (Gratis):**
```
Crear workspace:
- Base de datos de tareas
- Kanban board
- Calendario
- Notas de progreso
```

**Trello (Gratis):**
```
Crear board "censo-django v2.0":
Listas:
- 📋 Backlog
- 🚀 Esta Semana
- ⏳ En Progreso
- ✅ Completado
```

---

## 🗂️ ESTRUCTURA DE ARCHIVOS DE SEGUIMIENTO

```
censo-django/
├── docs/
│   ├── VERSION_1.0_RELEASE.md           ← Versión actual
│   ├── ROADMAP_V2.0_ANALISIS_COMPLETO.md ← Plan completo
│   ├── ROADMAP_TRACKER.md               ← 🆕 Seguimiento de tareas
│   ├── DAILY_LOG.md                     ← 🆕 Log diario
│   └── CHECKLIST_SEMANAL.md             ← 🆕 Checklist semanal
│
├── backups/                              ← Backups de BD
│   ├── backup_21_12_2024.json
│   └── backup_22_12_2024.json
│
└── .gitignore                            ← Qué NO subir a git
```

---

## ⚠️ PROBLEMAS COMUNES Y SOLUCIONES

### Problema 1: Conflictos de Git

```bash
# Si al hacer git pull dice "conflicto"

# Opción 1: Guardar tus cambios y aplicar los de GitHub
git stash                    # Guardar tus cambios temporalmente
git pull origin development  # Descargar cambios
git stash pop               # Aplicar tus cambios

# Opción 2: Commit forzado
git add -A
git commit -m "wip: cambios locales"
git pull origin development --rebase
git push origin development
```

### Problema 2: BD Diferente en Casa y Oficina

```bash
# Mejor solución: Base de datos en la nube (Railway)

# Alternativa: Backup/Restore
# EN CASA
python manage.py dumpdata > backup.json
git add backup.json && git commit -m "backup BD" && git push

# EN OFICINA
git pull
python manage.py loaddata backup.json
```

### Problema 3: Olvidé hacer push

```bash
# Si trabajaste en casa y olvidaste hacer push
# Y ahora estás en la oficina

# Solución: Trabaja con otra rama
git checkout -b trabajo-oficina
# Trabaja...
git add -A
git commit -m "feat: trabajo oficina"
git push origin trabajo-oficina

# Luego en casa, merge las ramas
git pull
git merge trabajo-oficina
git push origin development
```

---

## 📅 CALENDARIO DE TRABAJO SUGERIDO

### Semana 1: Dashboard Analítico

**Lunes (Casa):**
- Diseñar mockup del dashboard
- Crear vista básica
- Push a GitHub

**Martes (Oficina):**
- Pull de GitHub
- Implementar queries de estadísticas
- Push a GitHub

**Miércoles (Casa):**
- Pull de GitHub
- Agregar gráficos con Chart.js
- Push a GitHub

**Jueves (Oficina):**
- Pull de GitHub
- Implementar cards de KPIs
- Push a GitHub

**Viernes (Casa):**
- Pull de GitHub
- Testing y ajustes finales
- Actualizar ROADMAP_TRACKER.md
- Push a GitHub

---

## 🎯 RECOMENDACIONES FINALES

### DO ✅

1. **Hacer pull SIEMPRE al empezar**
2. **Hacer push SIEMPRE al terminar**
3. **Commits frecuentes** (cada hora o funcionalidad)
4. **Mensajes descriptivos** en commits
5. **Actualizar ROADMAP_TRACKER.md diariamente**
6. **Backup de BD semanalmente**
7. **Usar GitHub Desktop** si no te gusta la consola
8. **Revisar ROADMAP_TRACKER.md** cada mañana

### DON'T ❌

1. **No trabajes días sin hacer pull primero**
2. **No dejes código sin push** al terminar el día
3. **No edites archivos directamente en GitHub**
4. **No ignores conflictos de git**
5. **No trabajes en main**, siempre en development
6. **No subas la BD directamente** (solo backups JSON)
7. **No cambies entorno sin actualizar requirements.txt**

---

## 🚀 SETUP INICIAL (Una Vez)

### En Casa:

```bash
# 1. Ya tienes el proyecto clonado ✅

# 2. Instalar GitHub Desktop
# Descargar de: https://desktop.github.com/

# 3. Configurar git
git config --global user.name "Luis G"
git config --global user.email "tu-email@gmail.com"

# 4. Verificar que está sincronizado
git status
git pull origin development
```

### En la Oficina:

```bash
# 1. Clonar el repositorio
cd C:\Users\luisg\PycharmProjects
git clone https://github.com/LUISGA64/censo-django.git
cd censo-django

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Restaurar BD (si tienes backup)
python manage.py migrate
python manage.py loaddata backup_reciente.json

# 5. Configurar GitHub Desktop
# Abrir GitHub Desktop → Add Repository → Existing
```

---

## 📱 ACCESO RÁPIDO (Bookmarks)

**Guardar estos links:**

- 🌐 GitHub Repo: https://github.com/LUISGA64/censo-django
- 📊 GitHub Projects: https://github.com/LUISGA64/censo-django/projects
- 📝 Issues: https://github.com/LUISGA64/censo-django/issues
- 📥 GitHub Desktop: Icono en escritorio
- 📁 Carpeta Proyecto Casa: `C:\Users\luisg\PycharmProjects\censo-django`
- 📁 Carpeta Proyecto Oficina: `C:\Users\luisg\PycharmProjects\censo-django`

---

## 🎓 RECURSOS ADICIONALES

### Tutoriales Git:
- https://learngitbranching.js.org/ (Interactivo)
- https://github.github.com/training-kit/ (GitHub Training)

### Git Cheat Sheet:
```bash
# Comandos esenciales
git pull origin development   # Descargar cambios
git add -A                    # Agregar todos los cambios
git commit -m "mensaje"       # Guardar cambios
git push origin development   # Subir cambios
git status                    # Ver estado actual
git log --oneline            # Ver historial
```

---

## ✅ CHECKLIST DIARIO

```
🌅 AL EMPEZAR:
□ Abrir proyecto en VSCode
□ git pull origin development
□ Activar venv
□ python manage.py runserver
□ Revisar ROADMAP_TRACKER.md
□ Ver tarea de hoy

💼 DURANTE:
□ Trabajar en la funcionalidad
□ Commit cada hora o feature
□ Actualizar DAILY_LOG.md

🌙 AL TERMINAR:
□ git add -A
□ git commit -m "mensaje descriptivo"
□ git push origin development
□ Actualizar ROADMAP_TRACKER.md
□ Actualizar DAILY_LOG.md
```

---

## 🎯 SIGUIENTE PASO

1. **Lee los archivos que voy a crear:**
   - ROADMAP_TRACKER.md
   - DAILY_LOG.md
   - CHECKLIST_SEMANAL.md

2. **Instala GitHub Desktop** (recomendado)

3. **Empieza con el Dashboard** siguiendo el roadmap

4. **Usa el flujo diario** que te describí arriba

---

**Con este sistema podrás trabajar desde casa y oficina sin problemas, manteniendo todo sincronizado y siguiendo el roadmap ordenadamente.** 🚀

**¿Listo para empezar?** Revisa los archivos que voy a crear a continuación.

