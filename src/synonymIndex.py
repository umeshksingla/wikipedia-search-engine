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

synonymIndex = {}
wordIndex = {}

def synonymIndex(secIndexFile, out):
	"""
	input file is a secondary-indexed file
	"""
	with open(secIndexFile, "rb") as secIndex:
		size = cPickle.load(secIndex)
		for i in xrange(size):
			posting = cPickle.load(secIndex)
			low = posting[0].lower()
			if low not in wordIndex:
				wordIndex[low] = []
			wordIndex[low].append(posting[0])

	for word in wordIndex:
		if len(wordIndex[word]) > 1:
			synonymIndex[word] = wordIndex[word]

	with open(outsynIndexFile, "wb") as outsynIndex:
		cPickle.dump(synonymIndex, outsynIndex, 2)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: python synonymIndex.py <secIndexFile> <outsynIndexFile>")
		exit(1)
	synonymIndex(argv[1], argv[2])
