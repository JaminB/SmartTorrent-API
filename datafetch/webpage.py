#! /usr/bin/python
import sys
import StringIO
import gzip
import socks
import socket
import urllib2
class KickAssURLBuilder:
	#music, movie, tv, books, games, applications
	def __init__(self, search, category):
		#Variables used for URI generation.
		self.baseURI =  'http://kickass.to/usearch/'
		self.searchURI = 'category%3A*mutator*/?field=seeders&sorder=desc'  
		
		#User input variables
		self.search = search
		self.category = category
	
	def build(self):
	#	print self.baseURI + self.search + " " + self.searchURI.replace('*mutator*',self.category)
		if self.category.lower() == "any":
			return self.baseURI + self.search + " " + self.searchURI.replace('*mutator*','')
		return self.baseURI + self.search + " " + self.searchURI.replace('*mutator*',self.category)

class PirateBayURLBuilder:
	def __init__(self, search, category):	
		#Variables used for URI generation
		self.baseURI = 'http://thepiratebay.se/search/'
		self.audioURI = '*mutator*/0/7/100'
		self.videoURI = '*mutator*/0/7/200'
		self.tvURI = '*mutator*/0/7/205'
		self.gameURI = '*mutator*/0/7/400'
		self.bookURI = '*mutator*/0/7/601'
		self.applicationURI = '*mutator*/0/7/300'
		self.anyURI = '*mutator*/0/7/0'
		self.otherURI = '*mutator*/0/7/600'

		#User input variables
		self.search = search
		self.category = category

	def build(self):
		categoryURI = ""
		if self.category.lower() == "audio" or self.category.lower() == "music":	
			categoryURI = self.audioURI
		elif self.category.lower() == "video" or self.category.lower() == "videos" or self.category.lower() == "movie" or self.category.lower() == "movies":
			categoryURI = self.videoURI
		
		elif self.category.lower() == "application" or self.category.lower() == "applications" or self.category.lower() == "program" or self.category.lower() == "programs" or self.category.lower() == "software":
			categoryURI = self.applicationURI

		elif self.category.lower() == "tv" or self.category.lower() == "television":
			categoryURI = self.tvURI

		elif self.category.lower() == "books" or self.category.lower() == "book":
			categoryURI = self.booksURI

		
		elif self.category.lower() == "game" or self.category == "games":
			categoryURI = self.gameURI
		
		elif self.category.lower() == "other":
			categoryURI = self.otherURI
		
		else:
			categoryURI = self.anyURI

		return self.baseURI + categoryURI.replace('*mutator*', self.search)
		
class Content:
	def __init__(self, url):
		self.url = url

	def get(self):
		#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, "127.0.0.1", 9050)
		#socket.socket = socks.socksocket
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
