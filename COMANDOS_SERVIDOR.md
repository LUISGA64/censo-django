# 🔧 Comandos Útiles para Administración del Servidor

## 🔍 Verificar Estado de Servicios

```bash
# Ver estado de todos los servicios
systemctl status gunicorn
systemctl status nginx
systemctl status postgresql

# Ver si están habilitados para auto-inicio
systemctl is-enabled gunicorn
systemctl is-enabled nginx
systemctl is-enabled postgresql
```

## 🔄 Reiniciar Servicios

```bash
# Reiniciar Gunicorn (después de cambios en código Python)
sudo systemctl restart gunicorn

# Reiniciar Nginx (después de cambios en configuración)
sudo systemctl restart nginx

# Recargar Nginx sin downtime
sudo systemctl reload nginx

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

## 📊 Ver Logs en Tiempo Real

```bash
# Logs de Gunicorn
sudo journalctl -u gunicorn -f

# Logs de Nginx (errores)
sudo tail -f /var/log/nginx/error.log

# Logs de Nginx (acceso)
sudo tail -f /var/log/nginx/access.log

# Logs de la aplicación Django
sudo tail -f /var/www/censo-django/debug.log

# Logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*.log

# Ver últimas 100 líneas de logs de Gunicorn
sudo journalctl -u gunicorn -n 100 --no-pager
```

## 🗄️ Gestión de Base de Datos

```bash
# Conectar a PostgreSQL
sudo -u postgres psql

# Conectar a una base de datos específica
sudo -u postgres psql -d censo_db

# Crear backup de base de datos
sudo -u postgres pg_dump censo_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
sudo -u postgres psql censo_db < backup_20231222.sql

# Ver tamaño de la base de datos
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('censo_db'));"

# Ver tablas y su tamaño
sudo -u postgres psql -d censo_db -c "\dt+"
```

## 🐍 Gestión de Django

```bash
# Activar entorno virtual
cd /var/www/censo-django
source venv/bin/activate

# Ejecutar shell de Django
python manage.py shell

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario
python manage.py createsuperuser

# Verificar configuración
python manage.py check

# Ver todas las migraciones
python manage.py showmigrations

# Cargar datos desde fixture
python manage.py loaddata censoapp/fixtures/initial_data.json
```

## 📦 Actualizar la Aplicación

```bash
# Método 1: Script automático
cd /var/www/censo-django
./update_app.sh

# Método 2: Manual
cd /var/www/censo-django
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## 💾 Backups

```bash
# Crear backup manual
cd /var/www/censo-django
./backup.sh

# Ver backups existentes
ls -lh /var/backups/censo/

# Restaurar backup de base de datos
gunzip -c /var/backups/censo/db_20231222_120000.sql.gz | sudo -u postgres psql censo_db

# Restaurar backup de media
tar -xzf /var/backups/censo/media_20231222_120000.tar.gz -C /var/www/censo-django/
```

## 🔒 Gestión de SSL

```bash
# Renovar certificados SSL manualmente
sudo certbot renew

# Test de renovación (sin aplicar cambios)
sudo certbot renew --dry-run

# Ver certificados instalados
sudo certbot certificates

# Renovar certificado específico
sudo certbot renew --cert-name tu-dominio.com
```

## 🔥 Firewall

```bash
# Ver reglas del firewall
sudo ufw status verbose

# Permitir puerto
sudo ufw allow 8000

# Denegar puerto
sudo ufw deny 8000

# Eliminar regla
sudo ufw delete allow 8000

# Habilitar/deshabilitar firewall
sudo ufw enable
sudo ufw disable
```

## 📈 Monitoreo de Recursos

```bash
# Ver uso de CPU y memoria
top
htop  # (si está instalado)

# Ver uso de disco
df -h

# Ver espacio usado por directorio
du -sh /var/www/censo-django/*

# Ver procesos de Gunicorn
ps aux | grep gunicorn

# Ver conexiones activas de Nginx
sudo netstat -tulpn | grep nginx

# Ver estadísticas de PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

## 🧹 Limpieza y Mantenimiento

```bash
# Limpiar archivos de log antiguos
sudo find /var/log -type f -name "*.log" -mtime +30 -delete

