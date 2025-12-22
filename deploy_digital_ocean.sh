#!/bin/bash

# ============================================================================
# Script de Despliegue para Digital Ocean - Censo Indígena v1.0
# ============================================================================
# Este script debe ejecutarse en el servidor (droplet) después de clonar
# ============================================================================

set -e  # Salir si hay algún error

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}          CENSO INDÍGENA - SCRIPT DE DESPLIEGUE v1.0${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Variables
APP_DIR="/var/www/censo-django"
VENV_DIR="$APP_DIR/venv"
DB_NAME="censo_db"
DB_USER="censo_user"

# Verificar si se está ejecutando como root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Este script debe ejecutarse como root${NC}"
    exit 1
fi

echo -e "${GREEN}[1/12] Actualizando sistema...${NC}"
apt update && apt upgrade -y

echo -e "${GREEN}[2/12] Instalando dependencias del sistema...${NC}"
apt install -y python3.11 python3.11-venv python3-pip
apt install -y git nginx postgresql postgresql-contrib
apt install -y build-essential libpq-dev
apt install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0
apt install -y libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

echo -e "${GREEN}[3/12] Configurando PostgreSQL...${NC}"
# Solicitar contraseña de base de datos
read -sp "Ingrese contraseña para la base de datos PostgreSQL: " DB_PASSWORD
echo ""

# Crear base de datos y usuario
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'America/Bogota';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

echo -e "${GREEN}[4/12] Clonando repositorio...${NC}"
mkdir -p /var/www
cd /var/www

# Solicitar URL del repositorio
read -p "Ingrese la URL del repositorio Git: " REPO_URL
git clone $REPO_URL censo-django
cd censo-django

echo -e "${GREEN}[5/12] Creando entorno virtual...${NC}"
python3.11 -m venv venv
source venv/bin/activate

echo -e "${GREEN}[6/12] Instalando dependencias de Python...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary python-decouple

echo -e "${GREEN}[7/12] Configurando variables de entorno...${NC}"
# Solicitar configuración
read -p "Ingrese el dominio o IP del servidor: " DOMAIN
read -p "Ingrese la SECRET_KEY de Django (dejar vacío para generar una): " SECRET_KEY

if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
fi

# Crear archivo .env
cat > .env << EOF
# Django Settings
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432

# Site URL
SITE_URL=https://$DOMAIN
EOF

echo -e "${GREEN}[8/12] Ejecutando migraciones...${NC}"
python manage.py migrate

echo -e "${GREEN}[9/12] Recolectando archivos estáticos...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}[10/12] Creando superusuario...${NC}"
echo "Crear cuenta de administrador:"
python manage.py createsuperuser

echo -e "${GREEN}[11/12] Configurando Gunicorn...${NC}"
cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon for censo-django
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$VENV_DIR/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:$APP_DIR/gunicorn.sock \\
          censoProject.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl start gunicorn
systemctl enable gunicorn

echo -e "${GREEN}[12/12] Configurando Nginx...${NC}"
cat > /etc/nginx/sites-available/censo << EOF
server {
    listen 80;
    server_name $DOMAIN;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $APP_DIR/media/;
        expires 7d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/gunicorn.sock;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_redirect off;
    }
}
EOF

ln -sf /etc/nginx/sites-available/censo /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx

echo -e "${GREEN}Configurando firewall...${NC}"
ufw allow OpenSSH
ufw allow 'Nginx Full'
echo "y" | ufw enable

echo ""
echo -e "${BLUE}============================================================================${NC}"
echo -e "${GREEN}✓ ¡Despliegue completado exitosamente!${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""
echo "La aplicación está disponible en: http://$DOMAIN"
echo ""
echo "Próximos pasos:"
echo "1. Configurar SSL con: certbot --nginx -d $DOMAIN"
echo "2. Cargar datos iniciales si es necesario"
echo "3. Verificar que todo funcione correctamente"
echo ""
echo "Para ver logs:"
echo "  - Gunicorn: journalctl -u gunicorn -f"
echo "  - Nginx: tail -f /var/log/nginx/error.log"
echo ""
echo -e "${BLUE}============================================================================${NC}"

