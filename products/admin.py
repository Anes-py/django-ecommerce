from django.contrib import admin

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'id',
        'price',
        'stock',
        'status',
        'is_active',
        'created_at',
        'updated_at',
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_display_links = ['name']
    list_per_page = 20
    list_max_show_all = 30
    list_editable = ['status', 'is_active']
    list_filter = ['status', 'is_active', 'category']
    autocomplete_fields = ['category', 'brand']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'short_description']
    ordering = ['-created_at', 'stock']
