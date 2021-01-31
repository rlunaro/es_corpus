'''
main.py - a simple webcrawler

@author: rluna
'''

import sys
import couchdb

from urlsProvider import UrlsProviderReal
from common import parseArguments, setupLogger, readConfig, getServer
from engine import Engine
from sentenceProcessor import SentenceProcessorCouch
from urlProcessor import UrlProcessorCouch
from webSiteInfoProvider import WebSiteInfoProvider
from exclusion_rules import ExclusionRules

def getUrlList( node ):
    urls_to_visit = []
    node_list = node.find_all( 'a' )
    node_list.extend( node.find_all( 'A') )
    for child in node_list : 
        if 'href' in child.attrs :
            urls_to_visit.append( child.attrs['href'] )
    return urls_to_visit

def set_urls_as_not_visited( db : couchdb.Database, not_visited_view ):
    for url in db.iterview( not_visited_view, 100 ): 
        urlDoc = db[url.id]
        urlDoc['visited'] = False
        db.save(urlDoc)
                
if __name__ == '__main__':
    print("webcrawler v.1.0")
    (local_config_file, config_file, logging_file) = parseArguments( sys.argv[1:] )
    local_config = readConfig( local_config_file )
    setupLogger( logging_file )
    server = getServer( local_config )
    db = server[local_config["db"]["db"]]
    sp = SentenceProcessorCouch( db )
    up = UrlProcessorCouch( db )
    exclusions = ExclusionRules( config_file['exclusion_rules'] )
    webSiteInfoProvider = WebSiteInfoProvider( local_config['user_agent'], 
                                       max_wait_time_secs=10,
                                       default_crawl_delay=5 )
    engine = Engine( local_config['working_hours'],
                     local_config['max_jobs'],
                     local_config['user_agent'],
                     UrlsProviderReal(db, "urls/not_visited"), 
                     sp, 
                     up, 
                     webSiteInfoProvider, 
                     exclusions )
    engine.start()
    print("finished")



