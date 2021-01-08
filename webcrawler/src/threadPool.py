'''
Created on Jan 2, 2021

@author: rluna
'''
import logging
import time
from threading import Thread

class ThreadPool(object):

    def __init__(self, poolSize):
        self.poolSize = poolSize
        self.threadList = []
        self.statusInfo = 0 
        
    def addWorker(self, thread : Thread ):
        if len( self.threadList ) >= self.poolSize : 
            self.waitUntilOneThreadHasFinished()
        self.threadList.append( thread )
        thread.start()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.waitUntilAllThreadsFinished()
        
    def close(self):
        self.waitUntilAllThreadsFinished()
        
    def waitUntilOneThreadHasFinished(self):
        freeSlots = 0
        while freeSlots == 0:
            for thread in self.threadList: 
                if not thread.is_alive() : 
                    self.threadList.remove( thread )
                    freeSlots = freeSlots + 1 
            if freeSlots > 0 : 
                break
            else : 
                time.sleep( 1 )
        self.logStatusInfo()
                
    def waitUntilAllThreadsFinished(self):
        for thread in self.threadList: 
            if thread.is_alive() : 
                thread.join()
     
    def logStatusInfo(self):
        logging.debug( f"Size of pool: {len(self.threadList)}" )
        threadsAlive = 0
        threadsOther = 0
        for thread in self.threadList :
            if thread.is_alive() : 
                threadsAlive = threadsAlive + 1
            else : 
                threadsOther = threadsOther + 1 
        logging.debug( f"       Alive: {threadsAlive}" )
        logging.debug( f"   Not alive: {threadsOther}")
 
