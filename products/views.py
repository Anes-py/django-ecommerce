from django.views import generic

from .models import Product
from categories.models import Category

class HomeView(generic.TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'discounted_products':Product.objects.with_discount(),
            'newest_products':Product.objects.newest(),
            'top_categories':Category.objects.only('image', 'slug').prefetch_related("children")\
        .select_related("parent").filter(parent__isnull=True)[:6] # demo
        })
        return context