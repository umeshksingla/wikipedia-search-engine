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
import sys

def serve(indexDir):
	"""
	Serve the interface for searching a given query
	"""
	print "INITIALIZING..."
	search.initialize(indexDir)

	while True:
		print "\033[1;31m" + "Enter query:" + "\033[0m"
		query = raw_input()
		terms = query.strip().lower().split()
		if terms:
			result = search.search(terms)
			print "\033[0;36m" + "Results showed in", result["time"], "seconds" + "\033[0m"
			for page in result["pages"]:
				print "\033[0;32m" + page[1] + "\033[0;0m", '(' + page[0] + ')', ' Score: ' + str(page[2])
		else:
			print "Search field can not be empty"
		print '\n'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.stderr.write("Usage: python searcher.py <indexDir>\n")
		exit(1)
	serve(sys.argv[1])