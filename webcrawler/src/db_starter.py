'''
Created on Dec 17, 2020

@author: rluna
'''
import sys
import datetime
import logging
from bs4 import BeautifulSoup
import couchdb
import uuid

import sentences
from common import parseArguments, setupLogger, readConfig, getServer, getDatabaseConnection

def deleteDatabase( server, dbToDelete ):
    logging.info( f"deleting database {dbToDelete} if exists..." )
    if dbToDelete in server :
        server.delete( dbToDelete )

def createDatabase( server, dbToBeCreated ):
    logging.info( f"creating database {dbToBeCreated}" )
    server.create( dbToBeCreated )

def createView( dbConn, designDoc, viewName, viewFunction, reduceFunction = None ):
    data = {
            "_id": f"_design/{designDoc}",
            "views": {
                viewName: {
                    "map": viewFunction
                    }
            },
            "language": "javascript",
            "options": {"partitioned": False }
            }
    if reduceFunction : 
        designDoc['views'][viewName]['reduce'] = reduceFunction
    logging.info( f"creating view {designDoc}/{viewName}" )
    dbConn.save( data )

def addViewToDesignDocument( dbConn, designDoc, viewName, viewFunction, reduceFunction = None ):
    designDoc = dbConn.get( f"_design/{designDoc}" )
    designDoc['views'][viewName] =  { 'map' : viewFunction }
    if reduceFunction : 
        designDoc['views'][viewName]['reduce'] = reduceFunction
    logging.info( f"adding view {viewName} to design document {designDoc}" )
    dbConn.update( [designDoc] )

def deleteAllFoundationDocuments( db : couchdb.Database ):
    thereAreRecords = True
    while thereAreRecords :
        query = db.find( {'selector' : {
                            "source" : {
                                "$eq" : "foundation"
                                } 
                            },
                            "limit" : 10000000
                        } )
        thereAreRecords = False
        for row in query : 
            db.delete( row )
            thereAreRecords = True

def insertUrlList( db : couchdb.Database, urlList ):
    logging.info( "inserting url list..." )
    for url in urlList: 
        data = { '_id' : url,
                 'type' : 'url', 
                 'visited' : False }
        db.save( data )
        
def insertFoundationSentences( fileList ):
    for filename in fileList :
        logging.info( f"processing filename {filename}..." )
        processFile( filename, db )

def processFile( filename : str, db : couchdb.Database ):
    with open( filename, "rt", encoding = 'utf-8' ) as file : 
        htmlDoc = BeautifulSoup( file, 'html.parser' )
        # traverse all the contents of the document 
        print( filename )
        traverseTree( htmlDoc, db )
        
def traverseTree( node, db : couchdb.Database ):
    sizeOfBook = len(node.find_all('p'))
    paragraphs = 1
    for child in node.find_all('p') : 
        paragraph = ""
        printProgress( paragraphs, sizeOfBook )
        for string in child.stripped_strings: 
            paragraph = paragraph + " " + string
        for sentence in sentences.splitParagraph( paragraph ):
            # todo: add to couch db the stuf.....
            if sentence and sentence != "" : 
                now = datetime.datetime.now()
                doc = { '_id' : str(uuid.uuid4()), 
                        'type' : 'sentence', 
                        'sentence' : sentence, 
                        'source' : 'foundation', 
                        'date' : now.isoformat() }
                db.save( doc )
        paragraphs = paragraphs + 1
    print("")

def printProgress( partSize, totalSize, barSize = 40 ):
    progressSize = int((barSize * partSize) / totalSize)
    print( f"\r[{'#' * progressSize}{' ' * (barSize - progressSize)}]", end = '' )

def deleteAllWords( db : couchdb.Database ):
    for row in db.iterview( 'all_words/all_words', 100 ) :
        db.delete( row.value )

def processEntries( db : couchdb.Database ):
    totalSentences =  [x for x in db.iterview( 'sentences/sentences_count', 10 )][0].value
    sentenceCount = 1
    for entry in db.iterview( 'sentences/sentences', 100 ) :
        if sentenceCount % 1000 == 0 :
            printProgress( sentenceCount, totalSentences )
        for word in sentences.splitInWords( entry.value['sentence'] ) : 
            if word and word != "" :
                updateWordDocument( db, 
                                    word, 
                                    entry.value )
        sentenceCount = sentenceCount + 1
    print("") # to clear printProgress   

