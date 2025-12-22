#!/bin/bash

# ============================================================================
# Script de Actualización - Censo Indígena
# ============================================================================
# Ejecutar este script cada vez que se actualice el código
# ============================================================================

set -e

APP_DIR="/var/www/censo-django"
VENV_DIR="$APP_DIR/venv"

cd $APP_DIR

echo "🔄 Actualizando aplicación..."

# Activar entorno virtual
source $VENV_DIR/bin/activate

# Pull del código
echo "📥 Descargando cambios del repositorio..."
git pull origin main

# Instalar/actualizar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "🗄️  Ejecutando migraciones..."
python manage.py migrate

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Reiniciar Gunicorn
echo "🔄 Reiniciando Gunicorn..."
systemctl restart gunicorn

# Verificar estado
echo "✅ Verificando servicios..."
systemctl status gunicorn --no-pager

echo ""
echo "✓ Actualización completada exitosamente"
echo ""

