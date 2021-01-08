'''
Created on Dec 30, 2020

@author: rluna
'''

import sentences

class LanguageIdentifier(object):


    def __init__(self, foundation_words ):
        self.foundation_words = foundation_words
        
    def identify(self, sentence ): 
        '''
        a sentence will be in a given language if: 
            if it has more or equal than 10 words, at least 80 must be in the dictionary
            if it has less than 10 words, all the words must be in the dictionary
        '''
        wordList = sentences.splitInWords( sentence )
        areInDict = [ w for w in wordList if w in self.foundation_words ]
        print( f"{(len(areInDict) / len(wordList))=}" )
        if len(wordList) >= 10 :
            return len(areInDict) / len(wordList) >= 0.35
        else : 
            return len(wordList) == len(areInDict)
