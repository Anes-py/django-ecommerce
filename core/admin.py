from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields':('email',)}),
    )
    fieldsets = UserAdmin.fieldsets


class SliderBannerInline(admin.TabularInline):
    model = SliderBanners
    extra = 1
    max_num = 10


class SideBannerInline(admin.TabularInline):
    model = SideBanners
    extra = 2
    min_num = 2
    max_num = 2


class MiddleBannerInline(admin.TabularInline):
    model = MiddleBanners
    extra = 2
    min_num = 2
    max_num = 2


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name']
    list_display_links = ['site_name']
    inlines = [
        SliderBannerInline,
        SideBannerInline,
        MiddleBannerInline,
    ]
