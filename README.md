# Probr - A generic WiFi tracking system

With the vastly increased number of wireless enabled devices, the large amount of data produced by its packets contain large opportunities for usage in research and daily life. By passively listening to wireless signals, it is possible to gather information that can be used to answer interesting questions.
This project aims at developing a system, which helps researches, developers and engineers collecting such data for analysis tasks.

It is a master student research project at the [Communication Systems Group](http://www.csg.uzh.ch) of the  [Department of Informatics](http://www.ifi.uzh.ch), at the [University of Zurich](http://www.uzh.ch), Switzerland.



## probr-core


The probr-core project provides the core functionality for setting up devices for WiFi sniffing, managing them remotely and actually collecting and sniffing WiFi probe request packets.

### Technology

The frameworks, languages, tools and technologies used and required in the probr-core project are:

* Python 2.7
* [Django](https://www.djangoproject.com/)
* [Bower](http://bower.io/)
* [PIP](https://pip.pypa.io/en/latest/installing.html)


### Devices

The devices used for sniffing WiFi packets must fulfill the following requirements:

* \*NIX operating system or simliar (Debian, Ubuntu, OpenWRT, Mac OS X, Raspbian etc.)
* wget installed
* tcpdump installed
* internet access
* wireless interface with monitor mode capabilities


## Installation

We highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/) to manage the python environment for probr-core.

After cloning the project, create a virtual environment for probr outside the probr-core directory:

```
virtualenv .env_probr

```

Activate the virtual python environment:

```
source .env_probr/bin/activate

```

Go into the `probr-core` directory.
Now install the python dependencies of the project:

```
pip install -r requirements.txt

```

Now, install the frontend and web dependencies using bower:

```
bower install

```

You're pretty much set to start probr-core at this moment. What is left to do is:

Create the DB tables:

```
python manage.py migrate

```

Create an admin user for the Django webproject:

```
python manage.py createsuperuser

```

Make sure the mongodb deamon is running:

```
mongod &
```

Also, the redis-server must be running before you can use probr-core

```
redis-server &
```


## Start-Up

Finally, you're ready to start your probr-core server by running:

```
python manage.py runserver

```

In order for the data to be processed and entered into the database, you need to start
the celery worker:

```
celery worker -A probr
```

And you can check it out by visiting `http://localhost:8000`.
