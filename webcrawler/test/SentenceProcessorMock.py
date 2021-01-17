'''
Created on Jan 15, 2021

@author: rluna
'''

class SentenceProcessorMock(object):


    def __init__(self):
        self._sentenceList = []
    
    def isSentence(self, url, sentence ):
        return sentence in self._sentenceList
    
    def addSentence(self, url, sentence, wordList = None ): 
        self._sentenceList.append( sentence )
