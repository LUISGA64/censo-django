# Guía de Instalación para Cliente - Sistema de Censo

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación en Windows](#instalación-en-windows)
3. [Instalación en Linux](#instalación-en-linux)
4. [Configuración Inicial](#configuración-inicial)
5. [Carga de Datos Iniciales](#carga-de-datos-iniciales)
6. [Verificación de la Instalación](#verificación-de-la-instalación)
7. [Solución de Problemas](#solución-de-problemas)
8. [Mantenimiento](#mantenimiento)

---

## 📌 Requisitos Previos

### Hardware Mínimo Recomendado

- **Procesador:** Intel Core i3 o equivalente (2 núcleos)
- **RAM:** 4 GB mínimo, 8 GB recomendado
- **Disco Duro:** 20 GB de espacio libre
- **Conexión a Internet:** Solo para instalación inicial (opcional para operación)

### Software Requerido

- **Sistema Operativo:** Windows 10/11 o Linux (Ubuntu 20.04+, CentOS 7+)
- **Python:** Versión 3.8 o superior
- **Navegador Web:** Google Chrome, Firefox, Edge (última versión)

---

## 🪟 Instalación en Windows

### Paso 1: Instalar Python

1. Descargar Python desde: https://www.python.org/downloads/
2. Ejecutar el instalador
3. ✅ **IMPORTANTE:** Marcar "Add Python to PATH"
4. Completar la instalación

### Paso 2: Verificar Instalación de Python

Abrir PowerShell o CMD y ejecutar:

```powershell
python --version
pip --version
```

### Paso 3: Ejecutar Script de Instalación Automática

1. Descomprimir el archivo del sistema en `C:\censo-django`
2. Abrir PowerShell como Administrador
3. Navegar a la carpeta del proyecto:

```powershell
cd C:\censo-django
```

4. Ejecutar el script de instalación:

```powershell
.\scripts\install_windows.ps1
```

### Paso 4: Iniciar el Sistema

```powershell
.\scripts\start_server.ps1
```

El sistema estará disponible en: **http://localhost:8000**

---

## 🐧 Instalación en Linux

### Paso 1: Actualizar el Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### Paso 2: Instalar Dependencias

```bash
sudo apt install -y python3 python3-pip python3-venv git
```

### Paso 3: Ejecutar Script de Instalación

1. Descomprimir el archivo en `/opt/censo-django`
2. Navegar a la carpeta:

```bash
cd /opt/censo-django
```

3. Dar permisos de ejecución:

```bash
chmod +x scripts/install_linux.sh
chmod +x scripts/start_server.sh
```

4. Ejecutar instalación:

```bash
sudo ./scripts/install_linux.sh
```

### Paso 4: Iniciar el Sistema

```bash
./scripts/start_server.sh
```

El sistema estará disponible en: **http://localhost:8000**

---

## ⚙️ Configuración Inicial

### 1. Acceso al Sistema

1. Abrir navegador web
2. Ir a: `http://localhost:8000` o `http://IP-DEL-SERVIDOR:8000`
3. Credenciales iniciales:
   - **Usuario:** admin
   - **Contraseña:** admin123 (cambiar inmediatamente)

### 2. Cambiar Contraseña de Administrador

1. Iniciar sesión con credenciales iniciales
2. Ir a perfil de usuario (esquina superior derecha)
3. Seleccionar "Cambiar Contraseña"
4. Ingresar nueva contraseña segura

### 3. Configurar Asociación y Organización

1. Ir a **"Gestión de Asociación"**
2. Editar datos de la asociación:
   - Nombre
   - NIT
   - Dirección
   - Contacto
   - Logo (archivo PNG o JPG)

3. Ir a **"Gestión de Organizaciones"**
4. Crear o editar organizaciones (resguardos):
   - Nombre del resguardo
   - NIT
   - Territorio
   - Información de contacto
   - Logo

### 4. Crear Veredas

1. Ir a **"Admin" → "Veredas"**
2. Agregar las veredas correspondientes a cada organización

### 5. Configurar Parámetros del Sistema

1. Ir a **"Admin" → "System Parameters"**
2. Revisar y ajustar parámetros según necesidades:
   - `Datos de Vivienda`: S/N

### 6. Crear Usuarios Operadores

1. Ir a **"Admin" → "Usuarios"**
2. Crear usuarios para operadores
3. Asignar a cada usuario:
   - Organización correspondiente
   - Rol (Admin, Operador, Consulta)
   - Permisos específicos

---

## 📊 Carga de Datos Iniciales

### Catálogos Pre-cargados

El sistema incluye catálogos pre-cargados:

✅ Tipos de documento de identidad  
✅ Géneros  
✅ Estados civiles  
✅ Niveles educativos  
✅ EPS principales de Colombia  
✅ Tipos de parentesco  
✅ Ocupaciones comunes  
✅ Materiales de construcción  
✅ Tipos de combustible  
✅ Fuentes de agua  

### Validar Catálogos

1. Ir a **"Admin"**
2. Verificar cada catálogo
3. Agregar elementos faltantes según necesidad regional

---

## ✅ Verificación de la Instalación

### Lista de Verificación

- [ ] Python instalado correctamente
- [ ] Entorno virtual creado y activado
- [ ] Todas las dependencias instaladas
- [ ] Base de datos creada y migrada
- [ ] Datos iniciales cargados
- [ ] Servidor iniciado sin errores
- [ ] Acceso al sistema desde navegador
- [ ] Login con usuario admin exitoso
- [ ] Asociación configurada
- [ ] Al menos una organización creada
- [ ] Veredas creadas
- [ ] Usuarios operadores creados

### Comandos de Verificación

**Windows:**
```powershell
cd C:\censo-django
.\scripts\verify_installation.ps1
```

**Linux:**
```bash
cd /opt/censo-django
./scripts/verify_installation.sh
```

---

## 🔧 Solución de Problemas

### Error: "Python no reconocido"

**Solución:**
1. Reinstalar Python marcando "Add to PATH"
2. Reiniciar terminal/PowerShell
3. Verificar con `python --version`

### Error: "No module named 'django'"

**Solución:**
```powershell
# Activar entorno virtual
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

**Solución:**

**Windows:**
```powershell
# Encontrar proceso
netstat -ano | findstr :8000
# Matar proceso (reemplazar PID)
taskkill /PID <PID> /F
```

**Linux:**
```bash
# Encontrar y matar proceso
sudo lsof -ti:8000 | xargs kill -9
```

### Error: "Database is locked"

**Solución:**
1. Cerrar el servidor
2. Eliminar archivo `db.sqlite3-journal` si existe
3. Reiniciar el servidor

### Error: "Static files not found"

**Solución:**
```powershell
python manage.py collectstatic --noinput
```

### No se pueden subir imágenes/logos

**Solución:**
1. Verificar que existe la carpeta `media/`
2. Verificar permisos de escritura
3. En Linux: `sudo chmod -R 755 media/`

---

## 🔄 Mantenimiento

### Respaldo de Base de Datos

**Windows:**
```powershell
.\scripts\backup_database.ps1
```

**Linux:**
```bash
./scripts/backup_database.sh
```

Los respaldos se guardan en: `backups/backup_YYYYMMDD_HHMMSS.json`

### Restaurar Base de Datos

**Windows:**
```powershell
python manage.py loaddata backups\backup_NOMBRE.json
```

**Linux:**
```bash
python manage.py loaddata backups/backup_NOMBRE.json
```

### Actualizar el Sistema

1. Detener el servidor
2. Realizar respaldo completo
3. Reemplazar archivos del sistema
4. Ejecutar migraciones:

```powershell
python manage.py migrate
```

5. Reiniciar servidor

### Limpieza de Archivos Temporales

**Windows:**
```powershell
.\scripts\cleanup.ps1
```

**Linux:**
```bash
./scripts/cleanup.sh
```

### Monitoreo de Logs

Los logs se guardan en: `logs/censo.log`

**Ver últimos logs:**

**Windows:**
```powershell
Get-Content logs\censo.log -Tail 50
```

**Linux:**
```bash
tail -f logs/censo.log
```

---

## 📞 Soporte Técnico

### Información de Contacto

- **Email:** soporte@censo-indigena.com
- **Teléfono:** +57 XXX XXX XXXX
- **Horario:** Lunes a Viernes, 8:00 AM - 6:00 PM

### Reportar Problemas

Al reportar un problema, incluir:

1. Versión del sistema
2. Sistema operativo
3. Descripción del error
4. Pasos para reproducir
5. Captura de pantalla (si aplica)
6. Log de errores (últimas 50 líneas)

---

## 📄 Licencia y Términos de Uso

Este software es propiedad de [NOMBRE EMPRESA].  
Uso exclusivo para la organización contratante.  
Prohibida su distribución o modificación sin autorización.

---

**Versión del Documento:** 1.0  
**Fecha:** 20 de Diciembre de 2024  
**Última Actualización:** 20/12/2024

