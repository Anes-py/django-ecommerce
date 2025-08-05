from django.apps import AppConfig
from django.utils.text import gettext_lazy as _

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _("core")
