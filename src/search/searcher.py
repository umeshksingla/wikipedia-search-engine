#!/usr/local/bin/python
# coding: utf8

'''
	File name: searcher.py
	File description: Interface for search
	Author: Umesh Singla
	Date created: Sep 11, 2017
	Python Version: 2.7
'''

import search

def serve(indexDir):
	"""
	Serve the interface for searching a given query
	"""
	search.initialize(indexDir)

	while True:
		query = raw_input()
		terms = query.strip().lower().split()
		if terms:
			result = search.search(terms)
			print result
			print '\n'
		else:
			print "Search field can not be empty\n"
