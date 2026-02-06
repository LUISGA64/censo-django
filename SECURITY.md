# 🔒 GUÍA DE SEGURIDAD - CENSO WEB

**Última actualización:** 2026-02-06  
**Criticidad:** 🔴 ALTA

---

## 🚨 INCIDENTE DE SEGURIDAD - 2026-02-06

### Descripción:
**Credenciales SMTP expuestas en repositorio público**

- **Fecha:** 6 de febrero de 2026, 15:41:31 UTC
- **Detectado por:** GitGuardian
- **Archivo afectado:** `ROADMAP_ACTUALIZADO.md`
- **Tipo de secreto:** Credenciales SMTP (EMAIL_HOST_PASSWORD)
- **Severidad:** 🔴 CRÍTICA

### Acciones Tomadas:
- ✅ Credenciales eliminadas del archivo (commit 48e8955)
- ✅ Push inmediato a GitHub
- ✅ Documentación de seguridad creada
- ⏳ **PENDIENTE:** Revocar contraseña de aplicación actual
- ⏳ **PENDIENTE:** Generar nueva contraseña de aplicación

---

## 🔐 ACCIÓN INMEDIATA REQUERIDA

### 1. Revocar Contraseña de Aplicación Actual

**Pasos en Gmail:**
```
1. Ir a: https://myaccount.google.com/security
2. Click en "Contraseñas de aplicaciones"
3. Buscar la contraseña "webcenso" o similar
4. Click en "Eliminar" o "Revocar"
5. Confirmar revocación
```

### 2. Generar Nueva Contraseña de Aplicación

**Pasos:**
```
1. Gmail > Cuenta de Google > Seguridad
2. Verificación en 2 pasos debe estar activada
3. "Contraseñas de aplicaciones"
4. Seleccionar app: "Otro (nombre personalizado)"
5. Nombre: "Censo Web - Django"
6. Click en "Generar"
7. Copiar la contraseña de 16 caracteres
```

### 3. Actualizar Configuración Local

**Archivo `.env` (LOCAL - NO SUBIR):**
```bash
# Actualizar SOLO en tu máquina local
EMAIL_HOST_PASSWORD=NUEVA_CONTRASEÑA_AQUI
```

### 4. Actualizar Producción (PythonAnywhere)

**Vía Web Interface:**
```
1. Dashboard > Web > Variables de entorno
2. Buscar EMAIL_HOST_PASSWORD
3. Click en "Editar"
4. Pegar nueva contraseña
5. Guardar
6. Reload web app
```

**O vía SSH:**
```bash
ssh usuario@ssh.pythonanywhere.com
cd ~/censo-django
nano .env
# Actualizar EMAIL_HOST_PASSWORD
# Ctrl+X, Y, Enter
touch /var/www/usuario_pythonanywhere_com_wsgi.py
```

---

## 📋 CHECKLIST DE SEGURIDAD

### Inmediato:
- [x] Eliminar credenciales expuestas del código ✅
- [x] Push del fix a GitHub ✅
- [ ] Revocar contraseña de aplicación comprometida ⏳
- [ ] Generar nueva contraseña de aplicación ⏳
- [ ] Actualizar .env local ⏳
- [ ] Actualizar variables en producción ⏳

### Corto Plazo:
- [ ] Implementar git hooks pre-commit
- [ ] Configurar detección de secretos local
- [ ] Revisar todos los commits históricos
- [ ] Auditoría de seguridad completa

### Mediano Plazo:
- [ ] Implementar vault de secretos
- [ ] Configurar GitHub Secrets
- [ ] CI/CD con variables seguras
- [ ] Rotación automática de credenciales

---

## 🛡️ MEJORES PRÁCTICAS DE SEGURIDAD

### 1. Variables de Entorno

**✅ CORRECTO:**
```python
# settings.py
from decouple import config

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
SECRET_KEY = config('SECRET_KEY')
DB_PASSWORD = config('DB_PASSWORD')
```

```bash
# .env (LOCAL - EN .gitignore)
EMAIL_HOST_PASSWORD=contraseña_real_aqui
SECRET_KEY=clave_secreta_aqui
DB_PASSWORD=password_db_aqui
```

**❌ INCORRECTO:**
```python
# settings.py - NUNCA HACER ESTO
EMAIL_HOST_PASSWORD = "hywn djkz scdi xlbi"  # ❌ HARDCODEADO
SECRET_KEY = "django-insecure-12345"          # ❌ EXPUESTO
```

### 2. Archivos .gitignore

