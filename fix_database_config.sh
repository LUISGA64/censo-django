#!/bin/bash
# Script para cambiar configuración de MySQL a SQLite en PythonAnywhere

echo "===== CORRIGIENDO CONFIGURACIÓN DE BASE DE DATOS ====="
echo ""

cd ~/censo-django

echo "1. Verificando que existe db.censo_Web..."
if [ ! -f "db.censo_Web" ]; then
    echo "❌ ERROR: Base de datos SQLite no encontrada"
    echo "Por favor crea un backup o verifica el archivo"
    exit 1
fi

echo "✅ Base de datos SQLite encontrada"
echo ""

echo "2. Creando backup de settings_pythonanywhere.py..."
if [ -f "censoProject/settings_pythonanywhere.py" ]; then
    cp censoProject/settings_pythonanywhere.py censoProject/settings_pythonanywhere.py.backup
    echo "✅ Backup creado: settings_pythonanywhere.py.backup"
else
    echo "ℹ️  settings_pythonanywhere.py no existe, usando settings.py"
    cp censoProject/settings.py censoProject/settings_pythonanywhere.py
fi

echo ""
echo "3. Actualizando configuración de base de datos a SQLite..."

# Crear configuración correcta de base de datos
cat > /tmp/db_config.txt << 'EOF'

# Base de datos - SQLite para PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.censo_Web',
        'ATOMIC_REQUESTS': True,
    }
}
EOF

# Buscar y reemplazar la configuración de DATABASES
python3 << 'PYTHON_SCRIPT'
import re

# Leer el archivo
with open('censoProject/settings_pythonanywhere.py', 'r') as f:
    content = f.read()

# Nueva configuración de base de datos
new_db_config = """
# Base de datos - SQLite para PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.censo_Web',
        'ATOMIC_REQUESTS': True,
    }
}
"""

# Buscar el bloque DATABASES y reemplazarlo
pattern = r'DATABASES\s*=\s*\{[^}]*\{[^}]*\}[^}]*\}'
if re.search(pattern, content):
    content = re.sub(pattern, new_db_config.strip(), content)
    print("✅ Configuración de DATABASES actualizada")
else:
    print("⚠️  No se encontró configuración DATABASES, agregando al final")
    content += "\n" + new_db_config

# Guardar el archivo
with open('censoProject/settings_pythonanywhere.py', 'w') as f:
    f.write(content)

print("✅ Archivo settings_pythonanywhere.py actualizado")
PYTHON_SCRIPT

echo ""
echo "4. Verificando nueva configuración..."
grep -A 6 "DATABASES = {" censoProject/settings_pythonanywhere.py

echo ""
echo "5. Instalando dependencias faltantes..."
source /home/luisga64/.virtualenvs/censo-env/bin/activate
pip install django-otp==1.2.2 qrcode==7.4.2 pillow

echo ""
echo "6. Verificando Django..."
python manage.py check

echo ""
echo "===== CORRECCIÓN COMPLETADA ====="
echo ""
echo "✅ Base de datos cambiada de MySQL a SQLite"
echo "✅ Configuración actualizada en settings_pythonanywhere.py"
echo ""
echo "SIGUIENTE PASO:"
echo "1. Ve a Web Tab en PythonAnywhere"
echo "2. Click en 'Reload'"
echo "3. Prueba tu sitio: https://luisga64.pythonanywhere.com/"
echo ""
echo "La aplicación debe funcionar correctamente ahora."
