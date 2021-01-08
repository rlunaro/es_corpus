'''
Created on Dec 30, 2020

@author: rluna
'''
import unittest
import langdetect

from common import readConfig, getServer


class LanguageIdentifierTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def basicTest(self):
        localConfig = readConfig( '../config_local.yaml' )
        testConfig = readConfig( '../config_test.yaml' )
        db = getServer( localConfig )[localConfig["db"]["db"]]
        for sentence in testConfig['sentences_and_language']['es'] :
            print( sentence )
            print( langdetect.detect(sentence) )
            self.assertTrue( langdetect.detect(sentence) == 'es' )
        for sentence in testConfig['sentences_and_language']['pt'] :
            print( sentence )
            print( langdetect.detect(sentence) )
            self.assertTrue( langdetect.detect(sentence) == 'pt' )
        for sentence in testConfig['sentences_and_language']['cat'] :
            print( sentence )
            print( langdetect.detect(sentence) )
            self.assertTrue( langdetect.detect(sentence) == 'ca' )
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'LanguageIdentifierTest.basicTest']
    unittest.main()