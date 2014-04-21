#!/usr/bin/python
import re
class Comment:
	def __init__(self):
		self.comment = ""
		self.commentRating = 0
		self.flaggedWordRatings = [] #A list of tuples containg index of word in comment and it's rating
		self.contextWordRatings = []
		self.correctWords = [] #A list containing the correct spelling of the flagged word
		self.signatures = []
	def __str__(self):
		return str((self.comment, self.commentRating, self.flaggedWordRatings, self.contextWordRatings))
	def set_comment(self, comment):
		self.comment = comment

	def set_comment_rating(self, commentRating):
		self.commentRating = commentRating
	
	def add_flagged_word(self, word, correctWord, index, indexEnd, flaggedWordWeight):
		flaggedWord = (word, correctWord, index, indexEnd, flaggedWordWeight)
		self.flaggedWordRatings.append(flaggedWord)
	
	def add_context_word(self, word, correctWord, index, indexEnd, contentWordWeight):	
		contextWord = (word, correctWord, index, indexEnd, contentWordWeight)
		self.contextWordRatings.append(contextWord)

	def add_signature(self, signature):
		self.signatures.append(signature)

	def get_comment(self):
		return self.comment
	
	def get_comment_rating(self):
		return self.commentRating
	
	def get_flagged_words(self):
		return self.flaggedWordRatings
	
	def get_context_words(self):
		return self.contextWordRatings
	
	def get_signatures(self):
		return self.signatures
	

class Signatures:
	def __init__(self, wordList):
		self.wordList = wordList
		self.negaters = ["no", "nor", "not"]
		self.badAdjectives = ["awful", "bad", "low", "horrible", "shit", "terrible"]
		self.goodAdjectives = ["amazing", "awesome", "best", "excellent", "good", "great", "high", "incredible" "nice"]
		self.nouns = ["album", "content", "copy", "mix", "cd", "movie", "music", "quality", "song", "video", "torrent"]


	def sig_cease_and_decist(self):
		flaggedWords = self.wordList.get_flagged_words()
		score = 0
		indexes = []
		for element in flaggedWords:
			if element[1] == "cease" or element[1] == "decist" or element[1] == "letter" or element[1] == "isp" or element[1] == "watched" or element[1] == "tracked":
				score +=1
				indexes.append(element[2])
				indexes.append(element[3])
		if score > 1:
			return ("Monitored Torrent", min(indexes), max(indexes), -15)
		return ("Monitored Torrent", -1, -1, 0)

	def sig_bad_quality(self):
		correctlySpelled = []
		adjectiveFound = False
		contextFound = False
		indexes = []
		for element in self.wordList.get_flagged_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for element in self.wordList.get_context_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for word in correctlySpelled:
			if word in self.badAdjectives:
				adjectiveFound = True
			if word in self.nouns:
				contextFound = True
		if len(indexes) > 0:	
			if adjectiveFound and contextFound:
				return ("Bad Quality", min(indexes), max(indexes), -10)
		return ("Bad Quality", -1, -1, 0)
	def sig_good_quality(self):
		correctlySpelled = []
		adjectiveFound = False
		contextFound = False
		indexes = []
		for element in self.wordList.get_flagged_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for element in self.wordList.get_context_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for word in correctlySpelled:
			if word in self.goodAdjectives:
				adjectiveFound = True
			if word in self.nouns:
				contextFound = True

		if len(indexes) > 0:
			if adjectiveFound and contextFound:
				return ("Good Quality", min(indexes), max(indexes), 10)
		return ("Good Quality", -1, -1, 0)

	def sig_malware(self):
		correctlySpelled = []
		indexes = []
		for element in self.wordList.get_flagged_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for element in self.wordList.get_context_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
	
		if len(indexes) > 0:
			if "malware" in correctlySpelled or "trojan" in correctlySpelled or "virus" in correctlySpelled:
				return ("Malware Detected", min(indexes), max(indexes), -15)
		return (-1, -1, 0)
		
