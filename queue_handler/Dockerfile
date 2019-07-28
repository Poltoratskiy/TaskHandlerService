FROM python:3.6-alpine

ENV CELERY_BROKER_URL redis://redis:6379/2
ENV CELERY_RESULT_BACKEND redis://redis:6379/2
ENV POOL_SIZE 2
ENV C_FORCE_ROOT false



COPY ./queue_handler /queue
WORKDIR /queue


RUN pip install -r requirements.txt

ENTRYPOINT celery -A task_handler worker --loglevel=info -B