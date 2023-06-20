from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
    'import_export'
]

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
    'app_labels': ["apps.product", "apps.storehouse",
                   'apps.supplier', 'apps.invoice', "auth"],
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'TEST': {
            'NAME': os.environ.get('POSTGRES_DB_TEST'),
        },
    },
}

INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
