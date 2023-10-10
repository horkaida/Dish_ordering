import os

from celery import Celery

app = Celery('celery_task', broker=f"pyamqp://guest@{os.environ.get('rabbit_host', 'localhost')}//" )

@app.task
def send_confirmation(email):
    with open('celery_confirmation.txt', 'w') as file:
        file.write(f'Send email to {email}')
