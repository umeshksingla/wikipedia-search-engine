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
#from nltk import PorterStemmer
import Stemmer

StopWords = {'all': 1, 'whys': 1, 'being': 1, 'over': 1, 'isnt': 1,
	'through': 1, 'yourselves': 1, 'hell': 1, 'its': 1, 'before': 1,
	'wed': 1, 'with': 1, 'had': 1, 'should': 1, 'to': 1, 'lets': 1,
	'under': 1, 'ours': 1, 'has': 1, 'ought': 1, 'do': 1, 'them': 1,
	'his': 1, 'very': 1, 'cannot': 1, 'they': 1, 'werent': 1, 'not': 1,
	'during': 1, 'yourself': 1, 'him': 1, 'nor': 1, 'wont': 1, 'did': 1,
	'theyre': 1, 'this': 1, 'she': 1, 'each': 1, 'havent': 1,
	'where': 1, 'shed': 1, 'because': 1, 'doing': 1, 'theirs': 1, 'some': 1,
	'whens': 1, 'up': 1, 'are': 1, 'further': 1, 'ourselves': 1, 'out': 1,
	'what': 1, 'for': 1, 'heres': 1, 'while': 1, 'does': 1, 'above': 1,
	'between': 1, 'youll': 1, 'be': 1, 'we': 1, 'who': 1, 'were': 1, 'here': 1,
	'hers': 1, 'by': 1, 'both': 1, 'about': 1, 'would': 1, 'wouldnt': 1,
	'didnt': 1, 'ill': 1, 'against': 1, 'arent': 1, 'youve': 1, 'theres': 1,
	'or': 1, 'thats': 1, 'weve': 1, 'own': 1, 'whats': 1, 'dont': 1, 'into': 1,
	'youd': 1, 'whom': 1, 'down': 1, 'doesnt': 1, 'theyd': 1, 'couldnt': 1,
	'your': 1, 'from': 1, 'her': 1, 'hes': 1, 'there': 1, 'only': 1, 'been': 1,
	'whos': 1, 'hed': 1, 'few': 1, 'too': 1, 'themselves': 1, 'was': 1,
	'until': 1, 'more': 1, 'himself': 1, 'on': 1, 'but': 1, 'you': 1,
	'hadnt': 1, 'shant': 1, 'mustnt': 1, 'herself': 1, 'than': 1, 'those': 1,
	'he': 1, 'me': 1, 'myself': 1, 'theyve': 1, 'these': 1, 'cant': 1,
	'below': 1, 'of': 1, 'my': 1, 'could': 1, 'shes': 1, 'and': 1, 'ive': 1,
	'then': 1, 'wasnt': 1, 'is': 1, 'am': 1, 'it': 1, 'an': 1, 'as': 1,
	'itself': 1, 'im': 1, 'at': 1, 'have': 1, 'in': 1, 'id': 1, 'if': 1,
	'again': 1, 'hasnt': 1, 'theyll': 1, 'no': 1, 'that': 1, 'when': 1,
	'same': 1, 'any': 1, 'how': 1, 'other': 1, 'which': 1, 'shell': 1,
	'shouldnt': 1, 'our': 1, 'after': 1, 'most': 1, 'such': 1, 'why': 1,
	'wheres': 1, 'hows': 1, 'off': 1, 'i': 1, 'youre': 1, 'well': 1, 'www': 1,
	'yours': 1, 'their': 1, 'so': 1, 'the': 1, 'having': 1, 'once': 1, 'a': 1}


def tokenize(text, title):
	"""
	Tokenizer as a util
	"""
	
	# remove punctuation marks from the string and put space
	punct = r'[\\\/\{\}\(\)\<\>\:\!\?\;\|\=\*\&\$\#\@\^\-\+\×\%\.\,\"“”″•֊‐‑‒–—―⸺⸻〜﹘﹣－−__]'
	regex = re.compile(punct)
	word_list = re.sub(regex, ' ', text)

	# regex to replace by empty string
	regex = re.compile(r'[\'\`′‘’\[\]]')
	word_list = re.sub(regex, '', word_list)

	# regex to replace numbers by empty string
	# word_list = re.sub(r'\d+', '', word_list)

	# remove all the whitespaces and split on it
	word_list = word_list.split()

	# remove the empty strings, if any
	word_list = filter(None, word_list)

	stemmer = Stemmer.Stemmer('english')

	# remove the stopwords from normal text and not title
	if not title:
		word_list = filter(lambda x: x and x not in StopWords, word_list)
	# word_list = map(lambda x: stemmer.stemWord(x), word_list)
	return word_list
