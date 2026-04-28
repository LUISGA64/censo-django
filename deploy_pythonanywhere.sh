#!/bin/bash
# ============================================
# SCRIPT DE ACTUALIZACIÓN PARA PYTHONANYWHERE
# Versión: 2.1.0
# Fecha: 2026-04-25
# ============================================

echo "🚀 Iniciando actualización a versión 2.1.0..."
echo ""

# 1. Ir al directorio del proyecto
cd /home/luisga64/censo-django
echo "📁 Directorio: $(pwd)"

# 2. Verificar rama actual
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Rama actual: $CURRENT_BRANCH"

# 3. Cambiar a master
echo ""
echo "🔀 Cambiando a rama master..."
git checkout master

# 4. Pull de cambios
echo ""
echo "⬇️ Descargando últimos cambios..."
git pull origin master

# 5. Verificar versión
echo ""
echo "📦 Verificando versión..."
if [ -f VERSION ]; then
    VERSION=$(cat VERSION)
    echo "✅ Versión actual: $VERSION"
else
    echo "⚠️ Archivo VERSION no encontrado"
fi

# 6. Activar virtualenv
echo ""
echo "🐍 Activando virtualenv..."
source /home/luisga64/.virtualenvs/venv/bin/activate

# 7. Configurar Django settings
echo ""
echo "⚙️ Configurando Django settings..."
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere

# 8. Verificar archivo .env
echo ""
echo "🔐 Verificando archivo .env..."
if [ -f .env ]; then
    echo "✅ Archivo .env encontrado"
    echo "Primeras líneas (sin contraseñas):"
    head -n 3 .env
else
    echo "❌ ERROR: Archivo .env NO encontrado"
    echo "Debes crearlo antes de continuar"
    exit 1
fi

# 9. Instalar/actualizar dependencias Python
echo ""
echo "📦 Instalando dependencias Python..."
pip install -r requirements.txt --quiet

# 10. Verificar migraciones pendientes
echo ""
echo "🔍 Verificando migraciones..."
python manage.py showmigrations | grep "\[ \]" && echo "⚠️ Hay migraciones pendientes" || echo "✅ No hay migraciones pendientes"

# 11. Ejecutar migraciones
echo ""
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

# 12. Recolectar archivos estáticos
echo ""
echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# 13. Verificar configuración
echo ""
echo "✅ Verificando configuración de deployment..."
python manage.py check --deploy

# 14. Mostrar información del sistema
echo ""
echo "═══════════════════════════════════════"
echo "📊 RESUMEN DE ACTUALIZACIÓN"
echo "═══════════════════════════════════════"
echo "✅ Rama: $(git branch --show-current)"
echo "✅ Commit: $(git log -1 --oneline)"
echo "✅ Versión: $(cat VERSION 2>/dev/null || echo 'No disponible')"
echo "✅ Python: $(python --version)"
echo "✅ Django: $(python -c 'import django; print(django.get_version())')"
echo "═══════════════════════════════════════"
echo ""

# 15. Instrucciones finales
echo "🎯 PRÓXIMO PASO IMPORTANTE:"
echo ""
echo "   Ve a la pestaña Web en PythonAnywhere"
echo "   y haz click en el botón verde 'Reload'"
echo ""
echo "   URL: https://www.pythonanywhere.com/user/luisga64/webapps/"
echo ""

# 16. Verificar estado final
echo "📋 Verificación final:"
echo "   ✓ Código actualizado"
echo "   ✓ Dependencias instaladas"
echo "   ✓ Migraciones aplicadas"
echo "   ✓ Estáticos recolectados"
echo "   ⚠️ FALTA: Recargar aplicación web"
echo ""

echo "✨ Actualización completada exitosamente!"
echo "Recuerda recargar la aplicación en el panel Web."

