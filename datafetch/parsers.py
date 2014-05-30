#! /usr/bin/python
from converters import date
class SearchCache:
#Object to hold all torrent search data (titles, magnetlinks, sizes, seeds, leeches, and infoLinks)	
	def __init__(self):
		self.magnetLinks = []
		self.titles = []
		self.seeds = []
		self.leeches = []
		self.sizes = []
		self.infoLinks = []
	
	def add_magnet_link(self, magnetLink):
		self.magnetLinks.append(magnetLink)
	
	def add_title(self, title):
		self.titles.append(title)
	
	def add_seed(self, seed):
		self.seeds.append(seed)
	
	def add_leech(self, leech):
		self.leeches.append(leech)
	
	def add_size(self, size):
		self.sizes.append(size)
	
	def add_info_link(self, infoLink):
		self.infoLinks.append(infoLink)
		
	def get_magnet_links(self):
		return self.magnetLinks
	
	def get_titles(self):
		return self.titles	

	def get_seeds(self):
		return self.seeds
	
	def get_leeches(self):
		return self.leeches

	def get_sizes(self):
		return self.sizes
	
	def get_info_links(self):
		return self.infoLinks
class InfoCache:
	#Cache to store data from infoLinks (comments, languages, and numberOfFiles)
	def __init__(self):
		self.comments = []
		self.languages = "Unknown"
		self.numberOfFiles = 0
		self.date = "Unknown"
	
	def add_comment(self, comment):
		self.comments.append(comment)
	
	def add_language(self, language):
		self.languages = language
	
	def add_number_of_files(self, numberOfFiles):
		self.numberOfFiles = numberOfFiles
	
	def add_date(self, date):
		self.date = date

	def get_comments(self):
		return self.comments

	def get_languages(self):
		return self.languages

	def get_number_of_files(self):
		return self.numberOfFiles
	
	def get_date(self):
		return self.date

class KickAssSearchParser:
	#Pulls relevant data off the search page stores in cache
	def __init__(self, webpage):
		self.webpage = webpage
		self.cache = SearchCache()
		self.cacheSize = 0

	def build_cache(self):
		#Strings for finding magnetlinks
		searchMagTag =  '<a title="Torrent magnet link"' 
		endMagText = 'class="imagnet icon16"><span></span></a>'
		#Strings for finding titles
		searchTitleTag = '<strong class="red">'

		#Strings for finding sizes
		searchSizeTag = '<td class="nobr center">'
		endSizeText = '</span></td>'

		#Strings for finding seeds
		searchSeedTag = '<td class="green center">'
		
		#Strings for finding leaches
		searchLeechTag = '<td class="red lasttd center">'

		#Strings for finding comment-pages
		searchInfoLinks = 'class="torType'

		lines = self.webpage.split('\n')
		for line in lines:
			if searchTitleTag in line:
				self.cacheSize += 1
				p1 = line.split('class="cellMainLink">')
				sanitized = p1[1].replace('<strong class="red">',"").replace('</strong>',"").replace('</a>',"")
				self.cache.add_title(sanitized)
			if searchMagTag in line:
				sanitized = line.replace(endMagText, "").replace('href=',"").replace(searchMagTag, "").replace('"',"").replace('%3A1337',"").strip()
				self.cache.add_magnet_link(sanitized)
			if searchSizeTag in line:
				p1 = line.split('<span>')
				sanitized = p1[0].replace(searchSizeTag,"").strip() + " " + p1[1].replace(endSizeText,"")
				self.cache.add_size(sanitized)
			if searchSeedTag in line:
				sanitized = int(line.replace(searchSeedTag,"").replace('</td>',"").strip())
				self.cache.add_seed(sanitized)
			
			if searchLeechTag in line:
				sanitized = int(line.replace(searchLeechTag,"").replace('</td>',"").strip())
				self.cache.add_leech(sanitized)

			if searchInfoLinks in line:
				p1 = line.split('class=')
				sanitized = "http://kickass.to"+p1[0].replace("<a href=","").replace('"',"").strip()
				self.cache.add_info_link(sanitized)


	def get_magnet_links(self):
		return self.cache.get_magnet_links()
	
	def get_titles(self):
		return self.cache.get_titles()

	def get_seeds(self):
		return self.cache.get_seeds()
	
	def get_leeches(self):
		return self.cache.get_leeches()
	
	def get_sizes(self):
		return self.cache.get_sizes()
	
	def get_info_links(self):
		return self.cache.get_info_links()
	
	def get_cache(self):
		return self.cache
	
	def size(self):
		return self.cacheSize

