from django.contrib import admin

from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    list_display_links = ['name',]
    list_filter = ['name', 'parent']
    search_fields = ['name', 'parent__name']
    ordering = ['name']
    autocomplete_fields = ['parent']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    list_max_show_all = 30
