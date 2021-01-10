#!/bin/bash
#
# extract_words.sh
#
#

if [ -z "$extract_words_home" ] 
then  
    extract_words_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"
    PYTHONPATH="$extract_words_home;$extract_words_home/src"
    PYTHON_HOME="$extract_words_home"
    PATH="$PYTHON_HOME/bin:$PATH"
    PYTHON_EXE="$PYTHON_HOME/bin/python"
fi

nice --adjustment=19 "$PYTHON_EXE" -u "$extract_words_home/extract_words.py" \
--local-config="config_local.yaml" \
--logging="logging.json" \
$1 $2 $3 $4 $5 > extract_words.out



