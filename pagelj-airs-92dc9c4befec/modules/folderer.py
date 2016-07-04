# -*- coding: utf-8 -*-
"""
Created on Sun May  1 13:29:55 2016

@author: prajitdhar
"""

import os


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
        