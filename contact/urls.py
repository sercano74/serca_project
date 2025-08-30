from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('contactar/', views.contact_request, name='contact_request'),
    path('solicitudes/', views.contact_list, name='contact_list'),
]
