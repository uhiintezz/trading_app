FROM python:3.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

# Установка прав на выполнение для всех .sh файлов в директории docker

USER root

RUN chmod a+x docker/app.sh
RUN chmod a+x docker/celery.sh


# Проверка существования и прав доступа к файлам
RUN ls -l docker/


#WORKDIR src
#
#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000




