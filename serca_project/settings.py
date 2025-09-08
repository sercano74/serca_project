# ==================================================
# ====================  ACCESO =====================
# ==================================================
# En CMD entrar al:
#* venv\scripts\activate
#* python manage.py runserver
# ==================================================
# usuario   : admin
# kw        : 123
# email     :
# ==================================================
# usuario   : sercano
# kw        : 123
# email     :
# rol       : Gerencia
# ==================================================

# Limpia la caché de Django: En algunos casos, puede ser útil limpiar la caché de Django:
#* python manage.py clean_pyc.
# Este comando verifica la configuración de tu proyecto y te mostrará cualquier error o advertencia.
#* python manage.py check

import os
import dj_database_url
from pathlib import Path

# Carga las variables de entorno desde el archivo .env
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


#Configuración Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't') # Cambiar a False en producción


ALLOWED_HOSTS = ['web-production-4d2f.up.railway.app','localhost', '127.0.0.1', 'www.serca.online', 'serca.online'] # '*' Update this with your allowed hosts in production

CSRF_TRUSTED_ORIGINS = ['https://web-production-4d2f.up.railway.app','http://web-production-4d2f.up.railway.app','http://*', 'https://www.serca.online', 'https://serca.online'] # Update this with your trusted origins in production


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Cloudinary
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic', # Whitenoise
    # TODO 'django.contrib.humanize', # Formateo de números

    # Mis Apps
    'core',
    'projects',
    'A90_blog',
    'contact',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',


]

# Configuración para Allauth
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none' # Puedes cambiarlo a 'mandatory' en producción

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # Allauth

]

ROOT_URLCONF = 'serca_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Directorio de plantillas global 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'serca_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Configuración para producción en Railway
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/' # URL para archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Directorio para archivos estáticos en producción
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Directorios adicionales para archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # Whitenoise

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' '''ESTO ES PARA UN SERVIDOR DE PRUEBA'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

