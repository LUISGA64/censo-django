"""
Comando para crear backup mejorado de la base de datos con soporte para SQLite, MySQL y PostgreSQL
Uso: python manage.py backup_db [opciones]
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime, timedelta
import subprocess
import os
import shutil
import glob
import gzip
import json

class Command(BaseCommand):
    help = 'Crea un backup mejorado de la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Comprimir el backup con gzip',
        )
        parser.add_argument(
            '--keep-days',
            type=int,
            default=30,
            help='Días de retención de backups antiguos (default: 30)',
        )
        parser.add_argument(
            '--notify',
            action='store_true',
            help='Enviar notificación por email si hay error',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔄 Iniciando proceso de backup avanzado...'))

        # Crear directorio de backups si no existe
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        # Timestamp para el archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Información del backup
        backup_info = {
            'timestamp': timestamp,
            'date': datetime.now().isoformat(),
            'database': settings.DATABASES['default']['ENGINE'],
            'success': False,
            'files': []
        }

        try:
            # Backup de la base de datos
            db_backup = self._backup_database(backup_dir, timestamp, options['compress'])
            if db_backup:
                backup_info['files'].append({'type': 'database', 'path': db_backup})
                backup_info['success'] = True

            # Limpiar backups antiguos
            deleted = self._cleanup_old_backups(backup_dir, options['keep_days'])
            backup_info['deleted_old_backups'] = deleted

            # Guardar información del backup
            info_file = os.path.join(backup_dir, f'backup_info_{timestamp}.json')
            with open(info_file, 'w') as f:
                json.dump(backup_info, f, indent=2)

            # Resumen
            self.stdout.write(self.style.SUCCESS('\n✅ Backup completado exitosamente!'))
            self.stdout.write(f'  📁 Base de datos: {db_backup}')
            self.stdout.write(f'  📊 Directorio: {backup_dir}')
            self.stdout.write(f'  🗑️  Backups antiguos eliminados: {deleted}')

        except Exception as e:
            backup_info['error'] = str(e)
            self.stdout.write(self.style.ERROR(f'\n❌ Error en backup: {str(e)}'))

            # Enviar notificación si está habilitado
            if options['notify']:
                self._send_error_notification(e)

    def _backup_database(self, backup_dir, timestamp, compress):
        """Crea backup de la base de datos según el motor"""
        db_config = settings.DATABASES['default']
        engine = db_config['ENGINE']

        if 'sqlite' in engine:
            return self._backup_sqlite(backup_dir, timestamp, compress)
        elif 'mysql' in engine:
            return self._backup_mysql(backup_dir, timestamp, compress)
        elif 'postgresql' in engine:
            return self._backup_postgresql(backup_dir, timestamp, compress)
        else:
            self.stdout.write(self.style.ERROR(f'❌ Motor de BD no soportado: {engine}'))
            return None

    def _backup_sqlite(self, backup_dir, timestamp, compress):
        """Backup de SQLite"""
        self.stdout.write('📦 Creando backup de SQLite...')

        db_path = settings.DATABASES['default']['NAME']
        backup_file = os.path.join(backup_dir, f'censo_db_{timestamp}.sqlite')

        try:
            # Copiar archivo de base de datos
            shutil.copy2(str(db_path), backup_file)

            # Comprimir si se solicita
            if compress:
                compressed_file = f'{backup_file}.gz'
                with open(backup_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(backup_file)
                backup_file = compressed_file

            file_size = os.path.getsize(backup_file) / (1024 * 1024)  # MB
            self.stdout.write(self.style.SUCCESS(f'  ✓ Backup SQLite creado ({file_size:.2f} MB)'))

            return backup_file
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Error: {str(e)}'))
            raise

    def _backup_mysql(self, backup_dir, timestamp, compress):
        """Backup de MySQL"""
        self.stdout.write('📦 Creando backup de MySQL...')

        db_config = settings.DATABASES['default']
        backup_file = os.path.join(backup_dir, f'censo_db_{timestamp}.sql')

        # Comando mysqldump
        cmd = [
            'mysqldump',
            '-u', db_config['USER'],
            f"-p{db_config['PASSWORD']}",
            '-h', db_config.get('HOST', 'localhost'),
            '--single-transaction',
            '--quick',
            '--lock-tables=false',
            db_config['NAME']
        ]

        try:
            with open(backup_file, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True, stderr=subprocess.PIPE)

            # Comprimir
            if compress:
                compressed_file = f'{backup_file}.gz'
                with open(backup_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(backup_file)
                backup_file = compressed_file

            file_size = os.path.getsize(backup_file) / (1024 * 1024)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Backup MySQL creado ({file_size:.2f} MB)'))

            return backup_file

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Error: {str(e)}'))
            raise

    def _backup_postgresql(self, backup_dir, timestamp, compress):
        """Backup de PostgreSQL"""
        self.stdout.write('📦 Creando backup de PostgreSQL...')

        db_config = settings.DATABASES['default']
        backup_file = os.path.join(backup_dir, f'censo_db_{timestamp}.dump')

        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['PASSWORD']

        cmd = [
            'pg_dump',
            '-U', db_config['USER'],
            '-h', db_config.get('HOST', 'localhost'),
            '-F', 'c',
            '-f', backup_file,
            db_config['NAME']
        ]

        try:
            subprocess.run(cmd, env=env, check=True, stderr=subprocess.PIPE)

            file_size = os.path.getsize(backup_file) / (1024 * 1024)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Backup PostgreSQL creado ({file_size:.2f} MB)'))

            return backup_file

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Error: {str(e)}'))
            raise

    def _cleanup_old_backups(self, backup_dir, keep_days):
        """Elimina backups más antiguos que keep_days"""
        self.stdout.write(f'\n🗑️  Limpiando backups antiguos (manteniendo últimos {keep_days} días)...')

        cutoff = datetime.now() - timedelta(days=keep_days)
        deleted_count = 0

        patterns = ['censo_db_*.sqlite*', 'censo_db_*.sql*', 'censo_db_*.dump*']

        for pattern in patterns:
            for backup in glob.glob(os.path.join(backup_dir, pattern)):
                file_time = datetime.fromtimestamp(os.path.getmtime(backup))
                if file_time < cutoff:
                    try:
                        os.remove(backup)
                        deleted_count += 1
                        self.stdout.write(f'  🗑️  Eliminado: {os.path.basename(backup)}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  ❌ Error al eliminar {backup}: {e}'))

        if deleted_count == 0:
            self.stdout.write('  ℹ️  No hay backups antiguos para eliminar')
        else:
            self.stdout.write(self.style.SUCCESS(f'  ✓ {deleted_count} backup(s) eliminado(s)'))

        return deleted_count

    def _send_error_notification(self, error):
        """Envía notificación por email en caso de error"""
        try:
            from django.core.mail import send_mail

            subject = '❌ Error en Backup Automático - CensoWeb'
            message = f'''
            El proceso de backup automático ha fallado.
            
            Error: {str(error)}
            Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            Por favor, revisar el sistema de backups.
            '''

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMINS[0][1]] if settings.ADMINS else [],
                fail_silently=True,
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ⚠️  No se pudo enviar notificación: {e}'))
