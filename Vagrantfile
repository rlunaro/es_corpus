# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "generic/ubuntu2004"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # guest: 80, host: 8080
  #guest: 5984, host: 5984

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "10.0.0.2"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  #config.vm.network "public_network", bridge: "wlp2s0"
  #config.vm.network "public_network", bridge: "wlp2s0", ip: "192.168.0.49"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/vagrant_data", SharedFoldersEnableSymlinksCreate: false

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    #!/bin/bash
    #

    sync_dir=/vagrant
    apt-get update 

    # 
    # install of utilities
    #
    apt-get install -y unzip joe gawk net-tools

    # install couch-db
    sudo apt install curl    
    curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc | sudo apt-key add -
    echo "deb https://apache.bintray.com/couchdb-deb focal main" >> /etc/apt/sources.list
    apt-get -y update
###     debconf-set-selections << EndSelectionsFile
### # this sets automatically the values for the couchdb installation
### couchdb couchdb/adminpass       password "SECRET"
### couchdb couchdb/adminpass_again password "SECRET"
### couchdb couchdb/mode    select  standalone
### couchdb couchdb/cookie  string  monster
### couchdb couchdb/nodename        string  couchdb@localhost
### couchdb couchdb/have_1x_databases       note
### couchdb couchdb/bindaddress     string  "0.0.0.0"
### couchdb couchdb/postrm_remove_databases boolean false
### 
### EndSelectionsFile
###     apt-get -y install couchdb
###     systemctl enable couchdb.service
###     systemctl start couchdb.service

    ln -s /usr/bin/python3 /usr/bin/python
    apt-get -y install python3-pip
    apt-get -y install python3-virtualenv

    # apt get install debconf-utils
    # to install debconf-get-selections


  SHELL
end




