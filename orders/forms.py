from django.forms import ModelForm

from .models import Order, Address


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = (
            'shipping_address',
            'payment_method',
            'coupon_code',
            'notes',
        )


