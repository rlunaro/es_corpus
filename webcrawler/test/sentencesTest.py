'''
Created on Jan 6, 2021

@author: rluna
'''
import unittest

from sentences import clearWord

class SentencesTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testClearWords(self):
        self.assertTrue( clearWord( "‘grande’") == "grande" )
        self.assertTrue( clearWord( "“yo") == "yo" )
        self.assertTrue( clearWord( "porcentaje%" ) == "porcentaje" )
        self.assertTrue( clearWord( "orgullosos”") == "orgullosos" )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()