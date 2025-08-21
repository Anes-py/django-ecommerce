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


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = (
            'full_name',
            'phone',
            'country',
            'state',
            'city',
            'postal_code',
            'full_address',
            'is_default',
        )
