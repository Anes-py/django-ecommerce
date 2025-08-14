from django.views import generic

from core.models import SliderBanners, SideBanners, MiddleBanners, SiteSettings
from core.services.site_cache import get_site_context
from cart.forms import AddToCartForm
from .models import Product, FeatureOption, Comment
from .forms import CommentForm

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


class ProductDetailView(generic.DetailView):
    template_name = 'products/product_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.active().select_related('discount', 'brand').prefetch_related('images', 'specifications', 'feature_options', 'product_comments')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = Product.objects.by_category(category_slug=self.object.category.slug).exclude(id=self.object.id)
        comments = Comment.objects.active().filter(product=self.object).prefetch_related('replies').\
            select_related('user').order_by('-created_at')

        color_qs = (self.object.feature_options
                    .filter(feature=FeatureOption.Feature.Color))
        color_options = [
            {'code': option.color, 'name': option.get_color_display()}
            for option in color_qs
        ]

        size_options = list(
            self.object.feature_options
            .filter(feature=FeatureOption.Feature.Size)
            .values_list('value', flat=True)
        )

        context.update({
            'related_products':related_products,
            'color_options':color_options,
            'size_options':size_options,
            'comments':comments,
            'comment_form':CommentForm,
            'cart_form':AddToCartForm,
        })

        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj.user = self.request.user
        obj.product_id = self.kwargs['product_id']
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
