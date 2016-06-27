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
from modules.evaluation import *
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

        self.corpus_path = userargs.corpus
        self.random_number = userargs.random
        self.pickle_file_boolean = userargs.pickle


        # get the texts

        parsedoc_obj = Parsedoc(os.path.expanduser(self.corpus_path), self.random_number)
        texts_obj,file_name = parsedoc_obj.content,parsedoc_obj.docid

        self.doc_obj={}
        self.doc_obj=dict(zip(file_name,texts_obj))
        self._create_terms()

        if self.pickle_file_boolean:

            with open('../inverted_index.pkl','rb') as fp:

                self.inv_index = pickle.load(fp)

        else:

            self._create_inv_index()


        #self.interactive_query()

        self.eval_ranking()






    def interactive_query(self):

        while 1:

            query = Query('','interactive')

            postingslists = query.return_postingslist(query.query, self.inv_index)

            intersection = query.logical_and(postingslists)

            if intersection.postingslist == []:

                print '\nYour query could not be found in the collection.'

            else:

                print '\nYour queried word(s) occur in the following document(s):'
                print

                for doc_id in intersection.postingslist:

                    print
                    print doc_id
                    print Document.snippet(self.docs[doc_id],query)

            """
            if intersection.postingslist != []:

                ranking=Ranking(query,self.inv_index,self.docs,random_number)
                evaluation=Evaluation(ranking)
            """

            ranking=Ranking(query,self.inv_index,self.docs,self.random_number)
            evaluation=Evaluation(ranking)

            userinput = str(raw_input('\n\nWould you like to continue? Type "no" or "n" to quit the program.\n\n'))
            if userinput in ("no","n"):
                sys.exit("\nProgram quiting\n")


    def eval_ranking(self):

        tp_total_list = []
        fp_total_list = []
        fn_total_list = []
        tn_total_list = []
        precision_total = 0
        recall_total = 0
        f1_total = 0
        golddata = read_golddata('../golddata.txt')
        queries = golddata.keys()
        query_list=[]

        for query in queries:

            query = Query(query,'automatic')
            query_list.append(query)

        for query in query_list:

            prediction = []

            #print query.query
            ranking=Ranking(query,self.inv_index,self.docs,self.random_number)
            gold_docs = golddata[query.query]
            #print 'gold\n', gold_docs

            #print ranking.ranking.index

            for index in ranking.ranking[:15].index:

                prediction.append(index)

            #print 'prediction\n',prediction

            tp,fp,fn,tn = confusion_matrix(gold_docs,prediction)
            tp_total_list.append(tp)
            fp_total_list.append(fp)
            fn_total_list.append(fn)
            tn_total_list.append(tn)
            print tp,fp,fn,tn
            precision = compute_precision(tp,fp)
            print 'precision',precision
            recall = compute_recall(tp,fn)
            print 'recall',recall
            f1 = compute_f1(precision,recall)
            print 'f1',f1

        tp_total = sum(tp_total_list)
        fp_total = sum(fp_total_list)
        fn_total = sum(fn_total_list)
        tn_total = sum(tn_total_list)

        print
        print
        print 'total:',tp_total,fp_total,fn_total,tn_total

        precision_total = compute_precision(tp_total,fp_total)
        print 'precision total:',precision_total
        recall_total = compute_recall(tp_total,fn_total)
        print 'recall total:',recall_total

        f1_total = compute_f1(precision_total,recall_total)
        print 'f1 total:',f1_total


    def _create_terms(self):

        self.docs={}
        self.termsdict={}

        for name,document in self.doc_obj.items():

            doc=Document(document)
            self.docs[name]=doc
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

                    postingslist = Postingslist(term)
                    postingslist._update_postingslist(name)
                    self.inv_index[term]=postingslist
                    #print (term,self.inv_index[term].postingslist)

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
    ap.add_argument('-r', '--random', metavar='N', default='10',
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
