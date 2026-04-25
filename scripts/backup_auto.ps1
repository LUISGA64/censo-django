# Script de Backup Automático para Windows
# Ejecutar diariamente con Programador de Tareas de Windows

# Configuración
$PROYECTO_DIR = "C:\Users\LENOVO\PycharmProjects\censo-django"
$VENV_PYTHON = "$PROYECTO_DIR\venv\Scripts\python.exe"
$LOG_FILE = "$PROYECTO_DIR\logs\backup.log"

# Crear directorio de logs si no existe
if (!(Test-Path "$PROYECTO_DIR\logs")) {
    New-Item -ItemType Directory -Path "$PROYECTO_DIR\logs"
}

# Timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $LOG_FILE -Value "=== Backup iniciado: $timestamp ==="

# Cambiar al directorio del proyecto
Set-Location $PROYECTO_DIR

try {
    # Ejecutar backup con compresión
    Write-Host "Ejecutando backup de base de datos..."
    & $VENV_PYTHON manage.py backup_db --compress --keep-days 30 2>&1 | Tee-Object -FilePath $LOG_FILE -Append

    if ($LASTEXITCODE -eq 0) {
        Add-Content -Path $LOG_FILE -Value "✓ Backup completado exitosamente"
        Write-Host "✓ Backup completado exitosamente" -ForegroundColor Green
    } else {
        Add-Content -Path $LOG_FILE -Value "✗ Error en backup (Exit code: $LASTEXITCODE)"
        Write-Host "✗ Error en backup" -ForegroundColor Red
    }
} catch {
    $errorMsg = $_.Exception.Message
    Add-Content -Path $LOG_FILE -Value "✗ Excepción: $errorMsg"
    Write-Host "✗ Error: $errorMsg" -ForegroundColor Red
}

# Timestamp final
$timestamp_end = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $LOG_FILE -Value "=== Backup finalizado: $timestamp_end ===`n"

# Mantener solo últimos 90 días de logs
$cutoffDate = (Get-Date).AddDays(-90)
Get-ChildItem -Path "$PROYECTO_DIR\logs\backup_*.log" |
    Where-Object { $_.LastWriteTime -lt $cutoffDate } |
    Remove-Item -Force
