import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # Reads the .env file
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-@gs-)iy@)0!ttdcm5e_(!r_80ea%7ms)61qe1@2te2!ymkl5!w'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'otp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'otp_auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Ensure you have your templates folder here if needed
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

WSGI_APPLICATION = 'otp_auth.wsgi.application'

# Database settings (PostgreSQL for RDS)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Replace with your RDS database name
        'NAME': env('RDS_DB_NAME', default='mydjangodbotp'),
        # Replace with your RDS username
        'USER': env('RDS_USER', default='postgres'),
        # Replace with your RDS password
        'PASSWORD': env('RDS_PASSWORD', default='password'),
        # Replace with your RDS endpoint
        'HOST': env('RDS_HOST', default='mydjangodbotp.c526sy82k4ed.ap-south-1.rds.amazonaws.com'),
        'PORT': env('RDS_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "otp/static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings using .env values
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
