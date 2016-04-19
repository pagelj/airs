#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Tokenizer

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

################################################
##################### Import ###################
################################################

import re

################################################
##################### Classes ##################
################################################

class Tokenizer(object):

    
    def __init__(self, text):

        """
        Create object for storing tokenized text
        """

        self.tokenized = self._tokenize(text)
        
    def _tokenlist(self):
        return self.tokenized

    def _tokenize(self, text):

        """
        Simple tokenization function
        """


        # define punctuation
        punctuation = r'[^a-zA-Z\d\s]'

        text = text.split()

        text_new = []

        for token in text:


            # if a punctuation occurs in the token
            # separate it 
            if re.search(r'(' + punctuation + ')', token):

                token = re.sub(r'(' + punctuation + ')', r' \1 ', token)
                text_new.extend(token.split())

            else:

                text_new.append(token)

        return text_new


###########################################################
####################### Testing ###########################
###########################################################

def main():

    Tokenizer1 = Tokenizer('This is a test sentence.')
    print Tokenizer1.tokenized

if __name__=='__main__':

    main()
