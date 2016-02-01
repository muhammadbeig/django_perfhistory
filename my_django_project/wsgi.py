"""
WSGI config for my_django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django_project.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django_project.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "{{ project_name }}.settings"

application = get_wsgi_application()

# application =  django.core.handlers.wsgi.WSGIHandler()
