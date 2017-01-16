FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apt-get clean && apt-get update -y
RUN apt-get install npm supervisor -y
RUN npm install -g bower
RUN npm install -g less
RUN ln -s /usr/bin/nodejs /usr/bin/node

ADD requirements.txt /app/
ADD install/docker/web/conf/supervisor-app.conf /etc/supervisor/conf.d/
RUN pip install -r requirements.txt

ADD bower.json /app/
ADD .bowerrc /app/
RUN bower install --allow-root

ADD . /app/

RUN python manage.py collectstatic --noinput