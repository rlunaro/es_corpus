

INSTALLING ON A NEW SERVER
==========================

First of all, it's needed a running server with couchdb installed. The steps for doing that
are well documented, but essentially are: 


    sudo apt install curl    
    curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc | sudo apt-key add -
    echo "deb https://apache.bintray.com/couchdb-deb focal main" >> /etc/apt/sources.list
    apt-get -y update
    apt-get -y install couchdb
    systemctl enable couchdb.service
    systemctl start couchdb.service

Create a python environment
===

    $ virtualenv corpus_env  # I've picked up the name "corpus_env", but you can put whatever you want
    $ source corpus_env/activate 
    $ python -m pip install --upgrade pip
    $ pip install requests
    $ pip install bs4
    $ pip install pyyaml
    $ pip install couchdb
    $ pip install langdetect

RUNNING db_starter.py
===

The next step is running db_starter.py. Please configure before the file config_local.yaml to set 
the address of the couchdb database server. 

There is a file "example_db_start.sh" if you want a configured script who uses a virtual
python environment. 

Running the webcrawler
===


