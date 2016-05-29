#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Main File

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

v 0.3.0

"""

__version__ = 'v 0.3.0'

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
from modules.ranking import *
import os
import sys
import re
import itertools
import cPickle as pickle
import argparse


################################################
##################### Classes ##################
################################################


class InvertedIndex(object):

    # Class for managing and coordinating all the different components

    def __init__(self, userargs):

        # get user arguments

        self.userargs = userargs

        corpus_path = userargs.corpus
        random_number = userargs.random
        pickle_file_boolean = userargs.pickle


        # get the texts

        parsedoc_obj = Parsedoc(os.path.expanduser(corpus_path), random_number)
        texts_obj,file_name = parsedoc_obj.content,parsedoc_obj.docid

        self.doc_obj={}
        self.doc_obj=dict(zip(file_name,texts_obj))
        self._create_terms()

        if pickle_file_boolean:

            with open('../inverted_index.pkl','rb') as fp:

                self.inv_index = pickle.load(fp)

        else:

            self._create_inv_index()

        query = Query()

        postingslists = query.return_postingslist(query.query, self.inv_index)
        intersection = query.logical_and(postingslists)

        if intersection == []:

            print '\nYour query could not be found in the collection.'

        else:

            print '\nYour queried word(s) occur in the following document(s):'
            print
            for doc_id in intersection:
                print doc_id

        #ranking=Ranking(self.terms,intersection)



    def _create_terms(self):

        self.docs={}
        self.termsdict={}

        for name,document in self.doc_obj.items():

            doc=Document(document)
            self.docs[name]=doc.tokens
            term=Term(doc.tokens)
            self.termsdict[name]=term

        self.terms = self.termsdict.values()

    def _create_inv_index(self):

        self.inv_index={}

        for name,terms in self.termsdict.items():

            for term in terms.terms:

                if term in self.inv_index:

                    self.inv_index[term]._update_postingslist(name)
                    #print (term,self.inv_index[term])

                else:

                    self.inv_index[term]=Postingslist(term,name)
                    #print (term,self.inv_index[term])

        if self.userargs.store:

            filename='inverted_index'
            path='../'

            with open(path.strip()+filename.strip()+'.pkl','wb') as fp:

                pickle.dump(self.inv_index, fp)

            print "\nStored inverted index into " + str(filename) + ".pkl\n\n"


    # create terms on hard disk

    #FolderCreater([''])

###############################################
################# Functions ###################
###############################################


def get_user_args(args):

    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--corpus', metavar='PATH', type=str, default='./amazon_reviews',
                    help='specify a path for corpus files. Default is ./amazon_reviews')
    ap.add_argument('-r', '--random', metavar='N', default='100',
                    help='specify number of randomized documents used for the inverted index. Default is 100 files. If all documents should be considered, type -r all')
    ap.add_argument('-s', '--store', action='store_true',
                    help='activate this flag if you want to store the inverted index into a pickle file')
    ap.add_argument('-p', '--pickle', action='store_true',
                    help='activate this flag if you wish to read the inverted index from a stored pickle file')
    ap.add_argument('--version', action='version', version=__version__)

    return ap.parse_args(args)

###############################################
################# Main ########################
###############################################

def main(main_args):

    args = get_user_args(main_args[1:])

    ii1 = InvertedIndex(args)
    """
    for element in sorted(ii1.docs):

        print element,': ', ii1.docs[element],'\n'

    for element in sorted(ii1.termsdict):

        print element,': ', ii1.termsdict[element], '\n'

    """

    #for element in sorted(ii1.inv_index):

    #    print ii1.inv_index[element],'\n'

    """
    print ii1.terms
    allterms=[term for midlist in ii1.terms for term in midlist]
    print allterms
    """

if __name__=='__main__':

    main(sys.argv)