**Siempre Ignorar:**
```gitignore
# Secretos y configuración
.env
.env.*
!.env.example

# Credenciales
*.pem
*.key
*.p12
*.pfx
secrets.json
credentials.json

# Base de datos
*.db
*.sqlite3
db.sqlite3

# Logs con información sensible
*.log
logs/

# Backups
backups/*.sql
backups/*.json
*.backup
```

### 3. Archivos de Ejemplo

**✅ .env.example (PUEDE subirse a Git):**
```bash
# Django Core
SECRET_KEY=genera_una_clave_unica_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion

# Database
DB_NAME=nombre_db
DB_USER=usuario_db
DB_PASSWORD=password_db
DB_HOST=localhost
DB_PORT=3306
```

### 4. Detección de Secretos Pre-Commit

**Instalar git-secrets:**
```bash
# Windows (con Git Bash)
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
make install

# Linux/Mac
brew install git-secrets

# Configurar en el proyecto
cd ~/censo-django
git secrets --install
git secrets --register-aws
```

**O usar pre-commit hooks:**
```bash
pip install pre-commit detect-secrets

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### 5. Verificación Manual Antes de Commit

**Comando para buscar secretos:**
```bash
# Buscar passwords
git diff | grep -i "password"

# Buscar keys
git diff | grep -i "key"

# Buscar tokens
git diff | grep -i "token"

# Revisar archivos staged
git diff --staged
```

---

## 🔍 AUDITORÍA DE SEGURIDAD

### Verificar Historial de Git

**Buscar secretos en todo el historial:**
```bash
# Buscar "password" en todo el historial
git log -p -S 'password' --all

# Buscar archivos .env
git log --all --full-history -- .env

# Buscar credenciales
git log -p --all | grep -i "EMAIL_HOST_PASSWORD"
```

### Limpiar Historial (SI ES NECESARIO)

**⚠️ PELIGROSO - Solo si hay secretos en historial:**
```bash
# Backup primero
git clone --mirror https://github.com/LUISGA64/censo-django.git censo-backup

# Usar BFG Repo-Cleaner
java -jar bfg.jar --delete-files .env
java -jar bfg.jar --replace-text passwords.txt

