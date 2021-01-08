'''
Created on Jan 1, 2021

@author: rluna
'''
import unittest

from common import readConfig, getServer
from sentenceProcessor import SentenceProcessorCouch

class SentenceProcessorTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSentenceProcessor(self):
        localConfig = readConfig( '../config_local.yaml' )
        testConfig = readConfig( '../config_test.yaml' )
        db = getServer( localConfig )[localConfig["db"]["db"]]
        sp = SentenceProcessorCouch( db )
        sp.addSentence( 'https://es.wikipedia.org', 'This is a test',
                        ['this', 'is', 'a', 'test'] )
        sp.addSentence( 'https://es.wikipedia.org', 'This is another test',
                        ['this', 'is', 'another', 'test'] )
        self.assertTrue( sp.isSentence('https://es.wikipedia.org', 'This is a test') )
        self.assertTrue( sp.isSentence('https://es.wikipedia.org', 'This is another test') )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'SentenceProcessorTest.testSentenceProcessor']
    unittest.main()