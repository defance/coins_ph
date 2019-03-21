FROM python:3.6

LABEL maintainer="defance@gmail.com"

ADD . /opt/app
WORKDIR /opt/app

RUN pip install pip pipenv --upgrade && pipenv install --system --deploy
CMD gunicorn -b 0.0.0.0:8000 --capture-output wsgi
