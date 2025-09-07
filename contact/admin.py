from django.contrib import admin
from .models import Contact, Observation

class ObservationInline(admin.TabularInline):
    model = Observation
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)
    extra = 1 # Muestra un campo para añadir una nueva observación por defecto
    can_delete = False

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Requerimiento', {
            'fields': ('message',)
        }),
        ('Estado y Seguimiento', {
            'fields': ('status',)
        }),
        ('Fechas Importantes', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = [ObservationInline]

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('contact', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('content',)