def updateWordDocument( db, word, entry ):
    sentence = { 'sentence' : entry['sentence'],
                 'source' : entry['source'],
                 'date' : entry['date']
               }
    if word in db : 
        wordDoc = db[word]
        wordDoc['sentences'].append( sentence )
    else: 
        # create the word document with the 
        # first sentence added
        now = datetime.datetime.now()
        wordDoc = { '_id' : word,
                   'type' : 'word',
                   'subtype' : 'foundation', 
                   'creation-date' : now.isoformat(), 
                   'sentences' : [ sentence ] }
    db.save( wordDoc )
    
if __name__ == '__main__':
    print("db_starter v.1.0");
    (localConfigFile, 
     configFile, 
    loggingFile) = parseArguments( sys.argv[1:] )
    setupLogger( loggingFile )
    localConfig = readConfig( localConfigFile )
    config = readConfig( configFile )
    
    server = getServer( localConfig )
    deleteDatabase( server, localConfig['db']['db'] )
    createDatabase( server, localConfig['db']['db'] )
 
    db = getDatabaseConnection( server, localConfig['db']['db'] )
    mapFunction = '''function (doc) {
                          if( doc.type == 'word')
                          emit(doc._id, doc);
                        }'''
    createView( db, "all_words", "all_words", mapFunction )
    addViewToDesignDocument( db, "all_words", "all_words_count", mapFunction, '_count')

    mapFunction = '''function (doc) {
                          if( doc.type == 'word' && doc.sentences.length >= 10 )
                          emit(doc._id, doc);
                        }'''
    addViewToDesignDocument( db, "all_words", "basic_vocab", mapFunction )

    mapFunction = '''function (doc) {
                  if( doc.type == 'word' )
                    emit(doc.sentences.length, 1);
                }'''
    addViewToDesignDocument( db, "all_words", "sentences_length", mapFunction, '_count' )
    
    mapFunction = '''function (doc) {
                        if( doc.type == 'sentence' )  
                            emit(doc._id, doc);
                    }'''
    createView( db, "sentences", "sentences", mapFunction )
    
    mapFunction = '''function (doc) {
      if( doc.sentence && !doc.procesed )
        emit(doc._id, doc);
    }'''
    addViewToDesignDocument( db, "sentences", "sentences_not_processed", mapFunction )
    
    mapFunction = '''function (doc) {
      if( doc.sentence && !doc.procesed )
        emit(doc._id, doc);
    }'''
    addViewToDesignDocument( db, "sentences", "sentences_not_processed_count", mapFunction, '_count' )
    
    mapFunction = '''function (doc) {
                        if( doc.type == 'sentence' )  
                            emit(doc._id, doc.sentence);
                    }'''
    addViewToDesignDocument( db, "sentences", "sentences_count", mapFunction, '_count' )
    
    mapFunction = '''function (doc) {
      if( doc.sentence !== null )
        emit( [doc.source, doc.sentence], doc._id);
    }'''
    addViewToDesignDocument( db, "sentences", "sentence_by_url_sentence", mapFunction )
    
    mapFunction = '''function(doc) {
        if( doc.type == 'url' && !doc.visited ) 
            emit( Math.random(), doc._id )
    }'''
    createView( db, "urls", "not_visited", mapFunction )
    
    mapFunction = '''function(doc) {
        if( doc.type == 'url' && doc.visited ) 
            emit( doc._id, doc.visited )
    }'''
    addViewToDesignDocument( db, "urls", "visited", mapFunction )
    
    mapFunction = '''function (doc) {
      if( doc.type == 'url')
        emit(doc._id, 1);
    }'''
    addViewToDesignDocument( db, "urls", "all", mapFunction )
    
    insertUrlList( db, config['urlList'] )
        
#     logging.info( "creating a vocabulary out of the sentences found in the dictionary" )
#     insertFoundationSentences( localConfig['file_list'] )
#     deleteAllWords( db )
#     logging.info( "Starting to create new words....")
#     print("Transforming sentences into words....")
#     processEntries( db )
    
    print("Finished")

    


