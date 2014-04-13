#!/usr/bin/python
class Comment:
	def __init__(self):
		self.comment = ""
		self.commentRating = 0
		self.flaggedWordRatings = [] #A list of tuples containg index of word in comment and it's rating

	def set_comment(self, comment):
		self.comment = comment

	def set_comment_rating(self, commentRating):
		self.commentRating = commentRating

	def set_flagged_word_ratings(self, flaggedWordRatings):
		self.flaggedWordRatings = flaggedWordRating
	def get_comment(self):
		return self.comment
	
	def get_comment_rating(self):
		return self.commentRating
	
	def get_flagged_word_ratings(self):
		return self.flaggedWordRatings
 
class AnalysisCache: 
	#Holds all comment caches for a particular info page
	def __init__(self):
		self.comments = []
	
	def add_comment(comment):
		self.comments.append()
	
	def get_comment(self):
		return self.comment
	
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
		self.goodPhraseList = [("thank you", 10), ("audio: 10", 10), ("audio: 9", 9), ("audio: 8", 8),("audio: 7", 7),("audio: 6", 6),("audio: 5", 5), ("a: 10", 10), ("a: 9", 9), ("a: 8", 8),("a: 7", 7), ("a: 6", 6), ("a: 5", 5), ("video: 10", 10), ("video: 9", 9), ("video: 8", 8),("video: 7", 7),("video: 6", 6),("video: 5", 5), ("v: 10", 10), ("v: 9", 9), ("v: 8", 8),("v: 7", 7), ("v: 6", 6), ("v: 5", 5)]

		self.badPhraseList = [("do not download", -10), ("don't download", -10), ("audio: 4", -6), ("audio: 3", -7), ("audio: 2", -8),("audio: 1", -9),("audio: 0", -10), ("a: 4", -6), ("a: 3", -7), ("a: 2", -8), ("a: 1", -9),("a: 0", -10), ("video: 4", -6), ("video: 3", -7), ("video: 2", -8),("video: 1", -9),("video: 0", -10),("v: 4", -6), ("v: 3", -7), ("v: 2", -8),("v: 1", -9), ("v: 0", -10)]

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

	def levenshtein(self, seq1, seq2):
		#Implementation of string distance calculations
		#O(N*M) time and O(M) space, for N and M the lengths of the two sequences
		oneago = None
	    	thisrow = range(1, len(seq2) + 1) + [0]
	    	for x in xrange(len(seq1)):
			twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
			for y in xrange(len(seq2)):
		    		delcost = oneago[y] + 1
				addcost = thisrow[y - 1] + 1
			    	subcost = oneago[y - 1] + (seq1[x] != seq2[y])
				thisrow[y] = min(delcost, addcost, subcost)
	    	return thisrow[len(seq2) - 1]
	
