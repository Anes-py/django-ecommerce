from django.views import generic
from django.shortcuts import render, reverse

from orders.models import Order
from .models import *
from .forms import *

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


class SignUPView(generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('login')
