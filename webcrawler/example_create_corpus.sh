#!/bin/bash
#
# create_corpus.sh
#
#

if [ -z "$create_corpus_home" ] 
then  
    create_corpus_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"
    PYTHONPATH="$create_corpus_home;$create_corpus_home/src"
    PYTHON_HOME="$create_corpus_home"
    PATH="$PYTHON_HOME/bin:$PATH"
    PYTHON_EXE="$PYTHON_HOME/bin/python"
fi

nice --adjustment=19 "$PYTHON_EXE" -u "$create_corpus_home/create_corpus.py" \
--local-config="config_local.yaml" \
--logging="logging.json" \
$1 $2 $3 $4 $5 > create_corpus.out



