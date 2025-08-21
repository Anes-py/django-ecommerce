from django.contrib import admin

from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'status',
        'payment_method',
    ]
    list_filter = [
        'status',
        'payment_method'
    ]
    list_display_links = ['user']
    search_fields = [
        'user',
        'ship_full_name',
    ]
    list_per_page = 20
    list_max_show_all = 30
    inlines = [
        OrderItemInline,
    ]
