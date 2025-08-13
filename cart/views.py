from django.db.models import Prefetch
from django.views import generic
from django.shortcuts import get_object_or_404

from products.models import Product
from .models import Cart, CartItem


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
    def post(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=self.request.session.session_key)

        cart_item, created = CartItem.objects.get_or_create()
