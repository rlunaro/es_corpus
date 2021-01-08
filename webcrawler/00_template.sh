#!/bin/bash
#
# 00_template.sh
#
#

PYTHONIOENCODING=UTF-8

if [ -z "$00_template_home" ] 
then  
    00_template_home="PUT-HERE-THE-HOME-OF-YOUR-APPLICATION"
    PYTHONPATH="$00_template_home;$00_template_home/src"
    PYTHON_HOME="$00_template_home"
    PATH="$PYTHON_HOME/bin:$PATH"
    PYTHON_EXE="$PYTHON_HOME/bin/python"
fi

"$PYTHON_EXE" -u "$00_template_home/main.py" \
--config="config.yaml" \
--logging="logging.json" \
$1 $2 $3 $4 $5



