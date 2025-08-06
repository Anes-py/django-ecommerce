from django.apps import AppConfig
from django.contrib import admin
from django.utils.text import gettext_lazy as _

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _("core")

    def ready(self):
        admin.site.site_header = _('Store Admin Panel')
        admin.site.site_title = _('Store Admin')
        admin.site.index_title = _('Welcome to the Store Admin Panel')
