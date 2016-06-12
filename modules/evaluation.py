# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:09:40 2016

@author: prajitdhar
"""

from ranking import *
import pandas as pd
import random as rd

def natural_sortkey(string):

    # Function for sorting integer parts of
    # a string

    tokenize = re.compile(r'(\d+)|(\D+)').findall
    return tuple(int(num) if num else alpha for num, alpha in tokenize(string))

def read_golddata():

    golddata={}

    with open('../golddata.txt','r') as text:

        raw_text = text.read()

    for query_anno in raw_text.split('\n\n'):

        query_anno_split = query_anno.split('\n')
        query = query_anno_split.pop(0)

        for doc_anno in query_anno_split:

            doc_anno_split = doc_anno.split(',')

            try:

                doc = doc_anno_split[0]
                relevance = doc_anno_split[1]

            except IndexError:

                continue

            if query in golddata:

                golddata[query].extend([(doc,relevance)])

            else:

                golddata[query]=[(doc,relevance)]

    return golddata

def confusion_matrix(gold,pred):

    tp = 0
    fp = 0
    fn = 0
    tn = 0

    for annotation_gold in gold:

        doc_gold = annotation_gold[0]
        relevance_gold = annotation_gold[1]

        for annotation_pred in pred:

            doc_pred = annotation_pred[0]
            relevance_pred = annotation_pred[1]

            if doc_gold == doc_pred:

                if relevance_gold == '1' and relevance_pred == '1':

                    tp += 1

                elif relevance_gold == '0' and relevance_pred == '0':

                    tn += 1

                elif relevance_gold == '1' and relevance_pred == '0':

                    fn += 1

                elif relevance_gold == '0' and relevance_pred == '1':

                    fp += 1

    return tp,fp,fn,tn

def compute_precision(tp,fp):

    try:

        precision = float(tp)/(tp+fp)

    except ZeroDivisionError:

        precision = None

    return precision

def compute_recall(tp,fn):

    try:

        recall = float(tp)/(tp+fn)

    except ZeroDivisionError:

        recall = None

    return recall

def compute_f1(precision,recall):

    try:

        f1 = (2*float(precision*recall))/(precision+recall)

    except TypeError:

        f1 = None

    except ZeroDivisionError:

        f1 = None

    return f1

class Evaluation(object):

    def __init__(self,ranking):

        self.ranking = ranking.ranking

        self.get_annotation_files()

    def get_annotation_files(self):

        describe=self.ranking.Cosine_Similarity.describe()

        low=self.ranking[self.ranking.Cosine_Similarity<describe[4]]
        #        print "\nOld Low\n",low
        #        low.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)
        mid=self.ranking[(self.ranking.Cosine_Similarity>=describe[4]) & (self.ranking.Cosine_Similarity<describe[6])]
        #        mid.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)
        high=self.ranking[self.ranking.Cosine_Similarity>=describe[6]]
        #        high.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)


        try:
            samplelow=low.loc[rd.sample(list(low.index),5)]
        except ValueError:
            samplelow=low
        try:
            samplemid=mid.loc[rd.sample(list(mid.index),5)]
        except ValueError:
            samplemid=mid
        try:
            samplehigh=high.loc[rd.sample(list(high.index),5)]
        except ValueError:
            samplehigh=high


        files=[]
        filesamplelow=list(samplelow.index.values)
        filesamplemid=list(samplemid.index.values)
        filesamplehigh=list(samplehigh.index.values)
        files.extend(filesamplelow)
        files.extend(filesamplemid)
        files.extend(filesamplehigh)
        print sorted(files,key=natural_sortkey)

###########################################################
####################### Testing ###########################
###########################################################

def main():

    Eval1 = Evaluation()


if __name__=='__main__':

    main()
