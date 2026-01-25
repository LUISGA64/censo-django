#!/bin/bash
# Script para usar SQLite TEMPORALMENTE mientras configuras MySQL

echo "===== CAMBIANDO TEMPORALMENTE A SQLITE ====="
echo ""

cd ~/censo-django

echo "1. Creando backup de settings_pythonanywhere.py..."
cp censoProject/settings_pythonanywhere.py censoProject/settings_pythonanywhere.py.mysql_backup

echo ""
echo "2. Configurando SQLite temporal..."

python3 << 'PYTHON_SCRIPT'
import re

# Leer el archivo
with open('censoProject/settings_pythonanywhere.py', 'r') as f:
    content = f.read()

# Nueva configuración de base de datos SQLite
new_db_config = """
# Base de datos - SQLite TEMPORAL (cambiar a MySQL después)
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
    content = re.sub(pattern, new_db_config.strip(), content, flags=re.DOTALL)
    print("✅ Configuración cambiada a SQLite temporal")
else:
    print("⚠️  No se encontró DATABASES, agregando al final")
    content += "\n" + new_db_config

# Guardar
with open('censoProject/settings_pythonanywhere.py', 'w') as f:
    f.write(content)
PYTHON_SCRIPT

echo ""
echo "3. Instalando dependencias faltantes..."
source /home/luisga64/.virtualenvs/censo-env/bin/activate
pip install django-otp==1.2.2 qrcode==7.4.2 pillow

echo ""
echo "4. Verificando..."
python manage.py check

echo ""
echo "===== CONFIGURACIÓN TEMPORAL COMPLETADA ====="
echo ""
echo "✅ Ahora usando SQLite (db.censo_Web)"
echo "✅ Backup de configuración MySQL guardado en:"
echo "   censoProject/settings_pythonanywhere.py.mysql_backup"
echo ""
echo "SIGUIENTE PASO:"
echo "1. Web Tab -> Reload"
echo "2. Tu sitio debe funcionar con SQLite"
echo ""
echo "PARA VOLVER A MYSQL:"
echo "1. Configura MySQL en Database tab de PythonAnywhere"
echo "2. Edita censoProject/settings_pythonanywhere.py"
echo "3. Copia la configuración del backup .mysql_backup"
echo "4. Actualiza PASSWORD con el correcto"
echo "5. python manage.py migrate"
echo "6. Reload"
