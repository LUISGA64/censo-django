# Script de Verificación de Instalación - Windows
# Sistema de Censo

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Verificación de Instalación" -ForegroundColor Cyan
Write-Host "  Sistema de Censo" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

$allOk = $true

# 1. Verificar Python
Write-Host "1️⃣  Verificando Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python no encontrado" -ForegroundColor Red
    $allOk = $false
}

# 2. Verificar entorno virtual
Write-Host ""
Write-Host "2️⃣  Verificando entorno virtual..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "   ✅ Entorno virtual existe" -ForegroundColor Green
} else {
    Write-Host "   ❌ Entorno virtual no encontrado" -ForegroundColor Red
    $allOk = $false
}

# 3. Activar entorno y verificar Django
Write-Host ""
Write-Host "3️⃣  Verificando Django..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1
try {
    $djangoVersion = python -c "import django; print(django.get_version())" 2>&1
    Write-Host "   ✅ Django $djangoVersion instalado" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Django no instalado" -ForegroundColor Red
    $allOk = $false
}

# 4. Verificar base de datos
Write-Host ""
Write-Host "4️⃣  Verificando base de datos..." -ForegroundColor Cyan
if (Test-Path "db.censo_Web") {
    $dbSize = (Get-Item "db.censo_Web").Length / 1KB
    Write-Host "   ✅ Base de datos existe ($([math]::Round($dbSize, 2)) KB)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Base de datos no encontrada" -ForegroundColor Red
    $allOk = $false
}

# 5. Verificar directorios
Write-Host ""
Write-Host "5️⃣  Verificando estructura de directorios..." -ForegroundColor Cyan
$directories = @("media", "static", "logs", "backups", "templates")
foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "   ✅ $dir" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  $dir no existe" -ForegroundColor Yellow
    }
}

# 6. Verificar migraciones
Write-Host ""
Write-Host "6️⃣  Verificando migraciones..." -ForegroundColor Cyan
$migrations = python manage.py showmigrations --plan 2>&1
if ($migrations -match "FAILED" -or $LASTEXITCODE -ne 0) {
    Write-Host "   ⚠️  Hay migraciones pendientes" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Migraciones aplicadas" -ForegroundColor Green
}

# 7. Verificar superusuario
Write-Host ""
Write-Host "7️⃣  Verificando superusuario..." -ForegroundColor Cyan
$hasSuperuser = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>&1
if ($hasSuperuser -match "True") {
    Write-Host "   ✅ Superusuario existe" -ForegroundColor Green
} else {
    Write-Host "   ❌ No hay superusuario creado" -ForegroundColor Red
    $allOk = $false
}

# 8. Verificar dependencias críticas
Write-Host ""
Write-Host "8️⃣  Verificando dependencias críticas..." -ForegroundColor Cyan
$packages = @("django", "pillow", "reportlab", "qrcode", "openpyxl", "django-crispy-forms")
foreach ($package in $packages) {
    $installed = pip show $package 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ $package" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $package no instalado" -ForegroundColor Red
        $allOk = $false
    }
}

# 9. Probar servidor (sin iniciarlo)
Write-Host ""
Write-Host "9️⃣  Verificando configuración del servidor..." -ForegroundColor Cyan
$checkResult = python manage.py check --deploy 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Configuración correcta" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Advertencias de configuración (revisar para producción)" -ForegroundColor Yellow
}

# Resumen final
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
if ($allOk) {
    Write-Host "  ✅ SISTEMA VERIFICADO" -ForegroundColor Green
    Write-Host "  Todos los componentes están correctos" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  VERIFICACIÓN INCOMPLETA" -ForegroundColor Yellow
    Write-Host "  Revise los errores anteriores" -ForegroundColor Yellow
}
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

if ($allOk) {
    Write-Host "✅ El sistema está listo para usarse" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para iniciar el servidor:" -ForegroundColor Cyan
    Write-Host "  .\scripts\start_server.ps1" -ForegroundColor White
} else {
    Write-Host "⚠️  Corrija los errores antes de usar el sistema" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para reinstalar, ejecute:" -ForegroundColor Cyan
    Write-Host "  .\scripts\install_windows.ps1" -ForegroundColor White
}

Write-Host ""

