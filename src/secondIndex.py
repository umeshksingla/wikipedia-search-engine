#!/usr/local/bin/python
# coding: utf8

'''
	File name: secondIndex.py
	File description: Indexing for synonyms
	Author: Umesh Singla
	Date created: Sep 11, 2017
	Python Version: 2.7
'''

import cPickle
import sys

secondIndex = []
def secondIndex(primaryIndexFile, secIndexFile):
	"""
	"""
	position = 0
	infile = open(primaryIndexFile, "r")

	for i, line in enumerate(infile):
		l = line[:line.rfind(':')]
		l = unicode(l, "utf-8")
		parts = l.rsplit('_', 1)
		word = (parts[0], position, int(parts[1]))
		secondIndex.append(word)
		position += len(line)

	infile.close()

	with open(secondIndex, "wb") as outFile:
		cPickle.dump(len(secondIndex), outFile, 2)
		for each in secondIndex:
			cPickle.dump(each, outFile, 2)


if __main__ == '__main__':
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: python secondIndex.py <primaryIndexFile> secondIndex\n")
		exit(1)
	secondIndex(argv[1], argv[2])
