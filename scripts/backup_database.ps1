# Script de Respaldo de Base de Datos - Windows
# Sistema de Censo

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Respaldo de Base de Datos" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
& .\venv\Scripts\Activate.ps1

# Crear directorio de respaldos si no existe
if (-not (Test-Path "backups")) {
    New-Item -ItemType Directory -Path "backups" -Force | Out-Null
}

# Generar nombre de archivo con fecha y hora
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "backups\backup_$timestamp.json"

Write-Host "📦 Generando respaldo..." -ForegroundColor Green
Write-Host "   Archivo: $backupFile" -ForegroundColor Cyan
Write-Host ""

# Ejecutar comando de respaldo
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > $backupFile

if ($LASTEXITCODE -eq 0) {
    $fileSize = (Get-Item $backupFile).Length / 1KB
    Write-Host "✅ Respaldo creado exitosamente" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($fileSize, 2)) KB" -ForegroundColor Gray
    Write-Host "   Ubicación: $backupFile" -ForegroundColor Gray
    Write-Host ""

    # Listar respaldos anteriores
    Write-Host "📋 Respaldos existentes:" -ForegroundColor Cyan
    Get-ChildItem backups\*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 5 | ForEach-Object {
        $size = $_.Length / 1KB
        Write-Host "   • $($_.Name) - $([math]::Round($size, 2)) KB - $($_.LastWriteTime)" -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "💡 Para restaurar un respaldo, ejecute:" -ForegroundColor Yellow
    Write-Host "   python manage.py loaddata backups\backup_NOMBRE.json" -ForegroundColor White
} else {
    Write-Host "❌ Error al crear el respaldo" -ForegroundColor Red
    exit 1
}

