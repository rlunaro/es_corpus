'''
Created on Jan 3, 2021

@author: rluna
'''
import logging
import urllib.parse
import urllib.robotparser
import datetime
import time
from threading import Lock

def now():
    return datetime.datetime.now()

class WebSiteInfo(object):
    
    def __init__(self, url ):
        self.url = ''
        self.siteLock = Lock()
        self.robotsInfo = None
        self.crawlDelay = 0
        self.lastRequest = now()
        

class WebSiteInfoProvider(object):

    def __init__(self, 
                 user_agent : str,
                 max_wait_time_secs : int = 10, 
                 default_crawl_delay : int = 5 ):
        self.user_agent = user_agent
        self.max_wait_time = max_wait_time_secs
        self.default_crawl_delay = default_crawl_delay
        self.websitesLock = Lock()
        self.websitesMap = {}
        self.webSiteInfo = None

    def canFetchOrWaitErrorSafe(self, url):
        try: 
            return self.canFetchOrWait( url ) 
        except Exception as ex:
            logging.error( "Error in call to canFetchOrWait")
            logging.error( ex ) 
            return True

    def canFetchOrWait(self, url):
        '''
        returns: 
        - true, if the specified url can be retrieved with no problem
        - false, if the specified url cannot be retrieved at all
        - waits until it can if the specified url must wait until the next 
          url is done 
        - gives up and return false if the specified url is greater than max_wait_time
        '''
        parsedUrl = urllib.parse.urlparse( url )
        if not parsedUrl.hostname in self.websitesMap :
            robotsAndCrawl = self._robotsAndCrawlInfo( parsedUrl )
            self.websitesLock.acquire()
            self.websitesMap[parsedUrl.hostname] = robotsAndCrawl
            self.websitesLock.release()
        siteInfo = self.websitesMap[parsedUrl.hostname]
        okByLastAccess = self._checkLastAccessOrGiveUp( siteInfo )
        okByRobots = siteInfo.robotsInfo.can_fetch( self.user_agent, url )
        return okByLastAccess and okByRobots
        
    def _checkLastAccessOrGiveUp(self, siteInfo ):
        giveUpCounter = 5
        okByTime = False
        while True:
            okByTime = (now() - siteInfo.lastRequest > datetime.timedelta( seconds = siteInfo.crawlDelay ) )
            if okByTime : 
                break
            time.sleep( siteInfo.crawlDelay )
            giveUpCounter = giveUpCounter - 1
            if giveUpCounter == 0 : 
                break
        siteInfo.lastRequest = now()
        return okByTime
        
    def _robotsAndCrawlInfo(self, parsedUrl ):
        wInfo = WebSiteInfo( parsedUrl.hostname )
        base = f"{parsedUrl.scheme}://{parsedUrl.hostname}/"
        robotsUrl = urllib.parse.urljoin( base, "robots.txt" )
        wInfo.robotsInfo = urllib.robotparser.RobotFileParser( robotsUrl )
        wInfo.robotsInfo.read()
        wInfo.crawlDelay = wInfo.robotsInfo.crawl_delay( self.user_agent )
        if not wInfo.crawlDelay : 
            wInfo.crawlDelay = self.default_crawl_delay
        # if read crawlDelay is very big, cut down to default crawl delay
        if wInfo.crawlDelay > (self.default_crawl_delay * 100) : 
            wInfo.crawlDelay = self.default_crawl_delay
        wInfo.lastRequest = now()
        return wInfo




            
