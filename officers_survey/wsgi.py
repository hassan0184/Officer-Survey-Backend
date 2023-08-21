"""
WSGI config for officers_survey project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

if 'RDS_HOSTNAME' in os.environ:
    settings = os.environ['SETTINGS']
else:
    settings = config('SETTINGS')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

application = get_wsgi_application()
