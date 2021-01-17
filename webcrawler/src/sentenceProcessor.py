'''
Created on Jan 1, 2021

@author: rluna
'''
import couchdb
import uuid
import datetime


class SentenceProcessorCouch(object):
    
    def __init__(self, db : couchdb.Database):
        self._db = db
    
    def isSentence(self, url, sentence):
        for x in self._db.iterview( "sentences/sentence_by_url_sentence", 10, key = [url,sentence]) : 
            return x.value
        else:
            return None
    
    def addSentence(self, url, sentence, wordList = None ):
        if not self.isSentence( url, sentence ): 
            now = datetime.datetime.now()
            doc = { '_id' : str(uuid.uuid4()),
                    'type' : 'sentence', 
                    'sentence' : sentence, 
                    'word_list' : wordList, 
                    'source' : url, 
                    'date' : now.isoformat() }
            self._db.save( doc )

