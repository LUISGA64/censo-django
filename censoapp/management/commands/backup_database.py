"""
Comando de management para crear backups automáticos de la base de datos.

Uso:
    python manage.py backup_database
    python manage.py backup_database --output=/ruta/backup.json
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Crea un backup completo de la base de datos en formato JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Ruta del archivo de salida (opcional)',
        )

    def handle(self, *args, **options):
        # Crear directorio de backups si no existe
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            self.stdout.write(
                self.style.SUCCESS(f'Directorio {backup_dir}/ creado')
            )

        # Determinar nombre del archivo
        if options['output']:
            filepath = options['output']
        else:
            filename = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            filepath = os.path.join(backup_dir, filename)

        # Crear backup
        self.stdout.write('Creando backup de la base de datos...')

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                call_command(
                    'dumpdata',
                    '--exclude', 'contenttypes',
                    '--exclude', 'auth.permission',
                    '--exclude', 'sessions',
                    '--indent', '2',
                    stdout=f
                )

            # Obtener tamaño del archivo
            size_bytes = os.path.getsize(filepath)
            size_mb = size_bytes / (1024 * 1024)

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Backup creado exitosamente:'
                    f'\n  Archivo: {filepath}'
                    f'\n  Tamaño: {size_mb:.2f} MB'
                    f'\n  Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                )
            )

            # Listar backups existentes
            if os.path.exists(backup_dir):
                backups = [f for f in os.listdir(backup_dir) if f.endswith('.json')]
                if backups:
                    self.stdout.write(
                        f'\nBackups disponibles en {backup_dir}/: {len(backups)} archivo(s)'
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error al crear backup: {str(e)}')
            )
            raise

