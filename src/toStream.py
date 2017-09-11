#!/usr/local/bin/python
# coding: utf8

'''
    File name: toStream.py
    File description: Pickle text dump to byte stream
    Author: Umesh Singla
    Date created: Sep 11, 2017
    Python Version: 2.7
'''

import sys
import cPickle


def convert(inFilename, outFilename):
    """
    """
    with open(inFilename, "rb") as infile:
        index = cPickle.load(infile)

    with open(outFilename, "wb") as outfile:
        cPickle.dump(len(index), outfile, 2)
        for entry in index:
            cPickle.dump(entry, outfile, 2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python totoStream.py <secondary_index_text> <out_index>\n")
        exit(1)

    convert(sys.argv[1], sys.argv[2])