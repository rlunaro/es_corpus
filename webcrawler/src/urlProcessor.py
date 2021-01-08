'''
Created on Jan 1, 2021

@author: rluna
'''
import couchdb
from threading import Lock
import time

class UrlProcessorCouch(object):

    def __init__(self, db : couchdb.Database):
        self._db = db
        self.lock = Lock()
    
    def isUrl(self, url ):
        for x in self._db.iterview( "urls/all", 10, key = url ):
            return x.id
        else: 
            return None
    
    def addUrl(self, url : str, visited = False):
        try:
            if not self.isUrl( url ) :
                doc = { '_id' : url,
                        'type' : 'url', 
                        'visited' : visited }
                self._db.save( doc )
        except couchdb.http.ResourceConflict : 
            # wait some time and try it again
            time.sleep( 1 )
            self.addUrl( url, visited )
        
    def deleteUrl(self, url : str ):
        try :
            self._db.delete( self._db[url] )
        except couchdb.http.ResourceNotFound: 
            pass # if the document is not found, the error can be safely be ignored

    def anotateUrlAsVisited(self, url ): 
        try :
            urlDoc = self._db[url]
            urlDoc['visited'] = True
            self._db.save( urlDoc )
        except couchdb.http.ResourceNotFound: 
            pass # if the document is not found, the error can be safely be ignored


