# Script de Limpieza - Windows
# Sistema de Censo

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Limpieza de Archivos Temporales" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

$cleaned = 0

# 1. Limpiar archivos .pyc
Write-Host "🧹 Limpiando archivos .pyc..." -ForegroundColor Green
$pycFiles = Get-ChildItem -Path . -Filter "*.pyc" -Recurse -ErrorAction SilentlyContinue
if ($pycFiles) {
    $pycFiles | Remove-Item -Force
    $cleaned += $pycFiles.Count
    Write-Host "   ✅ Eliminados $($pycFiles.Count) archivos .pyc" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  No hay archivos .pyc" -ForegroundColor Gray
}

# 2. Limpiar directorios __pycache__
Write-Host ""
Write-Host "🧹 Limpiando directorios __pycache__..." -ForegroundColor Green
$pycacheDirs = Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory -ErrorAction SilentlyContinue
if ($pycacheDirs) {
    $pycacheDirs | Remove-Item -Recurse -Force
    $cleaned += $pycacheDirs.Count
    Write-Host "   ✅ Eliminados $($pycacheDirs.Count) directorios __pycache__" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  No hay directorios __pycache__" -ForegroundColor Gray
}

# 3. Limpiar archivos de log antiguos
Write-Host ""
Write-Host "🧹 Limpiando logs antiguos (>30 días)..." -ForegroundColor Green
if (Test-Path "logs") {
    $oldLogs = Get-ChildItem -Path "logs" -Filter "*.log" -ErrorAction SilentlyContinue | Where-Object {
        $_.LastWriteTime -lt (Get-Date).AddDays(-30)
    }
    if ($oldLogs) {
        $oldLogs | Remove-Item -Force
        $cleaned += $oldLogs.Count
        Write-Host "   ✅ Eliminados $($oldLogs.Count) archivos de log antiguos" -ForegroundColor Green
    } else {
        Write-Host "   ℹ️  No hay logs antiguos para eliminar" -ForegroundColor Gray
    }
} else {
    Write-Host "   ℹ️  Directorio de logs no existe" -ForegroundColor Gray
}

# 4. Limpiar archivos de sesión temporales
Write-Host ""
Write-Host "🧹 Limpiando archivos temporales de Django..." -ForegroundColor Green
if (Test-Path "db.censo_Web-journal") {
    Remove-Item "db.censo_Web-journal" -Force
    $cleaned++
    Write-Host "   ✅ Eliminado archivo de journal" -ForegroundColor Green
}

# 5. Limpiar archivos de respaldo antiguos (conservar últimos 10)
Write-Host ""
Write-Host "🧹 Limpiando respaldos antiguos (conservando últimos 10)..." -ForegroundColor Green
if (Test-Path "backups") {
    $backups = Get-ChildItem -Path "backups" -Filter "backup_*.json" -ErrorAction SilentlyContinue |
               Sort-Object LastWriteTime -Descending

    if ($backups.Count -gt 10) {
        $toDelete = $backups | Select-Object -Skip 10
        $toDelete | Remove-Item -Force
        $cleaned += $toDelete.Count
        Write-Host "   ✅ Eliminados $($toDelete.Count) respaldos antiguos" -ForegroundColor Green
        Write-Host "   ℹ️  Se conservaron los últimos 10 respaldos" -ForegroundColor Gray
    } else {
        Write-Host "   ℹ️  Hay $($backups.Count) respaldos (no se elimina nada)" -ForegroundColor Gray
    }
} else {
    Write-Host "   ℹ️  Directorio de backups no existe" -ForegroundColor Gray
}

# 6. Limpiar archivos de migración compilados
Write-Host ""
Write-Host "🧹 Limpiando migraciones compiladas..." -ForegroundColor Green
$migrationPyc = Get-ChildItem -Path "censoapp\migrations" -Filter "*.pyc" -Recurse -ErrorAction SilentlyContinue
if ($migrationPyc) {
    $migrationPyc | Remove-Item -Force
    $cleaned += $migrationPyc.Count
    Write-Host "   ✅ Eliminados $($migrationPyc.Count) archivos" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  No hay archivos compilados en migraciones" -ForegroundColor Gray
}

# 7. Limpiar archivos de staticfiles recolectados (opcional)
Write-Host ""
$cleanStatic = Read-Host "¿Desea limpiar archivos estáticos recolectados? (S/N)"
if ($cleanStatic -eq "S" -or $cleanStatic -eq "s") {
    if (Test-Path "staticfiles") {
        Remove-Item -Path "staticfiles" -Recurse -Force
        Write-Host "   ✅ Directorio staticfiles eliminado" -ForegroundColor Green
        Write-Host "   ℹ️  Ejecute 'python manage.py collectstatic' para regenerar" -ForegroundColor Yellow
    } else {
        Write-Host "   ℹ️  Directorio staticfiles no existe" -ForegroundColor Gray
    }
}

# Resumen
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  ✅ LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Total de elementos eliminados: $cleaned" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Recomendaciones:" -ForegroundColor Yellow
Write-Host "   • Ejecute esta limpieza periódicamente" -ForegroundColor White
Write-Host "   • Mantenga al menos 5-10 respaldos recientes" -ForegroundColor White
Write-Host "   • Revise logs regularmente" -ForegroundColor White
Write-Host ""

