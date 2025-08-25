from django.core.cache import cache

from categories.models import Category, Brand
from ..models import SiteSettings


def get_site_context(request):
    cached_data = cache.get('site_context_data')
    if not cached_data:
        cached_data = {
            'site_settings':SiteSettings.objects.first(),

            'categories': Category.objects.all().select_related('parent').prefetch_related('children').filter(parent__isnull=True),
            'brands':Brand.objects.all().only('id', 'name', 'slug'),
        }
        cache.set('site_context_data', cached_data, 3600) # 1 hour = 3600 seconds
    return cached_data
