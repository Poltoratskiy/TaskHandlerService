import os
import sys
import time
import pickle
import random
import redis
from celery import Celery

sys.path.append('../')
from model.Task import Task

r_new_tasks = redis.StrictRedis(host="redis", port=6379, db=0)
r_handled_tasks = redis.StrictRedis(host="redis", port=6379, db=1)

POOL_SIZE = int(os.getenv('POOL_SIZE', 2))
current_pool_size = 0
app = Celery('periodic', broker='redis://redis:6379/2', backend='redis://redis:6379/2')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, check_size.s(), name='check queue every 5 second')


@app.task
def task_handler(task):
    global current_pool_size
    time.sleep(random.randint(1, 10))
    task.complete()
    r_handled_tasks.set(task.id, pickle.dumps(task))
    current_pool_size -= 1


@app.task
def check_size():
    global current_pool_size
    if current_pool_size < POOL_SIZE:
        tasks = list(r_new_tasks.keys())
        if tasks:
            current_pool_size += 1
            min_idx = min(tasks)
            task = r_new_tasks.get(min_idx)
            t = pickle.loads(task)
            t.run()
            r_handled_tasks.set(min_idx, pickle.dumps(t))
            r_new_tasks.delete(min_idx)
            task_handler(task=t)
