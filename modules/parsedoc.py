#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Parse Document

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

################################################
##################### Import ###################
################################################

import os
import re


################################################
##################### Classes ##################
################################################

class Parsedoc(object):

    """
    Parsedoc reads in one file a time and provides
    the file content and file id
    """

    def __init__(self, filename):

        # Store the output of filereader as the content
        self.content = self.filereader(filename)
        # filename entails the whole path. On a *nix system
        # the following regex truncates the path and returns
        # only the filename, i.e. the docid
        self.docid = re.sub(r'^.*\/(.*)$',r'\1',filename)



    def filereader(self,filename):

        f = open(filename, 'r')
        content = f.read()
        f.close()
        return content



###########################################################
####################### Testing ###########################
###########################################################

def main():

    ParsedocObj1 = Parsedoc(os.path.relpath('../testfile_amazon_rewievs/1.txt'))
    print ParsedocObj1.docid
    print ParsedocObj1.content

if __name__=='__main__':

    main()
