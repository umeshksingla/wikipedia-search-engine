# coding: utf8

'''
	File name: contentHandler.py
	File description:
	Author: Umesh Singla
	Date created: Aug 21, 2017
	Python Version: 2.7
'''

import xml.sax
from page import Page

class WikiContentHandler(xml.sax.handler.ContentHandler):
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

	def startDocument(self):
		pass

	def endDocument(self):
		"""
		at the end of docoument, send the pages to pre-process
		"""
		# add a keyword 'finished' at the end of a queue
		self.pagesQueue.put("finished")
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

		self.elements.append(name)
		self.content = ""

	def endElement(self, name):
		"""
		when the event is "end" in the xml-tree
		"""
		# remove the current element from path
		self.elements.pop()

		if name == "page":
			# add it to the queue to process
			self.pagesQueue.put(self.currentPage)
			# nullify the current document
			self.currentPage = None
		elif name == "text":
			self.currentPage.setText(self.content)
		elif name == "title":
			self.currentPage.setTitle(self.content)
		elif name == "id":
			lastTag = self.elements[-1]
			if lastTag == "page":
				# use the id of the page as the currentPage's id
				# print "p", self.content
				self.currentPage.setId(self.content)

	def characters(self, content):
		"""
		the valid tags' content - id, title, text here
		"""
		lastTag = self.elements[-1]
		if lastTag == "title" or lastTag == "id" or lastTag == "text":
			self.content += content
	
	def setDocumentLocator(self, locator):
		"""
		Called by the parser to give the application a locator for locating
		the origin of document events.

		Provies a way to associate a SAX event with a page location.
		"""
		self.locator = locator


def parser(xmlFile, pagesQueue):
	"""
	"""
	# implement own content handler
	contentHandler = WikiContentHandler(pagesQueue)
	
	# get a SAX XMLReader object
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	# use above content handler instead of default
	parser.setContentHandler(contentHandler)

	# create a SAX parser and use it to parse a document
	parser.parse(xmlFile)
