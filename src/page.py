#!/usr/local/bin/python
# coding: utf8

'''
    File name: page.py
    File description: A Page consisting of xml <page>
    Author: Umesh Singla
    Date created: Aug 21, 2017
    Python Version: 2.7
'''

class Page():
    """
    A Page consisting of xml <page>
    """
    def __init__(self, n):

        self.id = None
        self.title = ""
        self.text = ""
        self.lineNo = n

    def setTitle(self, title):
        self.title = title

    def setText(self, text):
        self.text = text

    def setId(self, id):
        self.id = id
