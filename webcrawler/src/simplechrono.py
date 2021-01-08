'''
Created on Jan 4, 2021

@author: rluna
'''
import datetime 
import logging 

class SimpleChrono(object):
    '''
    measures the time taken by a process
    '''

    def __init__(self, onExitHook = None):
        self.startTime = datetime.datetime.now()
        self.endTime = datetime.datetime.now()
        self.onExitHook = onExitHook
    
    def __enter__(self):
        self.startTime = datetime.datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.endTime = datetime.datetime.now()
        if self.onExitHook: 
            self.onExitHook( self.endTime - self.startTime )
        else:
            logging.info( f"{( self.endTime - self.startTime ).seconds}" )
