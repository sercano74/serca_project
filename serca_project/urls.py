from django.contrib import admin
from django.urls import path, include # Asegúrate que 'include' esté importado
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Revisa esta línea
    path('obras/', include('projects.urls')),
    path('noticias/', include('A90_blog.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
