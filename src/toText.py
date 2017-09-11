#!/usr/local/bin/python
# coding: utf8

'''
    File name: toText.py
    File description: Pickle dump to text
    Author: Umesh Singla
    Date created: Sep 11, 2017
    Python Version: 2.7
'''

import sys
import codecs
import cPickle

def convert(inFilename, outFilename):
    """
    """
    with open(inFilename, "rb") as infile:
        index = cPickle.load(infile)

    with codecs.open(outFilename, "w", "utf-8") as outfile:
        for word, pos in index:
            outfile.write(word)
            outfile.write(":")
            outfile.write(str(pos))
            outfile.write("\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python toText.py <secondary_index> <out_index>\n")
        exit(1)

    convert(sys.argv[1], sys.argv[2])