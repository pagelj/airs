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

################################################
##################### Classes ##################
################################################


class InvertedIndex(object):

    # Class for managing and coordinating all the different components

    def __init__(self):

        # get the texts

        parsedoc_obj = Parsedoc(os.path.expanduser('./testfile_amazon_rewievs'))
        texts_obj,file_name = parsedoc_obj.content,parsedoc_obj.docid
        #print text_obj.docs
        doc_obj={}
        doc_obj=dict(zip(file_name,texts_obj))
        #print doc_obj
        docs={}
        termsdict={}

        for name,document in doc_obj.items():

            doc=Document(document)
            docs[name]=doc.tokens
            term=Term(doc.tokens)
            termsdict[name]=term

            #print doc.tokens

        for element in sorted(docs):

            print element,': ', docs[element],'\n'

        for element in sorted(termsdict):

            print element,': ', termsdict[element], '\n'

        inv_index={}

        for name,terms in termsdict.items():

            for term in terms.terms:

                if term in inv_index:

                    inv_index[term]._update_postingslist(name)

                else:

                    inv_index[term]=Postingslist(term,name)


        #inv_index = {term: index for index, term in terms.items()}
        for element in inv_index:

            print element,': ',inv_index[element],'\n'

        query = Query()

###############################################
################# Main ########################
###############################################

def main():

    ii1 = InvertedIndex()

if __name__=='__main__':

    main()
