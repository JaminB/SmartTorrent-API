#!/usr/bin/python

class SearchAnalysis:
	def __init__(self, resultCache):
		self.resultCache = resultCache
		
		#Single Words

		#Contains a list of common good words in torrent comments with their respective worth (1-10)
		self.goodWordList = [("appreciate", 5), ("awesome", 5), ("excellent", 6), ("good", 4), ("great", 5), ("incredible", 3), ("nice", 3), ("thank", 6)]

		#Contains a list of common bad words in torrent comments with their respective worth (-1-(-10))
		self.badWordList = [("awful", -5), ("bad", -4), ("cam", -1), ("crap", -3), ("fuck", -2), ("fucking", -2), ("horrible", -5), ("malware", -8), ("shit", -2), ("terrible", -5), ("trojan", -8), ("virus", -8)]

		#Words that add contextual support with their respective multiplier
		self.contextList = [("copy", 1.5), ("movie", 1.5), ("quality", 2), ("software", 1.5), ("song", 1.5), ("torrent", 2), ("upload", 2)] 

		#Phrases
		self.goodPhraseList = [("thank you", 10)]
		self.badPhraseList = [("do not download", -10), ("don't download", -10)]

	def _unpack_list(self, listType, values):
		unpackedList = []
		wordList = []	
		if listType.lower() == "good words":
			wordList = self.goodWordList
		if listType.lower() == "bad words":
			wordList = self.badWordList
		if listType.lower() == "good words":
			wordList = self.goodWordList
		if listType.lower() == "context words":
			wordList = self.contextList
		if listType.lower() == "good phrases":
			wordList = self.goodPhraseList
		if listType.lower() == "bad phrases":
			wordList = self.badPhraseList
		for word in wordList:
			if values == True:
				unpackedList.append(word[1])
			else:
				unpackeList.append(word[0])
		return unpackedList


