'''
Created on Jan 3, 2021

@author: rluna
'''
import unittest

from common import readConfig, getServer
from webSiteInfoProvider import WebSiteInfoProvider

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testWebSiteInfoProvider(self):
        localConfig = readConfig( '../config_local.yaml' )
        testConfig = readConfig( '../config_test.yaml' )
        wsInfo = WebSiteInfoProvider( user_agent = localConfig['user_agent'],
                                      max_wait_time_secs=10,
                                      default_crawl_delay = 3 )
        '''
        informacion que necesito: 
        1. última vez que lo visité 
        2. el can fetch, debe quedar expuesto
        
        '''
        wsInfo.canFetchOrWait( "https://es.wikipedia.org/wiki/Wikipedia:Portada" )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWebSiteInfoProvider']
    unittest.main()