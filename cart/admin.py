from django.contrib import admin
from .models import Cart, CartItem


# Register your models here.


class ItemInline(admin.TabularInline):
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]