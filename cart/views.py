from django.db.models import Prefetch
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import gettext_lazy as gt
from django.shortcuts import get_object_or_404, redirect, reverse


from products.models import Product
from orders.models import Address
from orders.forms import OrderForm, AddressForm
from .models import Cart, CartItem
from .forms import AddToCartForm


class CartDetailView(LoginRequiredMixin, generic.DetailView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_addresses': Address.objects.filter(user=self.request.user).order_by('-created_at'),
            'order_form': OrderForm(),
            'address_form': AddressForm(),
        })
        return context


class AddToCartView(generic.View):

    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        if not form.is_valid():
            return redirect('product-detail', slug=product.slug)
        quantity = form.cleaned_data['quantity']
        color = form.cleaned_data['color']
        size = form.cleaned_data['size']

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
        cart_item.save()
        messages.success(request, gt("Product successfully added to the cart ✅"))
        request.session['old_session_key'] = request.session.session_key
        return redirect('product-detail', slug=product.slug)


class CartItemRemove(generic.View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart = get_object_or_404(Cart, session_key=request.session.session_key)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return redirect('cart-detail')


class CartDelete(generic.View):
    def post(self, request):
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart = get_object_or_404(Cart, session_key=request.session.session_key)
        cart.delete()
        messages.success(request, 'ایتم های سبد شما با موفقیت حدف شد✅ ')
        return redirect('cart-detail')


class CartUpdateView(generic.View):
    def post(self, request, *args, **kwargs):
        # گرفتن cart
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart = get_object_or_404(Cart, session_key=request.session.session_key)

        updated = 0
        deleted = 0

        for item in cart.items.all():
            qty = request.POST.get(f"quantity_{item.id}")
            if qty is None:
                continue
            try:
                qty = int(qty)
                if qty <= 0:
                    item.delete()
                    deleted += 1
                else:
                    item.quantity = qty
                    item.save(update_fields=["quantity"])
                    updated += 1
            except (ValueError, TypeError):
                continue

        if updated or deleted:
            messages.success(request, "Cart has been updated ✅")
        else:
            messages.info(request, "No changes were made to the cart.✅")

        return redirect('cart-detail')
