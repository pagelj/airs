#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Term

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""
import re
################################################
##################### Classes ##################
################################################

special_char = r"""[!,."']"""

class Term(object):

    def __init__(self,tokens):
        self.tokens=tokens.tokenized
        self.terms=self.terminator(self.tokens)
        

    def __str__(self):

        return str(self.terms)


    def terminator(self,tokens):
        terms = set([x.lower() for x in tokens])
        newterms=[]
        for term in terms:
            if re.match(special_char,term):
                continue
            else:
                newterms.append(term)

        return newterms
    
###########################################################
####################### Testing ###########################
###########################################################

def main():

    pass

if __name__=='__main__':

    main()
