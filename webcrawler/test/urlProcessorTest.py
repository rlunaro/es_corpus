'''
Created on Jan 2, 2021

@author: rluna
'''
import unittest

from common import readConfig, getServer
from urlProcessor import UrlProcessorCouch

class Test(unittest.TestCase):


    def setUp(self):
        self.localConfig = readConfig( '../config_local.yaml' )
        self.testConfig = readConfig( '../config_test.yaml' )
        self.db = getServer( self.localConfig )[self.localConfig["db"]["db"]]
        self.up = UrlProcessorCouch( self.db )


    def tearDown(self):
        pass


    def testUrlProcessor(self):
        url = "https://www.example.com"
        self.up.deleteUrl( url )
        if not self.up.isUrl( url ):
            self.up.addUrl( url )
        self.assertTrue( self.up.isUrl( url ) )
        self.up.deleteUrl( url ) 
        self.assertFalse( self.up.isUrl( url ) )

    def secondTest(self):
        urlList = ["http://expreso.press",
            "http://lacronicavespertinodechilpancingo.blogspot.com",
            "http://monitoreconomico.org",
            "http://periodicociudadrealhoy.blogspot.com.es",
            "http://www.10minutos.com.uy",
            "http://www.12horas.com.mx",
            "http://www.16minutos.com",
            "http://www.2001.com.ve",
            "http://www.20minutos.es",
            "http://www.20minutos.es/cataluna",
            "http://www.20minutos.es/comunidad-valenciana",
            "http://www.24-7digital.com",
            "http://www.24-horas.mx",
            "http://www.24baires.com"]
        for url in urlList : 
            print( url )
            self.up.addUrl( url )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()