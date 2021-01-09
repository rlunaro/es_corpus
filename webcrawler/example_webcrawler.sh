#!/bin/bash
#
# webcrawler.sh
#
#

if [ -z "$webcrawler_home" ] 
then  
    webcrawler_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"
    PYTHONPATH="$webcrawler_home;$webcrawler_home/src"
    PYTHON_HOME="$webcrawler_home"
    PATH="$PYTHON_HOME/bin:$PATH"
    PYTHON_EXE="$PYTHON_HOME/bin/python"
fi

"$PYTHON_EXE" -u "$webcrawler_home/webcrawler.py" \
--local-config="config_local.yaml" \
--config="config.yaml" \
--logging="logging.json" \
$1 $2 $3 $4 $5 > webcrawler.out




