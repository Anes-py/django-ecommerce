from django.views import generic
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orders.models import Order
from .forms import *

@login_required
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

    def form_valid(self, form):
        messages.success(self.request, 'خوش آمدید')
        return super().form_valid(form)
