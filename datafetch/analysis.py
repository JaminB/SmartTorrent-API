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
		try:
			f = open("wordlist.wl", "r")
		except IOError:
			print "File Not Found Error: wordlist.wl cannot be found"
		allWords = []
		for line in f:
			if line.strip() != "":
				if "#" not in line:
					allWords.append(line.strip())
		try:
			loc_good_adjectives = allWords.index('~Good_Adjectives:') + 1	
		except ValueError:
			print "Content Error: wordlist.wl does not contain ~Good_Adjectives definition." 
		try:
			loc_bad_adjectives = allWords.index('~Bad_Adjectives:') + 1	
		except ValueError:
			print "Content Error: wordlist.wl does not contain ~Bad_Adjectives definition." 
		try:
			loc_negators = allWords.index('~Negators:') + 1	
		except ValueError:
			print "Content Error: wordlist.wl does not contain ~Negators definition." 
		try:
			loc_context_nouns = allWords.index('~Context_Nouns:') + 1
		except ValueError:
			print "Content Error: wordlist.wl does not contain ~Context_Nouns definition." 
		try:	
			loc_good_words = allWords.index('~Good_Words:') + 1
		except ValueError:
			print "Content Error: wordlist.wl does not contain ~Good_Words definition." 
		try:	
			loc_bad_words = allWords.index('~Bad_Words:') + 1
		except:
			print "Content Error: wordlist.wl does not contain ~Bad_Words definition." 
		try:
			loc_neutral_words = allWords.index('~Neutral_Words:') + 1
		except:
			print "Content Error: wordlist.wl does not contain ~Neutral_Words definition." 

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
			try:
				self.goodWords.append((split[0], int(split[1])))
			except IndexError:
				print "Incomplete definition in ~Good_Words: " + allWords[m] + " _ <---specify integer value"
		
		for n in range(loc_bad_words, len(allWords)):
			if "~" in allWords[n]:
				break
			split = allWords[n].split(' ')
			try:
				self.badWords.append((split[0], int(split[1])))
			except:
				print "Incomplete definition in ~Bad_Words: " + allWords[n] + " _ <---specify integer value"

		
		for o in range(loc_neutral_words, len(allWords)):
			if "~" in allWords[o]:
				break
			split = allWords[o].split(' ')
			try:
				self.neutralWords.append((split[0], int(split[1])))
			except:
				print "Incomplete definition in ~Neutral_Words: " + allWords[o] + " _ <---specify integer value"
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
		self.negaters = wordlist.get_negators() #Signature list
		self.badAdjectives = wordlist.get_bad_adjs() #Signature list
		self.goodAdjectives = wordlist.get_good_adjs() #Signature list
		self.contextNouns = wordlist.get_context_nouns() #Signature list

		self.flaggedWords = self.comment.get_flagged_words() #Comment flagged words
		self.neutralWords = self.comment.get_neutral_words() #Comment neutral words
	
	def get_good_adjs_in_comment(self):
		indexes = []
		foundWords = []
		for element in self.flaggedWords:
			if element[1] in self.goodAdjectives:
				indexes.append(element[2])
				indexes.append(element[3])
				foundWords.append(element[0])
		if len(foundWords) > 0:
			return (foundWords, min(indexes), max(indexes))
		return False
	
	def get_bad_adjs_in_comment(self):
		indexes = []
		foundWords = []
		for element in self.flaggedWords:
			if element[1] in self.badAdjectives:
				indexes.append(element[2])
				indexes.append(element[3])
				foundWords.append(element[0])
		if len(foundWords) > 0:
			return (foundWords, min(indexes), max(indexes))
		return False
	
	def get_custom_words_in_comment(self, words):
		indexes = []
		foundWords = []
		for element in self.flaggedWords + self.neutralWords:
			if element[1] in words:
				indexes.append(element[2])
				indexes.append(element[3])
				foundWords.append(element[0])
		if len(foundWords) > 0:
			return (foundWords, min(indexes), max(indexes))
		return False

	def get_context_nouns_in_comment(self):
		indexes = []
		foundWords = []
		for element in self.neutralWords:
			if element[1] in self.contextNouns:
				indexes.append(element[2])
				indexes.append(element[3])
				foundWords.append(element[0])
		if len(foundWords) > 0:
			return (foundWords, min(indexes), max(indexes))
		return False

	def combine_lists(self, words1, words2):
		indexes = []
		if words1 and words2:
			indexes.append(words1[1])
			indexes.append(words2[1]) 
			indexes.append(words1[2])
			indexes.append(words2[2])
			return (words1[0] + words2[0], min(indexes), max(indexes))
		else:
			return False
	def sizeOf(self, words):
		try:
			return len(words[0])
		except TypeError:
			return 0

	def create_signature(self, name, value, words):
		if words != False:
			return (name, words[1], words[2], value)
		return False

	#Signature for detecting comments regarding cease and decist letters for pirating -- i.e the torrent is illegal and you shouldn't download	
	def sig_cease_and_decist(self):
		result = self.get_custom_words_in_comment(["cease", "copyright", "decist", "isp", "watched", "tracked"])
		if self.sizeOf(result) > 1:
			return self.create_signature("Monitored Torrent", -15, result)
		return False

	#Signature for detecting comments referencing the content as "bad quality"
	def sig_bad_quality(self):
		result = self.create_signature("Bad Quality", -10, self.combine_lists(self.get_context_nouns_in_comment(), self.get_bad_adjs_in_comment()))
		return result

	#Signature for detecting comments referencing the content as "good quality"
	def sig_good_quality(self):
			
		result = self.create_signature("Good Quality", 10, self.combine_lists(self.get_context_nouns_in_comment(), self.get_good_adjs_in_comment()))
		return result
	#Signature for detecting in comment content rating - i.e "audio:10"
	def sig_rated_content(self):
		weight = []
		rating = 0
		contentType = []
		indexes = []
		digitFound = False
		keyFound = False
		markedWords = []
		for element in self.neutralWords:
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
		return self.create_signature("Malware Detected", -15, self.get_custom_words_in_comment(["malware", "trojan", "virus", "botnet"]))
		
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
		
		#Contains a list of words that may be relevant 
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
		if signatures.sig_cease_and_decist() != False:
			self.commentAnalysis.add_signature(signatures.sig_cease_and_decist())
			commentRating += signatures.sig_cease_and_decist()[3]
		if signatures.sig_good_quality() != False:
			self.commentAnalysis.add_signature(signatures.sig_good_quality())
			commentRating += signatures.sig_good_quality()[3]
		if signatures.sig_bad_quality() != False:
			self.commentAnalysis.add_signature(signatures.sig_bad_quality())
			commentRating += signatures.sig_bad_quality()[3]
		if signatures.sig_malware() != False:
			self.commentAnalysis.add_signature(signatures.sig_malware())
			commentRating += signatures.sig_malware()[3]
		if signatures.sig_rated_content()[1] != -1:
			self.commentAnalysis.add_signature(signatures.sig_rated_content())
			commentRating += signatures.sig_rated_content()[3]
		self.commentAnalysis.set_comment_rating(commentRating)
			
	def get_cache(self):
		return self.commentAnalysis
