'''
Created on Jan 15, 2021

@author: rluna
'''

class WebSiteInfoProviderMock(object):

    def __init__(self, url ):
        self.url = url
        
    def canFetchOrWaitErrorSafe(self, url ):
        return self.canFetchOrWait( url )
    
    def canFetchOrWait(self, url):
        return True
    
    