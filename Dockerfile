FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apt-get clean && apt-get update -y
RUN apt-get install npm -y
RUN npm install -g bower
RUN npm install -g less
RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN pip install amqp==1.4.6
RUN pip install anyjson==0.3.3
RUN pip install billiard==3.3.0.19
RUN pip install celery==3.1.17
RUN pip install Django==1.8
RUN pip install django-admin-bootstrapped==2.5.0
RUN pip install django-appconf==1.0.1
RUN pip install django-audit-log==0.7.0
RUN pip install django-bower==5.0.4
RUN pip install django-compressor==1.5
RUN pip install django-filter==0.10.0
RUN pip install django-taggit==0.13.0
RUN pip install django-taggit-serializer==0.1.1
RUN pip install django-websocket-redis==0.4.4
RUN pip install djangorestframework==3.1.1
RUN pip install djangorestframework-jwt==1.6.0
RUN pip install dpkt==1.8.6
RUN pip install gevent==1.0.2
RUN pip install greenlet==0.4.6
RUN pip install kombu==3.0.24
RUN pip install PyJWT==1.3.0
RUN pip install pymongo==3.0.1
RUN pip install pytz==2015.2
RUN pip install redis==2.10.3
RUN pip install scapy==2.3.1
RUN pip install six==1.9.0
RUN pip install uwsgi
RUN pip install psycopg2==2.6.1

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/
RUN adduser --disabled-password --gecos '' probruser