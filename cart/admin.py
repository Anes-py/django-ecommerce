from django.contrib import admin
from .models import Cart, CartItem


class ItemInline(admin.TabularInline):
    model = CartItem
    autocomplete_fields = ['product']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key']
    search_fields = ['id', 'session_key']
    inlines = [
        ItemInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')