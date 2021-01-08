'''
Created on Dec 30, 2020

@author: rluna
'''
import logging
import datetime 
import time

from worker import Worker
from threadPool import ThreadPool

class Engine():
    
    def __init__(self, 
                 working_hours,
                 max_jobs, 
                 user_agent,
                 urls_provider,
                 sentenceProcessor, 
                 urlProcessor,
                 webSiteInfoProvider ):
        self.working_hours = working_hours
        self.user_agent = user_agent
        self.urls_provider = urls_provider
        self.sentenceProcessor = sentenceProcessor
        self.urlProcessor = urlProcessor
        self.webSiteInfoProvider = webSiteInfoProvider
        self.MINIMUM_WORDS_PER_SENTENCE = 6
        self.max_jobs = max_jobs
        
    def start(self):
        with ThreadPool( self.max_jobs ) as tp :
            for url_to_visit in self.urls_provider : 
                logging.info( f"visiting url {url_to_visit.value}..." )
                try:
                    self._waitUntilWorkingHour()
                    w = Worker( self.user_agent,
                                self.sentenceProcessor, 
                                self.urlProcessor, 
                                self.webSiteInfoProvider,
                                self.MINIMUM_WORDS_PER_SENTENCE, 
                                url_to_visit.value )
                    tp.addWorker( w )
                except Exception as ex:
                    logging.error( f"Error fetching url {url_to_visit.value}") 
                    logging.error( ex )
    
    def _waitUntilWorkingHour(self):
        now = datetime.datetime.now()
        while not now.hour in self.working_hours: 
            logging.info( "Sleeping (webcrawler)...")
            time.sleep( 10 * 60 )

        


    

