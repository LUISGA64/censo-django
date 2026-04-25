#!/bin/bash
# Script de Deployment Automático para PythonAnywhere
# Ejecutar: bash deploy_pythonanywhere.sh

echo "======================================"
echo "CENSO WEB - DEPLOYMENT PYTHONANYWHERE"
echo "Versión 2.0 - Fase 1 Completa"
echo "======================================"
echo ""

# Variables (CAMBIAR ESTOS VALORES)
PROJECT_DIR="/home/tuusuario/censo-django"
VENV_NAME="censo-env"
PYTHON_VERSION="3.10"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "ℹ️  $1"
}

# Verificar que estamos en PythonAnywhere
if [ ! -d "/home" ]; then
    print_error "Este script debe ejecutarse en PythonAnywhere"
    exit 1
fi

# PASO 1: Actualizar código desde GitHub
echo ""
echo "PASO 1: Actualizando código desde GitHub..."
cd $PROJECT_DIR || exit 1

git fetch origin
print_info "Ramas disponibles:"
git branch -r

echo ""
read -p "¿Qué rama deseas deployar? (development/main): " BRANCH
BRANCH=${BRANCH:-development}

git checkout $BRANCH
git pull origin $BRANCH

if [ $? -eq 0 ]; then
    print_success "Código actualizado desde rama: $BRANCH"
else
    print_error "Error al actualizar código"
    exit 1
fi

# PASO 2: Activar entorno virtual
echo ""
echo "PASO 2: Activando entorno virtual..."
source ~/.virtualenvs/$VENV_NAME/bin/activate

if [ $? -eq 0 ]; then
    print_success "Entorno virtual activado: $VENV_NAME"
else
    print_error "Error al activar entorno virtual"
    exit 1
fi

# PASO 3: Actualizar dependencias
echo ""
echo "PASO 3: Actualizando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "Dependencias actualizadas"
else
    print_error "Error al instalar dependencias"
    exit 1
fi

# PASO 4: Verificar configuración
echo ""
echo "PASO 4: Verificando configuración..."
python manage.py check --deploy

if [ $? -eq 0 ]; then
    print_success "Configuración verificada"
else
    print_warning "Hay warnings en la configuración (pueden ser normales)"
fi

# PASO 5: Ejecutar migraciones
echo ""
echo "PASO 5: Ejecutando migraciones..."
python manage.py migrate

if [ $? -eq 0 ]; then
    print_success "Migraciones ejecutadas correctamente"
else
    print_error "Error en migraciones"
    exit 1
fi

# PASO 6: Recopilar archivos estáticos
echo ""
echo "PASO 6: Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

if [ $? -eq 0 ]; then
    print_success "Archivos estáticos recopilados"
else
    print_error "Error al recopilar archivos estáticos"
    exit 1
fi

# PASO 7: Crear directorios necesarios
echo ""
echo "PASO 7: Verificando directorios..."
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/backups
mkdir -p $PROJECT_DIR/media

print_success "Directorios verificados"

# PASO 8: Verificar permisos
echo ""
echo "PASO 8: Configurando permisos..."
chmod 755 $PROJECT_DIR/backups
chmod 755 $PROJECT_DIR/media

print_success "Permisos configurados"

# PASO 9: Recargar web app
echo ""
echo "PASO 9: Recargando aplicación web..."
touch /var/www/$(whoami)_pythonanywhere_com_wsgi.py

if [ $? -eq 0 ]; then
    print_success "Aplicación web recargada"
else
    print_warning "Recarga manual: ve a Web y click en 'Reload'"
fi

# PASO 10: Resumen
echo ""
echo "======================================"
echo "DEPLOYMENT COMPLETADO"
echo "======================================"
echo ""
print_success "Código actualizado desde: $BRANCH"
print_success "Dependencias instaladas"
print_success "Migraciones ejecutadas"
print_success "Archivos estáticos recopilados"
print_success "Aplicación recargada"
echo ""
print_info "Verifica el sitio en: https://$(whoami).pythonanywhere.com/"
echo ""
print_warning "IMPORTANTE: Verifica los logs si hay errores:"
echo "  tail -f /var/log/$(whoami).pythonanywhere.com.error.log"
echo ""
print_info "Para ver logs de Django:"
echo "  tail -f $PROJECT_DIR/logs/django.log"
echo ""

# PASO 11: Pruebas automáticas
echo "PASO 11: Ejecutando pruebas básicas..."
echo ""

# Test 1: Django check
python manage.py check > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Django check: OK"
else
    print_error "Django check: FAILED"
fi

# Test 2: Verificar archivos estáticos
if [ -d "$PROJECT_DIR/staticfiles/admin" ]; then
    print_success "Archivos estáticos de admin: OK"
else
    print_error "Archivos estáticos de admin: MISSING"
fi

# Test 3: Verificar base de datos
python manage.py showmigrations | grep "\[ \]" > /dev/null
if [ $? -ne 0 ]; then
    print_success "Migraciones aplicadas: OK"
else
    print_warning "Hay migraciones pendientes"
fi

echo ""
echo "======================================"
print_success "DEPLOYMENT FINALIZADO"
echo "======================================"
