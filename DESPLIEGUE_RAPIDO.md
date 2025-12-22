# 🚀 Guía Rápida de Despliegue

## Opción 1: Script Automático (Recomendado)

### 1. Crear Droplet en Digital Ocean
- Ubuntu 22.04 LTS
- 2GB RAM mínimo
- Anotar la IP pública

### 2. Conectar al Droplet
```bash
ssh root@TU_IP_DROPLET
```

### 3. Ejecutar Script de Despliegue
```bash
# Descargar el script
wget https://raw.githubusercontent.com/TU_USUARIO/censo-django/main/deploy_digital_ocean.sh

# Dar permisos de ejecución
chmod +x deploy_digital_ocean.sh

# Ejecutar
./deploy_digital_ocean.sh
```

### 4. Seguir las instrucciones del script
El script te pedirá:
- URL del repositorio Git
- Dominio o IP del servidor
- Contraseña de la base de datos
- Crear superusuario

### 5. Configurar SSL (Opcional)
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d tu-dominio.com
```

## Opción 2: Despliegue Manual

Ver la guía completa en: `GUIA_DESPLIEGUE_DIGITAL_OCEAN.md`

## 📋 Actualizar la Aplicación

```bash
cd /var/www/censo-django
./update_app.sh
```

## 💾 Crear Backup

```bash
/var/www/censo-django/backup.sh
```

## 📊 Ver Logs

```bash
# Logs de Gunicorn
journalctl -u gunicorn -f

# Logs de Nginx
tail -f /var/log/nginx/error.log

# Logs de la aplicación
tail -f /var/www/censo-django/debug.log
```

## 🆘 Solución Rápida de Problemas

### Error 502 Bad Gateway
```bash
systemctl restart gunicorn
systemctl restart nginx
```

### Verificar Estado de Servicios
```bash
systemctl status gunicorn
systemctl status nginx
systemctl status postgresql
```

## 💰 Costos Digital Ocean

| Plan | RAM | Costo/mes |
|------|-----|-----------|
| Básico | 1GB | $6 USD |
| Regular | 2GB | $12 USD |
| Profesional | 4GB | $24 USD |

**Recomendado para empezar**: Plan de 2GB ($12/mes)

## 📞 Soporte

- Documentación completa: `GUIA_DESPLIEGUE_DIGITAL_OCEAN.md`
- Digital Ocean Docs: https://docs.digitalocean.com/
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

