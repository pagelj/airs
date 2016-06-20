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

fileloc="/tmp"
slash="/"
special_char = r"""[!,."']"""

################################################
##################### Classes ##################
################################################

class Term(object):

    def __init__(self,term):

        self.term = term

    def __str__(self):

        return 'Term object:\n'+str(self.term)

    def __eq__(self,other):

        if self.term == other.term:

            return True

        else:

            return False


################################################
################# Functions ####################
################################################

def terminator(tokens):

    terms = set([x.lower() for x in tokens])
    newterms = []

    for term in terms:

        if re.match(special_char,term):

            continue

        # lemmatize clitics

        elif term == 'an':

            newterms.append('a')

        elif term == "'m":

            newterms.append('am')

        elif term == "'re":

            newterms.append('are')

        elif term == "'d":

            newterms.append('would')

        elif term == "'ll":

            newterms.append('will')

        elif term == "'t" or term == "'nt":

            newterms.append('not')

        else:

            newterms.append(term)

    return set(newterms)

"""
    def compute_tf(self, tokens, terms):

        tf_values = {}

        for term in terms:

            for token in tokens:

                if term == token:

                    if term in tf_values:

                        tf_values[term] += 1

                    else:

                        tf_values[term] = 1

        for term in tf_values:

            tf_values[term] = 1 + math.log10(tf_values[term])

        return tf_values
"""

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
