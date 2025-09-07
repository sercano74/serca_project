from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact
from .forms import ContactForm, ObservationForm, ContactStatusUpdateForm

def contact_request(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # El email se enviará a través de una señal post_save
            return redirect('contact:contact_success')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {'name': request.user.get_full_name(), 'email': request.user.email}
        form = ContactForm(initial=initial_data)

    return render(request, 'contact/contact_form.html', {'form': form})

@login_required
def contact_list(request):
    status_filter = request.GET.get('status', '')
    contacts = Contact.objects.all()
    if status_filter:
        contacts = contacts.filter(status=status_filter)
    
    return render(request, 'contact/contact_list.html', {
        'contacts': contacts,
        'status_choices': Contact._meta.get_field('status').choices
    })

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    observation_form = ObservationForm()
    status_form = ContactStatusUpdateForm(instance=contact)

    if request.method == 'POST':
        # Determinar qué formulario se envió
        if 'submit_observation' in request.POST:
            observation_form = ObservationForm(request.POST)
            if observation_form.is_valid():
                observation = observation_form.save(commit=False)
                observation.contact = contact
                observation.author = request.user
                observation.save()
                messages.success(request, 'Observación añadida correctamente.')
                return redirect('contact:contact_detail', pk=contact.pk)
        
        elif 'submit_status' in request.POST:
            status_form = ContactStatusUpdateForm(request.POST, instance=contact)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Estado del requerimiento actualizado.')
                return redirect('contact:contact_detail', pk=contact.pk)

    return render(request, 'contact/contact_detail.html', {
        'contact': contact,
        'observation_form': observation_form,
        'status_form': status_form,
    })

def contact_success(request):
    return render(request, 'contact/contact_success.html')
