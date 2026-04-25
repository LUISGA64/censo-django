# Script de Instalación Automática para Windows
# Sistema de Censo - Instalación para Cliente

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Sistema de Censo - Instalación" -ForegroundColor Cyan
Write-Host "  Versión 1.0" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si se ejecuta como Administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  ADVERTENCIA: Se recomienda ejecutar como Administrador" -ForegroundColor Yellow
    Write-Host ""
}

# 1. Verificar Python
Write-Host "1️⃣  Verificando Python..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Python instalado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python no encontrado. Por favor, instale Python 3.8 o superior" -ForegroundColor Red
    Write-Host "   Descargue desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 2. Verificar pip
Write-Host ""
Write-Host "2️⃣  Verificando pip..." -ForegroundColor Green
try {
    $pipVersion = pip --version 2>&1
    Write-Host "   ✅ pip instalado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ pip no encontrado. Reinstale Python con pip incluido" -ForegroundColor Red
    exit 1
}

# 3. Crear entorno virtual
Write-Host ""
Write-Host "3️⃣  Creando entorno virtual..." -ForegroundColor Green
if (Test-Path "venv") {
    Write-Host "   ⚠️  El entorno virtual ya existe" -ForegroundColor Yellow
    $response = Read-Host "   ¿Desea recrearlo? (S/N)"
    if ($response -eq "S" -or $response -eq "s") {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "   ✅ Entorno virtual recreado" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "   ✅ Entorno virtual creado" -ForegroundColor Green
}

# 4. Activar entorno virtual e instalar dependencias
Write-Host ""
Write-Host "4️⃣  Instalando dependencias..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host "   📦 Actualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Instalar dependencias
Write-Host "   📦 Instalando paquetes de Python (esto puede tomar varios minutos)..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

# 5. Crear directorios necesarios
Write-Host ""
Write-Host "5️⃣  Creando estructura de directorios..." -ForegroundColor Green
$directories = @("media", "media\Association", "media\Images", "static", "logs", "backups")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✅ Creado: $dir" -ForegroundColor Green
    } else {
        Write-Host "   ✔️  Existe: $dir" -ForegroundColor Gray
    }
}

# 6. Configurar archivo .env
Write-Host ""
Write-Host "6️⃣  Configurando variables de entorno..." -ForegroundColor Green
if (-not (Test-Path ".env")) {
    $envContent = @"
# Configuración del Sistema de Censo
DEBUG=True
SECRET_KEY=django-insecure-cambiar-en-produccion-$(Get-Random)
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (SQLite por defecto)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.censo_Web

# Configuración de medios
MEDIA_URL=/media/
MEDIA_ROOT=media

# Configuración de estáticos
STATIC_URL=/static/
STATIC_ROOT=staticfiles
"@
    $envContent | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "   ✅ Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Archivo .env ya existe, no se modificó" -ForegroundColor Yellow
}

# 7. Ejecutar migraciones
Write-Host ""
Write-Host "7️⃣  Configurando base de datos..." -ForegroundColor Green
Write-Host "   📊 Ejecutando migraciones..." -ForegroundColor Cyan
python manage.py migrate --noinput

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Base de datos configurada correctamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error al configurar la base de datos" -ForegroundColor Red
    exit 1
}

# 8. Cargar datos iniciales
Write-Host ""
Write-Host "8️⃣  Cargando datos iniciales..." -ForegroundColor Green
$fixtures = Get-ChildItem -Path "censoapp\fixtures" -Filter "*.json" -ErrorAction SilentlyContinue
if ($fixtures) {
    foreach ($fixture in $fixtures) {
        Write-Host "   📄 Cargando: $($fixture.Name)" -ForegroundColor Cyan
        python manage.py loaddata "censoapp\fixtures\$($fixture.Name)" --verbosity 0
    }
    Write-Host "   ✅ Datos iniciales cargados" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  No se encontraron fixtures para cargar" -ForegroundColor Yellow
}

# 9. Recolectar archivos estáticos
Write-Host ""
Write-Host "9️⃣  Recolectando archivos estáticos..." -ForegroundColor Green
python manage.py collectstatic --noinput --clear --verbosity 0

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Archivos estáticos recolectados" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Advertencia al recolectar estáticos (puede ser normal)" -ForegroundColor Yellow
}

# 10. Crear superusuario
Write-Host ""
Write-Host "🔟 Creando usuario administrador..." -ForegroundColor Green
Write-Host "   Por favor, ingrese los datos del administrador:" -ForegroundColor Cyan
Write-Host ""

# Verificar si ya existe un superusuario
$existingSuperuser = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>&1

if ($existingSuperuser -match "True") {
    Write-Host "   ⚠️  Ya existe un superusuario en el sistema" -ForegroundColor Yellow
    $createNew = Read-Host "   ¿Desea crear otro superusuario? (S/N)"
    if ($createNew -eq "S" -or $createNew -eq "s") {
        python manage.py createsuperuser
    }
} else {
    python manage.py createsuperuser
}

# 11. Resumen de instalación
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  ✅ INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Resumen de la instalación:" -ForegroundColor White
Write-Host "   • Entorno virtual: CREADO" -ForegroundColor Gray
Write-Host "   • Dependencias: INSTALADAS" -ForegroundColor Gray
Write-Host "   • Base de datos: CONFIGURADA" -ForegroundColor Gray
Write-Host "   • Datos iniciales: CARGADOS" -ForegroundColor Gray
Write-Host "   • Usuario admin: CREADO" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Para iniciar el servidor:" -ForegroundColor Yellow
Write-Host "   1. Ejecute: .\scripts\start_server.ps1" -ForegroundColor White
Write-Host "   2. Abra su navegador en: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentación disponible en: .\docs\" -ForegroundColor Cyan
Write-Host ""
Write-Host "¡Gracias por usar el Sistema de Censo!" -ForegroundColor Green
Write-Host ""

# Preguntar si desea iniciar el servidor
$startServer = Read-Host "¿Desea iniciar el servidor ahora? (S/N)"
if ($startServer -eq "S" -or $startServer -eq "s") {
    Write-Host ""
    Write-Host "🚀 Iniciando servidor..." -ForegroundColor Green
    Write-Host "   Presione Ctrl+C para detener el servidor" -ForegroundColor Yellow
    Write-Host ""
    python manage.py runserver
}

