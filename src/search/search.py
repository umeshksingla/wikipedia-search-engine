#!/usr/local/bin/python
# coding: utf8

'''
	File name: search.py
	File description: Performs the search in indexed files
	Author: Umesh Singla
	Date created: Sep 11, 2017
	Python Version: 2.7
'''

from pickledindex import Index
from tokenizer import tokenize

import datetime
import math
import re

MAX = 1000

fields = {
	'title': '_t',
    'heading': '_h',
    'ref': '_r',
    'category': '_c',
    'link': '_l',
    'info': '_i',
    'body': '_b'
}

field_weights = {
    't': 6,
    'h': 5,
    'r': 4,
    'c': 3,
    'l': 2,
    'i': 1
}

def initialize(outputFile):
	"""
	Loads the index into memory
	"""
	global indexed
	indexed = Index(outputFile)


def appendAppropriate(term):
	"""
	"""
	search_terms = []
	search_terms.append(term + '_t')
	if indexed.getCount(term + '_t') < MAX:
		search_terms.append(term + '_h')
		if indexed.getCount(term + '_h') < MAX:
			search_terms.append(term + '_i')
			if indexed.getCount(term + '_i') < MAX:
				search_terms.append(term + '_b')
				if indexed.getCount(term + '_b') < MAX:
					search_terms.append(term + '_c')
	return search_terms


def processTerm(term):
	"""
	"""
	# check for a field query
	field = None
	field_abb = None
	search_terms = []
	if term.find(':') != -1:
		# extract the field if : is present
		field = term.split(':')[0]
		if field in fields:
			field_abb = fields[field]
			term = term.split(':')[1]
	# remove punctuation, numbers, spaces etc.
	print term
	if field_abb == "_t" or field_abb == "_h":
		tokens = tokenize(term, True)
	else:
		tokens = tokenize(term, False)
	print tokens

	# if field is mentioned exclusively in query (ofc, except body),
	# append _t/_h/_r etc. and search.
	# else, append all possible fields according to frequency
	if field_abb:
		search_terms = map(lambda w: w + field_abb, tokens)
	else:
		for each in tokens:
			search_terms = appendAppropriate(each)
	print search_terms
	return search_terms


class aSearchResult():
	"""
	A potential search result candidate
	"""
	def __init__(self):
		self.present = 0
		self.score = 0
		self.titleScore = 0.0

	def addWeight(self, s):
		self.score += s

	def increment(self):
		self.present += 1

	def getTitle(self):
		return self.title

	def setTitle(self, title):
		self.title = title
		titleTokens = tokenize(title, True)
		negCharsReg = re.compile(ur'[.\/\\\|:\.]')
		negChars = len(re.findall(negCharsReg, title)) + 1
		if titleTokens:
			self.titleScore = (1.0/len(titleTokens)) + (1.0/negChars)

	def getFinalScore(self):
		return self.present + self.titleScore + math.log10(self.score)


def process(postings):
	"""
	Processing and combining the result pages
	"""
	intersect = []
	resultPages = {}
	for each in postings:
		# 'each' is one term
		# 'p' is postings for each term
		p = postings[each]
		if not p:
			continue
		if len(p) > 10*MAX:
			intersect.append((len(p), p))
			continue
		for page in p:
			if page not in resultPages:
				resultPages[page] = aSearchResult()
				title = indexed.getTitle(int(page))
				resultPages[page].setTitle(title)
			# idf
			resultPages[page].increment()
			# add to tf
			resultPages[page].addWeight(p[page])
	
	intersect.sort(key=lambda x: x[0])

	for l, p in intersect:
		# 'each' is postings of each term
		if len(resultPages) < 10*MAX:
			for page in p:
				if page not in resultPages:
					resultPages[page] = aSearchResult()
					title = indexed.getTitle(int(page))
					resultPages[page].setTitle(title)
				resultPages[page].increment()
				resultPages[page].addWeight(p[page])
		else:
			for page in p:
				if page in resultPages:
					resultPages[page].increment()
					resultPages[page].addWeight(p[page])
	return resultPages


def finalScore(w):
	return w[1].getFinalScore()


def search(terms):
	"""
	"""
	s = datetime.datetime.now()
	
	allTerms = []
	for each in terms:
		allTerms.extend(processTerm(each))
	
	postings = {}
	for each in allTerms:
		postings[each] = indexed.getPosting(each)

	results = process(postings)
	results = sorted(results.items(),
					 key=finalScore,
					 reverse=True)

	e = datetime.datetime.now()

	response = {}
	response['time'] = (e - s).total_seconds()
	response['pages'] = []
	serveSize = min(len(results), 25)
	for i in xrange(serveSize):
		r = (results[i][0],
			results[i][1].getTitle(),
			results[i][1].getFinalScore())
		response['pages'].append(r)
	return response