class KickAssInfoLinkParser:
	#Parses Information pages -- containing comments
	def __init__(self, webpage):
		self.webpage = webpage
		self.cache = InfoCache()
		self.cacheSize = 0
		
	def build_cache(self):
		#String for finding comments
		searchRatingTag = 'audio: '
		searchCommentTag = 'class="commentText botmarg5px topmarg5px"'	
		#String for finding number of files
		searchNumberOfFilesTag = '<td class="torFileName"'
		
		#String for finding language
		searchLanguageTag = '<span id="lang_'	
		
		#String for finding dates
		searchDateTag = "Added on"
		searchDateTag2 = "by <span"

		lines = self.webpage.split('\n')
		numberOfFiles = 0
		temp = ''
		commentOnLine = False
		for line in lines:
			if commentOnLine:
				self.cache.add_comment(line)
				commentOnLine = False
			if searchRatingTag in line:
				p1 = line.split('<span>')
				if len(p1) > 1:
					audio = p1[1].replace('<span>',"").replace('</span>',"").replace("<div>","").replace("</div>","").strip()
					video = p1[2].replace('<span>',"").replace('</span>',"").replace("<div>","").replace("</div>","").strip()
					self.cache.add_comment(audio)
					self.cache.add_comment(video)
			if searchCommentTag in line:
				commentOnLine = True
			if searchNumberOfFilesTag in line:	
				numberOfFiles += 1
			
			if searchLanguageTag in line:
				p1 = line.split('>')
				temp = p1[1]
				self.cache.add_language(temp)
			if searchDateTag in line and searchDateTag2 in line:
				p1 = line.split(" ")
				if len(p1[4]) != 2:
					convDate = date(p1[2].strip() + " " + p1[3].replace(",","").strip()+ " " + p1[4].strip()).convert()
					
				else:
					convDate = date(p1[2].strip() + " " + "1"+ " " + p1[5].strip()).convert()
				self.cache.add_date(convDate)
	
		self.cache.add_number_of_files(numberOfFiles)

	def get_comments(self):
		return self.cache.get_comments()
	
	def get_languages(self):
		return self.cache.get_languages()
	
	def get_number_of_files(self):
		return self.cache.get_number_of_files()

	def get_date(self):
		return self.cache.get_date()
	
	def get_cache(self):
		return self.cache

