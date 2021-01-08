'''
Created on Jan 2, 2021

@author: rluna
'''
import random
import time
from threading import Thread

class MockWorker(Thread):

    def __init__(self,  
                 userAgentHeaders,
                 sentenceProcessor, 
                 urlProcessor,
                 minimumWordsPerSentence,
                 url):
        self.url = url
        super().__init__()
        
    def run(self):
        print( f"Starting worker {self.url}...." )
        timeToSleep = random.randint( 1, 2 )
        time.sleep( timeToSleep )
        print( f"done after {timeToSleep} seconds" )
    