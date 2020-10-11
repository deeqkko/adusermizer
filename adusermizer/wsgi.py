"""
WSGI config for adusermizer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ['ENV_ROLE'] == 'development':
    print(os.environ['ENV_ROLE'])
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adusermizer.settings.base')

elif os.environ['ENV_ROLE'] == 'production':
    print(os.environ['ENV_ROLE'])
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adusermizer.settings.production')

else:
    print(os.environ['ENV_ROLE'])
    print('No ENV_ROLE set. Exiting...')
    

application = get_wsgi_application()
