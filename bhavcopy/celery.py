import os


from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhavcopy.settings')

appname = Celery('bhavcopy')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
appname.config_from_object('django.conf:settings', namespace='CELERY')

appname.autodiscover_tasks()