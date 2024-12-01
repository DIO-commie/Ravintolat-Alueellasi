from django.apps import AppConfig


from django.apps import AppConfig

class RavintolatConfig(AppConfig):
    name = 'ravintolat'

    def ready(self):
        import ravintolat.signals
