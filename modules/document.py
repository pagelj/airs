#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Document

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

#from modules.parsedoc import *
from tokenizer import *

class Document(object):


    def __init__(self, content):

        #print content

        self.length = len(content)
        #self.date

        self.tokens=Tokenizer(content)

        self.numofwords=len(self.tokens.tokenized)

        #return self.tokens




###########################################################
####################### Testing ###########################
###########################################################

def main():

    pass

if __name__=='__main__':

    main()
