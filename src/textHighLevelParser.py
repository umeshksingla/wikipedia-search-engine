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

pages_parse_sequence = None
pages_retrieve_sequence = None
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


def jobs(pages_parse_sequence, pages_retrieve_sequence, count):
	"""
	"""
	while True:
		# retrive a page
		page = pages_parse_sequence.get()

		if page == "finished":
			pages_parse_sequence.task_done()
			return

		text = highLevelParser(page)
		pages_retrieve_sequence.put(text)

		# increment the count of pages
		count.value += 1
		pages_parse_sequence.task_done()


def parser(parsedPagesQueue, processedPagesQueue):
	"""
	"""
	global pages_parse_sequence, pages_retrieve_sequence

	pages_parse_sequence = parsedPagesQueue
	pages_retrieve_sequence = processedPagesQueue

	th = Process(target=jobs, args=(pages_parse_sequence, pages_retrieve_sequence, count))

	pool = []
	pool.append(th)

	th.start()

	while any(th.is_alive() for th in pool):
		time.sleep(.1)

	for th in pool:
		th.join()

	pages_retrieve_sequence.put("finished")
	pages_retrieve_sequence.close()
	pages_retrieve_sequence.join()
