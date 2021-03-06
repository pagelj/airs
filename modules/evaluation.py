#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Evaluation

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
08/12/2016

"""

from ranking import *
from query import *
from auxiliary_functions import natural_sortkey
import pandas as pd
import random as rd

def read_golddata(path):

    golddata={}

    with open(path,'r') as text:

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
    spec=0
    templst=[]
    temp1=[i[0] for i in gold]
    temp2=pred
    templst=temp1+temp2
    #print "\nTemplist\n",templst
    total=len(set(templst))

    gold_relevant = []


    for tupel in gold:

        if tupel[1] == '1':

            gold_relevant.append(tupel[0])


    for doc in pred:

        if doc in gold_relevant:

            tp += 1
            gold_relevant.remove(doc)

        else:

            fp += 1

    fn = len(gold_relevant)

    tn=total-(tp+fn+fp)

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

def compute_specificity(fp,tn):

    try:

        spec = 1-(float(tn)/(fp+tn))

    except ZeroDivisionError:

        spec = None

    return spec


def compute_f1(precision,recall):

    try:

        f1 = (2*float(precision*recall))/(precision+recall)

    except TypeError:

        f1 = None

    except ZeroDivisionError:

        f1 = None

    return f1

class Evaluation(object):

    def __init__(self,ranking,query):
        self.ranking=ranking.ranking
        self.query=query.userinput
        self.describe=self.ranking.Cosine_Similarity.describe()

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




    def evaluation(self):


        low=self.ranking[self.ranking.Cosine_Similarity<self.describe[4]]
#        print "\nOld Low\n",low
#        low.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)
        mid=self.ranking[(self.ranking.Cosine_Similarity>=self.describe[4]) & (self.ranking.Cosine_Similarity<self.describe[6])]
#        mid.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)
        high=self.ranking[self.ranking.Cosine_Similarity>=self.describe[6]]
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
        scores=[]
        filesamplelow=list(samplelow.index.values)
        scorelow=list(samplelow.Cosine_Similarity)
        filesamplemid=list(samplemid.index.values)
        scoremid=list(samplemid.Cosine_Similarity)
        filesamplehigh=list(samplehigh.index.values)
        scorehigh=list(samplehigh.Cosine_Similarity)
        files.extend(filesamplelow)
        files.extend(filesamplemid)
        files.extend(filesamplehigh)
        scores.extend(scorelow)
        scores.extend(scoremid)
        scores.extend(scorehigh)
#        print sorted(files,key=natural_sortkey)
#        print scores

        nullme={}
        response=""
        i=0
        for f in files:
            temp=open(os.getcwd()+"/"+f)
            nullme[f]=list()
#            print temp.read()
            response=1
#            response=int(raw_input("\nRate 1 for relevancy and 0 for Irrelevancy\n"))
            nullme[f].append(response)
            nullme[f].append(scores[i])
            i+=1
        print nullme
        querylist=[]
        querylist.append(self.query)
        querylist=querylist*len(nullme)
        filedf=pd.DataFrame(nullme.keys(),columns=['File'])
        valuedf=pd.DataFrame(nullme.values(),columns=['Relevancy','Score'])
        querydf=pd.DataFrame(querylist,columns=['Query'])
        evaluation=pd.concat([querydf,filedf,valuedf],axis=1)
        print evaluation

        return evaluation

###########################################################
####################### Testing ###########################
###########################################################

def main():

    Eval1 = Evaluation()


if __name__=='__main__':

    main()
