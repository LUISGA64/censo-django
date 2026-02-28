from django.apps import AppConfig


class CensoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'censoapp'
    verbose_name = 'Censo Web'

    def ready(self):
        """Importar señales de seguridad al iniciar la aplicación"""
        try:
            import censoapp.security_signals
        except ImportError:
            pass

