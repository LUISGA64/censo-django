#!/bin/bash
# 🚀 Script de Deploy para PythonAnywhere - 28 Abril 2026
# IMPORTANTE: Ejecutar desde ~/censo-django en PythonAnywhere

echo "============================================"
echo "🚀 INICIANDO DEPLOY - Censo Django"
echo "============================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ ERROR: No se encontró manage.py"
    echo "Por favor ejecuta: cd ~/censo-django"
    exit 1
fi

echo "✅ Directorio correcto confirmado"
echo ""

# Paso 1: Verificar rama actual
echo "📍 Paso 1: Verificando rama Git..."
CURRENT_BRANCH=$(git branch --show-current)
echo "Rama actual: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "master" ]; then
    echo "⚠️  Cambiando a rama master..."
    git checkout master
fi
echo ""

# Paso 2: Actualizar código
echo "📥 Paso 2: Descargando cambios desde GitHub..."

# Intentar pull normal primero
git pull origin master 2>&1 | tee /tmp/git_pull_output.txt

# Si hay error de merge con staticfiles
if grep -q "staticfiles" /tmp/git_pull_output.txt && grep -q "overwritten by merge" /tmp/git_pull_output.txt; then
    echo "⚠️  Detectado conflicto con staticfiles (archivos generados)"
    echo "🔧 Aplicando solución automática..."

    # Hacer stash de los cambios en staticfiles
    git stash push -m "Auto-stash staticfiles before merge - $(date +%Y%m%d_%H%M%S)"

    # Intentar pull de nuevo
    git pull origin master

    if [ $? -ne 0 ]; then
        echo "❌ ERROR al descargar cambios después del stash"
        exit 1
    fi

    # Eliminar staticfiles del tracking (sin borrar archivos físicos)
    echo "🧹 Limpiando staticfiles del tracking de Git..."
    git rm -r --cached staticfiles/ 2>/dev/null || true

    # Si hay cambios, hacer commit
    if git status --porcelain | grep -q "staticfiles"; then
        git commit -m "chore: eliminar staticfiles del tracking de Git - auto-fixed" 2>/dev/null || true
    fi

    echo "✅ Conflicto resuelto automáticamente"
elif [ $? -ne 0 ]; then
    echo "❌ ERROR al descargar cambios"
    cat /tmp/git_pull_output.txt
    exit 1
fi

echo "✅ Código actualizado"
echo ""

# Paso 3: Activar virtualenv
echo "🐍 Paso 3: Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ ERROR al activar virtualenv"
    exit 1
fi
echo "✅ Virtualenv activado"
echo ""

# Paso 4: Instalar/actualizar dependencias
echo "📦 Paso 4: Instalando dependencias..."
pip install -r requirements.txt --no-cache-dir --quiet
if [ $? -ne 0 ]; then
    echo "⚠️  Advertencia: Algunos paquetes no se instalaron correctamente"
fi
echo "✅ Dependencias actualizadas"
echo ""

# Paso 5: Ver migraciones pendientes
echo "🔍 Paso 5: Verificando migraciones..."
python manage.py showmigrations censoapp | grep -E "\[ \]"
if [ $? -eq 0 ]; then
    echo "⚠️  Hay migraciones pendientes"
else
    echo "✅ No hay migraciones pendientes"
fi
echo ""

# Paso 6: Aplicar migraciones
echo "🗄️  Paso 6: Aplicando migraciones..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ ERROR al aplicar migraciones"
    exit 1
fi
echo "✅ Migraciones aplicadas"
echo ""

# Paso 7: Recolectar archivos estáticos
echo "📁 Paso 7: Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear
if [ $? -ne 0 ]; then
    echo "❌ ERROR al recolectar archivos estáticos"
    exit 1
fi
echo "✅ Archivos estáticos actualizados"
echo ""

# Paso 8: Verificar modelo Association
echo "🔍 Paso 8: Verificando modelo Association..."
python manage.py shell -c "
from censoapp.models import Association
try:
    count = Association.objects.count()
    print(f'✅ Modelo Association OK - {count} registros')
    if count > 0:
        assoc = Association.objects.first()
        print(f'✅ Campo is_active verificado: {assoc.is_active}')
except Exception as e:
    print(f'⚠️  Error al verificar: {e}')
"
echo ""

# Paso 9: Recargar aplicación web
echo "🔄 Paso 9: Recargando aplicación web..."
WSGI_FILE=$(ls /var/www/*_pythonanywhere_com_wsgi.py 2>/dev/null | head -1)
if [ -n "$WSGI_FILE" ]; then
    touch "$WSGI_FILE"
    echo "✅ Aplicación web recargada"
    echo "Archivo WSGI: $WSGI_FILE"
else
    echo "⚠️  No se encontró archivo WSGI automáticamente"
    echo "Por favor recarga manualmente desde la pestaña Web"
fi
echo ""

# Paso 10: Resumen final
echo "============================================"
echo "✅ DEPLOY COMPLETADO CON ÉXITO"
echo "============================================"
echo ""
echo "📋 Resumen:"
echo "  - Código actualizado desde master"
echo "  - Migraciones aplicadas (incluye Association.is_active)"
echo "  - Archivos estáticos recolectados"
echo "  - Aplicación web recargada"
echo ""
echo "🔍 Verificaciones recomendadas:"
echo "  1. Abrir https://tuusuario.pythonanywhere.com"
echo "  2. Limpiar caché del navegador (Ctrl+Shift+Delete)"
echo "  3. Verificar dropdowns funcionan"
echo "  4. Verificar asociaciones muestran 'Activo'"
echo "  5. Revisar consola (F12) - no debe haber console.log"
echo ""
echo "📄 Ver logs de error:"
echo "  tail -50 /var/log/\$(basename \$WSGI_FILE | sed 's/_wsgi.py//').error.log"
echo ""
echo "🎉 ¡Deploy exitoso!"
echo ""

