from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product


class Address(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='addresses',
        verbose_name=_('user'),
    )
    full_name = models.CharField(_('full_name'), max_length=155)
    phone = PhoneNumberField()

    country = models.CharField(_('country'), max_length=60, default='Iran')
    state = models.CharField(_('state/province'), max_length=60, blank=True)
    city = models.CharField(_('city'), max_length=60)
    postal_code = models.CharField(_('postal code'), max_length=20)

    is_default = models.BooleanField(_('user default address'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PENDING_PAYMENT = 'pending_payment', _('Pending Payment')
        PAID = 'paid', _('Paid')
        FULFILLED = 'fulfilled', _('Fulfilled / Shipped')
        CANCELLED = 'cancelled', _('Cancelled')
        REFUNDED = 'refunded', _('Refunded')
    class PaymentMethodChoices(models.TextChoices):
        CARD = 'card', _('Credit/Debit Card')
        COD = 'cod', _('Cash on Delivery')
        TRANSFER = 'transfer', _('Bank Transfer / EFT')

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_orders',
        verbose_name=_('user'),
    )

    ship_full_name = models.CharField(_('recipient name'), max_length=120)
    ship_phone = PhoneNumberField()
    ship_country = models.CharField(_('country'), max_length=60, default='iran')
    ship_state = models.CharField(_('state/province'), max_length=60, blank=True)
    ship_city = models.CharField(_('city'), max_length=60)
    ship_postal_code = models.CharField(_('postal code'), max_length=20)
    ship_line1 = models.CharField(_('address line 1'), max_length=255)
    ship_line2 = models.CharField(_('address line 2'), max_length=255, blank=True)

    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_('shipping address record'),
    )

    status = models.CharField(_('status'), max_length=32, choices=OrderStatus.choices, default=OrderStatus.DRAFT)
    payment_method = models.CharField(_('payment method'), max_length=16, choices=PaymentMethodChoices.choices)

    subtotal = models.PositiveIntegerField(_('subtotal'))
    discount_total = models.PositiveIntegerField(_('discount total'))
    shipping_total = models.PositiveIntegerField(_('shipping'))
    tax_total = models.PositiveIntegerField(_('tax total'))
    grand_total = models.PositiveIntegerField(_('grand total'))

    coupon_code = models.CharField(_('coupon code'), max_length=40, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='items', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='user_order_items')
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='product_orders',
        verbose_name=_('product'),
    )
    product_name = models.CharField(_('product name'), max_length=155)
    item_price = models.PositiveIntegerField(_('item price'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    total_price = models.PositiveIntegerField(_('total_price'))
    total_discount = models.PositiveIntegerField(_('total discount'))
    final_price = models.PositiveIntegerField(_('final price'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.product_name = self.product.name
        self.item_price = self.product.price
        return super().save()
    