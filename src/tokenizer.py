#!/usr/local/bin/python
# coding: utf8

'''
    File name: tokenizer.py
    File description:
    Author: Umesh Singla
    Date created: Aug 21, 2017
    Python Version: 2.7
'''

import string
import re
from nltk import PorterStemmer


StopWords = ['is', 'when', 'i', 'www', 'for', 'what',
	'com', 'as', 'this', 'at', 'to', 'of', 'are', 'it',
	'from', 'by', 'or', 'the', 'in', 'with', 'that',
	'where', 'how', 'was', 'the', 'an', 'will', 'on',
	'a', 'be', 'who', 'about']


def tokenize(text, title):
	
	# remove punctuation marks from the string
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	word_list = regex.sub('', text)

	# remove all the whitespaces and split on it
	regex = re.compile('[%s]' % re.escape(' '))
	word_list = regex.split(word_list)

	# remove the empty strings, if any
	word_list = filter(None, word_list)

	# remove the stopwords from normal text and not title, if any
	if title:
		word_list = filter(lambda x: x not in StopWords, word_list)

	return word_list
