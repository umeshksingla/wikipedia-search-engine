#!/usr/local/bin/python
# coding: utf8

'''
	File name: titlesIndex.py
	File description: Indexing for titles
	Author: Umesh Singla
	Date created: Sep 11, 2017
	Python Version: 2.7
'''

import sys
import xml.sax


class WikiContentHandler(xml.sax.handler.ContentHandler):
	"""
	"""
	def __init__(self, indexFile):
		self.outIndex = open(indexFile, "w")

		self.id = 0
		self.title = ""

		self.elements = []
		self.data = ""

	def startElement(self, name, attrs):
		"""
		when the event is "start" in the xml-tree
		"""
		self.elements.append(name)
		self.data = ""

	def characters(self, content):
		"""
		"""
		if self.elements[-1] in ["title", "id"]:
			self.data += content

	def endElement(self, name):
		"""
		when the event is "end" in the xml-tree
		"""
		# remove the current element from path
		self.elements.pop()
		if name == "page":
			# note down the page's id and title
			self.outIndex.write(self.id.encode('utf8') + ':')
			self.outIndex.write(self.title.encode('utf8') + '\n')
			# get ready for next page
			self.id = 0
			self.title = ''
		if name == "title":
			self.title = self.data
		elif name == "id" and self.elements[-1] == "page":
			self.id = self.data

	def endDocument(self):
		pass


def parseXML(xmlFile, indexFile):
	"""
	"""
	# implement own content handler
	contentHandler = WikiContentHandler(indexFile)
	
	# get a SAX XMLReader object
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	# use above content handler instead of default
	parser.setContentHandler(contentHandler)

	# create a SAX parser and use it to parse a document
	parser.parse(xmlFile)


if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: python titlesIndex.py <wikiXMLFile> titlesIndex\n")
		exit(1)

	parseXML(sys.argv[1], sys.argv[2])