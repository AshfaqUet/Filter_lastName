FROM python:3.6-alpine

WORKDIR /filterlastname

COPY requirements.txt /filterlastname
RUN pip install -r requirements.txt


COPY . /filterlastname
EXPOSE 5000
RUN flask run --host=0.0.0.0
