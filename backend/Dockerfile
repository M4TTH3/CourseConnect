FROM python:3.10-slim-buster

COPY ./app ./app

RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt

EXPOSE 80

CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]