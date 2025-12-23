# ✅ CHECKLIST COMPLETO - DESPLIEGUE PYTHONANYWHERE

## 📋 PRE-DESPLIEGUE (En tu PC)

### Verificación del Código
- [x] Base de datos limpia y probada
- [x] Carga masiva funcionando correctamente
- [x] Plantillas de documentos configuradas
- [x] Variables personalizadas creadas
- [x] Dashboard con estadísticas funcional
- [x] Búsqueda global operativa
- [x] Generación de documentos con QR

### Archivos Creados
- [x] `GUIA_DESPLIEGUE_PYTHONANYWHERE.md` - Guía completa
- [x] `DEPLOY_PYTHONANYWHERE_RAPIDO.md` - Pasos esenciales
- [x] `settings_pythonanywhere.py` - Configuración para producción
- [x] `.env.pythonanywhere.example` - Ejemplo de variables
- [x] `crear_datos_demo.py` - Script de datos iniciales
- [x] `requirements.txt` actualizado con mysqlclient

### Git Repository
- [ ] Todo el código committed
- [ ] Push a GitHub/GitLab
- [ ] Branch principal actualizado
- [ ] .gitignore configurado correctamente

**Comando para subir:**
```powershell
cd C:\Users\LENOVO\PycharmProjects\censo-django
git add .
git commit -m "Deploy v1.0 para PythonAnywhere - Demo Cabildos"
git push origin main
```

---

## 🌐 PYTHONANYWHERE - CONFIGURACIÓN

### 1. Cuenta
- [ ] Cuenta creada en pythonanywhere.com
- [ ] Email confirmado
- [ ] Username elegido (anotar): _______________

### 2. Clonar Código
- [ ] Consola Bash abierta
- [ ] Repositorio clonado
- [ ] Código verificado en ~/censo-django

**Comandos:**
```bash
git clone https://github.com/TU_USUARIO/censo-django.git
cd censo-django
ls -la
```

### 3. Entorno Virtual
- [ ] Virtual environment creado
- [ ] Nombre: censo-env
- [ ] Python 3.10 seleccionado
- [ ] Dependencies instaladas

**Comandos:**
```bash
mkvirtualenv censo-env --python=/usr/bin/python3.10
workon censo-env
pip install -r requirements.txt
```

**⚠️ Errores comunes:**
- Si falla WeasyPrint: `pip install --no-deps weasyprint`
- Si falta mysqlclient: Ya viene preinstalado en PythonAnywhere

### 4. Base de Datos MySQL
- [ ] MySQL inicializado
- [ ] Password establecido
- [ ] Credenciales anotadas

**Datos a anotar:**
```
DB_NAME: _______________$censodb
DB_USER: _______________
DB_PASSWORD: _______________
DB_HOST: _______________.mysql.pythonanywhere-services.com
```

### 5. Archivo .env
- [ ] Archivo .env creado en ~/censo-django/
- [ ] Variables de entorno configuradas
- [ ] SECRET_KEY generado
- [ ] Paths ajustados con username correcto

**Verificar con:**
```bash
cat .env
```

### 6. Migraciones
- [ ] Migraciones ejecutadas sin errores
- [ ] Superusuario creado
- [ ] Fixtures de catálogos cargados
- [ ] Archivos estáticos recolectados

