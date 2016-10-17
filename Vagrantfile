Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |v|
    v.memory = 8192
    v.cpus = 4
  end
  config.vm.network "public_network"

  ENV['LC_ALL']="en_US.UTF-8"

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
  end

end
