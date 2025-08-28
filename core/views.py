from django.views import generic
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orders.models import Order
from .forms import *

@login_required
def user_dashboard_view(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    for order in user_orders:
        if order.time_left() ==0 and order.status == Order.OrderStatus.PENDING_PAYMENT:
            order.status = Order.OrderStatus.CANCELLED
            order.save()
    return render(
        request,
        'core/user_dashboard.html',
        context={'user_orders':user_orders}
    )


class SignUPView(generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('login')

    def form_valid(self, form):
        messages.success(self.request, 'خوش آمدید')
        return super().form_valid(form)