**Comandos:**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata censoapp/fixtures/initial_data.json
python manage.py collectstatic --noinput
```

**Superusuario creado:**
```
Username: _______________
Email: _______________
Password: _______________
```

### 7. Datos de Demo
- [ ] Script crear_datos_demo.py ejecutado
- [ ] Asociación de prueba creada
- [ ] Organización de prueba creada
- [ ] Usuarios demo creados

**Comando:**
```bash
python crear_datos_demo.py
```

**Credenciales demo:**
- Admin: admin_cabildo / Demo2024!
- Consulta: consulta_cabildo / Consulta2024!

---

## 🌍 WEB APP - CONFIGURACIÓN

### 8. Crear Web App
- [ ] Web app creada desde dashboard
- [ ] Manual configuration seleccionado
- [ ] Python 3.10 configurado
- [ ] Dominio anotado: _______________.pythonanywhere.com

### 9. Archivo WSGI
- [ ] Archivo WSGI editado
- [ ] Username correcto en todos los paths
- [ ] settings_pythonanywhere configurado
- [ ] Cambios guardados

**Verificar que tenga:**
```python
path = '/home/TU_USERNAME/censo-django'
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'
activate_this = '/home/TU_USERNAME/.virtualenvs/censo-env/bin/activate_this.py'
```

### 10. Virtual Environment
- [ ] Path configurado en sección Virtualenv
- [ ] Path: `/home/TU_USERNAME/.virtualenvs/censo-env`

### 11. Static Files
- [ ] /static/ → /home/TU_USERNAME/censo-django/staticfiles
- [ ] /media/ → /home/TU_USERNAME/censo-django/media
- [ ] Directorios verificados que existen

### 12. Reload
- [ ] Botón "Reload" presionado
- [ ] Web app reiniciada
- [ ] Sin errores en reload

---

## 🧪 VERIFICACIÓN

### 13. Acceso a la Aplicación
- [ ] URL abre correctamente: https://_____.pythonanywhere.com
- [ ] Página de login se muestra
- [ ] CSS y estilos cargan correctamente
- [ ] No hay errores 404 en static files

### 14. Login y Autenticación
- [ ] Login con superusuario funciona
- [ ] Login con admin_cabildo funciona
- [ ] Login con consulta_cabildo funciona
- [ ] Redirect después de login correcto

### 15. Admin Panel
- [ ] /admin accesible
- [ ] Modelos visibles
- [ ] Catálogos presentes
- [ ] Datos demo visibles

### 16. Funcionalidades Principales
- [ ] Dashboard carga correctamente
- [ ] Gráficos se visualizan
- [ ] Estadísticas muestran datos
- [ ] Menú lateral funciona

### 17. Módulos Específicos
- [ ] Fichas familiares - Crear nueva ficha
- [ ] Personas - Listar personas
- [ ] Búsqueda global funciona
- [ ] Carga masiva - Vista accesible
- [ ] Documentos - Listar documentos
- [ ] Plantillas - Administrar plantillas

### 18. Carga Masiva (Prueba Real)
- [ ] Archivo Excel preparado
- [ ] Upload funciona
- [ ] Validación exitosa
- [ ] Preview de datos correcto
- [ ] Importación completa sin errores
- [ ] Log descargable

### 19. Generación de Documentos
- [ ] Seleccionar persona
- [ ] Generar certificado
- [ ] PDF se genera correctamente
- [ ] QR code visible
- [ ] Plantilla personalizada aplicada
- [ ] Download funciona

### 20. Verificación de Documentos
- [ ] URL de verificación funciona
- [ ] QR scaneable
- [ ] Datos correctos en verificación
- [ ] Vista pública accesible

---

## 📊 REVISIÓN DE LOGS

### 21. Logs del Sistema
- [ ] Error log revisado - Sin errores críticos
- [ ] Server log revisado - Requests OK
- [ ] Access log - Tráfico normal

**Ubicación de logs:**
- Dashboard → Web → Log files

**Comandos útiles:**
```bash
# Ver últimas líneas del error log
tail -50 /var/log/TU_USERNAME.pythonanywhere.com.error.log

# Seguir logs en tiempo real
tail -f /var/log/TU_USERNAME.pythonanywhere.com.error.log
```

---

## 🔒 SEGURIDAD

### 22. Configuración de Seguridad
- [ ] DEBUG=False en .env
- [ ] SECRET_KEY único generado
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] HTTPS funcionando (automático en PythonAnywhere)
- [ ] Contraseñas seguras establecidas

---

## 📝 DOCUMENTACIÓN

### 23. Información para Compartir
- [ ] URL de la aplicación documentada
- [ ] Credenciales demo documentadas
- [ ] Manual de usuario preparado (opcional)
- [ ] Video tutorial grabado (opcional)

**Información para Cabildos:**
```
🌐 URL: https://_____.pythonanywhere.com

👤 Usuario Administrador:
   Username: admin_cabildo
   Password: Demo2024!

👁️ Usuario Consulta:
   Username: consulta_cabildo
   Password: Consulta2024!

📧 Contacto Soporte: _______________
```

---

## 🚀 POST-DESPLIEGUE

### 24. Monitoreo Inicial
- [ ] Revisar logs primeras 24 horas
- [ ] Verificar que no haya errores frecuentes
- [ ] Monitorear performance

### 25. Feedback de Cabildos
- [ ] Enviar URL a cabildos
- [ ] Recopilar feedback inicial
- [ ] Documentar problemas reportados
- [ ] Planificar mejoras

### 26. Backup
- [ ] Documentar proceso de backup
- [ ] Exportar datos de prueba
- [ ] Guardar configuración

---

## 🔄 MANTENIMIENTO

### Actualizar Aplicación
```bash
cd ~/censo-django
git pull origin main
workon censo-env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Dashboard → Web → Reload
```

### Backup de Base de Datos
```bash
mysqldump -u TU_USERNAME -h TU_USERNAME.mysql.pythonanywhere-services.com TU_USERNAME$censodb > backup.sql
```

### Restaurar Backup
```bash
mysql -u TU_USERNAME -h TU_USERNAME.mysql.pythonanywhere-services.com TU_USERNAME$censodb < backup.sql
```

---

## ✅ DESPLIEGUE COMPLETADO

**Fecha de despliegue:** _____________  
**Versión:** 1.0  
**URL:** https://_____.pythonanywhere.com  
**Estado:** ✅ OPERATIVO

---

## 📞 CONTACTOS IMPORTANTES

**PythonAnywhere Support:** help@pythonanywhere.com  
**Documentación:** https://help.pythonanywhere.com  
**Forum:** https://www.pythonanywhere.com/forums/

---

**¡Sistema desplegado y listo para demostración a los cabildos! 🎉**

