import cloudinary.uploader
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Project


class ProjectAdminForm(forms.ModelForm):
    """Formulario personalizado que reemplaza el widget de CloudinaryField
    por un selector de archivos real (ClearableFileInput)."""
    image = forms.ImageField(
        required=False,
        label="Imagen",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*"}),
    )

    class Meta:
        model = Project
        fields = "__all__"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
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

    def save_model(self, request, obj, form, change):
        if request.FILES.get("image"):
            uploaded = cloudinary.uploader.upload(
                request.FILES["image"],
                folder="SERCA/",
                resource_type="image",
            )
            obj.image = uploaded["public_id"]
        elif change and not form.cleaned_data.get("image"):
            # Usuario limpió el campo — borrar imagen de Cloudinary
            try:
                old = Project.objects.get(pk=obj.pk)
                if old.image:
                    cloudinary.uploader.destroy(old.image.public_id)
            except Exception:
                pass
            obj.image = None

        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image:
                try:
                    cloudinary.uploader.destroy(obj.image.public_id)
                except Exception:
                    pass
            obj.delete()

    def delete_model(self, request, obj):
        if obj.image:
            try:
                cloudinary.uploader.destroy(obj.image.public_id)
            except Exception:
                pass
        super().delete_model(request, obj)
