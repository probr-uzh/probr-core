FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN apt-get clean && apt-get update -y
RUN apt-get install npm gettext libgettextpo-dev nginx supervisor -y
RUN npm install -g bower
RUN npm install -g less
RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN mkdir /conf
RUN mkdir /scripts

ADD ./docker/conf/uwsgi_app.ini /conf/
ADD ./docker/conf/uwsgi_params /conf/
ADD ./docker/scripts/wait-for-it.sh /scripts/

RUN mkdir /code
RUN mkdir /code/static
RUN mkdir /code/media

WORKDIR /code

ADD bower.json /code/
ADD .bowerrc /code/
RUN bower install --allow-root

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
COPY ./probr/settings.docker.py /code/probr/settings.py
RUN python /code/manage.py collectstatic --noinput
#RUN python /code/manage.py compilemessages
RUN curl -sLo /usr/local/bin/ep https://github.com/kreuzwerker/envplate/releases/download/v0.0.8/ep-linux && chmod +x /usr/local/bin/ep

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY docker/conf/nginx-app.conf /etc/nginx/sites-available/default
COPY docker/conf/supervisor-app.conf /etc/supervisor/conf.d/
