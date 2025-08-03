from django.apps import AppConfig
from django.utils.text import gettext_lazy as _

class CategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categories'
    verbose_name = _("categories")