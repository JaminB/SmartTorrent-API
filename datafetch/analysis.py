#!/usr/bin/python
import re
class Wordlist:
	def __init__(self):
		self.goodAdjs = []
		self.badAdjs = []
		self.contextNouns = []
		self.neutralWords = []
		self.negators = []
		self.goodWords = []
		self.badWords = []
		self._populate()
	
	def _populate(self):
		f = open("wordlist.wl", "r")
		allWords = []
		for line in f:
			if line.strip() != "":
				if "#" not in line:
					allWords.append(line.strip())
		loc_good_adjectives = allWords.index('~Good_Adjectives:') + 1	
		loc_bad_adjectives = allWords.index('~Bad_Adjectives:') + 1	
		loc_negators = allWords.index('~Negators:') + 1	
		loc_context_nouns = allWords.index('~Context_Nouns:') + 1
		loc_good_words = allWords.index('~Good_Words:') + 1
		loc_bad_words = allWords.index('~Bad_Words:') + 1
		loc_neutral_words = allWords.index('~Neutral_Words:') + 1

		for i in range(loc_good_adjectives, len(allWords)):
			if "~" in allWords[i]:
				break
			self.goodAdjs.append(allWords[i])
		
		for j in range(loc_bad_adjectives, len(allWords)):
			if "~" in allWords[j]:
				break
			self.badAdjs.append(allWords[j])
		
		for k in range(loc_negators, len(allWords)):
			if "~" in allWords[k]:
				break
			self.negators.append(allWords[k])
		
		for l in range(loc_context_nouns, len(allWords)):
			if "~" in allWords[l]:
				break
			self.contextNouns.append(allWords[l])

		for m in range(loc_good_words, len(allWords)):
			if "~" in allWords[m]:
				break
			split = allWords[m].split(' ')
			self.goodWords.append((split[0], int(split[1])))
		
		for n in range(loc_bad_words, len(allWords)):
			if "~" in allWords[n]:
				break
			split = allWords[n].split(' ')
			self.badWords.append((split[0], int(split[1])))
		
		for o in range(loc_neutral_words, len(allWords)):
			if "~" in allWords[o]:
				break
			split = allWords[o].split(' ')
			self.neutralWords.append((split[0], int(split[1])))
	
	def get_good_adjs(self):
		return self.goodAdjs	
		
	def get_bad_adjs(self):
		return self.badAdjs

	def get_context_nouns(self):
		return self.contextNouns
	
	def get_negators(self):
		return self.negators	

	def get_good_words_weighted(self):
		return self.goodWords

	def get_bad_words_weighted(self):
		return self.badWords

	def get_neutral_words_weighted(self):
		return self.neutralWords
class Comment:
	def __init__(self):
		self.comment = ""
		self.commentRating = 0
		self.flaggedWordRatings = [] #A list of tuples containg index of word in comment and it's rating
		self.neutralWords = []
		self.correctWords = [] #A list containing the correct spelling of the flagged word
		self.signatures = []

	def __str__(self):
		return str((self.comment, self.commentRating, self.flaggedWordRatings, self.neutralWords))
	
	def set_comment(self, comment):
		self.comment = comment

	def set_comment_rating(self, commentRating):
		self.commentRating = commentRating
	
	def add_flagged_word(self, word, correctWord, index, indexEnd, flaggedWordWeight):
		flaggedWord = (word, correctWord, index, indexEnd, flaggedWordWeight)
		self.flaggedWordRatings.append(flaggedWord)
	
	def add_neutral_word(self, word, correctWord, index, indexEnd, contentWordWeight):	
		contextWord = (word, correctWord, index, indexEnd, contentWordWeight)
		self.neutralWords.append(contextWord)

	def add_signature(self, signature):
		self.signatures.append(signature)

	def get_comment(self):
		return self.comment
	
	def get_comment_rating(self):
		return self.commentRating
	
	def get_flagged_words(self):
		return self.flaggedWordRatings
	
	def get_neutral_words(self):
		return self.neutralWords
	
	def get_signatures(self):
		return self.signatures
	

