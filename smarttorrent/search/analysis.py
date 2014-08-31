#! /usr/bin/python
import re
from settings import config

class Wordlist:

    def __init__(self):
        self.goodAdjs = []
        self.goodVerbs = []
        self.goodNouns = []
        self.badAdjs = []
        self.badVerbs = []
        self.badNouns = []
        self.contextNouns = []
        self.neutralWords = []
        self.negators = []
        self.goodWords = []
        self.badWords = []
        self.ratings = []
        self._populate()

    def _populate(self):
        try:
            f = open(config.variables.get('wordlist_location'), 'r')
        except IOError:
            print 'File Not Found Error: wordlist.wl cannot be found'
        allWords = []
        for line in f:
            if line.strip() != '':
                if '#' not in line:
                    allWords.append(line.strip())

        try:
            loc_good_adjectives = allWords.index('~Good_Adjectives:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Good_Adjectives definition.'
        try:
            loc_good_verbs = allWords.index('~Good_Verbs:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Good_Verbs definition.'
        try:
            loc_good_nouns = allWords.index('~Good_Nouns:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Good_Nouns definition.'
        try:
            loc_bad_adjectives = allWords.index('~Bad_Adjectives:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Bad_Adjectives definition.'
        try:
            loc_bad_verbs = allWords.index('~Bad_Verbs:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Bad_Verbs definition.'
        try:
            loc_bad_nouns = allWords.index('~Bad_Nouns:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Bad_Nouns definition.'
        try:
            loc_ratings = allWords.index('~Ratings:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Ratings definition.'
        try:
            loc_negators = allWords.index('~Negators:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Negators definition.'
        try:
            loc_ratings = allWords.index('~Ratings:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Ratings definition.'
        try:
            loc_context_nouns = allWords.index('~Context_Nouns:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Context_Nouns definition.'
        try:
            loc_good_words = allWords.index('~Good_Words:') + 1
        except ValueError:
            print 'Content Error: wordlist.wl does not contain ~Good_Words definition.'
        try:
            loc_bad_words = allWords.index('~Bad_Words:') + 1
        except:
            print 'Content Error: wordlist.wl does not contain ~Bad_Words definition.'
        try:
            loc_neutral_words = allWords.index('~Neutral_Words:') + 1
        except:
            print 'Content Error: wordlist.wl does not contain ~Neutral_Words definition.'
        for i in range(loc_good_adjectives, len(allWords)):
            if '~' in allWords[i]:
                break
            self.goodAdjs.append(allWords[i])

        for i1 in range(loc_good_verbs, len(allWords)):
            if '~' in allWords[i1]:
                break
            self.goodVerbs.append(allWords[i1])

        for i2 in range(loc_good_nouns, len(allWords)):
            if '~' in allWords[i2]:
                break
            self.goodNouns.append(allWords[i2])

        for j in range(loc_bad_adjectives, len(allWords)):
            if '~' in allWords[j]:
                break
            self.badAdjs.append(allWords[j])

        for j1 in range(loc_bad_verbs, len(allWords)):
            if '~' in allWords[j1]:
                break
            self.badVerbs.append(allWords[j1])

        for j2 in range(loc_bad_nouns, len(allWords)):
            if '~' in allWords[j2]:
                break
            self.badNouns.append(allWords[j2])

        for k in range(loc_negators, len(allWords)):
            if '~' in allWords[k]:
                break
            self.negators.append(allWords[k])

        for l in range(loc_context_nouns, len(allWords)):
            if '~' in allWords[l]:
                break
            self.contextNouns.append(allWords[l])

        for r in range(loc_ratings, len(allWords)):
            if '~' in allWords[r]:
                break
            self.ratings.append(allWords[r])

        for m in range(loc_good_words, len(allWords)):
            if '~' in allWords[m]:
                break
            split = allWords[m].split(' ')
            try:
                self.goodWords.append((split[0], int(split[1])))
            except IndexError:
                print 'Incomplete definition in ~Good_Words: ' + allWords[m] + ' _ <---specify integer value'

        for n in range(loc_bad_words, len(allWords)):
            if '~' in allWords[n]:
                break
            split = allWords[n].split(' ')
            try:
                self.badWords.append((split[0], int(split[1])))
            except:
                print 'Incomplete definition in ~Bad_Words: ' + allWords[n] + ' _ <---specify integer value'

        for o in range(loc_neutral_words, len(allWords)):
            if '~' in allWords[o]:
                break
            split = allWords[o].split(' ')
            try:
                self.neutralWords.append((split[0], int(split[1])))
            except:
                print 'Incomplete definition in ~Neutral_Words: ' + allWords[o] + ' _ <---specify integer value'



    def get_good_adjs(self):
        return self.goodAdjs


    def get_good_verbs(self):
        return self.goodVerbs


    def get_good_nouns(self):
        return self.goodNouns


    def get_bad_adjs(self):
        return self.badAdjs


    def get_bad_verbs(self):
        return self.badVerbs

    def get_bad_nouns(self):
        return self.badNouns

    def get_context_nouns(self):
        return self.contextNouns

    def get_negators(self):
        return self.negators

    def get_ratings(self):
        return self.ratings

    def get_good_words_weighted(self):
        return self.goodWords

    def get_bad_words_weighted(self):
        return self.badWords

    def get_neutral_words_weighted(self):
        return self.neutralWords


class Comment:

    def __init__(self):
        self.comment = ''
        self.commentRating = 0
        self.flaggedWordRatings = []
        self.negatorWordRatings = []
        self.neutralWords = []
        self.correctWords = []
        self.signatures = []


    def __str__(self):
        return str((self.comment,
         self.commentRating,
         self.flaggedWordRatings,
         self.neutralWords))


    def set_comment(self, comment):
        self.comment = comment

    def set_comment_rating(self, commentRating):
        self.commentRating = commentRating

    def add_flagged_word(self, word, correctWord, index, indexEnd, flaggedWordWeight):
        flaggedWord = (word, correctWord,index,indexEnd,flaggedWordWeight)
        self.flaggedWordRatings.append(flaggedWord)

    def add_negator_word(self, word, correctWord, index, indexEnd, negatorWordWeight):
        negatorWord = (word,correctWord,index,indexEnd, negatorWordWeight)
        self.negatorWordRatings.append(negatorWord)

    def add_neutral_word(self, word, correctWord, index, indexEnd, contentWordWeight):
        contextWord = (word, correctWord,index,indexEnd,contentWordWeight)
        self.neutralWords.append(contextWord)

    def add_signature(self, signature):
        self.signatures.append(signature)

    def get_comment(self):
        return self.comment

    def get_negator_words(self):
        return self.negatorWordRatings

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
        self.badVerbs = wordlist.get_bad_verbs()
        self.badNouns = wordlist.get_bad_nouns()
        self.goodAdjectives = wordlist.get_good_adjs()
        self.goodVerbs = wordlist.get_good_verbs()
        self.goodNouns = wordlist.get_good_verbs()
        self.ratings = wordlist.get_ratings()
        self.contextNouns = wordlist.get_context_nouns()
        self.negatorWords = self.comment.get_negator_words()
        self.flaggedWords = self.comment.get_flagged_words()
        self.neutralWords = self.comment.get_neutral_words()


    def get_negators_in_comment(self):
        if len(self.negatorWords) > 0:
            return self.negatorWords
        return False

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

    def get_digits_in_comment(self):
        indexes = []
        foundWords = []
        for element in self.neutralWords:
            if element[1].isdigit():
                indexes.append(element[2])
                indexes.append(element[3])
                foundWords.append(re.sub('[^\\w]', '', element[0]))

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

    def get_distance(self, word1, words2):
	try:
		return abs(word1[3] - words2[1])
	except:
		return -1



    def sizeOf(self, words):
        try:
            return len(words[0])
        except TypeError:
            return 0



    def create_signature(self, name, value, words):
        if words != False:
            return (name, words[1], words[2], value)
        return False



    def sig_cease_and_decist(self):
        result = self.get_custom_words_in_comment(['cease','copyright','decist','isp','watched','tracked'])
        if self.sizeOf(result) > 1:
            return self.create_signature('Monitored Torrent', -15, result)
        return False

    def sig_bad_quality(self):
        combinedLists = self.combine_lists(self.get_context_nouns_in_comment(), self.get_bad_adjs_in_comment())
	try:
		for word in self.get_negators_in_comment():
		    if self.get_distance(word, combinedLists) < 20: #Check if there is a negator within 20 characters of this word combo
			result = self.create_signature('Good Quality By Negation', 5, combinedLists)
			return result
		    else:
			result = self.create_signature('Bad Quality', -10, combinedLists)
			return result
        except:
		result = self.create_signature('Bad Quality', -10, combinedLists)
        	return result

    def sig_good_quality(self):
        combinedLists = self.combine_lists(self.get_context_nouns_in_comment(), self.get_good_adjs_in_comment())
	try:
		for word in self.get_negators_in_comment():
           		if self.get_distance(word, combinedLists) < 20: #Check if there is a negator within 20 characters of this word combo
        			result = self.create_signature('Bad Quality By Negation', -5, combinedLists)
				return result
			else:
        			result = self.create_signature('Good Quality', 10, combinedLists)
				return result
	except TypeError:
        	result = self.create_signature('Good Quality', 10, combinedLists)
        	return result

    def sig_rated_content(self):
        rating = 0
        digits = self.get_digits_in_comment()
        keyWords = self.get_custom_words_in_comment(['audio', 'video'])
        if self.combine_lists(digits, keyWords) != False:
            if self.sizeOf(digits) >= self.sizeOf(keyWords):
                for i in range(0, self.sizeOf(keyWords)):
                    if int(digits[0][i]) > 5:
                        rating += int(digits[0][i])
                    else:
                        rating -= 10 - int(digits[0][i])

            else:
                for i in range(0, int(self.sizeOf(digits))):
                    if int(digits[0][i]) > 5:
                        rating += int(digits[0][i])
                    else:
                        rating -= 10 - int(digits[0][i])

            return self.create_signature('Content Rating', rating, self.combine_lists(digits, keyWords))
        return False



    def sig_malware(self):
        return self.create_signature('Malware Detected', -15, self.get_custom_words_in_comment(['malware','trojan', 'virus', 'botnet']))


class CommentAnalysis:

    def __init__(self, comment):
        wordlist = Wordlist()
        self.commentPlain = comment
        self.comment = Comment()
        self.goodWordList = wordlist.get_good_words_weighted()
        self.badWordList = wordlist.get_bad_words_weighted()
        self.contextList = wordlist.get_neutral_words_weighted()
        self.negatorWordList = wordlist.get_negators()


    def _unpack_list(self, listType, values):
        unpackedList = []
        wordList = []
        if listType.lower() == 'good words':
            wordList = self.goodWordList
        if listType.lower() == 'bad words':
            wordList = self.badWordList
        if listType.lower() == 'good words':
            wordList = self.goodWordList
        if listType.lower() == 'context words':
            wordList = self.contextList
        for word in wordList:
            if values == True:
                unpackedList.append(word[1])
            else:
                unpackedList.append(word[0])

        return unpackedList


    def levenshtein(self, seq1, seq2):
        oneago = None
        thisrow = range(1, len(seq2) + 1) + [0]
        for x in xrange(len(seq1)):
            (twoago, oneago, thisrow,) = (oneago, thisrow, [0] * len(seq2) + [x + 1])
            for y in xrange(len(seq2)):
                delcost = oneago[y] + 1
                addcost = thisrow[(y - 1)] + 1
                subcost = oneago[(y - 1)] + (seq1[x] != seq2[y])
                thisrow[y] = min(delcost, addcost, subcost)


        return thisrow[(len(seq2) - 1)]

    def _get_tolerance(self, seq):
        return len(seq) * 0.25


    def build_cache(self):
        wordArray = self.commentPlain.split(' ')
        commentRating = 0
        flaggedWordList = []
        self.comment.set_comment(self.commentPlain)
        self.commentPlain = self.commentPlain.lower().strip()
        contextWords = self._unpack_list('context words', False)
        contextWordsWeight = self._unpack_list('context words', True)
        badWords = self._unpack_list('bad words', False)
        badWordsWeight = self._unpack_list('bad words', True)
        goodWords = self._unpack_list('good words', False)
        goodWordsWeight = self._unpack_list('good words', True)
        badWords = self._unpack_list('bad words', False)
        badWordsWeight = self._unpack_list('bad words', True)
        for i in range(0, len(contextWords)):
            index = 0
            for j in range(0, len(wordArray)):
                sanitized = re.sub('[^\\w]', ' ', wordArray[j]).lower().strip()
                if self.levenshtein(sanitized, contextWords[i]) < self._get_tolerance(contextWords[i]):
                    self.comment.add_neutral_word(wordArray[j], contextWords[i], index, index + len(wordArray[j]), contextWordsWeight[i])
                index += 1
                index += len(wordArray[j])


        for k in range(0, len(goodWords)):
            index = 0
            index = 0
            for l in range(0, len(wordArray)):
                sanitized = re.sub('[^\\w]', ' ', wordArray[l]).lower().strip()
                if self.levenshtein(sanitized, goodWords[k]) < self._get_tolerance(goodWords[k]):
                    self.comment.add_flagged_word(wordArray[l], goodWords[k], index, index + len(wordArray[l]), goodWordsWeight[k])
                index += 1
                index += len(wordArray[l])


        for m in range(0, len(badWords)):
            index = 0
            for n in range(0, len(wordArray)):
                sanitized = re.sub('[^\\w]', ' ', wordArray[n]).lower().strip()
                if self.levenshtein(sanitized, badWords[m]) < self._get_tolerance(badWords[m]):
                    self.comment.add_flagged_word(wordArray[n], badWords[m], index, index + len(wordArray[n]), badWordsWeight[m])
                index += 1
                index += len(wordArray[n])


        for o in range(0, len(self.negatorWordList)):
            index = 0
            for p in range(0, len(wordArray)):
                sanitized = re.sub('[^\\w]', ' ', wordArray[p]).lower().strip()
                if self.negatorWordList[o] == wordArray[p]:
                    self.comment.add_negator_word(wordArray[p], self.negatorWordList[o], index, index + len(wordArray[p]), 0)
                index += 1
                index += len(wordArray[p])


        flaggedWords = self.comment.get_flagged_words()
        for word in flaggedWords:
            commentRating += word[4]

        signatures = Signatures(self.comment)
        if signatures.sig_cease_and_decist() != False:
            self.comment.add_signature(signatures.sig_cease_and_decist())
            commentRating += signatures.sig_cease_and_decist()[3]
        if signatures.sig_good_quality() != False:
            self.comment.add_signature(signatures.sig_good_quality())
            commentRating += signatures.sig_good_quality()[3]
        if signatures.sig_bad_quality() != False:
            self.comment.add_signature(signatures.sig_bad_quality())
            commentRating += signatures.sig_bad_quality()[3]
        if signatures.sig_malware() != False:
            self.comment.add_signature(signatures.sig_malware())
            commentRating += signatures.sig_malware()[3]
        if signatures.sig_rated_content() != False:
            self.comment.add_signature(signatures.sig_rated_content())
            commentRating += signatures.sig_rated_content()[3]
        self.comment.set_comment_rating(commentRating)


    def get_cache(self):
        return self.comment


