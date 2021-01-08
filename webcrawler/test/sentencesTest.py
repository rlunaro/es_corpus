'''
Created on Jan 6, 2021

@author: rluna
'''
import unittest

from sentences import clearWord, splitInWords

class SentencesTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testSplitInWords(self):
        self.assertTrue( splitInWords( "Con Solo €250 en Acciones de #Amazon" ) == ["con", "solo", "en", "acciones", "de" ] )
        self.assertTrue( splitInWords( "No salgo de casa😩") == ["no", "salgo", "de"] )
        self.assertTrue( splitInWords( "A Valladolid llega el sábado❄️❄️❄️") == ["a", "valladolid", "llega", "el"])

    def testClearWords(self):
        self.assertTrue( clearWord( "‘grande’") == "grande" )
        self.assertTrue( clearWord( "“yo") == "yo" )
        self.assertTrue( clearWord( "porcentaje%" ) == "porcentaje" )
        self.assertTrue( clearWord( "orgullosos”") == "orgullosos" )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()