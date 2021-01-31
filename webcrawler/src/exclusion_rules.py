'''
Created on Jan 31, 2021

@author: rluna
'''
import logging
import re 

class ExclusionRules(object):

    def __init__(self, exclusionsList ):
        self.exclusionsList = exclusionsList
        
    def isExcluded(self, url):
        for rule in self.exclusionsList:
            if re.search( rule, url ) :
                logging.info( f"{url} is excluded" )
                return True
        return False

