import time
import configparser
import pickle
import random
import redis
from celery import Celery
from model.Task import Task

cfg = configparser.ConfigParser()
cfg.read("./configs/config.ini")
r_new_tasks = redis.StrictRedis(host="localhost", port=6379, db=0, password=cfg.get("redis", "api_key"))
r_handled_tasks = redis.StrictRedis(host="localhost", port=6379, db=1, password=cfg.get("redis", "api_key"))
POOL_SIZE = int(cfg.get("constraints", "pool_size"))
current_pool_size = 0
app = Celery('periodic',
             broker=f"""redis://:{cfg.get("redis", "api_key")}@localhost:6379/2""")


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
            print(min_idx)
            task = r_new_tasks.get(min_idx)
            print(task)
            task = pickle.loads(task)
            task.run()
            r_handled_tasks.set(min_idx, pickle.dumps(task))
            r_new_tasks.delete(min_idx)
            task_handler(task=task)
