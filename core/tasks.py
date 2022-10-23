from celery import shared_task

#to run this task asynchronoulsy, use the delay() method
@shared_task
def add(x,y):
    return x+y

