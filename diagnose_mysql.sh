#!/bin/bash
# Script para diagnosticar problema de conexión MySQL en PythonAnywhere

echo "===== DIAGNÓSTICO DE CONEXIÓN MYSQL ====="
echo ""

cd ~/censo-django
source /home/luisga64/.virtualenvs/censo-env/bin/activate

echo "1. Verificando configuración MySQL en settings..."
echo ""
grep -A 15 "DATABASES = {" censoProject/settings_pythonanywhere.py

echo ""
echo "2. Verificando que mysqlclient esté instalado..."
pip list | grep -i mysql

echo ""
echo "3. Intentando conectar a MySQL..."
python3 << 'PYTHON_SCRIPT'
import os
import sys

# Configurar Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'
sys.path.insert(0, '/home/luisga64/censo-django')

try:
    import django
    django.setup()

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ Conexión MySQL exitosa")
    print(f"✅ Versión MySQL: {version[0]}")

except Exception as e:
    print(f"❌ Error de conexión MySQL:")
    print(f"   {str(e)}")
    print("")
    print("Posibles causas:")
    print("1. Usuario o contraseña incorrectos")
    print("2. Base de datos no existe")
    print("3. mysqlclient no instalado")
    print("4. Permisos de usuario MySQL")
PYTHON_SCRIPT

echo ""
echo "4. Verificando bases de datos MySQL disponibles..."
echo "   (Ir a PythonAnywhere -> Databases para ver tus bases de datos)"

echo ""
echo "===== DIAGNÓSTICO COMPLETADO ====="
echo ""
echo "Si ves error de conexión arriba, verifica:"
echo "1. Web Tab -> Databases -> Usuario y contraseña MySQL"
echo "2. Nombre de la base de datos (formato: usuario\$nombredb)"
echo "3. Host de MySQL (probablemente: luisga64.mysql.pythonanywhere-services.com)"
