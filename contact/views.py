from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Importar messages

def contact_request(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''), # Usar .get para campos opcionales
                message=form.cleaned_data['message']
            )
            return redirect('contact:contact_success')
        else:
            # Si el formulario no es válido, se re-renderiza con los errores
            pass # No se necesita hacer nada aquí, el render de abajo lo maneja
    else: # GET request
        if request.user.is_authenticated:
            initial_data = {'email': request.user.email}
            # Asumiendo que el perfil de usuario tiene un campo 'phone'
            if hasattr(request.user, 'profile') and request.user.profile.phone:
                initial_data['phone'] = request.user.profile.phone
            form = ContactForm(initial=initial_data)
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
