#!/bin/bash

# ============================================================================
# Script de Backup - Censo Indígena
# ============================================================================
# Crea backups de la base de datos y archivos media
# ============================================================================

BACKUP_DIR="/var/backups/censo"
APP_DIR="/var/www/censo-django"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="censo_db"

# Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

echo "🗄️  Creando backup de la base de datos..."
sudo -u postgres pg_dump $DB_NAME > $BACKUP_DIR/db_$DATE.sql
gzip $BACKUP_DIR/db_$DATE.sql

echo "📁 Creando backup de archivos media..."
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $APP_DIR media/

echo "📊 Tamaño de los backups:"
du -h $BACKUP_DIR/db_$DATE.sql.gz
du -h $BACKUP_DIR/media_$DATE.tar.gz

# Eliminar backups antiguos (más de 30 días)
echo "🧹 Eliminando backups antiguos (más de 30 días)..."
find $BACKUP_DIR -type f -mtime +30 -delete

echo "✅ Backup completado: $DATE"
echo "📍 Ubicación: $BACKUP_DIR"

