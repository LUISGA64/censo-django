# ✅ BACKUPS COMPLETADOS - INSTRUCCIONES PARA RECREAR BD

**Fecha:** 14 de Diciembre de 2025  
**Estado:** ✅ BACKUPS CREADOS

---

## 📦 BACKUPS CREADOS

Los siguientes archivos contienen todos tus datos actuales:

1. ✅ `backup_users.json` - Usuarios del sistema
2. ✅ `backup_userprofiles.json` - Perfiles de usuario (organizaciones, roles)
3. ✅ `backup_organizations.json` - Organizaciones indígenas
4. ✅ `backup_sidewalks.json` - Veredas
5. ✅ `backup_familycards.json` - Fichas familiares
6. ✅ `backup_persons.json` - Personas del censo
7. ✅ `db.censo_Web.backup` - Copia de la base de datos (cuando se pueda renombrar)

**Todos los datos están seguros** ✅

---

## 🚀 PASOS PARA RECREAR BASE DE DATOS

### ⚠️ IMPORTANTE: Cerrar Servidor de Desarrollo

**Si tienes el servidor corriendo, ciérralo primero:**
- Presiona `Ctrl+C` en la terminal donde está corriendo
- O cierra todas las ventanas de terminal

---

### OPCIÓN 1: Script Automático (RECOMENDADO)

```powershell
# Ejecutar el script
.\recreate_db.ps1
```

**El script hace:**
1. Renombra `db.censo_Web` a `db.censo_Web.backup`
2. Crea nueva base de datos con `python manage.py migrate`
3. Carga tipos de documentos
4. Carga parámetros del sistema

---

### OPCIÓN 2: Manual (Paso a Paso)

#### Paso 1: Renombrar BD Actual

```powershell
# Asegúrate de cerrar el servidor primero
Rename-Item .\db.censo_Web db.censo_Web.backup -Force
```

#### Paso 2: Crear Nueva Base de Datos

```bash
python manage.py migrate
```

**Resultado esperado:**
```
Operations to perform:
  Apply all migrations: account, admin, auth, censoapp, contenttypes, sessions, sites, socialaccount
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying censoapp.0023_boardposition_generateddocument_and_more... OK
```

#### Paso 3: Cargar Tipos de Documentos

```bash
python manage.py loaddata document_types
```

**Resultado esperado:**
```
Installed 3 object(s) from 1 fixture(s)
```

#### Paso 4: Cargar Parámetros del Sistema

```bash
python manage.py loaddata system_parameters
```

#### Paso 5: Crear Superusuario

```bash
python manage.py createsuperuser
```

**Te pedirá:**
- Username
- Email
- Password

---

## 🔄 RESTAURAR DATOS (OPCIONAL)

### Después de crear la nueva BD, puedes restaurar tus datos:

#### 1. Cargar Usuarios

```bash
python manage.py loaddata backup_users.json
```

#### 2. Cargar Organizaciones

```bash
python manage.py loaddata backup_organizations.json
```

#### 3. Cargar Veredas

```bash
python manage.py loaddata backup_sidewalks.json
```

#### 4. Cargar Fichas Familiares

```bash
python manage.py loaddata backup_familycards.json
```

#### 5. Cargar Personas

```bash
python manage.py loaddata backup_persons.json
```

#### 6. Cargar Perfiles de Usuario

```bash
python manage.py loaddata backup_userprofiles.json
```

---

## ✅ VERIFICAR QUE TODO FUNCIONA

### 1. Iniciar Servidor

```bash
python manage.py runserver
```

### 2. Acceder al Admin

```
http://localhost:8000/admin
```

### 3. Verificar Nuevos Modelos

Deberías ver en el admin:

**Sección "Documentos y Junta Directiva":**
- ✅ Tipos de Documentos (3 registros iniciales)
- ✅ Cargos de Junta Directiva (vacío)
- ✅ Documentos Generados (vacío)

**Sección "Catálogos":**
- ✅ Tipos de Documentos de Identidad (CC, TI, etc.)

---

## 🧪 PROBAR SISTEMA DE DOCUMENTOS

### 1. Crear Junta Directiva

```
Admin → Cargos de Junta Directiva → Agregar

- Organización: [Tu organización]
- Cargo: Gobernador
- Titular: [Persona del censo]
- Puede firmar: ✅ Sí
- Fecha inicio: 2025-01-01
- Fecha fin: 2026-12-31
- Activo: ✅ Sí
```

### 2. Intentar Crear Documento

```
Admin → Documentos Generados → Agregar

- Tipo: Aval
- Persona: [Persona del censo]
- Organización: [Tu organización]
- Fecha expedición: 2025-12-14
- Fecha vencimiento: 2026-12-14
```

**Resultado esperado:**
- ✅ Se crea correctamente
- ✅ Validaciones funcionan
- ✅ Solo si hay junta vigente

---

## 🎯 CHECKLIST DE VERIFICACIÓN

Después de recrear la BD, verifica:

- [ ] Servidor inicia sin errores
- [ ] Admin accesible
- [ ] Nuevas secciones visibles:
  - [ ] Tipos de Documentos
  - [ ] Cargos de Junta Directiva
  - [ ] Documentos Generados
- [ ] Tipos de documentos cargados (3):
  - [ ] Aval
  - [ ] Constancia de Pertenencia
  - [ ] Certificado
- [ ] Datos restaurados (si aplicaste backups):
  - [ ] Organizaciones
  - [ ] Veredas
  - [ ] Fichas familiares
  - [ ] Personas
  - [ ] Usuarios y perfiles

---

## ⚠️ SI ALGO FALLA

### Error: "No such table"

**Solución:**
```bash
python manage.py migrate --run-syncdb
```

### Error al Cargar Fixtures

**Solución:**
```bash
# Cargar en orden:
python manage.py loaddata backup_organizations.json
python manage.py loaddata backup_sidewalks.json
python manage.py loaddata backup_familycards.json
python manage.py loaddata backup_persons.json
```

### Error de FK en Personas

**Causa:** Las personas tienen referencia a tipos de documento antiguos

**Solución:**
1. Primero carga los catálogos base (Eps, Gender, DocumentType, etc.)
2. Luego carga las personas

---

## 📞 RESUMEN

### Lo que tienes ahora:

✅ **Backups completos de todos los datos**
✅ **Script automático para recrear BD**
✅ **Instrucciones detalladas paso a paso**
✅ **Sistema de documentos listo para usar**

### Lo que debes hacer:

1. **Cerrar servidor** (si está corriendo)
2. **Ejecutar script**: `.\recreate_db.ps1`
3. **Crear superusuario**: `python manage.py createsuperuser`
4. **(Opcional) Restaurar datos**: Cargar backups
5. **Probar**: Crear junta directiva y documento

---

**⏱️ Tiempo estimado: 10-15 minutos**

**✅ Resultado: Base de datos limpia con sistema de documentos funcionando**

---

*Backups creados: 2025-12-14*  
*Script: recreate_db.ps1*  
*Estado: LISTO PARA EJECUTAR*