# Limpiar paquetes huérfanos
sudo apt autoremove -y
sudo apt autoclean

# Limpiar archivos de sesión de Django
cd /var/www/censo-django
source venv/bin/activate
python manage.py clearsessions

# Vacuumar base de datos PostgreSQL (optimizar)
sudo -u postgres psql -d censo_db -c "VACUUM ANALYZE;"

# Ver tamaño de tabla de sesiones
sudo -u postgres psql -d censo_db -c "SELECT pg_size_pretty(pg_total_relation_size('django_session'));"
```

## 🔐 Gestión de Permisos

```bash
# Establecer permisos correctos para la aplicación
sudo chown -R root:www-data /var/www/censo-django
sudo chmod -R 755 /var/www/censo-django

# Permisos para archivos media
sudo chown -R root:www-data /var/www/censo-django/media
sudo chmod -R 775 /var/www/censo-django/media

# Permisos para archivos estáticos
sudo chown -R root:www-data /var/www/censo-django/staticfiles
sudo chmod -R 755 /var/www/censo-django/staticfiles
```

## 🌐 Testing y Debugging

```bash
# Probar configuración de Nginx
sudo nginx -t

# Verificar socket de Gunicorn
ls -l /var/www/censo-django/gunicorn.sock

# Probar conectividad a PostgreSQL
sudo -u postgres psql -c "SELECT version();"

# Ver variables de entorno
cat /var/www/censo-django/.env

# Verificar puerto 80/443
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# Hacer request local
curl http://localhost
curl https://tu-dominio.com
```

## 📝 Editar Archivos de Configuración

```bash
# Editar settings de Django
nano /var/www/censo-django/censoProject/settings.py

# Editar configuración de Gunicorn
sudo nano /etc/systemd/system/gunicorn.service

# Editar configuración de Nginx
sudo nano /etc/nginx/sites-available/censo

# Editar variables de entorno
nano /var/www/censo-django/.env

# Después de editar archivos de servicio, recargar
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

## 🔄 Git

```bash
# Ver estado del repositorio
cd /var/www/censo-django
git status

# Ver log de commits
git log --oneline -10

# Cambiar de rama
git checkout main

# Descartar cambios locales
git reset --hard HEAD

# Ver diferencias
git diff

# Ver información del repositorio remoto
git remote -v
```

## 📊 Estadísticas Rápidas

```bash
# Contar usuarios en la base de datos
sudo -u postgres psql -d censo_db -c "SELECT COUNT(*) FROM auth_user;"

# Contar fichas familiares
sudo -u postgres psql -d censo_db -c "SELECT COUNT(*) FROM censoapp_familycard;"

# Contar documentos generados
sudo -u postgres psql -d censo_db -c "SELECT COUNT(*) FROM censoapp_generateddocument;"

# Ver últimos 10 usuarios registrados
sudo -u postgres psql -d censo_db -c "SELECT username, date_joined FROM auth_user ORDER BY date_joined DESC LIMIT 10;"
```

## 🆘 Comandos de Emergencia

```bash
# Reiniciar todos los servicios
sudo systemctl restart gunicorn nginx postgresql

# Matar todos los procesos de Gunicorn
sudo pkill -9 gunicorn
sudo systemctl start gunicorn

# Liberar espacio en disco rápidamente
sudo apt clean
sudo journalctl --vacuum-time=7d

# Ver últimos errores del sistema
sudo journalctl -p err -n 50 --no-pager

# Verificar integridad de base de datos
sudo -u postgres psql -d censo_db -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;"
```

---

## 📚 Notas Importantes

1. **Siempre hacer backup antes de cambios importantes**
2. **Probar en ambiente de desarrollo primero**
3. **Mantener logs de cambios realizados**
4. **Documentar configuraciones personalizadas**
5. **Revisar logs después de cada cambio**

---

**Última actualización**: Diciembre 2024

