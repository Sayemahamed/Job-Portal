from celery import shared_task

@shared_task
def add():
    return "Task executed! without delay"
