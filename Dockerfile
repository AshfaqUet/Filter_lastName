FROM python:3.6-alpine

WORKDIR /filterlastname
COPY . ./

RUN pip3 install -r requirements.txt
RUN pip3 install flask

ENV FLASK_APP 'filterlastname.py'

EXPOSE 5000:5000
CMD ["flask","run","--host","0.0.0.0"]

