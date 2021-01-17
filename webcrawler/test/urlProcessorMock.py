'''
Created on Jan 15, 2021

@author: rluna
'''

class UrlProcessorMock(object):


    def __init__(self, db ):
        self.db = db
        self.urlSet = set()
        
    def isUrl(self, url ):
        return True
    
    def addUrl(self, url: str, visited = False ):
        if not url in self.urlSet : 
            self.urlSet.add( url )
    
    def deleteUrl(self, url ):
        self.urlSet.remove( url )
        
    def anotateUrlAsVisited(self, url ):
        return 
    
