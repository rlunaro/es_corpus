#!/bin/bash
#
# corpus_extractor.sh
#
#

PYTHONIOENCODING=UTF-8

if [ -z "$corpus_extractor_home" ] 
then  
    corpus_extractor_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"
    PYTHONPATH="$corpus_extractor_home;$corpus_extractor_home/src"
    PYTHON_HOME="$corpus_extractor_home"
    PATH="$PYTHON_HOME/bin:$PATH"
    PYTHON_EXE="$PYTHON_HOME/bin/python"
fi

"$PYTHON_EXE" -u "$corpus_extractor_home/main.py" \
--config="config.yaml" \
--logging="logging.json" \
$1 $2 $3 $4 $5



