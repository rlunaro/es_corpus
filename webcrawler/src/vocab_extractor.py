'''
Created on Dec 17, 2020

@author: rluna
'''
import sys
import couchdb

from common import parseArguments, setupLogger, readConfig, getDatabaseConnection

def processEntries( db : couchdb.Database ):
    for row in db.iterview( 'all_words/all_words', 100 ) :
        print(  row.value['word'] )


if __name__ == '__main__':
    print("vocab_extractor v.1.0");
    (localConfigFile, 
     configFile, 
    loggingFile) = parseArguments( sys.argv[1:] )
    setupLogger( loggingFile )
    localConfig = readConfig( localConfigFile )
    db = getDatabaseConnection( localConfig )
    processEntries( db )
    print("Finished")




