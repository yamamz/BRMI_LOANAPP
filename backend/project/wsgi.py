"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os,sys
sys.path.append('C:/Bitnami/djangostack-2.1.1-1/apps/django/django_projects/django-vue-scaffold/backend')
os.environ.setdefault("PYTHON_EGG_CACHE", 'C:/Bitnami/djangostack-2.1.1-1/apps/django/django_projects/django-vue-scaffold/backend/egg_cache')



from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()
