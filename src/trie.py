#!/usr/local/bin/python
# coding: utf8

'''
    File name: trie.py
    File description: Implementation for Trie
    Date created: Sep 11, 2017
    Python Version: 2.7
'''


class Trie_Node:
    """
    """
    __slots__ = ('val', 'children')

    def __init__(self):
        self.val = None
        self.children = {}

    def get(self, letter):
        if letter not in self.children:
            self.children[letter] = Trie_Node()

        return self.children[letter]

    def exists(self, letter):
        return self.children[letter] if letter in self.children else None

    def setValue(self, val):
        self.val = val

    def getValue(self):
        return self.val


class Trie:
    """
    """
    __slots__ = ('root')

    def __init__(self):
        self.root = Trie_Node()
        pass

    def add(self, word, val):
        current = self.root
        for letter in word:
            current = current.get(letter)

        current.setValue(val)

    def get(self, word):
        current = self.root
        for letter in word:
            current = current.exists(letter)
            if current is None:
                return None

        if current:
            return current.getValue()
