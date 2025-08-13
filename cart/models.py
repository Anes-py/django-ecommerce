from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import gettext_lazy as _

from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
        verbose_name=_('user'),
    )
    session_key = models.CharField(_('session_key'), max_length=40, null=True, blank=True,)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def cart_final_price(self):
        return sum([item.item_final_price() for item in self.items.all()])

    def cart_org_total(self):
        return sum([item.get_item_org_total() for item in self.items.all()])

    def cart_discount(self):
        return self.cart_org_total() - self.cart_final_price()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"{_('cart of')} {self.user.username if self.user else 'Guest'}  | {self.session_key}"



class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("items")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("product"),
    )
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    color = models.CharField(_("color"), max_length=10, null=True, blank=True)
    size = models.CharField(_("size"), max_length=55, null=True, blank=True)

    def item_final_price(self):
        return self.quantity * self.product.get_final_price()

    def get_item_org_total(self):
        return self.quantity * self.product.price


    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
