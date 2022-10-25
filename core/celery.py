import os
from celery import Celery

# set the default django settings module for the celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

#To use celery in your app, you simply import this instance
"""Note that the format of broker URL should be:
transport://userid:password@hostname:port/virtual_host"""
app = Celery('core',
            broker='amqp://admin:Admin123@localhost/admin_vhost',
            backend='rpc://',
        
            )

"""
using a string here means the worker doesnt have to serialize the configuation object to child processes
namespace='CELERY' MEANS ALL CELERY-RELATED CONFIGURATION KEYS
SHOULD HAVE A 'CELERY_' prefix
"""
app.config_from_object('django.conf:settings',namespace='CELERY')

#Load task modules from all registered django apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'request: {self.request!r}')