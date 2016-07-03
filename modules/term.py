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
import os
import math
from parsedoc import *
from document import *
from tokenizer import *
from porter import *

fileloc="/tmp"
slash="/"

def FolderCreater(terms):
    alldirectories=[]
    for term in terms:
        alldirectories.extend(Recurser(term))
    print len(alldirectories)
    alldirectories=sorted(list(set(alldirectories)))

    print alldirectories

    for filedir in alldirectories:
        os.mkdir(filedir,0750)



def Recurser(term):
    lister=[]
    for i in range(len(term)):
        lister.append(Splitter(term[:i+1]))

    return lister

def Splitter(term):
    temp=str(slash+term)
    if len(term)==1:
        return str(fileloc+temp)
    else:
        return str(Splitter(term[:-1])+temp)


################################################
##################### Classes ##################
################################################

special_char = r"""[!,."']"""

class Term(object):

    def __init__(self,tokens):

        self.tokens = tokens.tokenized
        self.terms = set(terminator(self.tokens))

def terminator(tokens):

    terms = [x.lower() for x in tokens]
    newterms = []

    for term in terms:

        #if re.match(special_char,term):

        #    continue

        # lemmatize clitics

        if term == 'an':

            newterms.append(stem('a'))

        elif term == "'m":

            newterms.append(stem('am'))

        elif term == "'re":

            newterms.append(stem('are'))

        elif term == "'d":

            newterms.append(stem('would'))

        elif term == "'ll":

            newterms.append(stem('will'))

        elif term == "'t" or term == "'nt":

            newterms.append(stem('not'))

        else:

            newterms.append(stem(term))

    return newterms

###########################################################
####################### Testing ###########################
###########################################################

def main():

    parsedoc_obj = Parsedoc(os.path.expanduser('./testfile_amazon_rewievs'))
    texts_obj,file_name = parsedoc_obj.content,parsedoc_obj.docid

    doc_obj={}
    doc_obj=dict(zip(file_name,texts_obj))

    docs={}
    termsdict={}

    for name,document in doc_obj.items():

        doc=Document(document)
        docs[name]=doc.tokens
        term=Term(doc.tokens)
        termsdict[name]=term

    terms = termsdict.values()


    for term in terms:

        print term.tokens
        print term.terms
        print term.tf

if __name__=='__main__':

    main()
