Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 6379, host: 6379
  config.vm.network "forwarded_port", guest: 27017, host: 27017

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    # Install node
    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt-get install -y nodejs

    # Install python stuff
    sudo apt-get install -y python-dev python-pip

    # Install git
    sudo apt-get install -y git

    # Install postgres, redis
    sudo apt-get install -y postgresql libpq-dev redis-server

    # Let redis be accessible from outside
    sudo sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis/redis.conf
    sudo service redis-server restart

    # Install mongo
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
    sudo apt-get update

    # Let mongo be accessible from outside
    sudo sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/g' /etc/mongodb.conf
    sudo service mongodb restart

    # Set up postgres user and db
    echo "CREATE ROLE probr LOGIN ENCRYPTED PASSWORD 'probr';" | sudo -u postgres psql
    sudo su postgres -c "createdb probr --owner probr"
    sudo service postgresql reload

    # Install bower
    sudo npm install -g bower less

    # Create virtualenv and enable
    sudo pip install virtualenv
    virtualenv .env_probr
    source ./.env_probr/bin/activate

    # Clone core
    git clone https://github.com/probr/probr-core.git --depth 1
    cd probr-core

    # Set up settings
    # => Use postgres
    cp probr/settings.example.py probr/settings.py
    echo "DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2','NAME': 'probr','USER': 'probr','PASSWORD': 'probr','HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', 'localhost'),'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT', '5432'),}}" >> probr/settings.py

    # Install bower packages (suppress user statistic input stuff)
    bower install --config.interactive=false

    # Install all pip packages
    pip install -r requirements.txt

    # Migrate
    python manage.py migrate

    # Add a django admin/admin user
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@test.com', 'admin')" | python manage.py shell

    # Run worker with screen (so we can reattach)
    screen -d -m -S probrcoreworker bash -c 'celery worker -A probr'

    # Start server with screen (so we can reattach)
    screen -d -m -S probrcoreweb bash -c 'python manage.py runserver 0.0.0.0:8000'
  SHELL
end
