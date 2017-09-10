#!/usr/local/bin/python
# coding: utf8

'''
	File name: indexer.py
	File description:
	Author: Umesh Singla
	Date created: Aug 21, 2017
	Python Version: 2.7
'''

import contentHandler as content_p
import textHighLevelParser as retrieve_p

import combiner as cmb
import codecs
import sys
import os

from multiprocessing import Process, JoinableQueue

class PageIndex:
	"""
	"""
	def __init__(self, outputFile):

		self.outputFile = outputFile
		self.fileNo = 0

		self.index = {}
		self.pages = 0

	def getfile(self, n=None):
		"""
		"""
		if n is None:
			n = self.fileNo
			self.fileNo += 1

		return self.outputFile + '/index' + str(n)

	def indexPage(self, page):
		"""
		count of a word in each document, separately for title, body,
		headings, references, links etc.
		"""

		pageId = page["pageId"]
		fields = page["fields"]

		for f in fields:
			for word in fields[f]:
				id = word + "_" + f
				if id not in self.index:
					self.index[id] = {}

				if pageId not in self.index[id]:
					self.index[id][pageId] = 0

				self.index[id][pageId] += 1

		self.pages += 1

		# when so many files created
		if self.pages >= 500000:
			self.writeToFile1()

	def writeToFile1(self):
		"""
		"""
		self.writeToFile2(self.getfile())

		self.index = {}
		self.pages = 0

	def writeToFile2(self, fname):
		"""
		"""
		d = codecs.open(fname, "w", "utf-8")

		word_list = self.index.keys()
		word_list.sort()

		for w in word_list:

			# get the pages id in sorted order or linear merging
			pages = sorted(self.index[w].keys(), key=lambda x: int(x))

			c = str(len(self.index[w]))

			d.write(w + "_" + c + ":")
			for p in pages:
				c = str(self.index[w][p])
				d.write(str(p) + "_" + c + ",")

			d.write('\n')
			del self.index[w]

		d.close()

	def combineFiles(self, fm):
		"""
		temporarily combining files
		"""
		if len(fm) <= 1:
			return
		c = cmb.MergeFilesTool(self.getfile())
		for f in fm:
			c.appendFile(f)
		c.combine()
		del c

	def finishIndexing(self):
		"""
		"""
		fm = []
		c = 0

		self.writeToFile2(self.getfile())

		self.index = {}
		self.pages = 0

		while True:
			if c >= self.fileNo:
				break

			fm.append(self.getfile(c))

			if len(fm) >= 4:
				self.combineFiles(fm)
				fm = []
			c += 1

		# combine the remaining files now
		self.combineFiles(fm)


def jobs(pages_retrieve_sequence, outputFile):
	"""
	"""

	index = PageIndex(outputFile)

	if not os.path.exists(outputFile):
		os.makedirs(outputFile)

	while True:
		page = pages_retrieve_sequence.get()
		if page == "finished":
			pages_retrieve_sequence.task_done()
			break
		index.indexPage(page)
		pages_retrieve_sequence.task_done()

	index.finishIndexing()


def index(xmlFile, outputFile):
	"""
	"""
	if not os.path.exists(outputFile):
		os.makedirs(outputFile)

	pages_parse_sequence = JoinableQueue(15)
	pages_retrieve_sequence = JoinableQueue(10000)

	content_pr = Process(target=content_p.parser, args=(xmlFile, pages_parse_sequence))
	content_pr.start()

	retrieve_pr = Process(target=retrieve_p.parser, args=(pages_parse_sequence, pages_retrieve_sequence))
	retrieve_pr.start()

	index_pr = Process(target=jobs, args=(pages_retrieve_sequence, outputFile))
	index_pr.start()

	content_pr.join()
	retrieve_pr.join()
	index_pr.join()


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print """ USAGE: bash index.sh <path-to-wiki-dump> 
			<path-to-invertedindex (output directory)> """
		sys.exit(1)

	index(sys.argv[1], sys.argv[2])
