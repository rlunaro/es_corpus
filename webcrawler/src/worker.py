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

class SentenceData(object):
    pass

class Worker(Thread):

    CONTENT_TYPE = "Content-Type"
    TEXT_HTML = "text/html"
    
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
        self.languageToScan = 'es'
        self.minimumSentences = 3
        super().__init__()
        
    def run(self):
        self.urlProcessor.anotateUrlAsVisited( self.url )
        if self.webSiteInfoProvider.canFetchOrWaitErrorSafe( self.url ):
            headers = { 'User-Agent': self.userAgent }
            response = self._safeGet( self.url, headers )
            if response : 
                htmlDoc = BeautifulSoup( response.content, "html.parser" )
                newUrls = self._getUrlList( htmlDoc )
                paragraphsAnalized = self._paragraphAnalisys( self._getTexts( htmlDoc ) )
                if self._countLanguageSentences( paragraphsAnalized ) >= self.minimumSentences :
                    self._saveUrlList( self.url, newUrls )
                self._saveParagraphs( self.url, paragraphsAnalized)

    def _safeGet(self, url, headers ):
        response = None
        try:
            response = requests.get( url,
                                     verify = False, 
                                     timeout = 10, 
                                     headers = headers )
            if self.CONTENT_TYPE in response.headers : 
                contentType = response.headers[self.CONTENT_TYPE]
                logging.info( f"Content type: {contentType}")
                if self.TEXT_HTML in contentType : 
                    # only if is html the content will be returned
                    return response
            return None
        except Exception as ex : 
            logging.error( f"Exception getting url {url}" )
            logging.error( ex ) 
            return None
                    
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
    
    def _paragraphAnalisys(self, paragraphList ):
        result = []
        for paragraph in paragraphList : 
            sentenceList = sentences.splitParagraph( paragraph )
            for sentence in sentenceList: 
                sentenceData = SentenceData()
                sentenceData.sentence = sentence
                sentenceData.wordList = sentences.splitInWords( sentence )
                sentenceData.detectedLanguage = None
                if (len( sentenceData.wordList ) >= self.minimumWordsPerSentence ) : 
                    sentenceData.detectedLanguage = langdetect.detect( sentence ) 
                result.append( sentenceData )
        return result 
    
    def _countLanguageSentences(self, paragraphsAnalized ):
        scannedLang = 0
        for paragraphAnalized in paragraphsAnalized : 
            if paragraphAnalized.detectedLanguage == 'es' : 
                scannedLang = scannedLang + 1
        return scannedLang
           
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
    
    def _saveParagraphs(self, url, paragraphsAnalized ):
        for paragraphAnalized in paragraphsAnalized :
            if paragraphAnalized.detectedLanguage == 'es' :
                self.sentenceProcessor.addSentence( url, 
                                                    paragraphAnalized.sentence, 
                                                    paragraphAnalized.wordList )

    def _isNavigableString(self, tag):
        return isinstance(tag, NavigableString )



        