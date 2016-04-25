#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Main File

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

v 0.2.0

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
from modules.query import *
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
                    inv_index[term].append(name)
                else:
                    inv_index[term]=[name]
                
            
        #inv_index = {term: index for index, term in terms.items()}
        for element in inv_index:

            print element,': ',inv_index[element],'\n'

        query = Query()

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
            pass

        #choices will store the random N files we will use in the experiment
        choices=r.sample(xrange(len(files)),10)

        for x in choices:
            with open(files[x]) as inp_data:
                tempstore=inp_data.read()
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
