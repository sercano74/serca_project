from django.contrib import admin
from django.utils.html import format_html
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "image_tag")
    search_fields = ("title",)

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px; border-radius:4px;" />',
                obj.image.url,
            )
        return "<span style='color:#999'>Sin imagen</span>"

    image_tag.short_description = "Imagen"
