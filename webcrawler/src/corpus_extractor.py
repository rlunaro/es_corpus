'''
Created on Dec 17, 2020

@author: rluna
'''
import sys
import os
import os.path
import couchdb
import json

from common import parseArguments, setupLogger, readConfig, getServer, getDatabaseConnection

WORDS_TXT = 'words.txt'
CORPUS_TXT = 'corpus.txt'

def processEntries( db : couchdb.Database, corpus_result_dir : str ):
    words_path = os.path.join( corpus_result_dir, WORDS_TXT )
    corpus_path = os.path.join( corpus_result_dir, CORPUS_TXT )
    deleteFileIfExists( words_path ) 
    deleteFileIfExists( corpus_path )
    with open( words_path, "wt", encoding = "utf-8" ) as words: 
        with open( corpus_path, "wt", encoding = "utf-8" ) as corpus : 
            for row in db.iterview( 'all_words/all_words', 100 ) :
                words.write( f"{row.value['_id']}\n" )
                writeCorpusInfo( db, corpus, row.value )

def deleteFileIfExists( path : str ): 
    if os.path.exists( path ): 
        os.remove( path )

def writeCorpusInfo( db, file, wordData ):
    data = {}
    data['word'] = wordData['_id']
    data['sentences'] = []
    for sentenceId in wordData['sentences'] : 
        sentenceData = db[sentenceId]
        data['sentences'].append( { 'sentence' : sentenceData['sentence'], 
                                    'source' : sentenceData['source'], 
                                    'date' : sentenceData['date'] } )
    file.write( json.dumps( data ) + "\n" )

if __name__ == '__main__':
    print("corpus extractor v.1.0");
    (localConfigFile, 
     configFile, 
    loggingFile) = parseArguments( sys.argv[1:] )
    setupLogger( loggingFile )
    localConfig = readConfig( localConfigFile )
    server = getServer( localConfig )
    db = getDatabaseConnection( server, localConfig['db']['db'] )
    processEntries( db, localConfig['corpus_result_dir'] )
    print("Finished")




