# 📦 Kit de Implementación para Cliente
## Sistema de Censo - Versión 1.0

Este directorio contiene todos los recursos necesarios para implementar el Sistema de Censo en la infraestructura del cliente.

---

## 📂 Contenido del Kit

### 📄 Documentación

| Archivo | Descripción |
|---------|-------------|
| `GUIA_INSTALACION_CLIENTE.md` | Guía completa de instalación paso a paso |
| `MANUAL_USUARIO.md` | Manual de usuario final con capturas y ejemplos |
| `VARIABLES_MODELOS.md` | Documentación técnica de todos los campos disponibles |
| `CHECKLIST_IMPLEMENTACION.md` | Lista de verificación para la implementación |

### 🔧 Scripts de Instalación

#### Windows
- `scripts/install_windows.ps1` - Script de instalación automática
- `scripts/start_server.ps1` - Iniciar servidor
- `scripts/backup_database.ps1` - Crear respaldo de base de datos
- `scripts/verify_installation.ps1` - Verificar instalación

#### Linux
- `scripts/install_linux.sh` - Script de instalación automática
- `scripts/start_server.sh` - Iniciar servidor (creado durante instalación)
- `scripts/backup_database.sh` - Crear respaldo (creado durante instalación)

---

## 🚀 Inicio Rápido

### Para Windows

1. **Descomprimir** el archivo en `C:\censo-django`
2. **Abrir PowerShell** como Administrador
3. **Navegar** a la carpeta:
   ```powershell
   cd C:\censo-django
   ```
4. **Ejecutar** script de instalación:
   ```powershell
   .\scripts\install_windows.ps1
   ```
5. **Iniciar** el servidor:
   ```powershell
   .\scripts\start_server.ps1
   ```
6. **Abrir navegador** en: http://localhost:8000

### Para Linux

1. **Descomprimir** el archivo en `/opt/censo-django`
2. **Abrir terminal**
3. **Navegar** a la carpeta:
   ```bash
   cd /opt/censo-django
   ```
4. **Dar permisos**:
   ```bash
   chmod +x scripts/install_linux.sh
   ```
5. **Ejecutar** instalación:
   ```bash
   sudo ./scripts/install_linux.sh
   ```
6. **Iniciar** servidor:
   ```bash
   ./scripts/start_server.sh
   ```
7. **Abrir navegador** en: http://localhost:8000

---

## 📋 Requisitos Previos

### Hardware Mínimo
- **CPU:** Intel Core i3 o equivalente (2 núcleos)
- **RAM:** 4 GB (8 GB recomendado)
- **Disco:** 20 GB libres
- **Red:** Tarjeta de red (si se usa en red local)

### Software Necesario
- **SO:** Windows 10/11 o Linux (Ubuntu 20.04+, CentOS 7+)
- **Python:** 3.8 o superior
- **Navegador:** Chrome, Firefox o Edge (última versión)

---

## 📚 Guías de Implementación

### Fase 1: Pre-Instalación (30 min)
1. ✅ Verificar requisitos de hardware
2. ✅ Instalar Python 3.8+
3. ✅ Preparar información del cliente
4. ✅ Revisar CHECKLIST_IMPLEMENTACION.md

### Fase 2: Instalación (1 hora)
1. ✅ Ejecutar script de instalación
2. ✅ Verificar instalación con script verify_installation
3. ✅ Crear usuario administrador
4. ✅ Realizar respaldo inicial

### Fase 3: Configuración (1-2 horas)
1. ✅ Configurar datos de Asociación
2. ✅ Crear Organizaciones (Resguardos)
3. ✅ Registrar Veredas
4. ✅ Configurar Parámetros del Sistema
5. ✅ Crear usuarios operadores

### Fase 4: Capacitación (2-4 horas)
1. ✅ Capacitar administradores
2. ✅ Capacitar operadores
3. ✅ Realizar ejercicios prácticos
4. ✅ Resolver dudas

### Fase 5: Puesta en Producción (1 hora)
1. ✅ Cargar datos iniciales (si existen)
2. ✅ Realizar pruebas finales
3. ✅ Crear respaldo completo
4. ✅ Entregar documentación
5. ✅ Firmar acta de entrega

---

## 🔄 Mantenimiento

### Respaldos Automáticos

**Windows:**
```powershell
.\scripts\backup_database.ps1
```

**Linux:**
```bash
./scripts/backup_database.sh
```

**Frecuencia recomendada:** Diaria o semanal según volumen de datos

### Restaurar Respaldo

```powershell
python manage.py loaddata backups\backup_YYYYMMDD_HHMMSS.json
```

### Actualización del Sistema

1. Detener el servidor
2. Crear respaldo completo
3. Reemplazar archivos del sistema
4. Ejecutar migraciones:
   ```powershell
   python manage.py migrate
   ```
5. Reiniciar servidor

---

## 🆘 Solución de Problemas Comunes

