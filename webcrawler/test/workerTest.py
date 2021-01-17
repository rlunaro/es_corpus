'''
Created on Jan 15, 2021

@author: rluna
'''
import unittest

from common import readConfig, getServer
from SentenceProcessorMock import SentenceProcessorMock
from urlProcessorMock import UrlProcessorMock
from webSiteInfoProviderMock import WebSiteInfoProviderMock
from worker import Worker 


class WorkerTest(unittest.TestCase):


    def setUp(self):
        self.localConfig = readConfig( '../config_local.yaml' )
        self.testConfig = readConfig( '../config_test.yaml' )

    def tearDown(self):
        pass

    def testBasic(self):
        url = "http://www.joseluisluna.com/index.php?option=com_content&view=article&id=97&Itemid=268"
        sp = SentenceProcessorMock()
        up = UrlProcessorMock( None )
        webSiteInfoProvider = WebSiteInfoProviderMock( None )
        w = Worker( userAgent = self.localConfig['user_agent'],
                    sentenceProcessor = sp, 
                    urlProcessor = up, 
                    webSiteInfoProvider = webSiteInfoProvider, 
                    minimumWordsPerSentence = 3, 
                    url = url )
        w.run()
        print( len(up.urlSet) )
        print( len(sp._sentenceList) )
        self.assertTrue( len(up.urlSet) == 95 )
        self.assertTrue( len(sp._sentenceList) == 43 )

    def testEnglish(self):
        url = "https://en.wikipedia.org/wiki/Physa_mezzalirai"
        sp = SentenceProcessorMock()
        up = UrlProcessorMock( None )
        webSiteInfoProvider = WebSiteInfoProviderMock( None )
        w = Worker( userAgent = self.localConfig['user_agent'],
                    sentenceProcessor = sp, 
                    urlProcessor = up, 
                    webSiteInfoProvider = webSiteInfoProvider, 
                    minimumWordsPerSentence = 3, 
                    url = url )
        w.run()
        print( len(up.urlSet) )
        print( len(sp._sentenceList) )
        self.assertTrue( len(up.urlSet) == 0 )
        self.assertTrue( len(sp._sentenceList) == 0 )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBasic']
    unittest.main()