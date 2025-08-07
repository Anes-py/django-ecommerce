from django.db.models import Prefetch
from django.conf import settings

from categories.models import Category, Brand
from .models import SiteSettings


def site_settings(request):
    queryset = SiteSettings.objects.first()
    return {
        'site_settings': queryset,
        'categories': Category.objects.prefetch_related(
            Prefetch(
                "children",
                Category.objects.prefetch_related("children")
            )
        ).filter(parent__isnull=True),
        'brands' : Brand.objects.all(),
    }
