from django.apps import AppConfig


class FeesConfig(AppConfig):
    name = 'fees'

    def ready(self):
        from helpers import scheduler
        scheduler.start()
