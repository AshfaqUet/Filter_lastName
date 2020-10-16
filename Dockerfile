FROM python:3.6-alpine

RUN adduser -D filterlastname

WORKDIR /home/filterlastname

COPY requirements.txt requirements.txt
#RUN python -m venv venv
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY filterlastname.py config.py ./

ENV FLASK_APP filterlastname.py

EXPOSE 5000
