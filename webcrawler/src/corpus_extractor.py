'''
Created on Dec 17, 2020

@author: rluna
'''
import logging
import sys
import os.path
import couchdb
import json

from common import parseArguments, setupLogger, readConfig, getServer, getDatabaseConnection

WORDS_TXT = 'words.txt'
DISCARDED_WORDS_TXT = 'discarded_words.txt'
CORPUS_TXT = 'corpus.txt'

def getMinimumSentenceThreshold( db : couchdb.Database, sentences_length_view : str, threshold : int ):
    availableLengths = [ x.key for x in db.iterview( sentences_length_view, 2000000, group_level = 1 ) ]
    availableLengths.sort( reverse = True )
    logging.info( f'the available lengths per word are {availableLengths}')
    lastElement = round( len(availableLengths) * (threshold/100) )
    return availableLengths[lastElement]

def processEntries( db : couchdb.Database, corpus_result_dir : str, sentenceThreshold ):
    words_path = os.path.join( corpus_result_dir, WORDS_TXT )
    discarded_words_path = os.path.join( corpus_result_dir, DISCARDED_WORDS_TXT )
    corpus_path = os.path.join( corpus_result_dir, CORPUS_TXT )
    deleteFileIfExists( words_path ) 
    deleteFileIfExists( corpus_path )
    with open( words_path, "wt", encoding = "utf-8" ) as words: 
        with open( corpus_path, "wt", encoding = "utf-8" ) as corpus : 
            with open( discarded_words_path, "wt", encoding = "utf-8" ) as discarded :
                for row in db.iterview( 'all_words/all_words', 100 ) :
                    if len( row.value['sentences'] ) >= sentenceThreshold : 
                        words.write( f"{row.value['_id']}\n" )
                        writeCorpusInfo( db, corpus, row.value )
                    else: 
                        discarded.write( f"{row.value['_id']}\n" )

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
    logging.info("corpus extractor v.1.0")
    (localConfigFile, 
     configFile, 
    loggingFile) = parseArguments( sys.argv[1:] )
    setupLogger( loggingFile )
    localConfig = readConfig( localConfigFile )
    server = getServer( localConfig )
    db = getDatabaseConnection( server, localConfig['db']['db'] )
    sentenceThreshold = getMinimumSentenceThreshold( db, 'all_words/sentences_length', threshold=95 )
    logging.info( f"Processing word entries that have at least {sentenceThreshold}, the discarded words would be put into {DISCARDED_WORDS_TXT}")
    processEntries( db, localConfig['corpus_result_dir'], sentenceThreshold )
    print("Finished")
    logging.info( "finished" )




