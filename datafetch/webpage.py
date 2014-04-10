#! /usr/bin/python
import sys
import StringIO
import gzip
import socks
import socket
import urllib2
class KickAssURLBuilder:
	
	def __init__(self, search, category):
		#Variables used for URI generation.
		self.baseURI =  'http://kickass.to/usearch/'
		self.searchURI = 'category%3A*mutator*/?field=seeders&sorder=desc'  
		
		#User input variables
		self.search = search
		self.category = category
	
	def build(self):
		return self.baseURI + self.search + " " + self.searchURI.replace('*mutator*',self.category)

class PirateBayURLBuilder:
	def __init__(self, search, category):	
		#Variables used for URI generation
		self.baseURI = 'http://thepiratebay.se/search/'
		self.audioURI = '*mutator*/0/7/100'
		self.videoURI = '*mutator*/0/7/200'
		self.applicationURI = '*mutator*/0/7/300'
		self.otherURI = '*mutator*/0/7/600'

		#User input variables
		self.search = search
		self.category = category

	def build(self):
		categoryURI = ""
		if self.category.lower() == "audio" or self.category.lower() == "music":	
			categoryURI = self.audioURI
		elif self.category.lower() == "video" or self.category.lower() == "movie":
			categoryURI = self.videoURI
		
		elif self.category.lower() == "application" or self.category.lower() == "program" or self.category.lower() == "software":
			categoryURI = self.applicationURI
		else:
			categoryURI = self.otherURI
		return self.baseURI + categoryURI.replace('*mutator*', self.search)
		
class Content:
	def __init__(self, url):
		self.url = url

	def get(self):
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, "127.0.0.1", 9050)
		socket.socket = socks.socksocket
		self.url = self.url.replace(' ', '%20')
		
		if "http" not in str(self.url):	
			request = urllib2.Request("http://"+str(self.url))
		else:
			request = urllib2.Request(self.url)
		request.add_header('Accept-encoding', 'gzip')
		response = urllib2.urlopen(request)
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO.StringIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
			return data

		else:
			return response.read()
