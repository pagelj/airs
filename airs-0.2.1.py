#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Main File

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

v 0.2.1

"""

#################################################
######################### Import ################
#################################################

from modules.token import *
from modules.term import *
from modules.document import *
from modules.postingslist import *
from modules.parsedoc import *
from modules.tokenizer import *
from modules.query import *
import os
import re

################################################
##################### Classes ##################
################################################


class InvertedIndex(object):

    # Class for managing and coordinating all the different components

    def __init__(self):

        # get the texts

        parsedoc_obj = Parsedoc(os.path.expanduser('./testfile_amazon_rewievs'))
        texts_obj,file_name = parsedoc_obj.content,parsedoc_obj.docid

        self.doc_obj={}
        self.doc_obj=dict(zip(file_name,texts_obj))
        self._create_terms()
        self._create_inv_index()

    def _create_terms(self):

        self.docs={}
        self.termsdict={}

        for name,document in self.doc_obj.items():

            doc=Document(document)
            self.docs[name]=doc.tokens
            term=Term(doc.tokens)
            self.termsdict[name]=term

    def _create_inv_index(self):

        self.inv_index={}

        for name,terms in self.termsdict.items():

            for term in terms.terms:

                if term in self.inv_index:

                    self.inv_index[term]._update_postingslist(name)

                else:

                    self.inv_index[term]=Postingslist(term,name)

        #self.query = Query()

###############################################
################# Main ########################
###############################################

def main():

    ii1 = InvertedIndex()

    for element in sorted(ii1.docs):

        print element,': ', ii1.docs[element],'\n'

    for element in sorted(ii1.termsdict):

        print element,': ', ii1.termsdict[element], '\n'

    for element in sorted(ii1.inv_index):

        print ii1.inv_index[element],'\n'

if __name__=='__main__':

    main()
