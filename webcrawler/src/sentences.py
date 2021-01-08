'''
Created on Dec 30, 2020

@author: rluna
'''

import re 

def splitParagraph( paragraph ):
    sentences = re.split("[.!?]\s*", paragraph )
    # clean extra spaces and line breaks
    sentences = [ s.strip() for s in sentences ]
    sentences = [ re.sub( '\s+', ' ', s ) for s in sentences ]
    sentences = [ re.sub( '[\n\r]', ' ', s) for s in sentences ]
    return sentences

def splitInWords( sentence ):
    wordList = re.split("[’‘“”%'\",-:¿?¡!\(\)\s\.;«»\*—…\[\]\"\+]+", sentence )
    wordList = [ clearWord(x.lower()) for x in wordList if x != "" and isWord(x.lower()) ]
    return wordList

def isWord( word ):
    isWord = True
    for c in word : 
        if not c in "abcdefghijklmnopqrstuvwxyzáéíóúñäëïöüàèìòùç-" : 
            isWord = False
    return isWord
    
def clearWord( word ):
    out = ""
    for c in word : 
        if c in "abcdefghijklmnopqrstuvwxyzáéíóúñäëïöüàèìòùç-" : 
            out = out + c
    return out

