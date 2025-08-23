from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from decimal import Decimal

from cart.models import Cart
from orders.models import Order, OrderItem
from .forms import OrderForm


class OrderCreateView(generic.CreateView):
    model = Order
    form_class = OrderForm
    context_object_name = 'order'

    def form_valid(self, form):
        cart = get_object_or_404(Cart, user=self.request.user)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.subtotal = cart.cart_org_total()
        obj.discount_total = cart.cart_discount()
        obj.shipping_total = 28000
        obj.tax_total = int(Decimal(obj.subtotal - obj.discount_total) * Decimal(0.12))
        obj.grand_total = cart.cart_final_price() + obj.shipping_total + obj.tax_total
        obj.status = Order.OrderStatus.PENDING_PAYMENT
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
        return redirect('order-detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({

        })
        return context


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        try:
            order_obj = Order.objects.filter(
                user=self.request.user,
                status=Order.OrderStatus.PENDING_PAYMENT,
            ).latest('created_at')
        except Order.DoesNotExist:
            raise Http404("هیچ سفارشی یافت نشد.")
        return order_obj