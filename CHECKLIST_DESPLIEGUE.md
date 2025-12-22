# 📋 Checklist Pre-Despliegue - Censo Indígena v1.0

## ✅ Antes de Desplegar

### 1. Preparación del Código
- [ ] Todas las migraciones están creadas y probadas
- [ ] Los archivos estáticos funcionan correctamente
- [ ] Las plantillas de documentos están configuradas
- [ ] El sistema de autenticación funciona
- [ ] Los permisos de usuario están correctamente configurados

### 2. Configuración
- [ ] Archivo `.env.example` creado con todas las variables necesarias
- [ ] `settings_production.py` configurado
- [ ] `requirements.txt` actualizado con todas las dependencias
- [ ] `.gitignore` configurado para no subir archivos sensibles

### 3. Base de Datos
- [ ] Datos de prueba creados y verificados
- [ ] Fixtures de datos iniciales preparados (si aplica)
- [ ] Script de migración de datos probado (si migras de otro sistema)

### 4. Seguridad
- [ ] SECRET_KEY diferente para producción
- [ ] DEBUG=False en producción
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] Variables sensibles usando variables de entorno

### 5. Funcionalidades Críticas Probadas
- [ ] Creación de fichas familiares
- [ ] Registro de personas
- [ ] Generación de documentos con plantillas
- [ ] Sistema de verificación de documentos (QR)
- [ ] Dashboard con estadísticas
- [ ] Sistema de permisos multi-organización

## 🚀 Durante el Despliegue

### 1. Droplet de Digital Ocean
- [ ] Droplet creado (Ubuntu 22.04 LTS, 2GB RAM mínimo)
- [ ] IP pública anotada
- [ ] SSH configurado y acceso verificado

### 2. Configuración del Servidor
- [ ] Sistema actualizado
- [ ] Python 3.11 instalado
- [ ] PostgreSQL instalado y configurado
- [ ] Nginx instalado
- [ ] Firewall configurado

### 3. Aplicación
- [ ] Repositorio clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Variables de entorno configuradas (archivo .env)
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recolectados

### 4. Servicios
- [ ] Gunicorn configurado y corriendo
- [ ] Nginx configurado y corriendo
- [ ] SSL configurado (certbot)
- [ ] Servicios habilitados para auto-inicio

### 5. Backups
- [ ] Script de backup creado
- [ ] Cron job configurado para backups automáticos
- [ ] Backup inicial realizado

## ✅ Después del Despliegue

### 1. Verificación
- [ ] Aplicación accesible desde el navegador
- [ ] Login funciona correctamente
- [ ] Páginas principales cargan sin errores
- [ ] Archivos estáticos se muestran correctamente
- [ ] Archivos media se suben y visualizan correctamente

### 2. Funcionalidades
- [ ] Crear una ficha familiar de prueba
- [ ] Registrar una persona de prueba
- [ ] Generar un documento de prueba
- [ ] Verificar QR de documento
- [ ] Dashboard muestra estadísticas
- [ ] Sistema multi-organización funciona

### 3. Performance
- [ ] Tiempo de carga de páginas aceptable
- [ ] Generación de documentos funciona sin timeout
- [ ] Dashboard carga rápidamente

### 4. Seguridad
- [ ] HTTPS funcionando (candado verde en navegador)
- [ ] Redirección HTTP → HTTPS activa
- [ ] Headers de seguridad configurados
- [ ] Firewall activo

### 5. Monitoreo
- [ ] Logs de error revisados
- [ ] Monitoreo de uptime configurado (opcional)
- [ ] Alertas configuradas (opcional)

## 📝 Información para los Cabildos

### Datos de Acceso Demo
- **URL**: https://tu-dominio.com
- **Usuario Admin**: (crear para cada cabildo)
- **Documentación**: Incluir manual de usuario

### Capacitación
- [ ] Manual de usuario preparado
- [ ] Video tutorial grabado (opcional)
- [ ] Sesión de capacitación programada
- [ ] Soporte técnico disponible

### Datos de Prueba
- [ ] Organización de ejemplo creada
- [ ] Fichas familiares de ejemplo (5-10)
- [ ] Documentos generados de ejemplo

## 🆘 Contactos de Emergencia

- **Desarrollador**: Tu email/teléfono
- **Soporte Digital Ocean**: https://www.digitalocean.com/support
- **Documentación**: Archivo `GUIA_DESPLIEGUE_DIGITAL_OCEAN.md`

## 📊 Métricas a Monitorear

- Tiempo de respuesta del servidor
- Uso de CPU y memoria
- Espacio en disco
- Número de usuarios activos
- Documentos generados por día
- Errores en logs

---

**Fecha de despliegue**: _______________
**Versión desplegada**: 1.0
**Responsable**: _______________

