#!/bin/bash
# ==============================================================================
# CENSO INDÍGENA - INSTALADOR AUTOMÁTICO ON-PREMISE
# ==============================================================================
# Versión: 1.0
# Fecha: 17 de Diciembre 2025
# Sistema Operativo: Ubuntu 20.04/22.04 LTS
# ==============================================================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
print_message() {
    echo -e "${BLUE}[CENSO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Banner
clear
echo "=============================================================================="
echo "            CENSO INDÍGENA - INSTALADOR AUTOMÁTICO LOCAL"
echo "=============================================================================="
echo ""
echo "  Este instalador configurará el sistema completo en tu servidor local"
echo ""
echo "  Características:"
echo "  ✓ Instalación de dependencias"
echo "  ✓ Configuración de PostgreSQL"
echo "  ✓ Configuración de Nginx"
echo "  ✓ Servicios systemd"
echo "  ✓ Backups automáticos"
echo "  ✓ Certificados SSL opcionales"
echo ""
echo "=============================================================================="
echo ""

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    print_error "Por favor ejecute como root (sudo ./install.sh)"
    exit 1
fi

# Solicitar información
print_message "Configuración inicial..."
echo ""

read -p "Nombre de la organización: " ORG_NAME
read -p "Dominio o IP del servidor (ej: censo.resguardo.local o 192.168.1.100): " SERVER_DOMAIN
read -p "Email del administrador: " ADMIN_EMAIL
read -sp "Contraseña del administrador: " ADMIN_PASSWORD
echo ""
read -sp "Contraseña para PostgreSQL: " DB_PASSWORD
echo ""

# Generar SECRET_KEY
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' 2>/dev/null || openssl rand -base64 32)

echo ""
print_success "Configuración capturada"
echo ""

# ==================== PASO 1: ACTUALIZAR SISTEMA ====================
print_message "Paso 1/10: Actualizando sistema operativo..."
apt update > /dev/null 2>&1
apt upgrade -y > /dev/null 2>&1
print_success "Sistema actualizado"

# ==================== PASO 2: INSTALAR DEPENDENCIAS ====================
print_message "Paso 2/10: Instalando dependencias del sistema..."
apt install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    python3-dev \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    nginx \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    supervisor \
    ufw \
    > /dev/null 2>&1
print_success "Dependencias instaladas"

# ==================== PASO 3: CONFIGURAR POSTGRESQL ====================
print_message "Paso 3/10: Configurando PostgreSQL..."

# Crear base de datos y usuario
sudo -u postgres psql > /dev/null 2>&1 << EOF
-- Crear usuario
CREATE USER censo_user WITH PASSWORD '$DB_PASSWORD';

-- Crear base de datos
CREATE DATABASE censo_db OWNER censo_user;

-- Configurar permisos
ALTER ROLE censo_user SET client_encoding TO 'utf8';
ALTER ROLE censo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE censo_user SET timezone TO 'America/Bogota';
GRANT ALL PRIVILEGES ON DATABASE censo_db TO censo_user;
EOF

print_success "PostgreSQL configurado"

# ==================== PASO 4: CREAR ESTRUCTURA DE DIRECTORIOS ====================
print_message "Paso 4/10: Creando estructura de directorios..."

# Crear directorios
mkdir -p /opt/censo-django
mkdir -p /opt/censo-django/logs
mkdir -p /opt/censo-django/backups
mkdir -p /opt/censo-django/media
mkdir -p /opt/censo-django/static
mkdir -p /opt/censo-django/scripts

# Permisos
chown -R www-data:www-data /opt/censo-django
chmod 755 /opt/censo-django

print_success "Estructura de directorios creada"

# ==================== PASO 5: CLONAR/COPIAR APLICACIÓN ====================
print_message "Paso 5/10: Instalando aplicación..."

cd /opt/censo-django

# Si existe el código localmente, copiarlo, sino clonar de git
if [ -d "/tmp/censo-django" ]; then
    cp -r /tmp/censo-django/* .
    print_success "Código copiado desde /tmp/censo-django"
else
    # Aquí iría el git clone si estuviera en repositorio
    print_warning "Asegúrate de copiar los archivos de la aplicación a /opt/censo-django"
fi

# ==================== PASO 6: CONFIGURAR ENTORNO VIRTUAL ====================
print_message "Paso 6/10: Configurando entorno virtual de Python..."

python3 -m venv venv
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip > /dev/null 2>&1

# Instalar dependencias
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    print_success "Dependencias de Python instaladas"
else
    print_warning "requirements.txt no encontrado, instala las dependencias manualmente"
fi

# ==================== PASO 7: CONFIGURAR VARIABLES DE ENTORNO ====================
print_message "Paso 7/10: Configurando variables de entorno..."

cat > /opt/censo-django/.env << EOF
# Django Settings
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,$SERVER_DOMAIN,$(hostname -I | awk '{print $1}')

# Database
DATABASE_NAME=censo_db
DATABASE_USER=censo_user
DATABASE_PASSWORD=$DB_PASSWORD
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Site
SITE_URL=http://$SERVER_DOMAIN

# Email (configurar según necesidad)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Organization
ORGANIZATION_NAME=$ORG_NAME
ADMIN_EMAIL=$ADMIN_EMAIL
EOF

chmod 600 /opt/censo-django/.env
chown www-data:www-data /opt/censo-django/.env

print_success "Variables de entorno configuradas"

# ==================== PASO 8: APLICAR MIGRACIONES ====================
print_message "Paso 8/10: Aplicando migraciones de base de datos..."

cd /opt/censo-django
source venv/bin/activate

python manage.py migrate > /dev/null 2>&1

# Crear superusuario
DJANGO_SUPERUSER_PASSWORD=$ADMIN_PASSWORD python manage.py createsuperuser \
    --noinput \
    --username=admin \
    --email=$ADMIN_EMAIL \
    > /dev/null 2>&1

# Recolectar archivos estáticos
python manage.py collectstatic --noinput > /dev/null 2>&1

print_success "Migraciones aplicadas y superusuario creado"

# ==================== PASO 9: CONFIGURAR SERVICIOS ====================
print_message "Paso 9/10: Configurando servicios del sistema..."

# Configurar Gunicorn service
cat > /etc/systemd/system/censo.service << EOF
[Unit]
Description=Censo Indígena Django Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/censo-django
Environment="PATH=/opt/censo-django/venv/bin"
EnvironmentFile=/opt/censo-django/.env
ExecStart=/opt/censo-django/venv/bin/gunicorn \\
    --workers 3 \\
    --bind unix:/opt/censo-django/censo.sock \\
    --timeout 120 \\
    --access-logfile /opt/censo-django/logs/access.log \\
    --error-logfile /opt/censo-django/logs/error.log \\
    censoProject.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configurar Nginx
cat > /etc/nginx/sites-available/censo << EOF
server {
    listen 80;
    server_name $SERVER_DOMAIN;

    client_max_body_size 100M;

    # Logs
    access_log /opt/censo-django/logs/nginx-access.log;
    error_log /opt/censo-django/logs/nginx-error.log;

    # Static files
    location /static/ {
        alias /opt/censo-django/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /opt/censo-django/media/;
        expires 7d;
    }

    # Favicon
    location = /favicon.ico {
        access_log off;
        log_not_found off;
        alias /opt/censo-django/static/assets/img/favicon.png;
    }

    # Application
    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/censo-django/censo.sock;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
    }
}
EOF

# Habilitar sitio
ln -sf /etc/nginx/sites-available/censo /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Probar configuración de Nginx
nginx -t > /dev/null 2>&1

print_success "Servicios configurados"

# ==================== PASO 10: CONFIGURAR BACKUPS AUTOMÁTICOS ====================
print_message "Paso 10/10: Configurando backups automáticos..."

cat > /opt/censo-django/scripts/backup.sh << 'EOF'
#!/bin/bash
# Script de backup automático

BACKUP_DIR="/opt/censo-django/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DAYS_TO_KEEP=30

# Backup de base de datos
pg_dump -U censo_user censo_db | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Backup de archivos media
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" -C /opt/censo-django media/

# Eliminar backups antiguos
find $BACKUP_DIR -type f -mtime +$DAYS_TO_KEEP -delete

echo "$(date): Backup completado - db_$DATE.sql.gz y media_$DATE.tar.gz" >> /opt/censo-django/logs/backup.log
EOF

chmod +x /opt/censo-django/scripts/backup.sh

# Configurar cron para backup diario a las 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/censo-django/scripts/backup.sh") | crontab -

print_success "Backups automáticos configurados (diario 2:00 AM)"

# ==================== INICIAR SERVICIOS ====================
print_message "Iniciando servicios..."

# Iniciar y habilitar servicios
systemctl daemon-reload
systemctl start censo
systemctl enable censo > /dev/null 2>&1
systemctl restart nginx

print_success "Servicios iniciados"

# ==================== CONFIGURAR FIREWALL ====================
print_message "Configurando firewall..."

ufw allow 22/tcp > /dev/null 2>&1  # SSH
ufw allow 80/tcp > /dev/null 2>&1  # HTTP
ufw --force enable > /dev/null 2>&1

print_success "Firewall configurado"

# ==================== GUARDAR INFORMACIÓN DE ACCESO ====================
cat > /opt/censo-django/INFORMACION_ACCESO.txt << EOF
============================================================================
                    CENSO INDÍGENA - INFORMACIÓN DE ACCESO
============================================================================

ACCESO AL SISTEMA:
------------------
URL: http://$SERVER_DOMAIN
Usuario: admin
Contraseña: $ADMIN_PASSWORD

ORGANIZACIÓN:
-------------
Nombre: $ORG_NAME
Email: $ADMIN_EMAIL

BASE DE DATOS:
--------------
Base de datos: censo_db
Usuario: censo_user
Contraseña: $DB_PASSWORD
Host: localhost
Puerto: 5432

UBICACIÓN DE ARCHIVOS:
----------------------
Aplicación: /opt/censo-django
Logs: /opt/censo-django/logs
Backups: /opt/censo-django/backups
Media: /opt/censo-django/media
Static: /opt/censo-django/static

SERVICIOS:
----------
Aplicación: systemctl status censo
Servidor web: systemctl status nginx
Base de datos: systemctl status postgresql

COMANDOS ÚTILES:
----------------
Ver logs:
  tail -f /opt/censo-django/logs/error.log
  tail -f /opt/censo-django/logs/access.log

Reiniciar servicios:
  systemctl restart censo
  systemctl restart nginx

Backup manual:
  /opt/censo-django/scripts/backup.sh

Restaurar backup:
  gunzip -c /opt/censo-django/backups/db_FECHA.sql.gz | psql -U censo_user censo_db

BACKUPS AUTOMÁTICOS:
--------------------
Frecuencia: Diario a las 2:00 AM
Ubicación: /opt/censo-django/backups
Retención: 30 días

SOPORTE:
--------
Documentación: /opt/censo-django/docs/
Email: soporte@censo-indigena.com
Teléfono: +57 XXX XXX XXXX

NOTAS DE SEGURIDAD:
-------------------
1. Cambie la contraseña del administrador en el primer login
2. Configure el email para notificaciones
3. Revise los logs periódicamente
4. Verifique que los backups se estén ejecutando
5. Mantenga el sistema actualizado

============================================================================
                        Instalación completada: $(date)
============================================================================
EOF

chmod 600 /opt/censo-django/INFORMACION_ACCESO.txt

# ==================== RESUMEN FINAL ====================
clear
echo "=============================================================================="
echo "                          ¡INSTALACIÓN COMPLETADA!"
echo "=============================================================================="
echo ""
echo "✓ Sistema instalado correctamente en: /opt/censo-django"
echo "✓ Base de datos PostgreSQL configurada"
echo "✓ Servidor web Nginx configurado"
echo "✓ Servicios systemd habilitados"
echo "✓ Backups automáticos configurados"
echo "✓ Firewall configurado"
echo ""
echo "=============================================================================="
echo "                          INFORMACIÓN DE ACCESO"
echo "=============================================================================="
echo ""
echo "  URL del sistema:  http://$SERVER_DOMAIN"
echo "  Usuario:          admin"
echo "  Contraseña:       $ADMIN_PASSWORD"
echo ""
echo "=============================================================================="
echo "                          PRÓXIMOS PASOS"
echo "=============================================================================="
echo ""
echo "  1. Acceda al sistema en: http://$SERVER_DOMAIN"
echo "  2. Inicie sesión con las credenciales de arriba"
echo "  3. Configure los datos de su organización"
echo "  4. Cree usuarios adicionales"
echo "  5. Comience a registrar fichas familiares"
echo ""
echo "  IMPORTANTE: Toda la información de acceso se guardó en:"
echo "  /opt/censo-django/INFORMACION_ACCESO.txt"
echo ""
echo "  Para ver el estado de los servicios:"
echo "  systemctl status censo"
echo "  systemctl status nginx"
echo ""
echo "  Para ver los logs:"
echo "  tail -f /opt/censo-django/logs/error.log"
echo ""
echo "=============================================================================="
echo "                    ¡GRACIAS POR USAR CENSO INDÍGENA!"
echo "=============================================================================="
echo ""

# Guardar IP para referencia
IP_ADDRESS=$(hostname -I | awk '{print $1}')
if [ "$SERVER_DOMAIN" != "$IP_ADDRESS" ]; then
    echo "  Nota: También puede acceder mediante la IP: http://$IP_ADDRESS"
    echo ""
fi

exit 0

