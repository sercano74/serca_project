from django import forms
from .models import Contact, Observation, STATUS_CHOICES

class ContactForm(forms.ModelForm):
    """
    Formulario para que los clientes creen un nuevo requerimiento de contacto.
    """
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre Completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Correo Electrónico'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Teléfono (Opcional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe tu requerimiento...'}),
        }
        labels = {
            'name': 'Nombre',
            'email': 'Correo Electrónico',
            'phone': 'Teléfono',
            'message': 'Mensaje',
        }

class ObservationForm(forms.ModelForm):
    """
    Formulario para añadir una observación de seguimiento a un requerimiento.
    """
    class Meta:
        model = Observation
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Añadir una nueva observación...'}),
        }
        labels = {
            'content': 'Nueva Observación',
        }

class ContactStatusUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar el estado de un requerimiento.
    """
    class Meta:
        model = Contact
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Cambiar Estado del Requerimiento',
        }