### "Python no reconocido"
**Solución:** Reinstalar Python y marcar "Add to PATH"

### "Port 8000 already in use"
**Windows:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux:**
```bash
sudo lsof -ti:8000 | xargs kill -9
```

### "No module named 'django'"
**Solución:**
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Más problemas
Consultar **GUIA_INSTALACION_CLIENTE.md** sección "Solución de Problemas"

---

## 📞 Soporte Técnico

### Contacto
- **Email:** soporte@censo-indigena.com
- **Teléfono:** +57 XXX XXX XXXX
- **Horario:** Lunes a Viernes, 8:00 AM - 6:00 PM

### Al Reportar Problemas, Incluir:
1. Versión del sistema
2. Sistema operativo
3. Descripción del error
4. Pasos para reproducir
5. Captura de pantalla
6. Log de errores (últimas 50 líneas)

---

## 📊 Características Principales

### ✨ Funcionalidades

- ✅ **Gestión de Fichas Familiares:** Registro completo de familias
- ✅ **Gestión de Personas:** Datos demográficos y socioeconómicos
- ✅ **Datos de Vivienda:** Materiales, servicios públicos, saneamiento
- ✅ **Multi-Organización:** Múltiples resguardos independientes
- ✅ **Generación de Documentos:** Constancias y avales con QR
- ✅ **Reportes y Estadísticas:** Gráficos y exportación a Excel
- ✅ **Junta Directiva:** Gestión de cargos y firmantes
- ✅ **Auditoría:** Historial de cambios
- ✅ **Seguridad:** Control de acceso por roles

### 🔐 Roles de Usuario

| Rol | Permisos |
|-----|----------|
| **Superadmin** | Acceso total a todas las organizaciones |
| **Admin** | Gestión completa de su organización |
| **Operador** | Crear y editar datos de su organización |
| **Consulta** | Solo visualización de datos |

---

## 📖 Documentos de Referencia

### Para el Implementador
1. `GUIA_INSTALACION_CLIENTE.md` - Proceso completo de instalación
2. `CHECKLIST_IMPLEMENTACION.md` - Lista de verificación
3. `VARIABLES_MODELOS.md` - Referencia técnica

### Para el Usuario Final
1. `MANUAL_USUARIO.md` - Guía de uso del sistema

### Para el Administrador
1. Sección "Administración" en `MANUAL_USUARIO.md`
2. `GUIA_INSTALACION_CLIENTE.md` - Sección "Mantenimiento"

---

## 🎯 Casos de Uso

### Caso 1: Organización Pequeña
- 1 resguardo
- 2-3 veredas
- 100-500 familias
- **Infraestructura:** PC estándar, red local opcional

### Caso 2: Organización Mediana
- 1-2 resguardos
- 5-10 veredas
- 500-2000 familias
- **Infraestructura:** Servidor dedicado, red local

### Caso 3: Asociación Grande
- 3+ organizaciones
- 10+ veredas
- 2000+ familias
- **Infraestructura:** Servidor dedicado, red LAN/WAN

---

## 🔒 Seguridad y Privacidad

### Datos Protegidos
- ✅ Información personal (nombres, documentos)
- ✅ Datos de salud (EPS, discapacidades)
- ✅ Datos de ubicación (coordenadas GPS)
- ✅ Documentos generados

### Recomendaciones
- 🔐 Cambiar contraseñas por defecto
- 🔐 Usar contraseñas seguras
- 🔐 No compartir credenciales
- 🔐 Realizar respaldos periódicos
- 🔐 Mantener sistema actualizado

---

## 📝 Notas de Versión

### Versión 1.0 (20 de Diciembre 2024)

**Características:**
- Sistema completo de censo
- Multi-organización
- Generación de documentos con QR
- Exportación a Excel
- Auditoría de cambios
- Panel de estadísticas

**Tecnologías:**
- Django 4.2+
- Python 3.8+
- SQLite (base de datos)
- Bootstrap 5
- Chart.js
- ReportLab (PDF)

---

## 📄 Licencia

Este software es propiedad de [NOMBRE EMPRESA].  
Uso exclusivo para la organización contratante.  
Prohibida su distribución o modificación sin autorización.

---

## ✅ Checklist Rápido

Antes de entregar al cliente, verificar:

- [ ] Scripts de instalación probados
- [ ] Documentación completa entregada
- [ ] Sistema instalado y funcionando
- [ ] Datos iniciales cargados
- [ ] Usuarios creados y capacitados
- [ ] Respaldo inicial creado
- [ ] Acta de entrega firmada
- [ ] Información de soporte entregada

---

**Versión del Kit:** 1.0  
**Fecha de Creación:** 20 de Diciembre de 2024  
**Última Actualización:** 20/12/2024

---

## 🙏 Agradecimientos

Gracias por confiar en el Sistema de Censo para la gestión de su comunidad.

**¡Éxito en la implementación!** 🚀

