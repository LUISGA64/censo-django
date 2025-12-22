# Lista de Verificación de Implementación
# Sistema de Censo - Cliente

## 📋 PRE-INSTALACIÓN

### Información del Cliente

- [ ] **Nombre del Cliente/Organización:** _________________________
- [ ] **Contacto Técnico:** _________________________
- [ ] **Email:** _________________________
- [ ] **Teléfono:** _________________________
- [ ] **Fecha de Implementación:** _________________________

### Requisitos de Hardware

- [ ] Procesador: Intel Core i3 o superior (mínimo 2 núcleos)
- [ ] RAM: 4 GB mínimo, 8 GB recomendado
- [ ] Disco Duro: 20 GB de espacio libre
- [ ] Sistema Operativo: Windows 10/11 o Linux (Ubuntu 20.04+)

### Software Necesario

- [ ] Python 3.8+ instalado
- [ ] pip instalado
- [ ] Navegador web moderno (Chrome, Firefox, Edge)
- [ ] Acceso a internet (para instalación inicial)

---

## 🔧 INSTALACIÓN

### Transferencia de Archivos

- [ ] Sistema descomprimido en la ruta correcta
  - Windows: `C:\censo-django`
  - Linux: `/opt/censo-django`
- [ ] Todos los archivos transferidos correctamente
- [ ] Permisos de lectura/escritura verificados

### Ejecución de Scripts

- [ ] Script de instalación ejecutado sin errores
  - Windows: `scripts\install_windows.ps1`
  - Linux: `scripts/install_linux.sh`
- [ ] Entorno virtual creado correctamente
- [ ] Dependencias instaladas sin conflictos
- [ ] Directorios creados (media, logs, backups)

### Base de Datos

- [ ] Migraciones ejecutadas exitosamente
- [ ] Base de datos SQLite creada
- [ ] Datos iniciales (fixtures) cargados
- [ ] Catálogos verificados (EPS, géneros, etc.)

### Usuario Administrador

- [ ] Superusuario creado
- [ ] Credenciales documentadas de forma segura
- [ ] Primer acceso exitoso
- [ ] Contraseña cambiada del valor por defecto

---

## ⚙️ CONFIGURACIÓN INICIAL

### Asociación

- [ ] Datos de la asociación registrados
  - [ ] Nombre
  - [ ] NIT
  - [ ] Dirección
  - [ ] Teléfonos de contacto
  - [ ] Email
  - [ ] Logo cargado

### Organizaciones (Resguardos)

- [ ] Al menos una organización creada
  - [ ] Nombre del resguardo
  - [ ] NIT
  - [ ] Territorio
  - [ ] Información de contacto
  - [ ] Logo cargado

### Veredas

- [ ] Veredas creadas para cada organización
- [ ] Nombres correctamente registrados
- [ ] Asignadas a la organización correcta

### Parámetros del Sistema

- [ ] Parámetros revisados
- [ ] Configuración de "Datos de Vivienda" definida
- [ ] Otros parámetros ajustados según necesidad

### Usuarios Operadores

- [ ] Usuarios creados según organigrama
- [ ] Roles asignados correctamente
  - [ ] Administradores de organización
  - [ ] Operadores
  - [ ] Usuarios de solo consulta
- [ ] Permisos verificados
- [ ] Usuarios vinculados a organizaciones

---

## ✅ PRUEBAS FUNCIONALES

### Gestión de Fichas Familiares

- [ ] Crear ficha familiar de prueba
- [ ] Editar ficha familiar
- [ ] Visualizar detalle de ficha
- [ ] Listar fichas familiares
- [ ] Filtros funcionando correctamente
- [ ] Exportar a Excel

### Gestión de Personas

- [ ] Crear persona (cabeza de familia)
- [ ] Crear persona (miembro de familia)
- [ ] Editar persona
- [ ] Visualizar detalle de persona
- [ ] Listar personas
- [ ] Filtros funcionando (todos, jefes de familia)
- [ ] Exportar a Excel

### Datos de Vivienda (si aplica)

- [ ] Formulario de vivienda visible
- [ ] Registro de materiales de construcción
- [ ] Guardado correcto de datos
- [ ] Visualización en detalle de ficha

### Junta Directiva

- [ ] Crear cargos de junta directiva
- [ ] Asignar titular y suplente
- [ ] Configurar fechas de vigencia
- [ ] Autorización para firmar documentos

