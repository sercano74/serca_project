from django.contrib import admin

from .models import HomeNewsBadge


@admin.register(HomeNewsBadge)
class HomeNewsBadgeAdmin(admin.ModelAdmin):
    list_display = ("text", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("text",)
