from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Contact

@receiver(post_save, sender=Contact)
def send_contact_confirmation_email(sender, instance, created, **kwargs):
    """
    Envía un correo de confirmación al cliente cuando se crea un nuevo requerimiento.
    """
    if created:
        contact = instance
        subject = f"Hemos recibido tu requerimiento #{contact.pk}"
        
        # Renderizar el cuerpo del correo desde una plantilla de texto
        message = render_to_string('contact/emails/contact_confirmation.txt', {
            'contact': contact,
        })

        # Enviar el correo
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, # Remitente
            [contact.email],           # Destinatario
            fail_silently=False,
        )
