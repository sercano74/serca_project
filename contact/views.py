from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm
from django.contrib.auth.decorators import login_required

def contact_request(request):
    if request.user.is_authenticated:
        # Si el usuario estÃ¡ autenticado, crea la solicitud directamente
        Contact.objects.create(
            email=request.user.email,
            message="Solicitud de contacto de usuario registrado."
        )
        return redirect('contact:contact_success')
    else:
        # Si el usuario no estÃ¡ autenticado, muestra el formulario
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                Contact.objects.create(
                    email=form.cleaned_data['email'],
                    message="Solicitud de contacto de usuario anonimo."
                )
                return redirect('contact:contact_success')
        else:
            form = ContactForm()
        return render(request, 'contact/contact_form.html', {'form': form})

@login_required
def contact_list(request):
    status_filter = request.GET.get('status', '')
    contacts = Contact.objects.all()
    if status_filter:
        contacts = contacts.filter(status=status_filter)
    return render(request, 'contact/contact_list.html', {
        'contacts': contacts,
        'status_choices': Contact.STATUS_CHOICES
    })

def contact_success(request):
    return render(request, 'contact/contact_success.html')
