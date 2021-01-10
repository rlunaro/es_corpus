'''
Created on Dec 20, 2020

@author: rluna
'''
import unittest

from sentences import splitInWords
from bs4 import BeautifulSoup

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSplitInWords(self):
        sentence = "— Bien parece—respondió el galeote—"
        print( splitInWords( sentence ) )
        self.assertTrue( splitInWords( sentence ) == [ 'bien', 'parece', 'respondió', 'el', 'galeote' ] )

    def complexTest(self):
        html = '''    <p>
&mdash;Se trataba&mdash;a&ntilde;adi&oacute; Foja&mdash;de las varas que
toma o no toma cierta dama, hasta hoy muy respetada, y de los refuerzos
espirituales que su atribulada conciencia busca o no busca en la direcci&oacute;n
moral de don Ferm&iacute;n.... &iexcl;Je, je!...
        </p>'''
        htmlDoc = BeautifulSoup( html, 'html.parser' )
        for child in htmlDoc.find_all('p') : 
            paragraph = ""
            for string in child.stripped_strings: 
                paragraph = paragraph + " " + string
        print( splitInWords( paragraph ) )
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSplitInWords']
    unittest.main()