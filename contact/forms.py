from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(label="Tu correo electrÃ³nico")
    phone = forms.CharField(label="Tu telÃ©fono (opcional)", required=False, max_length=20)
    message = forms.CharField(label="Tu mensaje", widget=forms.Textarea)
