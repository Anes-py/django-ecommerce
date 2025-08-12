from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import gettext_lazy as _
from django.utils import timezone

class Cart(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
        verbose_name=_('user'),
    )
    session_key = models.CharField(_('session_key'), max_length=40)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"{_('cart of')} {self.user.username if self.user else 'Guest'}  | {self.session_key}"