# O git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (PELIGROSO)
git push origin --force --all
git push origin --force --tags
```

**⚠️ ADVERTENCIA:** Limpiar historial afecta a todos los colaboradores.

---

## 🔒 SECRETOS POR AMBIENTE

### Desarrollo Local

**Archivo:** `.env` (NO en Git)
```bash
DEBUG=True
SECRET_KEY=dev-secret-key-not-in-production
EMAIL_HOST_PASSWORD=dev_password
```

### Staging/QA

**Variables de entorno del servidor:**
```bash
export DEBUG=False
export SECRET_KEY=staging-secret-key
export EMAIL_HOST_PASSWORD=staging_password
```

### Producción (PythonAnywhere)

**Dashboard > Web > Variables de entorno:**
```
DEBUG=False
SECRET_KEY=production-super-secret-key
EMAIL_HOST_PASSWORD=production_app_password
DB_PASSWORD=production_db_password
```

---

## 🚨 QUÉ HACER SI SE EXPONE UN SECRETO

### Checklist de Respuesta a Incidentes:

1. **Evaluación Inmediata (5 min)**
   - [ ] ¿Qué se expuso?
   - [ ] ¿Cuándo fue expuesto?
   - [ ] ¿Quién tiene acceso al repositorio?
   - [ ] ¿Es repositorio público o privado?

2. **Contención (15 min)**
   - [ ] Revocar credencial inmediatamente
   - [ ] Eliminar del código
   - [ ] Commit y push del fix
   - [ ] Notificar al equipo

3. **Remediación (1 hora)**
   - [ ] Generar nuevas credenciales
   - [ ] Actualizar en todos los ambientes
   - [ ] Verificar accesos no autorizados
   - [ ] Revisar logs de uso

4. **Prevención (1 día)**
   - [ ] Implementar git hooks
   - [ ] Configurar detección automática
   - [ ] Capacitar al equipo
   - [ ] Documentar el incidente

5. **Post-Mortem (1 semana)**
   - [ ] Análisis de causa raíz
   - [ ] Medidas preventivas
   - [ ] Actualizar procedimientos
   - [ ] Auditoría completa

---

## 🛠️ HERRAMIENTAS DE SEGURIDAD

### Detección de Secretos:

1. **GitGuardian** (Usado actualmente) ✅
   - Monitoreo automático de repositorios
   - Alertas por email
   - Dashboard web
   - https://www.gitguardian.com

2. **git-secrets** (AWS)
   - Pre-commit hooks
   - Previene commits con secretos
   - https://github.com/awslabs/git-secrets

3. **detect-secrets** (Yelp)
   - Scan de repositorio
   - Baseline de secretos
   - https://github.com/Yelp/detect-secrets

4. **gitleaks**
   - Escaneo rápido
   - CI/CD integration
   - https://github.com/gitleaks/gitleaks

5. **truffleHog**
   - Búsqueda de secretos en historial
   - High entropy detection
   - https://github.com/trufflesecurity/trufflehog

### Gestión de Secretos:

1. **HashiCorp Vault**
   - Vault centralizado
   - Rotación automática
   - https://www.vaultproject.io

2. **AWS Secrets Manager**
   - Gestión en la nube
   - Integración con AWS
   - https://aws.amazon.com/secrets-manager

3. **Azure Key Vault**
   - Para Azure deployments
   - Encriptación de secretos
   - https://azure.microsoft.com/services/key-vault

4. **GitHub Secrets**
   - Para GitHub Actions
   - Variables de entorno seguras
   - Settings > Secrets and variables

---

## 📊 MONITOREO DE SEGURIDAD

### Configurar Alertas:

**GitHub:**
```
Settings > Security > Code security and analysis
✅ Dependency graph
✅ Dependabot alerts
✅ Dependabot security updates
✅ Secret scanning (Enterprise)
```

**GitGuardian:**
```
Dashboard > Integrations > GitHub
✅ Enable monitoring
✅ Email notifications
✅ Slack integration (opcional)
```

### Auditoría Regular:

**Semanal:**
- [ ] Revisar alertas de GitGuardian
- [ ] Verificar .gitignore actualizado
- [ ] Scan con gitleaks

**Mensual:**
- [ ] Auditoría de permisos de repositorio
- [ ] Revisar colaboradores
- [ ] Rotar credenciales críticas

**Trimestral:**
- [ ] Auditoría de seguridad completa
- [ ] Penetration testing
- [ ] Actualizar políticas de seguridad

---

## 📝 POLÍTICAS DE SEGURIDAD

### Para Desarrolladores:

1. **NUNCA** hardcodear secretos en el código
2. **SIEMPRE** usar variables de entorno
3. **VERIFICAR** antes de cada commit
4. **REPORTAR** inmediatamente si se expone un secreto
5. **USAR** .env.example para documentar

### Para el Equipo:

1. Capacitación en seguridad obligatoria
2. Revisar código antes de merge
3. Usar pull requests siempre
4. Activar protección de branches
5. Dos factores de autenticación en GitHub

### Para Producción:

1. Variables de entorno SOLO en el servidor
2. Rotación de credenciales cada 90 días
3. Acceso limitado a secretos
4. Logs de auditoría activados
5. Backups encriptados

---

## 🔗 RECURSOS ADICIONALES

### Documentación:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)

### Tutoriales:
- [Managing Secrets in Django](https://djangostars.com/blog/configuring-django-settings-best-practices/)
- [Git Secrets Management](https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/best-practices)

### Herramientas:
- GitGuardian: https://www.gitguardian.com
- git-secrets: https://github.com/awslabs/git-secrets
- gitleaks: https://github.com/gitleaks/gitleaks

---

## ✅ CHECKLIST DE VERIFICACIÓN

### Antes de Cada Commit:
```bash
# 1. Revisar cambios
git diff

# 2. Buscar secretos
git diff | grep -E "(password|secret|key|token)"

# 3. Verificar archivos staged
git status

# 4. Asegurar .env no está incluido
git ls-files | grep .env

# 5. Commit solo si todo está limpio
git commit -m "mensaje"
```

### Antes de Cada Push:
```bash
# 1. Revisar commits locales
git log origin/development..HEAD

# 2. Scan de secretos
gitleaks detect --no-git

# 3. Push
git push origin development
```

---

## 📞 CONTACTO EN CASO DE EMERGENCIA

**Incidente de Seguridad:**
- Email: webcenso@gmail.com
- GitHub Issues: https://github.com/LUISGA64/censo-django/issues
- Crear issue con etiqueta `security` 🔒

**Reportar Vulnerabilidad:**
- GitHub Security: Settings > Security > Security advisories
- Email directo al equipo de desarrollo

---

**Última actualización:** 2026-02-06  
**Próxima revisión:** 2026-03-06  
**Versión:** 1.0  
**Autor:** Equipo Censo Web - Seguridad
