'''
Created on Jan 31, 2021

@author: rluna
'''
import unittest

from exclusion_rules import ExclusionRules

class ExclusionRulesTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testExclusionRules(self):
        rules = [ "(?i).*web\.archive\.org.*" ]
        ex = ExclusionRules( rules )
        self.assertTrue( ex.isExcluded( "https://web.archive.org/web/20160901170533/http://dechalaca.com/copaperu/provincial-sechura-2013/" ) )
        self.assertFalse( ex.isExcluded( "http://www.google.com" ) )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()