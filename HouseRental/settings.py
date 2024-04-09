import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r5m-8b5@je#ctjf%x3q595c#2f%opiov@2(d6r@0jmu&s%#%!i'

# SECURITY WARNING: don't run with debug turned on in production!
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
    'ckeditor',
    'App_Account',
    'App_Rental',
]
CKEDITOR_CONFIGS = { 'default':
                         { 'toolbar': 'Custom', 'height': 200,'width': 'auto', 'toolbar_Custom':
                             [
                                 ['Styles', 'Format', 'FontSize','Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker'],
                                 ['Table', 'HorizontalRule'],
                                 ['TextColor', 'BGColor'],
                                 ['Smiley','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock',],
                             ],
                           }, 'special':
                    { 'toolbar': 'Special', 'toolbar_Special':
                            [
                             ['Bold'],
                            ],
                          }
                     }
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HouseRental.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'HouseRental.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'easyyrentt@gmail.com'
EMAIL_HOST_PASSWORD = 'ihilprokfwyahtzw'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STRIPE_PUBLISHABLE_KEY = 'pk_test_51OgtcCLCGAkvlIlNz6H8FwtAQbNS1uigVMzy6drr07FgGAtTS8Hgewk3Ov2gBGiltS0BEu34DRRbWF6G3wvm6bbX00NwQamDTm'
STRIPE_SECRET_KEY = 'sk_test_51OgtcCLCGAkvlIlNgoW57q9mkyMvLod817NagBUC8v4yDMzr2vnTd4berILbQNsBORDkUR7Oj1cveMudlLj546Xb00aRakTZVR'