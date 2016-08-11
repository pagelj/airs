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

from tokenizer import *
from term import *

class Document(object):


    def __init__(self, content):

        #print content

        self.length = len(content)
        #self.date

        self.tokens=Tokenizer(content)

        self.numofwords=len(self.tokens.tokenized)

        #return self.tokens

    def snippet(doc, query):

        terms = terminator(doc.tokens.tokenized)
        tokens = doc.tokens.tokenized
        query = query.terms
        snippet = []

        for token_id in range(len(tokens)):

            for word in query:

                if terms[token_id] == word:

                    try:

                        snippet.append(tokens[token_id-10])
                        snippet.append(tokens[token_id-9])
                        snippet.append(tokens[token_id-8])
                        snippet.append(tokens[token_id-7])
                        snippet.append(tokens[token_id-6])
                        snippet.append(tokens[token_id-5])
                        snippet.append(tokens[token_id-4])
                        snippet.append(tokens[token_id-3])
                        snippet.append(tokens[token_id-2])
                        snippet.append(tokens[token_id-1])
                        snippet.append('\033[1m'+tokens[token_id]+'\033[0m')
                        snippet.append(tokens[token_id+1])
                        snippet.append(tokens[token_id+2])
                        snippet.append(tokens[token_id+3])
                        snippet.append(tokens[token_id+4])
                        snippet.append(tokens[token_id+5])
                        snippet.append(tokens[token_id+6])
                        snippet.append(tokens[token_id+7])
                        snippet.append(tokens[token_id+8])
                        snippet.append(tokens[token_id+9])
                        snippet.append(tokens[token_id+10])
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
