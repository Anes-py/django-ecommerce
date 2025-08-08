from django.views import generic

from core.models import SliderBanners, SideBanners, MiddleBanners, SiteSettings
from core.services.site_cache import get_site_context
from categories.models import Category

from .models import Product


class HomeView(generic.TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_context = get_site_context(self.request)
        context.update({
            'discounted_products':Product.objects.with_discount(),
            'newest_products':Product.objects.newest(),
            'top_categories':site_context['categories'].filter(parent__isnull=True)[:6]
        })
        if SiteSettings.objects.all().first():
            context.update({
            'slider_banners': SliderBanners.objects.all(),
            'side_banners': SideBanners.objects.all(),
            'middleBanners':MiddleBanners.objects.all(),
            })
        return context


