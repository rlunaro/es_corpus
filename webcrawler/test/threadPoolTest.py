'''
Created on Jan 2, 2021

@author: rluna
'''
import unittest
from mockWorker import MockWorker
from threadPool import ThreadPool

class ThreadPoolTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSingleThread(self):
        w = MockWorker( None, None, None, "first thread" )
        w.start() 
        w.join()
        
    def testThreadPool(self):
        allTheThreads = []
        with ThreadPool( 10 ) as tp: 
            for i in range(200):
                w = MockWorker( None, None, None, None, f"Thread {i}" )
                allTheThreads.append( w )
                tp.addWorker( w )
        for thread in allTheThreads: 
            self.assertFalse( thread.is_alive() )



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ThreadPoolTest.testThread']
    unittest.main()