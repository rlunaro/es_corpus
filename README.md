# es_corpus

This is a hobby project to create a corpus of the spanish language. The idea is to recover sentences of the spanish language across the internet and compile them, with examples in a fancy, and very big, json file. 

To do so, I've created a simple webcrawler in python who stores the information in [couchdb](http://couchdb.apache.org).

## Creating your own corpus in spanish (or even in your own language)

### Installation on a clean machine

You should have a clean machine ready to work long hours. It's preferable to be a server, 
a cloud server or an interenet server. Although you can run this on laptop perfectly well, 
is too much stress for this type of computer, definitely not ready for intensive work during
long periods of time. 

**I have used Ubuntu linux for this project** although precautions have been taken to 
ensure that this could work on a Windows host or even on a mac. 

Said that, you have to be installed in your machine: 

  - A working [couch db](http://couchdb.apache.org) database server
  - Python version > 3.8

No explanation will be given on how to install a couchdb database or a python environment.

### Step 1: create a python a virtual environment to run the corpus

Python has a mechanism to create virtual environments, and I prefer that for no contaminate the 
*pristine* python environment and use a python virtual environment to accomplish these tasks. 

Let's say that the directory where we are going to create our project will be called `es_corpus`:

    $ virtualenv es_corpus
    $ cd es_corpus
    $ source bin/activate
    (es_corpus) $ pip install requests
    (es_corpus) $ pip install bs4
    (es_corpus) $ pip install pyyaml
    (es_corpus) $ pip install couchdb
    (es_corpus) $ pip install langdetect
    es_corpus$ git clone https://github.com/rlunaro/es_corpus.git

### Step 2: configure files

**Configure logging file***

From the `example_logging.json` file create three three files: 

    $ cp example_logging.json logging_db_start.json 
    $ cp example_logging.json logging_extract_words.json 
    $ cp example_logging.json logging_webcrawler.json
    $ cp example_logging.json logging_corpus_extractor.json

Edit the three files and change the line where the "filename" appears to something that 
suit your needs: 

        "handlers" : {
        "handler1" : {
            "class" : "logging.handlers.RotatingFileHandler",
            "filename" : "/PATH/TO/YOUR/OWN/INSTALLATION/db_start.log", 

**The log file for each file cannot be shared in certain cases** (webcrawler and extract_words) because
these files will be run in parallel. 

Remove the console handler also to prevent the output to be shown in the console and change the level
to INFO or higher level: 

    "loggers" : {
        "rotatingFileLogger" : {
            "level" : "INFO",
            "handlers": [ "handler1" ]
        }

**Configure the starting scripts**

Next step is change the name of those `example_XXX.sh` files into `XXX.sh` and configure them
to run using the virtual environment. 

    $ mv example_db_start.sh db_start.sh
    $ mv example_webcrawler.sh webcrawler.sh
    $ mv example_extract_words.sh extract_words.sh
    $ mv example_corpus_extractor.sh corpus_extractor.sh

Then, you have to configure adequately the four files. Change the directory where your configuration
is located: 

    corpus_extractor_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"

In the case of `webcrawler.sh` and `extract_words.sh`, it si advisable to put the output to a 
file, because they will be running as daemons: 

    "$PYTHON_EXE" -u "$webcrawler_home/webcrawler.py" \
    --local-config="config_local.yaml" \
    --config="config.yaml" \
    --logging="logging.json" \
    $1 $2 $3 $4 $5 > webcrawler.out

**Configure the config files**

Rename the files `example_config_local.yaml` and `example_config.yaml` to `config_local.yaml` 
and `config.yaml` respectively: 

   $ mv example_config.yaml config.yaml 
   $ mv example_config_local.yaml config_local.yaml 

and configure them. 

*config.yaml - urllist* 

Here you have to place all the starting url's you want. For instance, I've started with the wikipedia: 

    urlList:
      - "http://es.wikipedia.org"

Another interesting entry would be [project gutemberg for spanish](http://www.gutenberg.org/browse/languages/es)
and [wikilibros](https://es.wikilibros.org). 

*config_local.yaml - db*

Here goes the configuration of your couchdb installation. 

*config_local.yaml - working_hours / working_hours_extract_words*

The working_hours parameter establishes at what hour the webcrawler would be working crawling web pages. 

On the other hand, the working_hours_extract_words parameter establishes the
hours the extract_words program can work. In this manner, you can safely
left both programs running indefinitely on the target machine, everyone 
starting at the scheduled hours and doing its job.

*config_local.yaml - max_jobs*

How much jobs the webcrawler will run in paralell. I've put 100 in my setup, and 2 for development. 

*config_local.yaml - user_agent* 

This configures how the webcrawler will be identified as the different webservers.

*config_local.yaml - corpus_result_dir*

Where the result of the vocabulary and the corpus will be left. 

**Launch db_start.sh**

**This must be done only once**: it configures couchdb creating a database and the necessary views 
for the project. 

**Launch webcrawler and extract_words as daemons**

    $ ./webcrawler.sh & 
    $ ./extract_words.sh & 
    $ disown -a

The `disown -a` command will left the commands running even when you close the session. 

**Launch corpus_extractor whenever you want a fresh copy of the corpus**

You can run corpus_extractor whenever you want to create a fresh copy of the corpus. 

## Reading the content of the corpus

The corpus consist of two files, both written in utf-8. 

The first one, called words.txt, has a clear format: 

    a
    de
    del
    embarazada
    enero
    la

Each word in a single line, ended in new line character (\n). Nothing to say about this. 

The other one, `corpus.txt`, has the following format: 

    {"word": "a", "sentences": [{"sentence": "Un joven mat\u00f3 a una adolescente de 14 a\u00f1os: estaba embarazada", "source": "http://www.lmneuquen.com", "date": "2021-01-10T09:53:10.649373"}]}
    {"word": "de", "sentences": [{"sentence": "Quiniela de la Provincia: La Nocturna del s\u00e1bado 9 de enero", "source": "http://www.lmneuquen.com", "date": "2021-01-10T09:53:12.695909"}, {"sentence": "Un joven mat\u00f3 a una adolescente de 14 a\u00f1os: estaba embarazada", "source": "http://www.lmneuquen.com", "date": "2021-01-10T09:53:10.649373"}]}
    {"word": "del", "sentences": [{"sentence": "Quiniela de la Provincia: La Nocturna del s\u00e1bado 9 de enero", "source": "http://www.lmneuquen.com", "date": "2021-01-10T09:53:12.695909"}]}
    {"word": "embarazada", "sentences": [{"sentence": "Un joven mat\u00f3 a una adolescente de 14 a\u00f1os: estaba embarazada", "source": "http://www.lmneuquen.com", "date": "2021-01-10T09:53:10.649373"}]}
    {"word": "enero", "sentences": [{"sentence": "Quiniela de la Provincia: La Nocturna del s\u00e1bado 9 de enero", "source": "http://www.lmneuquen.com", "date": "2021-01-10T09:53:12.695909"}]}
    {"word": "la", "sentences": [{"sentence": "Quiniela de la Provincia: La Nocturna del s\u00e1bado 9 de enero", "source": "http://www.lmneuquen.com", "date": "2021-01-10T09:53:12.695909"}]}

Each line is a json object. You have to read it line by line, and transform into json
the read line. Why is that??? I expect the corpus to be a HUGE file, so, load it entirely 
into memory is impossible: it is better to read and process it line by line. 

And because json is a popular standard, I'thought that a line in json would be nice. 


