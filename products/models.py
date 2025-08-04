from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import gettext_lazy as _
from django.shortcuts import reverse

from categories.models import Category, Brand

def get_all_category(category):
    subs = [category]
    for category in category.children.all():
        subs += get_all_category(category)
    return subs

class ProductManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True).prefetch_related('images')

    def newest(self):
        return self.active().order_by('-created_at').select_related('discount')

    def with_discount(self):
        now = timezone.now()
        return self.active().filter(
            Q(discount__start_date__lte=now) | Q(discount__start_date__isnull=True),
            Q(discount__expire_date__gte=now) | Q(discount__expire_date__isnull=True),
            discount__is_active=True,
        ).select_related('discount').order_by('-discount__value')

    def by_category(self, category_slug):
        try:
            category = Category.objects.prefetch_related("children").get(slug=category_slug)
        except Category.DoesNotExist:
            return self.none()
        subcategories = get_all_category(category)
        return self.active().filter(category__in=subcategories)

    def by_brand(self, brand_slug):
        return self.active().filter(brand__slug=brand_slug)

    def search(self, query):
        return self.active().filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) | Q(description__icontains=query)
        )

    def most_expensive(self):
        return self.active().order_by('-price')

    def cheapest(self):
        return self.active().order_by('price')


class FeatureOption(models.Model):
    class Feature(models.TextChoices):
        Color = 'c', _('Color')
        Size = 's', _('Size')
    class Color(models.TextChoices):
        RED = 'red', _('red')
        BLUE = 'blue', _('blue')
        GREEN = 'green', _('green')
        BLACK = 'black', _('black')
        WHITE = 'white', _('white')
        YELLOW = 'yellow', _('yellow')
        ORANGE = 'orange', _('orange')
        PURPLE = 'purple', _('purple')
        PINK = 'pink', _('pink')
        BROWN = 'brown', _('brown')
        GRAY = 'gray', _('gray')
        SILVER = 'silver', _('silver')
        GOLD = 'gold', _('gold')
        BEIGE = 'beige', _('beige')
        MAROON = 'maroon', _('maroon')
        NAVY = 'navy', _('navy')
        TEAL = 'teal', _('teal')
        TURQUOISE = 'turquoise', _('turquoise')
        CYAN = 'cyan', _('cyan')
        MAGENTA = 'magenta', _('magenta')
        LIME = 'lime', _('lime')
        OLIVE = 'olive', _('olive')
        INDIGO = 'indigo', _('indigo')
        VIOLET = 'violet', _('violet')
        CORAL = 'coral', _('coral')
        SALMON = 'salmon', _('salmon')
        KHAKI = 'khaki', _('khaki')
        MINT = 'mint', _('mint')
        PEACH = 'peach', _('peach')
        IVORY = 'ivory', _('ivory')
        LAVENDER = 'lavender', _('lavender'),

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='feature_options',
        verbose_name=_('product'),
    )
    feature = models.CharField(
        _('feature'),
        max_length=1,
        choices=Feature.choices
    )
    color = models.CharField(
        _('color'), max_length=20,
        choices=Color.choices,
        blank=True,
        help_text=_('If this feature is a color, fill this field and leave the value field empty.')
    )
    value = models.CharField(
        _('value'),
        max_length=55,
        blank=True,
        help_text=_('If this feature is a size, fill this field and leave the color field empty.')
    )

    def __str__(self):
        if self.Feature == self.Feature.Color:
            return f"{self.feature}: {self.color}"
        else:
            return f"{self.feature}: {self.value}"

    def clean(self):
        if self.feature == self.Feature.Color:
            if not self.color:
                raise ValidationError(_("Color feature must have a color value."))
            if self.value:
                raise ValidationError(_("Color feature must not have a size value."))
        elif self.feature == self.Feature.Size:
            if not self.value:
                raise ValidationError(_("Size feature must have a size value."))
            if self.color:
                raise ValidationError(_("Size feature must not have a color value."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='specifications',
        verbose_name=_('product'),
    )
    key = models.CharField(_('key'), max_length=55)
    value = models.CharField(_('value'), max_length=155)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        unique_together = ('product', 'key')
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")


def product_image_upload_path(instance, filename):
    return f'products/{instance.slug}/{filename}'

class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to=product_image_upload_path)

    def __str__(self):
        return self.image.name


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

    def get_final_price(self):
        if self.has_valid_discount():
            return self.discount.apply_discount(self.price)
        return self.price

    def has_valid_discount(self):
        return self.discount and self.discount.is_valid()

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    objects = ProductManager()


class Discount(models.Model):
    value = models.DecimalField(_("value"), max_digits=5, decimal_places=2)
    is_active = models.BooleanField(_("is active"), default=True)
    start_date = models.DateTimeField(_("start date"), null=True, blank=True)
    expire_date = models.DateTimeField(_("expire date"), null=True, blank=True)

    def __str__(self):
        status = "Active" if self.is_valid() else "InActive"
        return f"{self.value}% ({status})"

    def is_valid(self):
        now = timezone.now()
        return self.is_active and (self.start_date is None or self.start_date <= now) and (self.expire_date is None or self.expire_date >= now)

    def apply_discount(self, price):
        if not self.is_valid():
            return price
        return max(price * (1 - self.value / 100), 0)

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.CommentStatus.APPROVED)


class Comment(models.Model):
    class CommentStatus(models.TextChoices):
        APPROVED = 'aprv', _('APPROVED'),
        DRAFT = 'drf', _('draft'),
        REJECTED = 'rjk', _('rejected')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_comments', null=True, blank=True)
    display_name = models.CharField(max_length=55)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments', null=True, blank=True)
    title = models.CharField(max_length=55)
    text = models.TextField()
    recommend = models.BooleanField()
    status = models.CharField(max_length=4, choices=CommentStatus.choices, default=CommentStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    active = CommentManager()

    def __str__(self):
        return f"comment by: {self.display_name} on {self.product} - {self.status}"
