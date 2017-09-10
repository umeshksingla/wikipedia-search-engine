#!/usr/local/bin/python
# coding: utf8

'''
	File name: pickledindex.py
	File description: Builds a cPickled Index
	Author: Umesh Singla
	Date created: Sep 11, 2017
	Python Version: 2.7
'''

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

		self.initialIndexFile = open(openFile("initialIndex"), "r")
		self.titlesIndexFile = open(openFile("titlesIndex"), "r")
		self.getSecondaryIndex()

	def getSecondaryIndex():
		"""
		Loads the secondary index, titles and synonymns index files into
		memory to use for searching. These files should be prepared before.
		"""
		with open(openFile("titlesIndex"), "r") as titlesIndex:
			position = 0
			for each in titlesIndex:
				titleIndex = each.split(':', 1)[0]
				self.pageList.append(int(titleIndex))
				self.titlePos.append(position)
				position += len(each)

		with open(openFile("secondIndex"), "rb") as secondIndex:
			size = cPickle.load(secondIndex)
			for i in xrange(size):
				# get the entry tuple
				entry = cPickle.load(secondIndex)
				self.wordIndex.append(entry[0])
				self.posIndex.append(entry[1])
				self.freqIndex.append(entry[2])

		with open(openFile("synonymIndex"), "rb") as synonymIndex:
			self.synonymIndex = cPickle.load(synonymIndex)

	def openFile(self, f):
		"""
		"""
		return os.path.abspath(self.indexDir) + '/' + f