class CommentAnalysis:
	def __init__(self, comment):
		self.comment = comment
		self.commentAnalysis = Comment()
		#Single Words

		#Contains a list of common good words in torrent comments with their respective worth (1-10)
		self.goodWordList = [("amazing", 5), ("appreciate", 5), ("awesome", 5), ("best", 6), ("enjoyed", 4), ("excellent", 6), ("good", 4), ("great", 5), ("incredible", 3), ("like", 3), ("love", 4), ("nice", 3), ("outstanding", 6), ("perfect", 6), ("thanks", 6)]


		#Contains a list of common bad words in torrent comments with their respective worth (-1-(-10))
		self.badWordList = [("awful", -5), ("bad", -4), ("cam", -1), ("cease", 0), ("crap", -3), ("botnet", -5), ("decist", 0), ("fuck", -2), ("fucking", -2), ("letter", 0), ("horrible", -5), ("isp", -9), ("malware", -8), ("shit", -2), ("tracked", -2), ("trojan", -8), ("virus", -8), ("watched", -2)]

		#Words that add contextual support with their respective multiplier
		self.contextList = [ ("album",0), ("copy", 0), ("download", 0), ("movie", 0), ("quality", 0), ("rip", 0), ("software", 0), ("song", 0), ("torrent", 0), ("upload", 0), ("version", 0)] 

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
		for word in wordList:
			if values == True:
				unpackedList.append(word[1])
			else:
				unpackedList.append(word[0])
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
	
	def _get_tolerance(self, seq):
		return len(seq) * .25

	def build_cache(self):
		wordArray = self.comment.split(" ")
                commentRating = 0
                flaggedWordList = []
                self.commentAnalysis.set_comment(self.comment)
                self.comment = self.comment.lower().strip()
                contextWords = self._unpack_list("context words", False)
                contextWordsWeight = self._unpack_list("context words", True)
                badWords = self._unpack_list("bad words", False)
                badWordsWeight = self._unpack_list("bad words", True)
                goodWords = self._unpack_list("good words", False)
                goodWordsWeight = self._unpack_list("good words", True)
                badWords = self._unpack_list("bad words", False)
                badWordsWeight = self._unpack_list("bad words",True)


                for i in range(0, len(contextWords)):
                        index = 0
                        for j in range(0, len(wordArray)):
                                sanitized = re.sub(r'[^\w]', ' ', wordArray[j]).lower().strip()
                                if self.levenshtein(sanitized, contextWords[i]) < self._get_tolerance(contextWords[i]):
                                        self.commentAnalysis.add_context_word(wordArray[j], contextWords[i], index, index + len(wordArray[j]), contextWordsWeight[i])
                                index += 1 #Add one to index space
                                index += len(wordArray[j])
                for k in range(0, len(goodWords)):
                        index = 0
                        for l in range(0, len(wordArray)):
                                sanitized = re.sub(r'[^\w]', ' ', wordArray[l]).lower().strip()
                                if self.levenshtein(sanitized, goodWords[k]) < self._get_tolerance(goodWords[k]):
                                        self.commentAnalysis.add_flagged_word(wordArray[l], goodWords[k], index, index + len(wordArray[l]), goodWordsWeight[k])
                                index += 1 #Add one to index space
                                index += len(wordArray[l])
                for m in range(0, len(badWords)):
                        index = 0
                        for n in range(0, len(wordArray)):
                                sanitized = re.sub(r'[^\w]', ' ', wordArray[n]).lower().strip()
                                if self.levenshtein(sanitized, badWords[m]) < self._get_tolerance(badWords[m]):
                                        self.commentAnalysis.add_flagged_word(wordArray[n], badWords[m], index, index + len(wordArray[n]), badWordsWeight[m])
                                index += 1 #Add one to index space
                                index += len(wordArray[n])
                flaggedWords = self.commentAnalysis.get_flagged_words()
                for word in flaggedWords:
                        commentRating += word[4]

		#Signatures

		signatures = Signatures(self.commentAnalysis)
		if signatures.sig_cease_and_decist()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_cease_and_decist())
		if signatures.sig_good_quality()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_good_quality())
		if signatures.sig_bad_quality()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_bad_quality())
		if signatures.sig_malware()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_malware())
		
		self.commentAnalysis.set_comment_rating(commentRating)
			
	def get_cache(self):
		return self.commentAnalysis
