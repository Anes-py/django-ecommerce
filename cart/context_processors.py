from django.db.models import Prefetch
from .models import Cart, CartItem


def cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.select_related('user').prefetch_related(Prefetch(
            'items',
            queryset=CartItem.objects.select_related('product', 'product__discount')
        )).get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.prefetch_related(Prefetch(
            'items',
            queryset=CartItem.objects.select_related('product', 'product__discount')
        )).get_or_create(session_key=session_key)
    return {
        'cart':cart
    }
