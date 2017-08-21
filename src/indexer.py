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
	# return a SAX XMLReader objec
	parser = xml.sax.make_parser()
	pass


def index(xmlFile, outputFile):
	"""
	Steps:
	1. parse
	2. index
	"""
	pass

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: bash index.sh <path-to-wiki-dump> <path-to-invertedindex (outputfile)>"
		sys.exit(1)
