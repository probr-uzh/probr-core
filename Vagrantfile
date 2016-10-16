Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 6379, host: 6379
  config.vm.network "forwarded_port", guest: 27017, host: 27017

  ENV['LC_ALL']="en_US.UTF-8"

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
  end

end
