#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Document

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
08/12/2016

"""

from tokenizer import *
from term import *

class Document(object):

    # Represent documents.


    def __init__(self, content):


        self.length = len(content)

        self.tokens=Tokenizer(content)

        self.numofwords=len(self.tokens.tokenized)

    def snippet(doc, query):

        # Function for printing snippets for the
        # interactive query interface.

        terms = terminator(doc.tokens.tokenized)
        tokens = doc.tokens.tokenized
        query = query.terms
        snippet = []
        left_context = 10
        right_context = 10

        for token_id in range(len(tokens)):

            for word in query:

                if terms[token_id] == word:

                    try:

                        snippet.append(' [...]')

                        for context in xrange(1,left_context+1,1):

                            snippet.append(tokens[token_id-context])

                        snippet.append('\033[1m'+tokens[token_id]+'\033[0m')

                        for context in xrange(1,right_context+1,1):

                            snippet.append(tokens[token_id+context])

                        snippet.append('[...]')
                        snippet.append('\n\n')

                    except IndexError:

                        snippet.append('[...]')
                        snippet.append('\n\n')

                        continue

        return ' '.join(snippet)


###########################################################
####################### Testing ###########################
###########################################################

def main():

    pass

if __name__=='__main__':

    main()
