from django.apps import AppConfig


class ElectroSocialConfig(AppConfig):
    name = 'electro_social'
    def ready(self):
        import electro_social.signals
