from django.apps import AppConfig
from django.db.models.signals import post_save


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        from . import signals
        # Явно подключаем обработчик сигнала.
        post_save.connect(signals.distribute_users_to_groups, sender=self)
