from django.db import models
from django.contrib.auth.models import User

# Opciones para el campo de estado del requerimiento (CRM)
STATUS_CHOICES = [
    ('ingresado', 'Ingresado'),
    ('en_revision', 'En Revisión'),
    ('en_curso', 'En Curso'),
    ('cotizacion_enviada', 'Cotización Enviada'),
    ('aprobado', 'Aprobado'),
    ('finalizado', 'Finalizado'),
    ('descartado', 'Descartado'),
]

class Contact(models.Model):
    """
    Modelo para registrar los requerimientos de contacto de potenciales clientes.
    Funciona como la entidad principal de un mini-CRM.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    message = models.TextField(verbose_name="Mensaje del Requerimiento")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ingresado', 
        verbose_name="Estado del Requerimiento"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Requerimiento de Contacto"
        verbose_name_plural = "Requerimientos de Contacto"
        ordering = ['-created_at']

    def __str__(self):
        return f"Requerimiento de {self.name} ({self.get_status_display()})"

class Observation(models.Model):
    """
    Modelo para registrar las observaciones o seguimientos de un requerimiento.
    """
    contact = models.ForeignKey(
        Contact, 
        related_name='observations', 
        on_delete=models.CASCADE, 
        verbose_name="Requerimiento Asociado"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Autor de la Observación"
    )
    content = models.TextField(verbose_name="Contenido de la Observación")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la Observación")

    class Meta:
        verbose_name = "Observación"
        verbose_name_plural = "Observaciones"
        ordering = ['-created_at']

    def __str__(self):
        return f'Observación de {self.author.username} el {self.created_at.strftime("%Y-%m-%d %H:%M")}'