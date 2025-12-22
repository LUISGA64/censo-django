# Script para recrear base de datos

Write-Host "=== RECREANDO BASE DE DATOS ===" -ForegroundColor Green
Write-Host ""

# Paso 1: Renombrar BD actual
Write-Host "Paso 1: Renombrando base de datos actual..." -ForegroundColor Yellow
if (Test-Path ".\db.censo_Web") {
    if (Test-Path ".\db.censo_Web.backup") {
        Remove-Item ".\db.censo_Web.backup" -Force
    }
    Rename-Item ".\db.censo_Web" "db.censo_Web.backup" -Force
    Write-Host "✓ Base de datos renombrada a db.censo_Web.backup" -ForegroundColor Green
} else {
    Write-Host "✓ No hay base de datos anterior" -ForegroundColor Green
}

Write-Host ""

# Paso 2: Crear nueva BD
Write-Host "Paso 2: Creando nueva base de datos..." -ForegroundColor Yellow
python manage.py migrate
Write-Host "✓ Base de datos creada" -ForegroundColor Green

Write-Host ""

# Paso 3: Cargar tipos de documentos
Write-Host "Paso 3: Cargando tipos de documentos..." -ForegroundColor Yellow
python manage.py loaddata document_types
Write-Host "✓ Tipos de documentos cargados" -ForegroundColor Green

Write-Host ""

# Paso 4: Cargar datos catalogos
Write-Host "Paso 4: Cargando datos de catálogos..." -ForegroundColor Yellow
python manage.py loaddata system_parameters
Write-Host "✓ Parámetros del sistema cargados" -ForegroundColor Green

Write-Host ""

# Paso 5: Crear superusuario
Write-Host "Paso 5: Ahora necesitas crear un superusuario" -ForegroundColor Yellow
Write-Host "Ejecuta: python manage.py createsuperuser" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== PROCESO COMPLETADO ===" -ForegroundColor Green
Write-Host ""
Write-Host "BACKUPS CREADOS:" -ForegroundColor Yellow
Write-Host "  - backup_users.json"
Write-Host "  - backup_userprofiles.json"
Write-Host "  - backup_organizations.json"
Write-Host "  - backup_sidewalks.json"
Write-Host "  - backup_familycards.json"
Write-Host "  - backup_persons.json"
Write-Host "  - db.censo_Web.backup"
Write-Host ""
Write-Host "Para restaurar datos, ejecuta:" -ForegroundColor Cyan
Write-Host "  python manage.py loaddata backup_users.json"
Write-Host "  python manage.py loaddata backup_organizations.json"
Write-Host "  python manage.py loaddata backup_sidewalks.json"
Write-Host "  python manage.py loaddata backup_familycards.json"
Write-Host "  python manage.py loaddata backup_persons.json"
Write-Host "  python manage.py loaddata backup_userprofiles.json"
Write-Host ""

