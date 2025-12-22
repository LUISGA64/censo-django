#!/bin/bash

# Script de Instalación Automática para Linux
# Sistema de Censo - Instalación para Cliente

echo "======================================="
echo "  Sistema de Censo - Instalación"
echo "  Versión 1.0"
echo "======================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 1. Verificar si se ejecuta como root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Se recomienda NO ejecutar como root${NC}"
    echo ""
fi

# 2. Verificar Python
echo -e "${GREEN}1️⃣  Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "   ${GREEN}✅ Python instalado: $PYTHON_VERSION${NC}"
else
    echo -e "   ${RED}❌ Python no encontrado${NC}"
    echo -e "   ${YELLOW}Instalando Python...${NC}"
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# 3. Verificar pip
echo ""
echo -e "${GREEN}2️⃣  Verificando pip...${NC}"
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo -e "   ${GREEN}✅ pip instalado: $PIP_VERSION${NC}"
else
    echo -e "   ${RED}❌ pip no encontrado${NC}"
    sudo apt install -y python3-pip
fi

# 4. Instalar dependencias del sistema
echo ""
echo -e "${GREEN}3️⃣  Instalando dependencias del sistema...${NC}"
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
echo -e "   ${GREEN}✅ Dependencias del sistema instaladas${NC}"

# 5. Crear entorno virtual
echo ""
echo -e "${GREEN}4️⃣  Creando entorno virtual...${NC}"
if [ -d "venv" ]; then
    echo -e "   ${YELLOW}⚠️  El entorno virtual ya existe${NC}"
    read -p "   ¿Desea recrearlo? (s/n): " recreate
    if [ "$recreate" = "s" ] || [ "$recreate" = "S" ]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "   ${GREEN}✅ Entorno virtual recreado${NC}"
    fi
else
    python3 -m venv venv
    echo -e "   ${GREEN}✅ Entorno virtual creado${NC}"
fi

# 6. Activar entorno virtual
source venv/bin/activate

# 7. Actualizar pip
echo ""
echo -e "${GREEN}5️⃣  Actualizando pip...${NC}"
pip install --upgrade pip --quiet
echo -e "   ${GREEN}✅ pip actualizado${NC}"

# 8. Instalar dependencias de Python
echo ""
echo -e "${GREEN}6️⃣  Instalando dependencias de Python...${NC}"
echo -e "   ${CYAN}📦 Esto puede tomar varios minutos...${NC}"
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ Dependencias instaladas correctamente${NC}"
else
    echo -e "   ${RED}❌ Error al instalar dependencias${NC}"
    exit 1
fi

# 9. Crear directorios necesarios
echo ""
echo -e "${GREEN}7️⃣  Creando estructura de directorios...${NC}"
directories=("media" "media/Association" "media/Images" "static" "logs" "backups")
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "   ${GREEN}✅ Creado: $dir${NC}"
    else
        echo -e "   ✔️  Existe: $dir"
    fi
done

# Establecer permisos
chmod -R 755 media
chmod -R 755 logs
chmod -R 755 backups
echo -e "   ${GREEN}✅ Permisos configurados${NC}"

# 10. Configurar archivo .env
echo ""
echo -e "${GREEN}8️⃣  Configurando variables de entorno...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Configuración del Sistema de Censo
DEBUG=True
SECRET_KEY=django-insecure-cambiar-en-produccion-$RANDOM$RANDOM
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (SQLite por defecto)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.censo_Web

# Configuración de medios
MEDIA_URL=/media/
MEDIA_ROOT=media

# Configuración de estáticos
STATIC_URL=/static/
STATIC_ROOT=staticfiles
EOF
    echo -e "   ${GREEN}✅ Archivo .env creado${NC}"
else
    echo -e "   ${YELLOW}⚠️  Archivo .env ya existe, no se modificó${NC}"
fi

# 11. Ejecutar migraciones
echo ""
echo -e "${GREEN}9️⃣  Configurando base de datos...${NC}"
echo -e "   ${CYAN}📊 Ejecutando migraciones...${NC}"
python manage.py migrate --noinput

