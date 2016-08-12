#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Main File

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
08/12/2016

"""

__version__ = 'v 1.0.0'

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
import numpy as np
import matplotlib.pyplot as plt


################################################
##################### Classes ##################
################################################


class System(object):

    # Class for managing and coordinating all the different components

    def __init__(self, userargs):

        # get user arguments

        self.userargs = userargs

        # Store the inverted index into a pickle file
        # if requested by the user
        if self.userargs.pickle:

            try:

                with open('docs.pkl','rb') as fp:

                    print "\nRead documents from docs.pkl\n"

                    self.docs = pickle.load(fp)

            except IOError:

                with open('../docs.pkl','rb') as fp:

                    print "\nRead documents from docs.pkl\n"

                    self.docs = pickle.load(fp)

            try:

                with open('inverted_index.pkl','rb') as fp:

                    print "\nRead inverted index from inverted_index.pkl\n"

                    self.inv_index = pickle.load(fp)

                    self.corpussize = len(self.docs.keys())


            except IOError:

                with open('../inverted_index.pkl','rb') as fp:

                    print "\nRead inverted index from inverted_index.pkl\n"

                    self.inv_index = pickle.load(fp)

                    self.corpussize = len(self.docs.keys())

        else:

            # get the texts

            print "\nReading in the corpus\n"

            parsedoc_obj = Parsedoc(os.path.expanduser(self.userargs.corpus), self.userargs)
            texts_obj,file_name = parsedoc_obj.content,parsedoc_obj.docid

            self.doc_obj={}
            self.doc_obj=dict(zip(file_name,texts_obj))

            print "\nReading in of corpus finished\n"

            # Create the terms for the inverted index

            print "\nCreate terms\n"

            self._create_terms()

            print "\nTerms created\n"

            # Create the inverted index

            print "\nStart creating the inverted index\n"

            self._create_inv_index()

            print "\nInverted index created\n"


        # Run interactive query if set by
        # user, else run ranking on given queries from
        # the gold standard.

        if self.userargs.interactive:

            self.interactive_query()

        else:


            print "\nStart ranking of documents\n"

            # Call evaluation function depending on the system
            # the user wants to evaluate.

            if self.userargs.eval == 'bool':

                self.eval_bool()

            elif self.userargs.eval == 'tfidf' or self.userargs.eval == 'prox':

                self.eval_ranking()

            print "\nRanking of documents finished\n"


    def _create_terms(self):

        # Function for creating the terms.

        self.docs={}
        self.termsdict={}

        # Iterate over all documents and
        # create term objects out of the
        # document content.

        for name,document in self.doc_obj.items():

            doc=Document(document)
            self.docs[name]=doc
            term=Term(doc.tokens)
            self.termsdict[name]=term

        self.terms = self.termsdict.values()

        self.corpussize = len(self.docs.keys())

        filename_terms='terms'
        filename_docs='docs'
        path='../'

        # Store the terms if the user wants to.

        if self.userargs.store:

            with open(path.strip()+filename_terms.strip()+'.pkl','wb') as fp:

                pickle.dump(self.terms, fp)

            print "\nStored terms into " + str(filename_terms) + ".pkl\n"

            with open(path.strip()+filename_docs.strip()+'.pkl','wb') as fp:

                pickle.dump(self.docs, fp)

            print "\nStored documents into " + str(filename_docs) + ".pkl\n"


    def _create_inv_index(self):

        # Function for creating the inverted index.

        self.inv_index={}

        # Iterate over all terms.

        for name,terms in self.termsdict.items():

            for term in terms.terms:

                # Update the postingslist for every new document the term
                # occurs in as well as the term frequency for that document
                # and the position(s) of the term in it.

                if term in self.inv_index:

                    self.inv_index[term]._update_postingslist(name)
                    self.inv_index[term]._gettf(name,self.docs)
                    self.inv_index[term]._getposition(name,self.docs)

                else:

                    postingslist = Postingslist(term,self.docs)
                    postingslist._update_postingslist(name)
                    postingslist._gettf(name,self.docs)
                    postingslist._getposition(name,self.docs)
                    self.inv_index[term]=postingslist


        # Store the inverted index if the user wants to.

        if self.userargs.store:

            filename='inverted_index'
            path='../'

            with open(path.strip()+filename.strip()+'.pkl','wb') as fp:

                pickle.dump(self.inv_index, fp)

            print "\nStored inverted index into " + str(filename) + ".pkl\n"


    def interactive_query(self):

        # Function to realize an interactive query interface.


        # Return the N most highest ranked documents to the user.
        top_rank = 10

        while 1:

            # Initialize an empty query
            # that is filled with the user input.
            query = Query('','interactive')

            # Get the postingslists of the query words.
            postingslists = query.return_postingslist(query.terms, self.inv_index)

            # Get the intersection of the postingslists.
            intersection = query.logical_and(postingslists)

            # First check if the query words occur in the collection
            # using boolean search. If not return a message that
            # the search was not successful.

            if intersection.postingslist == []:

                print '\nYour query could not be found in the collection.'

            else:

                print '\nYour queried word(s) occur in the following document(s):'
                print

                if self.userargs.eval == 'bool':

                    for doc_id in intersection.postingslist:

                        print
                        print doc_id
                        print
                        print Document.snippet(self.docs[doc_id],query)

                elif self.userargs.eval == 'tfidf' or self.userargs.eval == 'prox':

                    # If at least one query word occured, rank the documents using
                    # either tf-idf or prximity ranking (Can be specified in the ranking class).
                    ranking=Ranking(query,self.inv_index,self.corpussize,self.userargs)

                    # Return the top N ranked documents and snippets of the context the search
                    # words occured in.
                    for doc_id in ranking.ranking.index[:top_rank]:

                        print
                        print doc_id
                        print
                        print Document.snippet(self.docs[doc_id],query)

            # Ask the user if they would like to continue.
            userinput = str(raw_input('\n\nIf you would like to continue type "yes" or "y".\nType "no" or "n" to quit the program.\n\n'))
            if userinput in ("no","n"):
                sys.exit("\nProgram quiting\n")
            elif userinput in ("yes","y"):
                continue
            else:
                print '\nError: Could not recognize input.\nPlease type "yes" or "y" if you wish to continue and "no" or "n" if you wish to quit the program.\n'
                continue

    def eval_bool(self):

        # Function for evaluating the boolean system.

        precision_total = []
        recall_total = []

        # Get the gold data.

        try:

            golddata = read_golddata('golddata.txt')

        except IOError:

            golddata = read_golddata('../golddata.txt')

        # Get the queries from the gold data.
        queries = golddata.keys()

        query_list=[]

        # Convert the query strings to query objects.
        for query in queries:

            query = Query(query,'automatic')
            query_list.append(query)

        # Perform the boolean search using logical and
        # and evaluate the output of the intersection
        # for every single query and for the whole system.

        for query in query_list:

            print '\nQuery: '+str(query.userinput)+'\n'

            postingslists = query.return_postingslist(query.terms, self.inv_index)

            intersection = query.logical_and(postingslists)

            gold_docs = golddata[query.userinput]

            tp,fp,fn,tn = confusion_matrix(gold_docs,intersection.postingslist)

            precision = compute_precision(tp,fp)
            print 'Precision:',precision
            recall = compute_recall(tp,fn)
            print 'Recall:',recall
            f1 = compute_f1(precision,recall)
            print 'F1-Score:',f1

            precision_total.append(precision)
            recall_total.append(recall)

        # None values are filtered out since the evaluation functions return None
        # if there is a division by 0.
        precision_avg = float(sum(filter(None,precision_total)))/len(filter(None,precision_total))
        recall_avg = float(sum(filter(None,recall_total)))/len(filter(None,recall_total))


        print
        print 'Average precision:', precision_avg
        print 'Average recall:', recall_avg

        f1_total = compute_f1(precision_avg,recall_avg)

        print 'F1-Score:',f1_total


    def eval_ranking(self):

        # Function for evaluating the systems
        # tf-idf and prox.

        spec_total_list=[]
        eleven_precision_total = []
        precision_recall_total = {}
        specificity_total = {}

        if self.userargs.eval == 'tfidf':

            graph_path = 'graphs_tfidf/'

        elif self.userargs.eval == 'prox':

            graph_path = 'graphs_prox/'

        try:

            golddata = read_golddata('golddata.txt')

        except IOError:

            golddata = read_golddata('../golddata.txt')

        queries = golddata.keys()

        query_list=[]

        for query in queries:

            query = Query(query,'automatic')
            query_list.append(query)

        for query in query_list:

            print '\nQuery: '+str(query.userinput)+'\n'

            precision = []
            eleven_prec = []
            specificity=[]
            recall = []

            ranking=Ranking(query,self.inv_index,self.corpussize,self.userargs)
            print "\nRanking\n"
            print ranking.ranking
            print '\n'

            totalpred=ranking.ranking.index.values.tolist()
            gold_docs = golddata[query.userinput]

            for i in xrange(1,len(ranking.ranking),1):

                prediction = totalpred[:i]

              #  for index in ranking.ranking[:i].index:

               #     prediction.append(index)


                tp,fp,fn,tn = confusion_matrix(gold_docs,prediction)

                precision_value = compute_precision(tp,fp)
                precision.append(precision_value)
                spec = compute_specificity(fp,tn)
                specificity.append(spec)
                recall_value = compute_recall(tp,fn)
                recall.append(recall_value)


            for index in xrange(len(recall)):

                if recall[index] == 0.0:

                    eleven_prec.append((0.0,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] <= 0.1:

                    eleven_prec.append((0.1,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.1 and recall[index] <= 0.2:

                    eleven_prec.append((0.2,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.2 and recall[index] <= 0.3:

                    eleven_prec.append((0.3,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.3 and recall[index] <= 0.4:

                    eleven_prec.append((0.4,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.4 and recall[index] <= 0.5:

                    eleven_prec.append((0.5,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.5 and recall[index] <= 0.6:

                    eleven_prec.append((0.6,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.6 and recall[index] <= 0.7:

                    eleven_prec.append((0.7,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.8 and recall[index] <= 0.9:

                    eleven_prec.append((0.8,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] > 0.9 and recall[index] < 1.0:

                    eleven_prec.append((0.9,precision[index]))

                    break

            for index in xrange(len(recall)):

                if recall[index] == 1.0:

                    eleven_prec.append((1.0,precision[index]))

                    break

            rec_tmp = []
            prec_tmp = []

            for tupel in eleven_prec:

                rec_tmp.append(tupel[0])
                prec_tmp.append(tupel[1])

            #plt.plot(recall,precision,'b-')
            #plt.plot(rec_tmp,prec_tmp,'r-')
            #plt.xlabel('Recall')
            #plt.ylabel('Precision')
            #plt.title("Precision-Recall graph for query '"+str(query.userinput)+"'")

            plt.plot(specificity,recall,'b-',label='overall ROC')
            plt.xlabel('1-Specificity')
            plt.ylabel('Sensitivity')
            plt.title("ROC graph for query '"+str(query.userinput)+"'")

            try:

                plt.savefig(graph_path+"roc_"+str(query.userinput).replace(' ','_')+".png", bbox_inches='tight')
                print "\nStored graph in "+graph_path+"roc_"+str(query.userinput).replace(' ','_')+".png\n"

            except IOError:

                plt.savefig("../"+graph_path+"roc_"+str(query.userinput).replace(' ','_')+".png", bbox_inches='tight')
                print "\nStored graph in "+"../"+graph_path+"roc_"+str(query.userinput).replace(' ','_')+".png\n"

            plt.close()

            prec_recall_plot, = plt.plot(recall,precision,'b-',label='overall precision-recall')
            eleven_prec_recall_plot, = plt.plot(rec_tmp,prec_tmp,'r-',label='11-point precision-recall')
            plt.axis([0.0,1.0,0.0,1.0])
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title("Precision-Recall graph for query '"+str(query.userinput)+"'")
            plt.legend(handles=[prec_recall_plot,eleven_prec_recall_plot])

            try:

                plt.savefig(graph_path+"precrec_"+str(query.userinput).replace(' ','_')+".png", bbox_inches='tight')
                print "\nStored graph in "+graph_path+"precrec_"+str(query.userinput).replace(' ','_')+".png\n"

            except IOError:

                plt.savefig("../"+graph_path+"precrec_"+str(query.userinput).replace(' ','_')+".png", bbox_inches='tight')
                print "\nStored graph in "+"../"+graph_path+"precrec_"+str(query.userinput).replace(' ','_')+".png\n"

            plt.close()

            print '11-point-precision'
            for rec,prec in eleven_prec:
                print rec,'\t',prec
            print '\n'

            eleven_precision_total.append(eleven_prec)

            # For each recall in the query eval store the corresponding precision value

            for rec_id in xrange(len(recall)):

                if recall[rec_id] in precision_recall_total:

                    precision_recall_total[recall[rec_id]].append(precision[rec_id])

                else:

                    precision_recall_total[recall[rec_id]] = [precision[rec_id]]

            # Store specificity for 1-Specificity values for each query

            for spec_id in xrange(len(recall)):

                if recall[spec_id] in specificity_total:

                    specificity_total[recall[spec_id]].append(specificity[spec_id])

                else:

                    specificity_total[recall[spec_id]] = [specificity[spec_id]]




        # Calculate the average overall precision

        precision_average = {}

        for rec in precision_recall_total:

            if rec == None:

                continue

            else:


                if precision_recall_total[rec] == [None]:

                    continue

                elif None in precision_recall_total[rec]:

                    precision_average[rec] = float(sum(filter(None,precision_recall_total[rec])))/len(precision_recall_total[rec])

                else:

                    precision_average[rec] = float(sum(precision_recall_total[rec]))/len(precision_recall_total[rec])


        # Plot Precision average

        prec_tmp = []
        rec_tmp = []

        for rec in sorted(precision_average.keys()):

            rec_tmp.append(rec)
            prec_tmp.append(precision_average[rec])


        total_prec_recall, = plt.plot(rec_tmp,prec_tmp,'b-', label="overall precision-recall")
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        #plt.title("Precision-Recall graph for all queries")


        # Calculate the average 11-point precision

        eleven_precision_average = {}

        for pres in eleven_precision_total:

            for tupel in pres:

                if tupel[0] in eleven_precision_average:

                    eleven_precision_average[tupel[0]].append(tupel[1])

                else:

                    eleven_precision_average[tupel[0]] = [tupel[1]]

        for rec in eleven_precision_average:

            eleven_precision_average[rec] = float(sum(eleven_precision_average[rec]))/len(eleven_precision_average[rec])

        prec_tmp = []
        rec_tmp = []

        for rec in sorted(eleven_precision_average.keys()):

            rec_tmp.append(rec)
            prec_tmp.append(eleven_precision_average[rec])



        total_eleven_prec_recall, = plt.plot(rec_tmp,prec_tmp,'rs', label="11-point precision-recall")
        plt.legend(handles=[total_prec_recall,total_eleven_prec_recall])

        try:

            plt.savefig(graph_path+"total_precrec.png", bbox_inches='tight')
            print "\nStored graph in "+graph_path+"total_precrec.png\n"

        except IOError:

            plt.savefig("../"+graph_path+"total_precrec.png", bbox_inches='tight')
            print "\nStored graph in ../"+graph_path+"total_precrec.png\n"

        plt.close()

        # Plot total specificity

        specificity_average = {}


        for spec in specificity_total:

            if spec == None:

                continue

            else:

                if specificity_total[spec] == [None]:

                    continue

                elif None in specificity_total[spec]:

                    specificity_average[spec] = float(sum(filter(None,specificity_total[spec])))/len(specificity_total[spec])

                else:

                    specificity_average[spec] = float(sum(specificity_total[spec]))/len(specificity_total[spec])

        spec_tmp = []
        rec_tmp = []


        for spec in sorted(specificity_average.keys()):

            spec_tmp.append(spec)
            rec_tmp.append(specificity_average[spec])

        plt.plot(spec_tmp,rec_tmp,'b-',label='overall ROC')
        plt.xlabel('1-Specificity')
        plt.ylabel('Sensitivity')
        #plt.title("ROC graph for all queries")

        try:

            plt.savefig(graph_path+"total_roc.png", bbox_inches='tight')
            print "\nStored graph in "+graph_path+"total_roc.png\n"

        except IOError:

            plt.savefig("../"+graph_path+"total_roc.png", bbox_inches='tight')
            print "\nStored graph in ../"+graph_path+"total_roc.png\n"

        plt.close()

        print 'System 11-point-precision'
        for rec in sorted(eleven_precision_average.keys()):
            print rec,'\t',eleven_precision_average[rec]
        print '\n'


###############################################
################# Functions ###################
###############################################


def get_user_args(args):

    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--corpus', metavar='PATH', type=str, default='./amazon_reviews',
                    help='specify a path for corpus files. Default is ./amazon_reviews')
    ap.add_argument('-rand', '--random', metavar='N',
                    help='specify number of randomized documents used for the inverted index.')
    ap.add_argument('-rank', '--ranking', metavar='N',
                    help='specify upper bound for documents to be ranked')
    ap.add_argument('-e', '--eval', metavar='SYSTEM', choices=['bool','tfidf','prox'], default='tfidf',
                    help='specifiy on which system you want to perform the evaluation. Possible values are bool, tfidf and prox.')
    ap.add_argument('-s', '--store', action='store_true',
                    help='activate this flag if you want to store the inverted index into a pickle file')
    ap.add_argument('-p', '--pickle', action='store_true',
                    help='activate this flag if you wish to read the inverted index from a stored pickle file')
    ap.add_argument('-i', '--interactive', action='store_true',
                    help='activate this flag if you want to enter interactive mode')
    ap.add_argument('--version', action='version', version=__version__)

    return ap.parse_args(args)

###############################################
################# Main ########################
###############################################

def main(main_args):

    # Get the user arguments.
    args = get_user_args(main_args[1:])

    # Initialize the system.
    system = System(args)


if __name__ == '__main__':

    # Execute the main file.
    main(sys.argv)
