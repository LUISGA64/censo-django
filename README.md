# 🏛️ CensoWeb - Sistema de Gestión de Comunidades

Sistema web integral para la administración de información de comunidades indígenas.

## 📚 Documentación

- 📖 **[MANUAL_MANTENIMIENTO.md](MANUAL_MANTENIMIENTO.md)** - Guía completa de mantenimiento y optimización
- 🗺️ **[docs/ROADMAP_V2.0_ANALISIS_COMPLETO.md](docs/ROADMAP_V2.0_ANALISIS_COMPLETO.md)** - Roadmap y mejoras futuras
- 📋 **[docs/ROADMAP_TRACKER.md](docs/ROADMAP_TRACKER.md)** - Seguimiento de tareas

## 🚀 Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/LUISGA64/censo-django.git
cd censo-django

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 5. Configurar base de datos
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

Abrir navegador: http://127.0.0.1:8000/

## ✨ Características Principales

- 👥 **Gestión de Personas y Familias** - Registro completo de miembros
- 🏠 **Fichas Familiares** - Información detallada por hogar
- 📄 **Generación de Documentos** - Certificados y constancias automáticas
- 🔍 **Búsqueda Global** - Búsqueda rápida con autocompletado
- 📊 **Dashboard Analítico** - Estadísticas y métricas en tiempo real
- 🗺️ **Geolocalización** - Mapas interactivos
- 💾 **Backups Automáticos** - Respaldos programados
- 📥 **Importación Masiva** - Carga de datos en lote
- 🔐 **API REST con JWT** - Integración con otras aplicaciones
- 👥 **Multi-tenancy** - Múltiples organizaciones

## 🛠️ Herramientas de Mantenimiento

```bash
# Análisis completo de base de datos
python scripts/optimize_database.py

# Backup manual
python manage.py dumpdata > backup.json

# Verificar configuración
python manage.py check --deploy

# Limpiar sesiones
python manage.py clearsessions
```

## 📊 Stack Tecnológico

- **Backend:** Django 6.0.1
- **Database:** MySQL (prod) / SQLite (dev)
- **Frontend:** Bootstrap + Gentelella Theme
- **API:** Django REST Framework
- **Auth:** JWT + Django Allauth
- **Maps:** Leaflet.js
- **Cache:** Redis (recomendado)

## 🚀 Deployment

### Desarrollo Local
```bash
python manage.py runserver
```

### Producción (PythonAnywhere)
```bash
cd ~/censo-django
workon censo-env
git pull origin development
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/*_pythonanywhere_com_wsgi.py
```

Ver [MANUAL_MANTENIMIENTO.md](MANUAL_MANTENIMIENTO.md) para más detalles.

## 📖 Documentación Adicional

- 📊 [Roadmap V2.0](docs/ROADMAP_V2.0_ANALISIS_COMPLETO.md)
- ✅ [Version 1.0 Release](docs/VERSION_1.0_RELEASE.md)
- 🎯 [Tracker de Progreso](docs/ROADMAP_TRACKER.md)

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 📝 Licencia

Proyecto propietario - Todos los derechos reservados

## 👤 Contacto

- **Repositorio:** https://github.com/LUISGA64/censo-django
- **Issues:** https://github.com/LUISGA64/censo-django/issues
- **Email:** webcenso@gmail.com

---

**Versión:** 2.0  
**Última actualización:** 2026-02-06  
**Estado:** ✅ En producción
