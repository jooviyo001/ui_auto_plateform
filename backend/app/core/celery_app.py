from celery import Celery
 
celery_app = Celery(
    'ui_auto_platform',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
) 