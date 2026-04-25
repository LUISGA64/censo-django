# 📁 Scripts de Utilidad - Censo Web

Esta carpeta contiene scripts útiles para el mantenimiento y deployment del proyecto.

## 🔧 Scripts Disponibles

### Backup y Mantenimiento

#### `backup_auto.ps1` / `backup_auto.sh`
Scripts para backup automático de la base de datos.

**Uso (PowerShell):**
```powershell
.\scripts\backup_auto.ps1
```

**Uso (Linux/Mac):**
```bash
bash scripts/backup_auto.sh
```

**Características:**
- Backup de base de datos con timestamp
- Compresión automática
- Limpieza de backups antiguos (>30 días)

---

#### `backup_database.ps1`
Backup manual de base de datos (Windows).

**Uso:**
```powershell
.\scripts\backup_database.ps1
```

---

### Deployment

#### `deploy_pythonanywhere.sh`
Script de deployment a PythonAnywhere.

**Uso:**
```bash
bash scripts/deploy_pythonanywhere.sh
```

**Acciones:**
- Pull de cambios desde Git
- Instalación de dependencias
- Migración de base de datos
- Colección de archivos estáticos
- Reload de aplicación web

---

### Instalación

#### `install_linux.sh`
Script de instalación completa para Linux.

**Uso:**
```bash
bash scripts/install_linux.sh
```

**Instala:**
- Dependencias del sistema
- Python y pip
- Virtualenv
- Dependencias de Python
- Configuración inicial

---

#### `install_windows.ps1`
Script de instalación completa para Windows.

**Uso:**
```powershell
.\scripts\install_windows.ps1
```

**Instala:**
- Dependencias de Python
- Virtualenv
- Configuración inicial

---

### Servidor de Desarrollo

#### `start_server.ps1`
Inicia el servidor de desarrollo Django (Windows).

**Uso:**
```powershell
.\scripts\start_server.ps1
```

**Características:**
- Activa el entorno virtual automáticamente
- Ejecuta migraciones pendientes
- Inicia servidor en http://127.0.0.1:8000

---

### Diagnóstico y Optimización

#### `optimize_database.py`
Análisis completo de la base de datos.

**Uso:**
```bash
python scripts/optimize_database.py
```

**Proporciona:**
- Estadísticas de registros
- Tamaño de tablas
- Índices actuales
- Sugerencias de optimización
- Análisis de rendimiento de consultas

**Salida:**
```
📊 Registros totales
📈 Promedios
🏆 Top organizaciones
🔍 Índices de base de datos
💡 Sugerencias de índices
⚡ Análisis de rendimiento
```

---

#### `health_check.py`
Verificación de salud del sistema.

**Uso:**
```bash
python scripts/health_check.py
```

**Verifica:**
- Conexión a base de datos
- Configuración de entorno
- Variables críticas

---

## 🚀 Uso Recomendado

### Desarrollo Local

**Iniciar servidor:**
```powershell
.\scripts\start_server.ps1
```

**Optimizar base de datos:**
```bash
python scripts/optimize_database.py
```

**Crear backup:**
```powershell
.\scripts\backup_database.ps1
```

---

### Producción (PythonAnywhere)

**Deploy completo:**
```bash
bash scripts/deploy_pythonanywhere.sh
```

**Backup automático (crontab):**
```bash
# Ejecutar diariamente a las 2 AM
0 2 * * * cd ~/censo-django && bash scripts/backup_auto.sh
```

---

### Mantenimiento

**Análisis de base de datos:**
```bash
# Semanal
python scripts/optimize_database.py

# Revisar salida y aplicar recomendaciones
```

**Health check:**
```bash
# Antes y después de cambios importantes
python scripts/health_check.py
```

---

## 📋 Checklist de Mantenimiento

### Diario
- [ ] Health check en producción
- [ ] Revisar logs de errores

### Semanal
- [ ] Ejecutar optimize_database.py
- [ ] Verificar backups automáticos
- [ ] Limpiar backups antiguos

### Mensual
- [ ] Backup manual completo
- [ ] Auditoría de seguridad
- [ ] Optimizar tablas MySQL
- [ ] Actualizar dependencias

---

## 🔒 Seguridad

**Credenciales:**
- Nunca hardcodear credenciales en scripts
- Usar variables de entorno
- Mantener .env en .gitignore

**Backups:**
- Encriptar backups en producción
- Almacenar en ubicación segura
- Probar restauración regularmente

---

## 📝 Notas

### PowerShell (.ps1)
Los scripts de PowerShell son para Windows. Ejecutar con:
```powershell
.\scripts\nombre_script.ps1
```

Si hay error de ejecución, habilitar scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Bash (.sh)
Los scripts de Bash son para Linux/Mac. Dar permisos de ejecución:
```bash
chmod +x scripts/*.sh
```

### Python (.py)
Los scripts de Python funcionan en todos los sistemas:
```bash
python scripts/nombre_script.py
```

---

## 🆘 Solución de Problemas

### Script no se ejecuta (PowerShell)
```powershell
# Verificar política de ejecución
Get-ExecutionPolicy

# Cambiar si es necesario
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Script no se ejecuta (Bash)
```bash
# Dar permisos
chmod +x scripts/nombre_script.sh

# Verificar shebang
head -1 scripts/nombre_script.sh
# Debería ser: #!/bin/bash
```

### Error en Python
```bash
# Verificar entorno virtual
which python  # Linux/Mac
where python  # Windows

# Activar si es necesario
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

---

## 📞 Soporte

- **Documentación:** [MANUAL_MANTENIMIENTO.md](../MANUAL_MANTENIMIENTO.md)
- **Issues:** https://github.com/LUISGA64/censo-django/issues
- **Email:** webcenso@gmail.com

---

**Última actualización:** 2026-02-08  
**Versión:** 2.0
