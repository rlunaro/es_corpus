'''
Created on Dec 18, 2020

@author: rluna
'''
import sys
import logging.config
import json
import getopt
import yaml 
import couchdb

def parseArguments( argumentList : list ):
    unixArgs = "c:l:"
    gnuArgs = ["config=", "local-config=", "logging="]
    # default values
    config_file = 'config.yaml'
    local_config = 'config_local.yaml'
    logging_file = 'logging.json'
    try : 
        args, values = getopt.getopt( argumentList, 
                                      unixArgs, 
                                      gnuArgs )
        for currentArgument, currentValue in args: 
            if currentArgument in ["--config", "c"] : 
                config_file = currentValue
            if currentArgument in ["--local-config", "c"] : 
                local_config = currentValue
            if currentArgument in ["--logging", "l"] :
                logging_file = currentValue
    except getopt.error as err:
        print( str(err) )
        sys.exit(2)
    return (local_config, config_file, logging_file)

def setupLogger( logging_file : str ):
    with open( logging_file, 'rt', encoding='utf-8') as log_file_json: 
        loggingConfig = json.load( log_file_json )
    logging.config.dictConfig( loggingConfig )
    
def readConfig( filepath : str ) :
    with open( filepath, encoding = 'utf-8' ) as config_file : 
        data = yaml.safe_load( config_file ) 
    return data

def getServer( configData ):
    url = f"{configData['db']['protocol']}://{configData['db']['username']}:{configData['db']['password']}@{configData['db']['host']}:{configData['db']['port']}"
    logging.info( f"trying to connect to {url.replace(configData['db']['password'],'SECRET')}")
    server = couchdb.Server( url )
    return server 

def getDatabaseConnection( server, dbName ):
    db = server[dbName]
    return db
