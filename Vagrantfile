Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.100.10"
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    # Install node
    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt-get install -y nodejs

    # Install python stuff
    sudo apt-get install -y python-dev python-pip

    # Install git
    sudo apt-get install -y git

    # Install postgres, mongo and redis
    sudo apt-get install -y postgresql libpq-dev mongodb redis-server

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
