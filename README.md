# es_corpus

This is a hobby project to create a corpus of the spanish language. The idea is to recover sentences of the spanish language across the internet and compile them, with examples in a fancy, and very big, json file. 

To do so, I've created a simple webcrawler in python who stores the information in [couchdb](http://couchdb.apache.org).

## Creating your own corpus in spanish (or even in your own language)

The process is relatively simple: 

  1. Install [couchdb](http://couchdb.apache.org) in a computer of your choice
  1. es_corpus run on python, so I prefer to create a virtual environment for that: 
  
     $ virtualenv es_corpus
     
  1. in the same directory, copy the contents of the **webcrawler** directory
  1. change the name of the file example_config_local.yaml to config_local.yaml, example_logging.json to example.json 
  and example_config.yaml to config.yaml
  1. make the apropiate configurations in those files: file paths, url's to start exploring, couchdb configuration
  


## Or you can download a copy of the corpus

As soon as I can, I will provide the result of my own compilation of words.

