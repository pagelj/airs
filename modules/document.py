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
from query import *

class Document(object):


    def __init__(self, content):

        #print content

        self.length = len(content)
        #self.date

        self.tokens=Tokenizer(content)

        self.numofwords=len(self.tokens.tokenized)

        #return self.tokens

    def snippet(doc, query):

        tokens = doc.tokens.tokenized
        query = query.query
        snippet = []

        for token_id in range(len(tokens)):

            for word in query:

                if tokens[token_id] == word:

                    try:

                        snippet.append(tokens[token_id-5])
                        snippet.append(tokens[token_id-4])
                        snippet.append(tokens[token_id-3])
                        snippet.append(tokens[token_id-2])
                        snippet.append(tokens[token_id-1])
                        snippet.append('>>>'+tokens[token_id]+'<<<')
                        snippet.append(tokens[token_id+1])
                        snippet.append(tokens[token_id+2])
                        snippet.append(tokens[token_id+3])
                        snippet.append(tokens[token_id+4])
                        snippet.append(tokens[token_id+5])
                        snippet.append('\n\n')

                    except IndexError:

                        continue

        return ' '.join(snippet)


###########################################################
####################### Testing ###########################
###########################################################

def main():

    pass

if __name__=='__main__':

    main()
