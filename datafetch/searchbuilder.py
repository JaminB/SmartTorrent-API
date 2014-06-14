#!/usr/bin/python 
import sys
import time
import json
from multiprocessing.dummy import Pool as ThreadPool
from webpage import KickAssURLBuilder 
from webpage import Content
from parsers import KickAssSearchParser
from parsers import KickAssInfoLinkParser
from parsers import PirateBaySearchParser
from parsers import PirateBayInfoLinkParser
from webpage import PirateBayURLBuilder
from analysis import CommentAnalysis

class ResultCache:
	#Object to hold all data relevant to search including metadata such as comments, languages, and number of files
	def __init__(self):
		self.magnetLinks = []
		self.titles = []
		self.seeds = []
		self.leeches = []
		self.sizes = []
		self.infoLinks = []
		self.comments = []
		self.overallRating = []
		self.commentAnalysis = []
		self.languages = []
		self.numberOfFilesList = []
		self.dates = [] 
	def __str__(self):
		return str(self.titles) + str(self.magnetLinks) + str(self.seeds) + str(self.leeches) + str(self.sizes) + str(self.infoLinks) + str(self.comments) + str(self.languages)
	
	def _get_magnet_hashes(self):
		#Returns a list of all the magnet hashes in a given search
		magHashes = []
		for link in self.magnetLinks:
			p1 = link.split('&')
			hash = p1[0].replace("magnet:?xt=urn:btih:","").strip().lower()
			magHashes.append(hash)
		return magHashes
	
	def _get_duplicate_hashes(self):
		#Returns a list of all duplicate hashes
		duplicates = []
		hashes = self._get_magnet_hashes()
		for i in range(0, len(hashes)):
			for j in range(i,len(hashes)):
				if i != j:
					if hashes[i] == hashes[j]:
						duplicates.append(hashes[i])
		return duplicates
	def _get_duplicate_hash_first_occurences(self):
		#Gets all the indexes of first occurences of duplicate hashes
		duplicates = self._get_duplicate_hashes()
		hashes = self._get_magnet_hashes()
		firstOccurences = []
		for duplicate in duplicates:
			firstOccurences.append(hashes.index(duplicate))
		return firstOccurences

	def de_duplicate_cache(self):
		#Finds duplicate data using magnet hashes, removes this duplicate data and aggregate comments to first occurence.
		dTitles = self.titles
		dMagnetLinks = self.magnetLinks
		dSeeds = self.seeds
		dLeeches = self.leeches
		dSizes = self.sizes
		dInfoLinks = self.infoLinks
		dComments = self.comments
		dLanguages = self.languages
		dNumberOfFilesList = self.numberOfFilesList
		dDates = self.dates
		hashes = self._get_magnet_hashes()
		markedHashes = []
		duplicates = self._get_duplicate_hashes()
		dIndexes = self._get_duplicate_hash_first_occurences()
		oTitles, oMagnetLinks, oSeeds, oLeeches, oSizes, oInfoLinks, oComments, oLanguages, oNumberOfFilesList, oDates = ([] for i in range(10))
		
		for i in range(0, len(hashes)):
			if hashes[i] not in duplicates:
				#print dTitles[i]
				oTitles.append(self.titles[i])
				oMagnetLinks.append(self.magnetLinks[i])
				oSeeds.append(self.seeds[i])
				oLeeches.append(self.leeches[i])
				oSizes.append(self.sizes[i])
				oInfoLinks.append(self.infoLinks[i])
				oComments.append(self.comments[i])
				oLanguages.append(self.languages[i])
				oNumberOfFilesList.append(self.numberOfFilesList[i])
				oDates.append(self.dates[i])


			else:
				if hashes[i] not in markedHashes:
					markedHashes.append(hashes[i])
					oTitles.append(self.titles[i])
					oMagnetLinks.append(self.magnetLinks[i])
					oSeeds.append(self.seeds[i])
					oLeeches.append(self.leeches[i])
					oSizes.append(self.sizes[i])
					oInfoLinks.append(self.infoLinks[i])
					oComments.append(self.comments[i])
					oLanguages.append(self.languages[i])
					oNumberOfFilesList.append(self.numberOfFilesList[i])
					oDates.append(self.dates[i])
				else:
					oComments[markedHashes.index(hashes[i])] += self.comments[i]

		self.titles = oTitles
		self.magnetLinks = oMagnetLinks
		self.seeds = oSeeds
		self.leeches= oLeeches
		self.sizes = oSizes
		self.infoLinks = oInfoLinks
		self.comments = oComments
		self.languages = oLanguages
		self.NumberOfFilesList = oNumberOfFilesList
		self.dates = oDates
		#for title in self.titles:
		#	print title
		
	def analyze_comments(self):
		#Adds a analysis to results cache
		for commentList in self.comments:
			analyzedCommentsBlock = []
			overallRating = 0
			for comment in commentList:
				analyze = CommentAnalysis(comment)
				analyze.build_cache()
				overallRating += analyze.get_cache().get_comment_rating()
				analyzedCommentsBlock.append((analyze.get_cache().get_comment(), analyze.get_cache().get_comment_rating(), analyze.get_cache().get_flagged_words(), analyze.get_cache().get_neutral_words(), analyze.get_cache().get_signatures()))
			self.commentAnalysis.append(analyzedCommentsBlock)
			self.overallRating.append(overallRating)

			


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
	
	def add_comments(self, comment):
		self.comments.append(comment)
	
	def add_language(self, language):
		self.languages.append(language)
	
	def add_number_of_files(self, numberOfFiles):
		self.numberOfFilesList.append(numberOfFiles)
	
	def add_date(self, date):
		self.dates.append(date)
	
	def get_comments(self):
		return self.comments

	def get_languages(self):
		return self.languages

	def get_number_of_files(self):
		return self.numberOfFilesList

	def get_dates(self):
		return self.dates
	
	def to_json(self):
		return json.dumps({"titles": self.titles, "magnet_links": self.magnetLinks, "info_links": self.infoLinks, "seeds" : self.seeds, "leeches" : self.leeches, "sizes" : self.sizes, "languages" : self.languages, "number_of_files" : self.numberOfFilesList, "dates:" : self.dates, "comments" : self.commentAnalysis, "rating": self.overallRating},sort_keys=True, indent=4)


