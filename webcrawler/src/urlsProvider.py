'''
Created on Jan 1, 2021

@author: rluna
'''

import couchdb

class UrlsProviderReal(object):

    def __init__(self, db :couchdb.Database, urls_view):
        self.db = db
        self._urls_view = urls_view
    
    def __iter__(self):
        return self.db.iterview( self._urls_view, 100 )
    
class UrlsProviderMock(object):

    def __init__(self, urls_list ):
        self._urls_list = urls_list
    
    def __iter__(self):
        return iter(self._urls_list)

