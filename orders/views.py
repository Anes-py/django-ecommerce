from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from cart.models import Cart
from orders.models import Order, Address, OrderItem
from .forms import OrderForm, AddressForm


class OrderCreateView(generic.CreateView):
    template_name = 'orders/order_create.html'
    model = Order
    form_class = OrderForm


    def form_valid(self, form):
        cart = get_object_or_404(Cart, user=self.request.user)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.subtotal = cart.cart_org_total()
        obj.discount_total = cart.cart_discount()
        obj.shipping_total = 28000
        obj.tax_total = int(obj.subtotal * 0.12)
        obj.grand_total = int(cart.cart_final_price() + obj.tax_total)
        obj.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=obj,
                user=self.request.user,
                product=item.product,
                quantity=item.quantity,
                total_discount=item.item_discount(),
                final_price=item.item_final_price(),
            )
        cart.items.all().delete()
        messages.success(self.request, "!فاکتور شما آماده پرداخت است")
        return redirect('checkout-cart')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_addresses':Address.objects.filter(user=self.request.user),
            'order_form':OrderForm(),
            'address_form':AddressForm(),
        })
        return context

