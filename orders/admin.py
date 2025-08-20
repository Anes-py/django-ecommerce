from django.contrib import admin

from .models import *

class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ship_full_name',
        'status',
        'payment_method',
    ]
    list_filter = [
        'status',

    ]