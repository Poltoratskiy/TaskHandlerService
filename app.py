import ast
import pickle
import configparser
import redis
from flask import Flask

from model.Task import Task

app = Flask(__name__)
cfg = configparser.ConfigParser()
cfg.read("./configs/config.ini")

r_new_tasks = redis.StrictRedis(host="localhost", port=6379, db=0, password=cfg.get("redis", "api_key"))
r_handled_tasks = redis.StrictRedis(host="localhost", port=6379, db=1, password=cfg.get("redis", "api_key"))


def idx_generator():
    '''
    generate id for new task
    :return: int id
    '''
    try:
        lst = list(map(int, list(map(lambda x: x.decode("UTF-8"), list(r_handled_tasks.keys())))))
        print(lst)
        if not lst:
            lst = list(map(int, list(map(lambda x: x.decode("UTF-8"), list(r_new_tasks.keys())))))
            print(lst)
            if not lst:
                i = 1
            else:
                i = max(lst) + 1
        else:
            i = max(lst) + 1
    except ValueError:
        i = 1
    while True:
        yield i
        i += 1


@app.route('/tasks', methods=['POST'])
def put_task_in_queue():
    """
    route for new task
    :return: int id task
    """
    global idx_gen
    new_idx = next(idx_gen)
    task = Task(new_idx)
    r_new_tasks.set(new_idx, pickle.dumps(task))
    return str(new_idx)


@app.route('/tasks/<int:task_id>')
def get_task_status(task_id):
    """
    route for checking status of the task by id
    :param task_id: int task identifier
    :return: json response:
    {
    "create_time": datetime,
    "start_time": datetime,
    "status": ["Completed"|"Run"|"In Queue"],
    "time_to_execute": 1.001128911972046
    }
    """
    task = r_handled_tasks.get(task_id)
    if task is None:
        task = r_new_tasks.get(task_id)
        if task is None:
            response = app.response_class(
                status=404
            )
            return response
    task = pickle.loads(task)
    return ast.literal_eval(str(task))


idx_gen = idx_generator()

if __name__ == '__main__':
    app.run()
