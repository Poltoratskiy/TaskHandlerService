### TaskHandlerService

Tech stack: Flask, Celery, Redis, Docker

First, clone the repository to your local machine:

```bash
git clone https://github.com/Poltoratskiy/TaskHandlerService.git
```

Run:

```bash
docker-compose up
```

The project will be available at **127.0.0.1:5000/**

## Routes
POST http://127.0.0.1:5000/task - create a new task

GET http://127.0.0.1:5000/task/:id - get status of the task by id
