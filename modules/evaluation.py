# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:09:40 2016

@author: prajitdhar
"""

from ranking import *
import pandas as pd
import random as rd


class Evaluation(object):
    
    def __init__(self,ranking):
        self.ranking=ranking.ranking

        describe=self.ranking.Cosine_Similarity.describe()
        
        low=self.ranking[self.ranking.Cosine_Similarity<describe[4]]
#        print "\nOld Low\n",low
#        low.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)
        mid=self.ranking[(self.ranking.Cosine_Similarity>=describe[4]) & (self.ranking.Cosine_Similarity<describe[6])]
#        mid.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)
        high=self.ranking[self.ranking.Cosine_Similarity>=describe[6]]
#        high.rename(columns={'Unnamed: 0':'Filename'}, inplace=True)
        
        samplelow=low.loc[rd.sample(list(low.index),5)]
        samplemid=mid.loc[rd.sample(list(mid.index),5)]
        samplehigh=high.loc[rd.sample(list(high.index),5)]
        
        
        files=[]
        filesamplelow=list(samplelow.index.values)
        filesamplemid=list(samplemid.index.values)
        filesamplehigh=list(samplehigh.index.values)
        files.extend(filesamplelow)
        files.extend(filesamplemid)
        files.extend(filesamplehigh)
        print files
        