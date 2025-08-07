from django.core.cache import cache
from django.db.models import Prefetch

from categories.models import Category, Brand
from .models import SiteSettings


def site_settings(request):
    cached_data = cache.get('site_context_data')
    if not cached_data:
        cached_data = {
            'site_settings':SiteSettings.objects.first(),

            'categories':Category.objects.prefetch_related(
                Prefetch('children', queryset=Category.objects.only('id', 'name', 'slug', 'image'))
            ).only('id', 'name', 'slug', 'image'),

            'brands':Brand.objects.all().only('id', 'name'),
        }
        cache.set('site_context_data', cached_data, 3600) # 1 hour = 3600 seconds
    return cached_data
