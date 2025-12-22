# 🚀 Guía de Despliegue - Digital Ocean (Versión 1.0)

## 📋 Requisitos Previos

### 1. Cuenta de Digital Ocean
- Crear cuenta en [Digital Ocean](https://www.digitalocean.com/)
- Agregar método de pago (tarjeta de crédito o PayPal)
- **Costo estimado**: $6-12 USD/mes para un droplet básico

### 2. Dominio (Opcional pero Recomendado)
- Registrar un dominio (ej: censo-indigena.com)
- Configurar DNS apuntando a tu droplet
- Si no tienes dominio, puedes usar la IP pública del droplet

---

## 🖥️ PASO 1: Crear el Droplet en Digital Ocean

### 1.1 Crear Droplet
1. Ir a Digital Ocean Dashboard → **Create** → **Droplets**
2. Seleccionar configuración:
   - **Distribución**: Ubuntu 22.04 LTS x64
   - **Plan**: Basic
   - **CPU Options**: Regular (Intel)
   - **RAM**: 2 GB / 1 vCPU ($12/mes) o 1 GB / 1 vCPU ($6/mes)
   - **Región**: New York, San Francisco o el más cercano
   - **Autenticación**: SSH keys (recomendado) o Password
   - **Hostname**: censo-indigena

3. Click en **Create Droplet**
4. Anotar la **IP pública** del droplet (ej: 159.89.123.456)

### 1.2 Configurar SSH (si usas SSH Keys)
```powershell
# En Windows (PowerShell)
ssh-keygen -t rsa -b 4096 -C "tu_email@ejemplo.com"
# Presiona Enter para guardar en la ubicación por defecto
# Copia la clave pública que está en: C:\Users\LENOVO\.ssh\id_rsa.pub
```

---

## 🔧 PASO 2: Conectarse al Droplet

### 2.1 Conectar vía SSH
```powershell
# Desde PowerShell
ssh root@TU_IP_DROPLET
# Ejemplo: ssh root@159.89.123.456
```

### 2.2 Actualizar el Sistema
```bash
apt update && apt upgrade -y
```

---

## 📦 PASO 3: Instalar Dependencias en el Droplet

### 3.1 Instalar Python y herramientas básicas
```bash
apt install -y python3.11 python3.11-venv python3-pip
apt install -y git nginx postgresql postgresql-contrib
apt install -y build-essential libpq-dev
apt install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0
apt install -y libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

### 3.2 Configurar PostgreSQL
```bash
# Cambiar a usuario postgres
sudo -u postgres psql

# Dentro de psql, ejecutar:
CREATE DATABASE censo_db;
CREATE USER censo_user WITH PASSWORD 'TuPasswordSegura123!';
ALTER ROLE censo_user SET client_encoding TO 'utf8';
ALTER ROLE censo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE censo_user SET timezone TO 'America/Bogota';
GRANT ALL PRIVILEGES ON DATABASE censo_db TO censo_user;
\q
```

---

## 🌐 PASO 4: Configurar el Proyecto

### 4.1 Clonar el repositorio
```bash
# Crear directorio para la aplicación
mkdir -p /var/www
cd /var/www

# Clonar tu repositorio
git clone https://github.com/TU_USUARIO/censo-django.git
cd censo-django
```

### 4.2 Crear entorno virtual
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 4.3 Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary python-decouple
```

### 4.4 Configurar variables de entorno
```bash
# Crear archivo .env
nano .env
```

Contenido del archivo `.env`:
```env
# Django Settings
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-aqui-cambiarla
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,TU_IP_DROPLET

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=censo_db
DB_USER=censo_user
DB_PASSWORD=TuPasswordSegura123!
DB_HOST=localhost
DB_PORT=5432

# Site URL
SITE_URL=https://tu-dominio.com
```

### 4.5 Configurar settings para producción
Ejecuta en tu computadora local antes de subir al repo:
```bash
# Ya tenemos el archivo creado (ver más abajo)
```

---

## 🔨 PASO 5: Preparar la Aplicación

### 5.1 Ejecutar migraciones
```bash
cd /var/www/censo-django
source venv/bin/activate
python manage.py migrate
```

### 5.2 Crear superusuario
```bash
python manage.py createsuperuser
# Seguir las instrucciones
```

### 5.3 Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 5.4 Cargar datos iniciales (opcional)
```bash
python manage.py loaddata censoapp/fixtures/initial_data.json
```

---

## 🚀 PASO 6: Configurar Gunicorn

### 6.1 Crear archivo de servicio systemd
```bash
nano /etc/systemd/system/gunicorn.service
```

Contenido:
```ini
[Unit]
Description=gunicorn daemon for censo-django
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/censo-django
EnvironmentFile=/var/www/censo-django/.env
ExecStart=/var/www/censo-django/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/var/www/censo-django/gunicorn.sock \
          censoProject.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 6.2 Iniciar y habilitar Gunicorn
```bash
systemctl start gunicorn
systemctl enable gunicorn
systemctl status gunicorn
```

---

## 🌐 PASO 7: Configurar Nginx

### 7.1 Crear configuración de Nginx
```bash
nano /etc/nginx/sites-available/censo
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com TU_IP_DROPLET;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/censo-django/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/censo-django/media/;
        expires 7d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/censo-django/gunicorn.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### 7.2 Activar configuración
```bash
ln -s /etc/nginx/sites-available/censo /etc/nginx/sites-enabled
nginx -t  # Verificar configuración
systemctl restart nginx
```

---

## 🔒 PASO 8: Configurar SSL con Let's Encrypt (OPCIONAL)

### 8.1 Instalar Certbot
```bash
apt install -y certbot python3-certbot-nginx
```

### 8.2 Obtener certificado SSL
```bash
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

### 8.3 Renovación automática
```bash
certbot renew --dry-run  # Test
systemctl status certbot.timer  # Verificar timer
```

---

## 🔥 PASO 9: Configurar Firewall

```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
ufw status
```

---

## 📊 PASO 10: Verificar el Despliegue

### 10.1 Verificar servicios
```bash
systemctl status gunicorn
systemctl status nginx
systemctl status postgresql
```

### 10.2 Ver logs
```bash
# Logs de Gunicorn
journalctl -u gunicorn -f

# Logs de Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### 10.3 Acceder a la aplicación
- Abre un navegador
- Ve a: `http://TU_IP_DROPLET` o `https://tu-dominio.com`
- Deberías ver la página de inicio

---

## 🔄 PASO 11: Actualizar la Aplicación

### Script para futuras actualizaciones
```bash
cd /var/www/censo-django
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart gunicorn
```

---

## 🗄️ PASO 12: Backups Automáticos

### 12.1 Crear script de backup
```bash
nano /usr/local/bin/backup_censo.sh
```

Contenido:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/censo"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup de base de datos
sudo -u postgres pg_dump censo_db > $BACKUP_DIR/db_$DATE.sql

# Backup de archivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/censo-django/media/

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completado: $DATE"
```

### 12.2 Dar permisos y configurar cron
```bash
chmod +x /usr/local/bin/backup_censo.sh

# Editar crontab
crontab -e

# Agregar esta línea (backup diario a las 2 AM)
0 2 * * * /usr/local/bin/backup_censo.sh >> /var/log/censo_backup.log 2>&1
```

---

## 📋 Checklist Final

- [ ] Droplet creado y accesible vía SSH
- [ ] Dependencias instaladas (Python, PostgreSQL, Nginx)
- [ ] Base de datos PostgreSQL configurada
- [ ] Repositorio clonado
- [ ] Variables de entorno configuradas (.env)
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recolectados
- [ ] Gunicorn funcionando
- [ ] Nginx configurado y funcionando
- [ ] SSL configurado (si aplica)
- [ ] Firewall configurado
- [ ] Backups automáticos configurados
- [ ] Aplicación accesible desde el navegador

---

## 🆘 Solución de Problemas

### Problema: Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
systemctl status gunicorn
journalctl -u gunicorn -n 50

# Reiniciar servicios
systemctl restart gunicorn
systemctl restart nginx
```

### Problema: Archivos estáticos no cargan
```bash
# Verificar permisos
chown -R root:www-data /var/www/censo-django
chmod -R 755 /var/www/censo-django/staticfiles

# Recolectar nuevamente
python manage.py collectstatic --noinput
```

### Problema: No se puede conectar a la base de datos
```bash
# Verificar PostgreSQL
systemctl status postgresql

# Verificar credenciales en .env
cat /var/www/censo-django/.env

# Probar conexión manual
sudo -u postgres psql -d censo_db -U censo_user
```

---

## 📞 Recursos Adicionales

- **Documentación Django**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Digital Ocean Tutorials**: https://www.digitalocean.com/community/tutorials
- **Let's Encrypt**: https://letsencrypt.org/getting-started/

---

## 💰 Costos Estimados

| Servicio | Costo Mensual |
|----------|---------------|
| Droplet 1GB | $6 USD |
| Droplet 2GB | $12 USD |
| Dominio | $10-15 USD/año |
| **Total** | **$6-12 USD/mes** |

---

## 🎯 Próximos Pasos

1. **Monitoreo**: Configurar herramientas de monitoreo (ej: UptimeRobot)
2. **CDN**: Implementar CDN para archivos estáticos (ej: Digital Ocean Spaces)
3. **Escalamiento**: Aumentar recursos según demanda
4. **Testing**: Realizar pruebas de carga

---

**¡Listo para mostrar tu proyecto a los cabildos!** 🎉

