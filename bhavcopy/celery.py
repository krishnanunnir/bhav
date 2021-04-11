import os


from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhavcopy.settings')

appname = Celery('bhavcopy')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
appname.config_from_object('django.conf:settings', namespace='CELERY')

appname.autodiscover_tasks()
appname.conf.timezone='Asia/Kolkata'
appname.conf.beat_schedule = {
    "Write csv to db everyday at 6pm": {
        "task": "app.tasks.writeCSVToDB",  # <---- Name of task
        "schedule": crontab(hour='01',minute='41')
    },
}