class Signatures:
	def __init__(self, comment):
		wordlist = Wordlist()
		self.comment = comment
		self.negaters = wordlist.get_negators()
		self.badAdjectives = wordlist.get_bad_adjs()
		self.goodAdjectives = wordlist.get_good_adjs()
		self.nouns = wordlist.get_context_nouns()


	def sig_cease_and_decist(self):
		flaggedWords = self.comment.get_flagged_words()
		score = 0
		indexes = []
		for element in flaggedWords:
			if element[1] == "cease" or element[1] == "copyright" or element[1] == "decist" or element[1] == "isp" or element[1] == "watched" or element[1] == "tracked":
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
		for element in self.comment.get_flagged_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for element in self.comment.get_neutral_words():
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
		for element in self.comment.get_flagged_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for element in self.comment.get_neutral_words():
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
	
	def sig_rated_content(self):
		weight = []
		rating = 0
		contentType = []
		indexes = []
		digitFound = False
		keyFound = False
		markedWords = []
		neutralWords = self.comment.get_neutral_words()
		for element in neutralWords:
			if element[1].isdigit():
				digitFound = True
				weight.append(element[1])
				indexes.append(element[2])
				indexes.append(element[3])
			if element[1] == "audio" or element[1] == "video":
				keyFound = True
				contentType.append(element[1])
				indexes.append(element[2])
				indexes.append(element[3])
		
		if len(weight) >= len(contentType):
			for i in range(0, len(contentType)):
				if contentType[i] not in markedWords:
					markedWords.append(contentType[i])
					if int(weight[i]) < 11:
						if int(weight[i]) > 5:
							rating += int(weight[i])
						else:
							rating -= (10 - int(weight[i]))
		else:
			for i in range(0, len(weight)):
				if contentType[i] not in markedWords:
					markedWords.append(contentType[i])
					if int(weight[i]) < 11:
						if int(weight[i]) > 5:
							rating += int(weight[i])
						else:
							rating -= (10 - int(weight[i]))

		if len(indexes) > 0:
				if digitFound and keyFound:
					return ("Content Rating", min(indexes), max(indexes), rating)
		return (-1, -1, 0)
		
	def sig_malware(self):
		correctlySpelled = []
		indexes = []
		for element in self.comment.get_flagged_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
		for element in self.comment.get_neutral_words():
			correctlySpelled.append(element[1])
			indexes.append(element[2])
			indexes.append(element[3])
	
		if len(indexes) > 0:
			if "malware" in correctlySpelled or "trojan" in correctlySpelled or "virus" in correctlySpelled:
				return ("Malware Detected", min(indexes), max(indexes), -15)
		return (-1, -1, 0)
	#	
class CommentAnalysis:
	def __init__(self, comment):
		wordlist = Wordlist()
		self.comment = comment
		self.commentAnalysis = Comment()
		#Single Words

		#Contains a list of common good words in torrent comments with their respective worth (1-10)
		self.goodWordList = wordlist.get_good_words_weighted()


		#Contains a list of common bad words in torrent comments with their respective worth (-1-(-10))
		self.badWordList = wordlist.get_bad_words_weighted()

		#Words that add contextual support with their respective multiplier
		self.contextList = wordlist.get_neutral_words_weighted()

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
                                        self.commentAnalysis.add_neutral_word(wordArray[j], contextWords[i], index, index + len(wordArray[j]), contextWordsWeight[i])
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
			commentRating += signatures.sig_cease_and_decist()[3]
		if signatures.sig_good_quality()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_good_quality())
			commentRating += signatures.sig_good_quality()[3]
		if signatures.sig_bad_quality()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_bad_quality())
			commentRating += signatures.sig_bad_quality()[3]
		if signatures.sig_malware()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_malware())
			commentRating += signatures.sig_malware()[3]
		if signatures.sig_rated_content()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_rated_content())
			commentRating += signatures.sig_rated_content()[3]
		self.commentAnalysis.set_comment_rating(commentRating)
			
	def get_cache(self):
		return self.commentAnalysis
