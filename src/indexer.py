#!/usr/local/bin/python
# coding: utf8

'''
    File name: indexer.py
    File description:
    Author: Umesh Singla
    Date created: Aug 21, 2017
    Python Version: 2.7
'''

import sys
import xml.sax

def parser(xmlFile):
	"""
	"""
	# implement own content handler
	contentHandler = WikiContentHandler()
	
	# get a SAX XMLReader object
	parser = xml.sax.make_parser()

	# use above content handler instead of default
	parser.setContentHandler(contentHandler)

	# create a SAX parser and use it to parse a document
	parser.parse(xmlFile)


def index(xmlFile, outputFile):
	"""
	Steps:
	1. parse
	2. index
	"""
	parser(xmlFile)
	pass

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print """ USAGE: bash index.sh <path-to-wiki-dump> 
			<path-to-invertedindex (outputfile)> """
		sys.exit(1)

	index(sys.argv[1], sys.argv[2])