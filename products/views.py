from django.views import generic

from core.models import SliderBanners, SideBanners, MiddleBanners
from categories.models import Category

from .models import Product


class HomeView(generic.TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'slider_banners': SliderBanners.objects.all(),
            'side_banners': SideBanners.objects.all(),
            'middleBanners':MiddleBanners.objects.all(),
            'discounted_products':Product.objects.with_discount(),
            'newest_products':Product.objects.newest(),
            'top_categories':Category.objects.only('image', 'slug', 'parent').prefetch_related("children")\
        .select_related("parent").filter(parent__isnull=True)[:6] # demo

        })
        return context
