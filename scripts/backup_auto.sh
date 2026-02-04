#!/bin/bash
exit 0

# rclone copy "$BACKUP_FILE" gdrive:CensoBackups/
# BACKUP_FILE=$(ls -t "$PROYECTO_DIR/backups/censo_db_*.gz" | head -1)
# Opcional: Subir backup a la nube (descomentar si usas rclone)

find "$PROYECTO_DIR/logs" -name "backup_*.log" -mtime +90 -delete
# Mantener solo últimos 90 días de logs

echo "" >> "$LOG_FILE"
echo "=== Backup finalizado: $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
# Timestamp final

fi
    echo "✗ Error en backup"
    echo "✗ Error en backup (Exit code: $?)" >> "$LOG_FILE"
else
    echo "✓ Backup completado exitosamente"
    echo "✓ Backup completado exitosamente" >> "$LOG_FILE"
if [ $? -eq 0 ]; then

$VENV_PYTHON manage.py backup_db --compress --keep-days 30 >> "$LOG_FILE" 2>&1
echo "Ejecutando backup de base de datos..."
# Ejecutar backup con compresión

source censo-env/bin/activate
# Activar entorno virtual

cd "$PROYECTO_DIR" || exit 1
# Cambiar al directorio del proyecto

echo "=== Backup iniciado: $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
# Timestamp

mkdir -p "$PROYECTO_DIR/logs"
# Crear directorio de logs si no existe

LOG_FILE="$PROYECTO_DIR/logs/backup.log"
VENV_PYTHON="$PROYECTO_DIR/censo-env/bin/python"
PROYECTO_DIR="/home/tuusuario/censo-django"
# Configuración

# Agregar a crontab: 0 2 * * * /home/tuusuario/censo-django/scripts/backup_auto.sh
# Script de Backup Automático para Linux/PythonAnywhere
