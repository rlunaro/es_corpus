#!/bin/bash
#
# db_start.sh
#
#

PYTHONIOENCODING=UTF-8

if [ -z "$db_start_home" ] 
then  
    db_start_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"
    PYTHONPATH="$db_start_home;$db_start_home/src"
    PYTHON_HOME="$db_start_home"
    PATH="$PYTHON_HOME/bin:$PATH"
    PYTHON_EXE="$PYTHON_HOME/bin/python"
fi

"$PYTHON_EXE" -u "$db_start_home/main.py" \
--config="config.yaml" \
--logging="logging.json" \
$1 $2 $3 $4 $5



