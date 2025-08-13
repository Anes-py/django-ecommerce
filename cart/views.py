from django.db.models import Prefetch
from django.views import generic
from django.shortcuts import get_object_or_404, redirect

from products.models import Product
from .models import Cart, CartItem
from .forms import AddToCartForm


class CartDetailView(generic.DetailView):
    template_name = 'cart/cart_detail.html'
    context_object_name = 'cart'
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.select_related('user').prefetch_related(
                Prefetch('items', queryset=CartItem.objects.select_related('product', 'product__discount'))
            ).get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            session_key = self.request.session.session_key
            cart, _ = Cart.objects.prefetch_related(
                Prefetch('items', queryset=CartItem.objects.select_related('product', 'product__discount'))
            ).get_or_create(session_key=session_key)
        return cart


class AddToCartView(generic.View):

    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        if not form.is_valid():
            return redirect(request.META.get('HTTP_REFERER', '/'))
        quantity = form.cleaned_data['quantity']
        color = form.cleaned_data['color']
        size = form.cleaned_data['size']

        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
