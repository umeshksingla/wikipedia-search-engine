#!/usr/local/bin/python
# coding: utf8

'''
	File name: pickledindex.py
	File description: Builds a cPickled Index
	Author: Umesh Singla
	Date created: Sep 11, 2017
	Python Version: 2.7
'''

from bisect import bisect_left

import cPickle
import array
import os


class Index():
	"""
	"""
	def __init__(self, indexDir):
		self.indexDir = indexDir
		self.wordIndex = []
		self.synonymIndex = {}

		self.pageList = array.array('L')
		self.posIndex = array.array('L')
		self.freqIndex = array.array('I')
		self.titlePos = array.array('I')

		self.getSecondaryIndex()
		self.initialIndexFile = open(self.openFile("initialIndex"), "r")
		self.titlesIndexFile = open(self.openFile("titlesIndex"), "r")

	def openFile(self, f):
		"""
		"""
		return os.path.abspath(self.indexDir) + '/' + f

	def getTitle(self, pageId):
		"""
		retrieves the title from a pageId
		"""
		i = bisect_left(self.pageList, pageId)
		position = None

		if i != len(self.pageList) and self.pageList[i] == pageId:
			position = self.titlePos[i]

		if position is None:
			return None

		# Go to that position in titles indexed file and take one line
		self.titlesIndexFile.seek(position)
		line = self.titlesIndexFile.readline()
		title = line.split(':', 1)[1]
		return unicode(title, 'utf-8').strip()

	def getSynonyms(self, word):
		"""
		"""
		if word in self.synonymIndex:
			return self.synonymIndex[word]
		else:
			return [word]

	def getPosition(self, word):
		"""
		"""
		i = bisect_left(self.wordIndex, word)
		if i != len(self.wordIndex) and self.wordIndex[i] == word:
			return i
		return None

	def getCount(self, word):
		"""
		"""
		synonymns = self.getSynonyms(word)
		count = 0
		for each in synonymns:
			position = self.getPosition(each)
			if position:
				count += self.freqIndex[position]
		return count

	def getPosting(self, word):
		"""
		"""
		postings = {}
		count = 0
		synonymns = self.getSynonyms(word)
		for each in synonymns:
			position = self.getPosition(each)
			if position is None:
				continue
			else:
				count += self.freqIndex[position]
				self.initialIndexFile.seek(self.posIndex[position])
				line = self.initialIndexFile.readline()
				line = unicode(line.strip(), 'utf-8')
				line = line.split(':')[1][:-1].split(',')
				for page in line:
					page = page.rsplit('_', 1)
					if page[0] not in postings:
						postings[page[0]] = 0
					postings[page[0]] += int(page[1])
		return postings

	def getSecondaryIndex(self):
		"""
		Loads the secondary index, titles and synonymns index files into
		memory to use for searching. These files should be prepared before.
		"""
		with open(self.openFile("titlesIndex"), "r") as titlesIndex:
			position = 0
			for each in titlesIndex:
				titleIndex = each.split(':', 1)[0]
				self.pageList.append(int(titleIndex))
				self.titlePos.append(position)
				position += len(each)

		with open(self.openFile("secondIndex"), "rb") as secondIndex:
			size = cPickle.load(secondIndex)
			for i in xrange(size):
				# get the entry tuple
				entry = cPickle.load(secondIndex)
				self.wordIndex.append(entry[0])
				self.posIndex.append(entry[1])
				self.freqIndex.append(entry[2])

		with open(self.openFile("synonymIndex"), "rb") as synonymIndex:
			self.synonymIndex = cPickle.load(synonymIndex)
