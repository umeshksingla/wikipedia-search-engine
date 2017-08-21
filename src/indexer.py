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

from page import Page

class WikiContentHandler(xml.sax.ContentHandler):
	"""
	These methods are called by the parser on the appropriate events in the
	input document.
	"""
	def __init__(self, pagesQueue):

		# queue to process pages
		self.pagesQueue = pagesQueue

		self.locator = None

		# current page information
		self.currentPage = None
		# content of the current (desired) elements
		self.content = ""

		self.totalPages = 0

		# xml elements occuring in the order
		self.elements = []

	def setDocumentLocator(self, locator):
		"""
		Called by the parser to give the application a locator for locating
		the origin of document events.

		Provies a way to associate a SAX event with a page location.
		"""
		self.locator = locator

	def startDocument(self):
		pass

	def endDocument(self):
		"""
		at the end of docoument, send the pages to pre-process
		"""
		# add a keyword 'stop' at the end of a queue
		self.pagesQueue.put("stop")
		self.pagesQueue.close()

		# join the parent process
		self.pagesQueue.join()

	def startElement(self, name, attrs):
		"""
		when the event is "start" in the xml-tree
		"""
		# need to process its contents
		if name == "page":
			# create a nice doucment out of it
			self.currentPage = Page(self.locator.getLineNumber())
			self.totalPages = self.totalPages + 1

		elements.append(name)
		self.content = ""

	def endElement(self, name):
		"""
		when the event is "end" in the xml-tree
		"""
		lastTag = elements[-1]
		if name == "page":
			# add it to the queue to process
			self.pagesQueue.put(self.currentDoc)
			# nullify the current document
			self.currentPage = None
		elif name == "text":
			self.currentPage.setText(self.data)
		elif name == "title":
			self.currentPage.setTitle(self.data)
		elif name == "id" and lastTag == "page":
			# use the id of the page as the currentPage's id
			self.currentPage.setId(self.data)

		# remove the current element from path
		self.currentPath.pop()

	def characters(self, content):
		"""
		the valid tags' content - id, title, text here
		"""
		lastTag = elements[-1]
		if lastTag == "title" or lastTag == "id" or lastTag == "text":
			self.content += content


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