if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ Base de datos configurada correctamente${NC}"
else
    echo -e "   ${RED}❌ Error al configurar la base de datos${NC}"
    exit 1
fi

# 12. Cargar datos iniciales
echo ""
echo -e "${GREEN}🔟 Cargando datos iniciales...${NC}"
if [ -d "censoapp/fixtures" ]; then
    for fixture in censoapp/fixtures/*.json; do
        if [ -f "$fixture" ]; then
            echo -e "   ${CYAN}📄 Cargando: $(basename $fixture)${NC}"
            python manage.py loaddata "$fixture" --verbosity 0
        fi
    done
    echo -e "   ${GREEN}✅ Datos iniciales cargados${NC}"
else
    echo -e "   ${YELLOW}⚠️  No se encontraron fixtures para cargar${NC}"
fi

# 13. Recolectar archivos estáticos
echo ""
echo -e "${GREEN}1️⃣1️⃣  Recolectando archivos estáticos...${NC}"
python manage.py collectstatic --noinput --clear --verbosity 0

if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ Archivos estáticos recolectados${NC}"
else
    echo -e "   ${YELLOW}⚠️  Advertencia al recolectar estáticos (puede ser normal)${NC}"
fi

# 14. Crear superusuario
echo ""
echo -e "${GREEN}1️⃣2️⃣  Creando usuario administrador...${NC}"
echo -e "   ${CYAN}Por favor, ingrese los datos del administrador:${NC}"
echo ""

# Verificar si ya existe un superusuario
SUPERUSER_EXISTS=$(python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>&1)

if [[ "$SUPERUSER_EXISTS" == *"True"* ]]; then
    echo -e "   ${YELLOW}⚠️  Ya existe un superusuario en el sistema${NC}"
    read -p "   ¿Desea crear otro superusuario? (s/n): " create_new
    if [ "$create_new" = "s" ] || [ "$create_new" = "S" ]; then
        python manage.py createsuperuser
    fi
else
    python manage.py createsuperuser
fi

# 15. Crear script de inicio
echo ""
echo -e "${GREEN}1️⃣3️⃣  Creando scripts de utilidad...${NC}"

# Script de inicio
cat > scripts/start_server.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
EOF
chmod +x scripts/start_server.sh
echo -e "   ${GREEN}✅ Script de inicio creado${NC}"

# Script de respaldo
cat > scripts/backup_database.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > backups/backup_$TIMESTAMP.json
echo "Respaldo creado: backups/backup_$TIMESTAMP.json"
EOF
chmod +x scripts/backup_database.sh
echo -e "   ${GREEN}✅ Script de respaldo creado${NC}"

# 16. Resumen de instalación
echo ""
echo "======================================="
echo -e "  ${GREEN}✅ INSTALACIÓN COMPLETADA${NC}"
echo "======================================="
echo ""
echo -e "${NC}📋 Resumen de la instalación:${NC}"
echo "   • Entorno virtual: CREADO"
echo "   • Dependencias: INSTALADAS"
echo "   • Base de datos: CONFIGURADA"
echo "   • Datos iniciales: CARGADOS"
echo "   • Usuario admin: CREADO"
echo ""
echo -e "${YELLOW}🚀 Para iniciar el servidor:${NC}"
echo -e "   ${NC}1. Ejecute: ./scripts/start_server.sh${NC}"
echo -e "   ${NC}2. Abra su navegador en: http://localhost:8000${NC}"
echo ""
echo -e "${CYAN}📚 Documentación disponible en: ./docs/${NC}"
echo ""
echo -e "${GREEN}¡Gracias por usar el Sistema de Censo!${NC}"
echo ""

# Preguntar si desea iniciar el servidor
read -p "¿Desea iniciar el servidor ahora? (s/n): " start_server
if [ "$start_server" = "s" ] || [ "$start_server" = "S" ]; then
    echo ""
    echo -e "${GREEN}🚀 Iniciando servidor...${NC}"
    echo -e "   ${YELLOW}Presione Ctrl+C para detener el servidor${NC}"
    echo ""
    python manage.py runserver 0.0.0.0:8000
fi

