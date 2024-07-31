from celery import Celery

app = Celery('tasks', broker='redis://52.204.247.130:6379/0',
             backend='redis://52.204.247.130:6379/0')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_prefetch_multiplier=1,
    tasks_acks_late=True,
    worker_max_tasks_per_child=100,

    worker_autoscaler='celery.worker.autoscale:Autoscaler',
    worker_autoscaler_conf={
        'min_concurrency': 1,
        'max_concurrency': 1
    }
)
