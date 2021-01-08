'''
Created on Jan 2, 2021

@author: rluna
'''
import logging
import langdetect
import requests
import urllib3
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin, urlparse

import sentences
from threading import Thread

class Worker(Thread):

    def __init__(self, 
                 userAgent,
                 sentenceProcessor, 
                 urlProcessor,
                 webSiteInfoProvider,
                 minimumWordsPerSentence,
                 url ):
        urllib3.disable_warnings()
        self.userAgent = userAgent
        self.sentenceProcessor = sentenceProcessor
        self.urlProcessor = urlProcessor
        self.webSiteInfoProvider = webSiteInfoProvider
        self.minimumWordsPerSentence = minimumWordsPerSentence 
        self.url = url
        super().__init__()
        
    def run(self):
        if self.webSiteInfoProvider.canFetchOrWaitErrorSafe( self.url ):
            headers = { 'User-Agent': self.userAgent }
            response = self._safeGet( self.url, headers )
            if response : 
                htmlDoc = BeautifulSoup( response.content, "html.parser" )
                newUrls = self._getUrlList( htmlDoc )
                self._saveUrlList( self.url, newUrls )
                self._saveParagraphs( self.url, self._getTexts( htmlDoc ) )
                self.urlProcessor.anotateUrlAsVisited( self.url )

    def _safeGet(self, url, headers ):
        response = None
        try:
            response = requests.get( url,
                                     verify = False, 
                                     timeout = 10, 
                                     headers = headers )
        except Exception as ex : 
            logging.error( f"Exception getting url {url}" )
            logging.error( ex ) 
        return response
                    
    def _getUrlList( self, node ):
        urls_to_visit = []
        node_list = node.find_all( 'a' )
        node_list.extend( node.find_all( 'A') )
        for child in node_list : 
            if 'href' in child.attrs :
                urls_to_visit.append( child.attrs['href'] )
        return urls_to_visit
    
    def _getTexts(self, node ):
        texts = []
        node_list = node.find_all( "P" )
        node_list.extend( node.find_all( "p") )
        for child in node_list : 
            text = child.get_text()
            if text.strip() != "" :
                texts.append( text )
        return texts
      
    def _saveUrlList(self, urlBase, urlList ):
        for url in urlList : 
            if not self._isOnlyFragment( url ) :
                url = self._urlCanonicalize(urlBase, url)
                self.urlProcessor.addUrl( url )
    
    def _isOnlyFragment(self, url ):
        parsedUrl = urlparse( url )
        return (parsedUrl.scheme == '' 
            and parsedUrl.netloc == ''
            and parsedUrl.path == ''
            and parsedUrl.params == ''
            and parsedUrl.query == ''
            and parsedUrl.fragment != '' )
    
    def _urlCanonicalize(self, urlBase, url ):
        '''
        goes from "/wiki/Ayuda:Contenidos" to "https://es.wikipedia.org/wiki/Ayuda:Contenidos"
        '''
        return urljoin( urlBase, 
                             url )
    
    def _saveParagraphs(self, url, paragraphList ):
        for paragraph in paragraphList : 
            sentenceList = sentences.splitParagraph( paragraph )
            for sentence in sentenceList: 
                wordList = sentences.splitInWords( sentence )
                if (len( wordList ) >= self.minimumWordsPerSentence 
                and langdetect.detect( sentence ) == 'es' ):
                    self.sentenceProcessor.addSentence( url, sentence, wordList )

    def _isNavigableString(self, tag):
        return isinstance(tag, NavigableString )



        