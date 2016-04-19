#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Main File

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

v 0.1.0

"""

#################################################
######################### Import ################
#################################################

from modules.token import *
from modules.term import *
from modules.document import *
from modules.postingslist import *
from modules.dictionary import *
#from modules.parsedoc import *
from modules.tokenizer import *
import os
import random as r
################################################
##################### Classes ##################
################################################


class InvertedIndex(object):

    # Class for managing and coordinating all the different components
    
    def __init__(self):

        # get the texts

        
        texts_obj,file_name = self.filereader('/home/users0/pageljs/teamlab/airs/testfile_amazon_rewievs')
        #print text_obj.docs

        doc_obj=[]
        for document,name in texts_obj,file_name:
            
            doc_obj.append(Document(document[0],name))

        print doc_obj


    def filereader(self, directory):


        r.seed(20)
        # store is a list to hold the file contents    
        store=[]
        tempstore=[]
        # names is a list to hold the file names       
        names=[]
        # The below code will traverse the given directory and store all the file names in it    
        os.chdir(directory)
        for dirpath, dirs, files in os.walk(directory):
            print files[0]
        
        #choices will store the random N files we will use in the experiment        
        choices=r.sample(xrange(len(files)),5)
        
        for x in choices:
            with open(files[x]) as inp_data:
                tempstore=inp_data.readlines()
                store.append(tempstore)
                names.append(files[x])
        #print names
        return store,names
        
###############################################
################# Main ########################
###############################################

def main():

    ii1 = InvertedIndex()

if __name__=='__main__':

    main()
