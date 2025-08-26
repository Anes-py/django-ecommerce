from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal

from cart.models import Cart
from orders.models import Order, OrderItem
from .forms import OrderForm


class OrderCreateView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        cart = get_object_or_404(Cart, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
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
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_discount=item.item_discount(),
                    final_price=item.item_final_price(),
                )
                item.product.total_sell += item.quantity
                item.save()
                cart.items.all().delete()
        messages.success(request, "!فاکتور شما آماده پرداخت است")
        return redirect('order-detail')


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order_obj = get_object_or_404(Order, user=self.request.user, pk=self.kwargs['pk'])
        if order_obj.time_left == 0 and order_obj.status == Order.OrderStatus.PENDING_PAYMENT:
            order_obj.status=Order.OrderStatus.CANCELLED
            order_obj.save()
        return order_obj