#!/usr/local/bin/python
# coding: utf8

'''
	File name: combiner.py
	File description:
	Author: Umesh Singla
	Date created: Aug 21, 2017
	Python Version: 2.7
'''

from collections import deque
import codecs
import os

class MergeFilesTool():
	"""
	"""
	def __init__(self, outputFile):

		self.outputFile = codecs.open(outputFile, "w", "utf-8")

		self.fileslist = []
		self.blocks = []

		self.mergedBlocks = []

	def minvalue(self):
		"""
		"""
		n = len(self.fileslist)
		
		children = []
		for i in xrange(n):
			if self.blocks[i][0] is not None:
				children.append((i, self.blocks[i][0]))

		if len(children) == 0:
			return None

		ml = []
		minchild = min(children, key=lambda x: x[1][0])
		minValue = minchild[1][0]

		locations = filter(lambda x: x[1][0] == minValue, children)

		for loc in locations:
			self.blocks[loc[0]].popleft()
			ml.extend(loc[1][1])
		ml.sort(key=lambda x: int(x[0]))
		return (minValue, ml)

	def appendFile(self, f):
		"""
		"""
		self.fileslist.append(codecs.open(f, "r", "utf-8"))
		self.blocks.append(deque([]))

	def next(self, n):
		"""
		"""
		f = self.fileslist[n]
		l = f.readline()
		if l == '':
			return None

		parts = l.split(':')		
		a = parts[0].split('_')[:-1]
		b = parts[1].strip()[:-1]
		b = b.split(',')
		
		words = '_'.join(a)
		locations = map(lambda x: x.split('_'), b)

		return (words, locations)

	def loadNext(self):
		"""
		"""
		for i, block in enumerate(self.blocks):
			if not len(block):
				self.nextBlock(i)

	def nextBlock(self, n):
		"""
		"""
		block = self.blocks[n]
		l = True
		while l and len(block) < 1000:
			l = self.next(n)
			block.append(l)

	def writeToFile(self):
		"""
		"""
		for i in self.mergedBlocks:
			c = str(len(i[1]))
			self.outputFile.write(i[0] + '_' + c + ':')
			for page in i[1]:
				s = str(page[0]) + "_" + str(page[1]) + ","
				self.outputFile.write(s)
			self.outputFile.write('\n')

		self.mergedBlocks = []

	def combine(self):
		"""
		"""
		self.loadNext()
		while True:
			v = self.minvalue()
			if v is None:
				break
			self.mergedBlocks.append(v)
			if len(self.mergedBlocks) >= 4000:
				self.writeToFile()
			self.loadNext()
		self.writeToFile()

		for f in self.fileslist:
			f.close()
			os.remove(f)

if __name__ == '__main__':
	m = MergeFilesTool('merged')
	m.appendFile('../rough/index0')
	m.appendFile('../rough/index1')
	m.appendFile('../rough/index2')
	m.combine()
