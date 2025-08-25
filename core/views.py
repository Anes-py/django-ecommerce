from django.shortcuts import render
from django.views import generic

from orders.models import Order


def user_dashboard_view(request):
    context = {
    'pending_orders':Order.objects.filter(
        status=Order.OrderStatus.PENDING_PAYMENT,
    ),
    'paid_orders':Order.objects.filter(
        status=Order.OrderStatus.PAID,
    ),
    'refunded_orders':Order.objects.filter(
        status=Order.OrderStatus.REFUNDED,
    ),
    'fulfilled_orders':Order.objects.filter(
        status=Order.OrderStatus.FULFILLED,
    ),
    'delivered_orders':Order.objects.filter(status=Order.OrderStatus.DELIVERED)
    }


    return render(request, 'core/user_dashboard.html', context=context)

