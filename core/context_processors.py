from .services.site_cache import get_site_context


def site_settings(request):
    return get_site_context(request)