### Generación de Documentos

- [ ] Generar constancia de pertenencia
- [ ] Generar aval
- [ ] Código QR generado correctamente
- [ ] Previsualización de PDF
- [ ] Descarga de PDF
- [ ] Validación de QR desde externa
- [ ] Validación de QR como usuario autenticado

### Estadísticas y Reportes

- [ ] Estadísticas generales visibles
- [ ] Gráficos cargando correctamente
- [ ] Datos filtrados por organización
- [ ] Exportación de datos

### Multi-Organización

- [ ] Filtros por organización funcionando
- [ ] Usuarios ven solo datos de su organización
- [ ] Superadmin ve todas las organizaciones
- [ ] Permisos aplicados correctamente

---

## 🔒 SEGURIDAD

### Configuraciones de Seguridad

- [ ] DEBUG=False en producción (.env)
- [ ] SECRET_KEY única generada
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] Contraseñas seguras establecidas
- [ ] Permisos de archivos verificados

### Respaldos

- [ ] Script de respaldo probado
- [ ] Primer respaldo creado
- [ ] Ubicación de respaldos documentada
- [ ] Procedimiento de restauración probado

---

## 📚 CAPACITACIÓN

### Usuarios Administradores

- [ ] Gestión de organizaciones
- [ ] Creación de usuarios
- [ ] Asignación de permisos
- [ ] Configuración de parámetros
- [ ] Generación de respaldos
- [ ] Exportación de datos

### Usuarios Operadores

- [ ] Creación de fichas familiares
- [ ] Registro de personas
- [ ] Edición de datos
- [ ] Generación de documentos
- [ ] Uso de filtros y búsquedas

### Usuarios de Consulta

- [ ] Navegación del sistema
- [ ] Consulta de información
- [ ] Uso de filtros
- [ ] Visualización de reportes

---

## 📝 DOCUMENTACIÓN ENTREGADA

- [ ] Guía de Instalación para Cliente
- [ ] Manual de Usuario
- [ ] Documentación de Variables de Modelos
- [ ] Scripts de instalación y mantenimiento
- [ ] Información de contacto de soporte

---

## 🚀 PUESTA EN PRODUCCIÓN

### Verificación Final

- [ ] Todas las pruebas funcionales exitosas
- [ ] Datos de prueba eliminados
- [ ] Datos reales iniciales cargados
- [ ] Respaldo inicial creado
- [ ] Sistema accesible desde red local (si aplica)
- [ ] Rendimiento verificado

### Entrega al Cliente

- [ ] Cliente capacitado
- [ ] Credenciales entregadas de forma segura
- [ ] Documentación entregada
- [ ] Contactos de soporte proporcionados
- [ ] Acta de entrega firmada

---

## 📞 SOPORTE POST-IMPLEMENTACIÓN

### Seguimiento

- [ ] **Día 1:** Verificación de operación normal
- [ ] **Semana 1:** Revisión de uso y resolución de dudas
- [ ] **Mes 1:** Evaluación de satisfacción
- [ ] **Mes 3:** Revisión general del sistema

### Información de Contacto

**Soporte Técnico:**
- Email: _________________________
- Teléfono: _________________________
- Horario: _________________________

---

## 📊 MÉTRICAS DE IMPLEMENTACIÓN

| Métrica | Objetivo | Real | Estado |
|---------|----------|------|--------|
| Tiempo de instalación | < 1 hora | _____ | ☐ |
| Usuarios creados | _____ | _____ | ☐ |
| Fichas cargadas (inicial) | _____ | _____ | ☐ |
| Personas registradas (inicial) | _____ | _____ | ☐ |
| Documentos generados (prueba) | 2+ | _____ | ☐ |
| Usuarios capacitados | _____ | _____ | ☐ |

---

## ✍️ FIRMAS

**Implementador:**
- Nombre: _________________________
- Firma: _________________________
- Fecha: _________________________

**Cliente (Representante Autorizado):**
- Nombre: _________________________
- Cargo: _________________________
- Firma: _________________________
- Fecha: _________________________

---

## 📌 NOTAS ADICIONALES

_Espacio para observaciones, configuraciones especiales o requisitos particulares del cliente:_

_______________________________________________
_______________________________________________
_______________________________________________
_______________________________________________
_______________________________________________

---

**Versión del Checklist:** 1.0  
**Fecha:** 20 de Diciembre de 2024

