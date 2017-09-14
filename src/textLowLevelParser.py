#!/usr/local/bin/python
# coding: utf8

'''
	File name: textLowLevelParser.py
	File description:
	Author: Umesh Singla
	Date created: Aug 21, 2017
	Python Version: 2.7
'''

import re
import HTMLParser

# TODO: try to avoid global variables
infoboxContent = ''
html_parser = None

def replaceFunction(matchObj):
	"""
	"""
	parts = matchObj.group().split('|')
	name = parts[0]

	# split() used because Infobox and cite are followed by a name before | occurs
	if len(name.split()) and name.split()[0] == "infobox":
		infoboxContent += ' '.join(parts[1:])
		return ''
	elif name == "main":
		return ' '.join(parts[1:])
	elif name == "see also":
		return ' '.join(parts[1:])
	else:
		return ''


def splitPageContents(text):
	"""
	Split the page contents into Infobox, Main, See Also,
	quote, cite etc. sections, helpful for search
	"""
	regex = re.compile(u'\{\{([^\}]*?)\}\}', re.MULTILINE | re.DOTALL)
	return re.sub(regex, replaceFunction, text)


def getSectionRegex(sectionName):
	"""
	regular expression for getting any section, example == References == or ===Communication===
	"""
	regexString = r'^==\s*' + sectionName.lower() + r'\s*==\s*$(.*?)^(?:==|$)'
	regex = re.compile(regexString, re.MULTILINE | re.IGNORECASE | re.DOTALL)
	return regex


def getSectionText(sectionName, text, remove=True):
	"""
	get the section
	"""
	regex = getSectionRegex(sectionName)
	sectionText = re.findall(regex, text)
	text = re.sub(regex, u'==', text)

	return sectionText, text


def removeHTML(text):
	"""
	remove HTML comments and tags
	"""
	regex = re.compile(r'(<su[bp].*?>|<!--.*?-->)', re.DOTALL)
	return re.sub(regex, '', text)


def removeURLPrefix(text):
	"""
	remove the prefix https:// or ftp:// from the text
	"""
	regex = re.compile(r'((?:https?)\:\/\/[^\]\s]+)')
	text = re.sub(regex, '', text)
	
	regex = re.compile(r'((ftp)\:\/\/[^\]\s]+)')
	return re.sub(regex, '', text)


def getInfoboxText(text):
	"""
	Example: 
	{{Infobox U.S. state symbols
		.
		.
		|Boxwidth= 25e
		|Flower= [[Camellia]], [[Hydrangea quercifolia|Oak-leaf Hydrangea]]'
		.
		.
	}}
	"""
	regex = re.compile(r'\[\[([^\]]*?)\]\]', re.DOTALL)
	subs = True
	
	while subs is not 0:
		# keep splitting the links at '|' removing '[[ ]]'
		text, subs = re.subn(regex,
							lambda x: x.group(1).split('|')[-1], text)

	return text


def parseinfoboxContentText(text):
	"""
	"""
	text = removeHTML(text)
	text = getInfoboxText(text)
	text = removeURLPrefix(text)
	return text


def getReferencesText(text):
	"""
	Example:
	<ref name="Trinity College">
		[http://starbase.trincoll.edu/~crypto/resources/LetFreq.html
		"Percentages of Letter frequencies per Thousand words"],
		Trinity College, Retrieved 1 May 2006.
	</ref>
	"""
	regex = re.compile(r'\[\[([^\]]*?)\]\]', re.DOTALL)
	subs = True
	
	while subs is not 0:
		# keep splitting the links at '|' removing '[[ ]]'
		text, subs = re.subn(regex,
							lambda x: x.group(1).split('|')[-1], text)

	return text


def parseReferencesText(referencesSectionText, text):
	"""
	"""
	refRegex = re.compile(ur"\<ref(?:\s[^\>]*[^\/])?(?:\>(.*?)\<\/ref|\/)\>",
					   re.DOTALL)
	references = ' '.join(re.findall(refRegex, text))
	references += ' '.join(referencesSectionText)
	
	references = removeHTML(references)
	references = getReferencesText(references)
	references = removeURLPrefix(references)

	# remove references text from main text now
	text = re.sub(refRegex, '', text)

	return references, text


def parseCategoryText(text):
	"""
	"""
	regex = re.compile(r'\[\[category:(.*?)\]\]', re.DOTALL)
	categories = re.findall(regex, text)
	categories = ' '.join(categories)
	text = re.sub(regex, '', text)
	return categories, text


def parseLinks(text):
	"""
	"""
	text = removeHTML(text)
	text = getInfoboxText(text)
	text = removeURLPrefix(text)
	return text


def retrieveDifferentTitles(text):
	"""
	"""
	regex = re.compile(r'^==([^=]*)==$', re.MULTILINE)
	a = re.findall(regex, text)
	regex = re.compile(r'^===([^=]*)===$', re.MULTILINE)
	b = re.findall(regex, text)
	regex = re.compile(r'^====([^=]*)====$', re.MULTILINE)
	c = re.findall(regex, text)
	regex = re.compile(r'^=====([^=]*)====$', re.MULTILINE)
	d = re.findall(regex, text)

	text = re.sub(r'^==.*==$', '', text, flags=re.MULTILINE)
	
	titles = ' '.join( reduce(lambda a, x: a + x, [a, b, c, d], []))

	return titles, text


def parseText(text):
	"""
	"""
	text = removeHTML(text)
	text = getInfoboxText(text)
	text = removeURLPrefix(text)
	return text


def html_decode(text):
	"""
	"""
	global html_parser
	if not html_parser:
		html_parser = HTMLParser.HTMLParser()
	return html_parser.unescape(text)


def parseWikipediaText(text):
	"""
	"""
	# lower case everything in the page
	text = html_decode(text).lower()

	# process infobox content
	text = splitPageContents(text)
	infobox = parseinfoboxContentText(infoboxContent)

	# process references
	referencesSectionText, text = getSectionText("References?", text)
	references, text = parseReferencesText(referencesSectionText, text)

	# process categories
	categories, text = parseCategoryText(text)

	# process external links
	links, text = getSectionText("External links", text)
	links = parseLinks(' '.join(links))

	# process titles
	titles, text = retrieveDifferentTitles(text)

	# process the main text now
	text = parseText(text)

	# return all the content
	return (text, titles, references, categories, links, infobox)
