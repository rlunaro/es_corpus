# -*- coding: utf8 -*-
'''
Created on 24 abr. 2020

@author: rlunaro
'''
import unittest


class Resource(object):
    
    def __init__(self):
        pass
    
    def open(self):
        print("open")
        return self
        
    def __enter__(self):
        return self.open()
        
    def close(self):
        print("close")
    
    def __exit__(self, type, value, tb ):
        self.close()  

class OpenCloseTest(unittest.TestCase):

    def test(self):
        with Resource() as pepe:
            print( pepe )
            
        print("outside the with")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()