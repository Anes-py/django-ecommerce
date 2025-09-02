# carts/signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import Cart


@receiver(user_logged_in)
def merge_cart_with_user(sender, request, user, **kwargs):
    session_key = request.session.get('old_session_key')
    if not session_key:
        return

    try:

        guest_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
        if not guest_cart:
            return


        user_cart, created = Cart.objects.get_or_create(user=user)


        for item in guest_cart.items.all():
            existing_item = user_cart.items.filter(
                product=item.product,
                color=item.color,
                size=item.size,
            ).first()

            if existing_item:
                # اگر قبلاً همون محصول بوده فقط تعداد رو جمع می‌کنیم
                existing_item.quantity += item.quantity
                existing_item.save()
            else:
                # اگر محصول جدید بود به کارت کاربر اضافه می‌کنیم
                item.cart = user_cart
                item.save()

        guest_cart.delete()

    except Exception as e:
        # برای دیباگ بهتره لاگ بگیری
        print(f"⚠️ Cart merge failed: {e}")
