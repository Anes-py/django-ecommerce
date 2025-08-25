from django.contrib import admin
from .models import Cart, CartItem


class ItemInline(admin.TabularInline):
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [
        ItemInline,
    ]