class Search:
	#Create search and store in ResultCache	
	def __init__(self, searchTitle, searchCategory):
		self.searchTitle = searchTitle
		self.searchCategory = searchCategory
		self.cache = ResultCache()
		
	
	def _get_content(self,url):
		#Get the actual raw HTML of info page and return a tuple containing the raw_html ([0]) and the url ([1]) associated with it
		content = Content(url)
		rawResults = (content.get(), url)
		return rawResults
	
	
	def _get_kat_search_cache(self):
		#Get the initial kat search cache
		kURLBuilder=KickAssURLBuilder(self.searchTitle, self.searchCategory)
		content = Content(kURLBuilder.build())
		kSearchParser = KickAssSearchParser(content.get())
		kSearchParser.build_cache()
		katSearchCache = kSearchParser.get_cache()
		return katSearchCache
	
	def _get_pirate_search_cache(self):
		#Get the intitial pirate search cache
		pURLBuilder=PirateBayURLBuilder(self.searchTitle,self.searchCategory)
		content = Content(pURLBuilder.build())
		pSearchParser = PirateBaySearchParser(content.get())
		pSearchParser.build_cache()
		pirateSearchCache = pSearchParser.get_cache()
		return pirateSearchCache

	def _thread_get_info_pages(self, urls):
		#print "Spawning " + str(len(urls)) + " processes."
		pool = ThreadPool(len(urls))
		results = pool.map(self._get_content, urls)
		results = self._thread_result_sort(results, urls)
		pool.close()
		pool.join()
		return results
	
	def _thread_result_sort(self, rawResults, orderedURLList):
		#Sort the results from all concurrent threads
		results = []
		unorderedURLs = []
		unorderedContent = []
		for rawResult in rawResults:
			unorderedURLs.append(rawResult[1])
			unorderedContent.append(rawResult[0])
		orderedURLs = orderedURLList
		for i in range(0,len(orderedURLs)):
			for j in range(0, len(unorderedURLs)):
				if orderedURLs[i] == unorderedURLs[j]:
					results.append(unorderedContent[j])
		return results
	
	def build_kat_cache(self):
		#Determine number of processes to designate for search
		cache = self._get_kat_search_cache()
		urls = cache.get_info_links()
		titles = cache.get_titles()
		magnetLinks = cache.get_magnet_links()
		seeds = cache.get_seeds()
		leeches = cache.get_leeches()
		sizes = cache.get_sizes()
		
		#Download and sort info-link pages
		results = self._thread_get_info_pages(urls)
		
		#Store results (metadata) from each InfoPage
		for result in results:
			kInfoParser = KickAssInfoLinkParser(result)
			kInfoParser.build_cache()
			comments =  kInfoParser.get_comments()
			languages = kInfoParser.get_languages()
			numberOfFiles = kInfoParser.get_number_of_files()
			date = kInfoParser.get_date()
			self.cache.add_comments(comments)
			self.cache.add_language(languages)
			self.cache.add_number_of_files(numberOfFiles)
			self.cache.add_date(date)

		for i in range(0, len(urls)):
			self.cache.add_info_link(urls[i])
			self.cache.add_title(titles[i])
			self.cache.add_magnet_link(magnetLinks[i])
			self.cache.add_seed(seeds[i])
			self.cache.add_leech(leeches[i])
			self.cache.add_size(sizes[i])
		#print "Kickass cache built."
	
	def build_pirate_cache(self):
		#Determine number of processes to designate for search
		cache = self._get_pirate_search_cache()
		urls = cache.get_info_links()
		titles = cache.get_titles()
		magnetLinks = cache.get_magnet_links()
		seeds = cache.get_seeds()
		leeches = cache.get_leeches()
		sizes = cache.get_sizes()
		
		#Download and sort info-link pages
		results = self._thread_get_info_pages(urls)
		
		#Store results (metadata) from each InfoPage
		for result in results:
			pInfoParser = PirateBayInfoLinkParser(result)
			pInfoParser.build_cache()
			comments =  pInfoParser.get_comments()
			languages = pInfoParser.get_languages()
			numberOfFiles = pInfoParser.get_number_of_files()
			date = pInfoParser.get_date()
			self.cache.add_comments(comments)
			self.cache.add_language(languages)
			self.cache.add_number_of_files(numberOfFiles)
			self.cache.add_date(date)

		for i in range(0, len(urls)):
			self.cache.add_info_link(urls[i])
			self.cache.add_title(titles[i])
			self.cache.add_magnet_link(magnetLinks[i])
			self.cache.add_seed(seeds[i])
			self.cache.add_leech(leeches[i])
			self.cache.add_size(sizes[i])
		#print "Pirate cache built."	
	
	def build_cache(self):	
		pool = ThreadPool(2)
		pool.apply_async(self.build_kat_cache)
		pool.apply_async(self.build_pirate_cache)
		pool.close()
		pool.join()
	
	def get_cache(self):
		return self.cache
	
