from django.views import generic

from orders.models import Order, Address
from .forms import OrderForm

class OrderCreateView(generic.CreateView):
    template_name = 'orders/order_create.html'
    model = Order
    form_class = OrderForm


    def form_valid(self, form):
        pass
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'user_addresses':Address.objects.filter(user=self.request.user),
            'order_form':OrderForm,
        })
        return context