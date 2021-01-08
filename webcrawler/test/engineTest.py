'''
Created on Jan 2, 2021

@author: rluna
'''
import unittest

from engine import Engine

class Test(unittest.TestCase):


    def setUp(self):
        self._urlBase = "https://es.wikipedia.org/wiki/Wikipedia:Portada"
        self._urlList = [
                { "input" : "#mw-head", 
                  "output" : "https://es.wikipedia.org/wiki/Wikipedia:Portada#mw-head",
                  "is_only_fragment" : True },
                { "input" : "/wiki/Ayuda:Contenidos#test2", 
                  "output" : "https://es.wikipedia.org/wiki/Ayuda:Contenidos#test2",
                  "is_only_fragment" : False },
                { "input" : "/wiki/Ayuda:Contenidos", 
                  "output" : "https://es.wikipedia.org/wiki/Ayuda:Contenidos",
                  "is_only_fragment" : False },
                { "input" : "//donate.wikimedia.org/wiki/Special:FundraiserRedirector?utm_source=donate&utm_medium=sidebar&utm_campaign=C13_es.wikipedia.org&uselang=es", 
                  "output" : "https://donate.wikimedia.org/wiki/Special:FundraiserRedirector?utm_source=donate&utm_medium=sidebar&utm_campaign=C13_es.wikipedia.org&uselang=es",
                  "is_only_fragment" : False  },
                { "input" : "/wiki/Especial:CambiosEnEnlazadas/Wikipedia:Portada", 
                  "output" : "https://es.wikipedia.org/wiki/Especial:CambiosEnEnlazadas/Wikipedia:Portada",
                  "is_only_fragment" : False  },
                { "input" : "//commons.wikimedia.org/wiki/Special:UploadWizard?uselang=es", 
                  "output" : "https://commons.wikimedia.org/wiki/Special:UploadWizard?uselang=es",
                  "is_only_fragment" : False  },
                { "input" : "https://www.wikidata.org/wiki/Special:EntityPage/Q5296", 
                  "output" : "https://www.wikidata.org/wiki/Special:EntityPage/Q5296",
                  "is_only_fragment" : False  },
                { "input" : "/w/index.php?title=Especial:Libro&bookcmd=book_creator&referer=Wikipedia%3APortada", 
                  "output" : "https://es.wikipedia.org/w/index.php?title=Especial:Libro&bookcmd=book_creator&referer=Wikipedia%3APortada",
                  "is_only_fragment" : False  }]


    def tearDown(self):
        pass


    def testUrlCanonicalize(self):
        e = Engine( None, None, None )
        for url in self._urlList : 
            print( url["input"] )
            canonical = e._urlCanonicalize( self._urlBase, 
                                 url["input"] )
            print( canonical )
            self.assertTrue( canonical == url["output"] )
            self.assertTrue( e._isOnlyFragment( url["input"] ) == url["is_only_fragment"])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUrlCanonicalize']
    unittest.main()