#!/usr/local/bin/python
# coding: utf8

'''
	File name: textHighLevelParser.py
	File description:
	Author: Umesh Singla
	Date created: Aug 21, 2017
	Python Version: 2.7
'''

from tokenizer import tokenize
from textLowLevelParser import parseWikipediaText

from multiprocessing import Process, Value

import time

parsedPagesQueue = None
processedPagesQueue = None
count = Value('i', 0)


def highLevelParser(page):
	"""
	"""
	page.wikitext, page.titles, page.references, page.categories,\
		page.links, page.infobox = parseWikipediaText(page.text)
	
	word_list = { 
		'pageId': page.id,
		'fields': { 't': [], 'h': [], 'b': [], 'i': [], 'c': [], 'r': [], 'l': []}
		}

	word_list['fields']['t'] = tokenize(page.title, True)
	word_list['fields']['h'] = tokenize(page.titles, True)
	
	word_list['fields']['b'] = tokenize(page.wikitext, False)
	word_list['fields']['i'] = tokenize(page.infobox, False)
	word_list['fields']['c'] = tokenize(page.categories, True)

	word_list['fields']['r'] = tokenize(page.references, False)
	word_list['fields']['l'] = tokenize(page.links, False)
	return word_list


def jobs(parsedPagesQueue, processedPagesQueue, count):
	"""
	"""
	while True:
		# retrive a page
		page = parsedPagesQueue.get()

		if page == "finished":
			parsedPagesQueue.task_done()
			return

		text = highLevelParser(page)
		processedPagesQueue.put(text)

		# increment the count of pages
		count.value += 1
		parsedPagesQueue.task_done()


def parser(parsedPagesQueue, processedPagesQueue):
	"""
	"""
	global parsedpages, processedpages

	parsedPagesQueue = parsedPagesQueue
	processedPagesQueue = processedPagesQueue

	threadProcess = Process(target=jobs, args=(parsedPagesQueue, processedPagesQueue, count))

	pool = []
	pool.append(threadProcess)

	threadProcess.start()

	while any(threadProcess.is_alive() for threadProcess in pool):
		time.sleep(.1)

	for threadProcess in pool:
		threadProcess.join()

	processedPagesQueue.put("finished")
	processedPagesQueue.close()
	processedPagesQueue.join()
