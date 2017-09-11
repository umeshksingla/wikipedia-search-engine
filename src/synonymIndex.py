#!/usr/local/bin/python
# coding: utf8

'''
	File name: synonymIndex.py
	File description: Indexing for synonyms
	Author: Umesh Singla
	Date created: Sep 11, 2017
	Python Version: 2.7
'''

import cPickle
import sys

synIndex = {}
wordIndex = {}

def synonymIndex(secIndexFile, outsynIndexFile):
	"""
	input file is a secondary-indexed file
	"""
	with open(secIndexFile, "rb") as secIndex:
		size = cPickle.load(secIndex)
		for i in xrange(size):
			posting = cPickle.load(secIndex)
			#print posting
			low = posting[0].lower()
			if low not in wordIndex:
				wordIndex[low] = []
			wordIndex[low].append(posting[0])

	for word in wordIndex:
		if len(wordIndex[word]) > 1:
			synIndex[word] = wordIndex[word]

	with open(outsynIndexFile, "wb") as outsynIndex:
		cPickle.dump(synIndex, outsynIndex, 2)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: python synonymIndex.py <secIndexFile> synonymIndex\n")
		exit(1)
	synonymIndex(sys.argv[1], sys.argv[2])
