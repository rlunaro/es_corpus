'''
Created on Dec 17, 2020

@author: rluna
'''
import sys
import datetime
import time
import logging
import couchdb

from sentences import clearWord
from common import parseArguments, setupLogger, readConfig, getServer, getDatabaseConnection

def processEntries( db : couchdb.Database, sleepHourList : list ):
    totalSentences =  [x for x in db.iterview( 'sentences/sentences_not_processed_count', 10 )][0].value
    sentenceCount = 1
    for entry in db.iterview( 'sentences/sentences_not_processed', 100 ) :
        waitWhileSleepHour( sleepHourList ) 
        if sentenceCount % 1000 == 0 :
            printProgress( sentenceCount, totalSentences )
        wordSet = { word for word in entry.value["word_list"] if word != "" }
        for word in wordSet:
            clearedWord = clearWord( word )
            if clearedWord != "" :
                updateWordDocument( db, 
                                    clearedWord, 
                                    entry.value )
        sentenceCount = sentenceCount + 1
    print("") # to clear printProgress
    
def waitWhileSleepHour( sleepHourList : list ):
    now = datetime.datetime.now()
    while now.hour in sleepHourList: 
        logging.info( "Sleeping (create_corpus)...")
        time.sleep( 10 * 60 )

def updateWordDocument( db, word, entry ):
    if word[0] == '_' :
        return
    if word in db : 
        wordDoc = db[word]
        wordDoc['sentences'].append( entry['_id'] )
    else: 
        # create the word document with the 
        # first sentence added
        now = datetime.datetime.now()
        wordDoc = { '_id' : word,
                   'type' : 'word',
                   'subtype' : 'foundation', 
                   'creation-date' : now.isoformat(), 
                   'sentences' : [ entry['_id'] ] }
    db.save( wordDoc )

def printProgress( partSize, totalSize, barSize = 40 ):
    progressSize = int((barSize * partSize) / totalSize)
    print( f"\r[{'#' * progressSize}{' ' * (barSize - progressSize)}]", end = '' )

if __name__ == '__main__':
    print("create_corpus v.1.0");
    (localConfigFile, 
     configFile, 
    loggingFile) = parseArguments( sys.argv[1:] )
    setupLogger( loggingFile )
    localConfig = readConfig( localConfigFile )
    config = readConfig( configFile )
    
    server = getServer( localConfig )
    db = getDatabaseConnection( server, localConfig['db']['db'] )

    logging.info( "Starting to create new words....")
    print("Transforming sentences into words....")
    while True : 
        processEntries( db, localConfig['working_hours'] )
    
    print("Finished")