class PirateBaySearchParser:	
	#Pulls relevant data off the search page stores in cache
	def __init__(self, webpage):
		self.webpage = webpage
		self.cache = SearchCache()
		self.cacheSize = 0
	
	def build_cache(self):
		#Strings for finding magnet links
		searchMagTag = '/static/img/icon-magnet.gif'
		
		#Strings for finding titles
		searchTitleTag = 'class="detLink"'
		
		#Strings for finding sizes
		searchSizeTag = 'class="detDesc"'

		#Strings for finding seeds and leeches
		searchSeedLeechTag = '<td align="right">'
		
		#Strings for finding comment-pages
		searchInfoLinkTag = 'class="detName"'
	
		lines = self.webpage.split('\n')
		
		isSeed = True
		for line in lines:
			if searchMagTag in line:
				p1 = line.split('"')
				sanitized = p1[1].replace("%3A1337", "")
				self.cache.add_magnet_link(sanitized)
			
			if searchTitleTag in line:
				self.cacheSize += 1
				p1 = line.split("title=")
				p2 = p1[1].split(">")
				sanitized = p2[1].replace("</a", "")
				self.cache.add_title(sanitized)
			
			if searchSizeTag in line:
				p1 = line.split(",")
				sanitized =  p1[1].replace('&nbsp;',"").replace("Size ", "").replace ('i', "").replace('M', ' M').replace('G', ' G').replace('K', ' K').strip()
				self.cache.add_size(sanitized)
			if searchSeedLeechTag in line:
				sanitized = int(line.replace(searchSeedLeechTag, "").replace("</td>", "").strip())
				if isSeed:
					self.cache.add_seed(sanitized)
				else:
					self.cache.add_leech(sanitized)
				isSeed = not isSeed
			if searchInfoLinkTag in line:
				p1 = line.split("href=")
				p2 = p1[1].split('"')
				sanitized = "http://piratebay.net" + p2[1] 
				self.cache.add_info_link(sanitized)
	
	def get_magnet_links(self):
		return self.cache.get_magnet_links()
	
	def get_titles(self):
		return self.cache.get_titles()

	def get_seeds(self):
		return self.cache.get_seeds()
	
	def get_leeches(self):
		return self.cache.get_leeches()
	
	def get_sizes(self):
		return self.cache.get_sizes()
	
	def get_info_links(self):
		return self.cache.get_info_links()
	
	def get_cache(self):
		return self.cache
	
	def size(self):
		return self.cacheSize
class PirateBayInfoLinkParser:
	#Pulls relevant data off the info page stores in cache
	def __init__(self, webpage):
		self.webpage = webpage
		self.cache = InfoCache()
		self.cacheSize = 0
	
	def build_cache(self):
		#Strings for finding languages
		searchTextLanguageTag = '<dt>Texted language(s):</dt>'
		searchSpokenLanguageTag = '<dt>Spoken language(s):</dt>'
		languageOnLine = False
		
		#Strings for finding number of files
		searchNumberOfFilesTag = '<dt>Files:</dt>'
		numberOfFilesOnLine = False
		lineCountFromTag = 0
		lines = self.webpage.split('\n')
		languages = ""

		#Strings for finding comments
		searchCommentTag ='<div class="comment">'
		commentsOnLine = False
		
		#Strings for finding dates
		searchDateTag = '<dt>Uploaded:</dt>'
		dateOnLine = False

		for line in lines:
			if languageOnLine:
				sanitized = line.replace("<dd>","").replace("</dd>", "").strip()
				p1 = []
				if "," in sanitized:
					p1 = sanitized.split(",")	
				if len(p1) > 0:
					for element in p1:
						if element not in languages:
							languages += element
						languageOnLine = False
				else:
					if sanitized not in languages:
						languages += sanitized + " "
					languageOnLine = False
			if numberOfFilesOnLine:
				lineCountFromTag += 1
				if lineCountFromTag == 5:
					numberOfFilesOnLine = False
					p1 = line.split(">")
					sanitized = int(p1[1].replace("</a","").strip())
					self.cache.add_number_of_files(sanitized)
					lineCountFromTag = 0
			if commentsOnLine:
				comment = line
				self.cache.add_comment(comment)
				commentsOnLine = False
			if searchTextLanguageTag in line:
				languageOnLine = True
			if searchSpokenLanguageTag in line:
				languageOnLine = True
			if searchNumberOfFilesTag in line:
				numberOfFilesOnLine = True
			if searchCommentTag in line:
				commentsOnLine = True
			if dateOnLine:
				p1 = line.split(" ")
				sanitized = p1[0].replace("<dd>","").strip()
				self.cache.add_date(sanitized)	
				dateOnLine = False	
			if searchDateTag in line:
				dateOnLine = True
					
				
				
		if languages == "":
			languages = "Unknown"
		self.cache.add_language(languages)
	
	def get_comments(self):
		return self.cache.get_comments()
	
	def get_number_of_files(self):
		return self.cache.get_number_of_files()

	def get_languages(self):
		return self.cache.get_languages()
	
	def get_date(self):
		return self.cache.get_date()

