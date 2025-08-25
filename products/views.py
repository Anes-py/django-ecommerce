from django.db.models import Q
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect

from core.models import SliderBanners, SideBanners, MiddleBanners, SiteSettings
from core.services.site_cache import get_site_context
from categories.models import Category
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


class ProductListView(generic.ListView):
    template_name = 'products/product_list.html'
    paginate_by = 10

    def get_queryset(self):
        sort_query_map = {
            'newest': lambda: Product.objects.newest(),
            'best-sell': lambda: Product.objects.active(),
            'most-expensive': lambda: Product.objects.most_expensive(),
            'cheapest': lambda: Product.objects.cheapest(),
            'discounted': lambda: Product.objects.with_discount(),
        }
        queryset = Product.objects.active()
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        category_slug = self.request.GET.get('category_slug')
        brand_slug = self.request.GET.get('brand_slug')
        available = self.request.GET.get('available')
        special = self.request.GET.get('special')

        sort_query = self.request.GET.get('sort_query')
        search_query = self.request.GET.get('q')

        if sort_query in sort_query_map:
            queryset = sort_query_map[sort_query]()
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        if available:
            queryset = queryset.filter(status=Product.ProductStatus.AVAILABLE)
        if special:
            now = timezone.now()
            queryset = queryset.filter(
            Q(discount__start_date__lte=now) | Q(discount__start_date__isnull=True),
            Q(discount__expire_date__gte=now) | Q(discount__expire_date__isnull=True),
            discount__is_active=True,
        ).select_related('discount').order_by('-discount__value')

        if search_query:
            queryset = queryset.filter(
                Q(brand__name__icontains=search_query)|
                Q(name__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(description__icontains=search_query)
            )



        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
            'parent_categories': Category.objects.filter(parent__isnull=True).select_related('parent').prefetch_related('children'),
            'search_form':True,
        })
        return context


class ProductDetailView(generic.DetailView):
    template_name = 'products/product_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (Product.objects.active().select_related('discount', 'brand')
                .prefetch_related('images', 'specifications', 'feature_options', 'product_comments'))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = Product.objects.by_category(category_slug=self.object.category.slug).exclude(id=self.object.id)
        comments = Comment.objects.active().filter(product=self.object, parent__isnull=True).prefetch_related('replies').\
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
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            obj.parent_id = parent_id
            messages.success(self.request, 'پاسخ شما ارسال شد و پس از تایید ادمین منتشر میشود')
        obj.save()

        messages.success(self.request, 'کامنت شما ارسال شد و پس از تایید ادمین منتشر میشود')
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
