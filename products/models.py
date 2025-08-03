from django.db import models
from django.utils.text import gettext_lazy as _

from categories.models import Category, Brand



def product_image_upload_path(instance, filename):
    return f'products/{instance.slug}/{filename}'

class Product(models.Model):
    class ProductStatus(models.TextChoices):
        AVAILABLE = 'a',  _('Available'),
        SOON = 's', _('Coming Soon'),
        NOT_AVAILABLE = 'na', _('Not Available'),

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_products',
        verbose_name=_('category'),
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='brand_products',
        verbose_name=_('brand'),
        null=True,
        blank=True,
    )
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    main_image = models.ImageField(upload_to=product_image_upload_path)
    short_description = models.CharField(_('short description'),max_length=155)
    description = models.TextField(_('description'))
    price = models.PositiveIntegerField(_('price'), default=0)
    stock = models.PositiveIntegerField(_('stock'), default=0)
    status = models.CharField(
        _('status'),
        max_length=2,
        choices=ProductStatus.choices,
    )
    is_active = models.BooleanField(_('is active'), default=True)

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
