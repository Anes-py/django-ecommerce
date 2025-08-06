from django.db import models
from django.utils.text import gettext_lazy as _, slugify


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name=_("parent"),

    )
    name = models.CharField(_("name"), max_length=155)
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        blank=True,
        allow_unicode=True,
    )
    image = models.ImageField(_("image"), upload_to='categories/')
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")



class Brand(models.Model):
    name = models.CharField(_("name"), max_length=155)
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )
    description = models.CharField(_("description"), max_length=255)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
