#!/usr/bin/python
import os
import json
import re
import config
import searchcache
from analysis import Wordlist

class Comments:
	#Provides functions needed to extrapolate comment data from individual files

	def __init__(self, hash):
		wordlist = Wordlist()
		self.hash = hash
		self.goodAdjectives = wordlist.get_good_adjs()
		self.badAdjectives = wordlist.get_bad_adjs()
		self.negators = wordlist.get_negators()
		self.contextWords = wordlist.get_context_nouns()
		self.allWords = self.badAdjectives + self.goodAdjectives + self.negators + self.contextWords
		self.commentsAndValues = []

	def mark_visited(self):
		#Marks the hash of a file that has already been visited
		f = open(config.variables.get("session_data"), "w")
		f.write(self.hash)

	def set_comments(self):
		#Gets all the comments and values of those comments for a particular file
		comment = ()
		data = searchcache.open_search_by_hash(self.hash)
		jsonObject = json.loads(data)
		for key, value in jsonObject.iteritems():
			if key == "comments":
				for comments in value:
					if len(comments) > 0:
						comment = (comments[0][0].strip().replace("<br />",""), str(comments[0][1]))
						self.commentsAndValues.append(comment)
		self.commentsAndValues.append(comment)
	
	def get_positive_comments(self):
		positiveComments = []
		for comment in self.commentsAndValues:
			if int(comment[1]) > 0:
				positiveComments.append(comment)
		return positiveComments
	
	def get_negative_comments(self):
		negativeComments = []
		for comment in self.commentsAndValues:
			if int(comment[1]) < 0:
				negativeComments.append(comment)
		return negativeComments

	def get_words_from_negative_comments(self):
		negativeWords = []
		negativeComments = self.get_negative_comments()
		for comment in negativeComments:
			words = comment[0].split(" ")
			for word in words:
				if len(word) > 3 and word not in self.allWords:
					negativeWords.append(str(re.sub(r'[^\w]', '', word).lower().strip()))
		return negativeWords
	
	def get_words_from_positive_comments(self):
		positiveWords = []
		positiveComments = self.get_positive_comments()
		for comment in positiveComments:
			words = comment[0].split(" ")
			for word in words:
				if len(word) > 3 and word not in self.allWords:	
					positiveWords.append(str(re.sub(r'[^\w]', '', word).lower().strip()))
		return positiveWords
