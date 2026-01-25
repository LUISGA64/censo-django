#!/bin/bash
# Script para configurar correctamente MySQL en PythonAnywhere

echo "===== CONFIGURANDO MYSQL EN PYTHONANYWHERE ====="
echo ""

cd ~/censo-django
source /home/luisga64/.virtualenvs/censo-env/bin/activate

echo "1. Instalando mysqlclient..."
pip install mysqlclient

echo ""
echo "2. Verificando instalación..."
pip show mysqlclient

echo ""
echo "3. Creando configuración correcta de settings_pythonanywhere.py..."
echo ""

# Crear backup
if [ -f "censoProject/settings_pythonanywhere.py" ]; then
    cp censoProject/settings_pythonanywhere.py censoProject/settings_pythonanywhere.py.backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup creado"
else
    cp censoProject/settings.py censoProject/settings_pythonanywhere.py
    echo "✅ Creado desde settings.py"
fi

echo ""
echo "4. Configuración MySQL típica de PythonAnywhere:"
echo ""
cat << 'EOF'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'luisga64$censo',  # Formato: tu_usuario$nombre_base_datos
        'USER': 'luisga64',  # Tu usuario de PythonAnywhere
        'PASSWORD': 'TU_PASSWORD_MYSQL_AQUI',  # Password de MySQL (ver en Database tab)
        'HOST': 'luisga64.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
EOF

echo ""
echo "===== PASOS SIGUIENTES ====="
echo ""
echo "1. Ve a PythonAnywhere -> Databases tab"
echo "2. Copia el password de MySQL"
echo "3. Verifica el nombre de tu base de datos (usuario\$nombredb)"
echo "4. Edita: censoProject/settings_pythonanywhere.py"
echo "5. Actualiza la sección DATABASES con:"
echo "   - USER: tu usuario de PythonAnywhere"
echo "   - PASSWORD: el password que copiaste"
echo "   - NAME: usuario\$nombredb"
echo "   - HOST: usuario.mysql.pythonanywhere-services.com"
echo ""
echo "6. Migrar la base de datos:"
echo "   python manage.py migrate"
echo ""
echo "7. Reload en Web Tab"
echo ""
echo "NOTA: Si prefieres SQLite temporalmente mientras configuras MySQL,"
echo "      ejecuta: bash use_sqlite_temp.sh"
