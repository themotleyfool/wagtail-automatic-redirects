from django.apps import AppConfig


class WagtailAutomaticRedirectsAppConfig(AppConfig):
    name = 'wagtail_automatic_redirects'

    def ready(self):
        from .signal_handlers import register_signal_handlers
        register_signal_handlers()
