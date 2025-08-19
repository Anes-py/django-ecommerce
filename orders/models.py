from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
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

    def __str__(self):
        return self.user.username