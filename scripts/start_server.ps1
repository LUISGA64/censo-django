# Script para Iniciar el Servidor - Windows
# Sistema de Censo

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Sistema de Censo - Servidor" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
Write-Host "🔄 Activando entorno virtual..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Verificar que el entorno esté activado
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "❌ Error al activar entorno virtual" -ForegroundColor Red
    exit 1
}

# Verificar base de datos
Write-Host ""
Write-Host "🔍 Verificando base de datos..." -ForegroundColor Green
if (Test-Path "db.censo_Web") {
    Write-Host "✅ Base de datos encontrada" -ForegroundColor Green
} else {
    Write-Host "⚠️  Base de datos no encontrada. Ejecutando migraciones..." -ForegroundColor Yellow
    python manage.py migrate --noinput
}

# Iniciar servidor
Write-Host ""
Write-Host "🚀 Iniciando servidor..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 El servidor estará disponible en:" -ForegroundColor Cyan
Write-Host "   • http://localhost:8000" -ForegroundColor White
Write-Host "   • http://127.0.0.1:8000" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Presione Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

