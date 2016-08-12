#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Parse Document

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
08/12/2016

"""

################################################
##################### Import ###################
################################################

import os
import re
import random as r
from evaluation import *
from auxiliary_functions import natural_sortkey


################################################
##################### Classes ##################
################################################

golddata = read_golddata('golddata.txt')
gold_tupels = golddata.values()
gold_docs = []
for list in gold_tupels:
    for tupel in list:
        gold_docs.append(int(tupel[0].rstrip('.txt')))


class Parsedoc(object):

    """
    Parsedoc reads in one file a time and provides
    the file content and file id
    """

    def __init__(self, directory, userargs):

        # Store the directory
        self.directory = directory
        
        # Store the output of filereader as the content and the docid
        self.content, self.docid = self.filereader(self.directory, userargs)

    def filereader(self, directory, userargs):

        r.seed(20)

        # store is a list to hold the file contents
        store=[]
        tempstore=[]

        # names is a list to hold the file names
        names=[]

        # The below code will traverse the given directory and store all the file names in it
        os.chdir(directory)
        for dirpath, dirs, files in os.walk('.'):
            pass


        files = sorted(files, key=natural_sortkey)

        #choices will store the random N files we will use in the experiment
        if userargs.random:

            if userargs.random == 'all':

                N = len(files)

            else:

                N = int(userargs.random)

            choices=r.sample(xrange(len(files)),N)

            for x in choices:
                with open(files[x]) as inp_data:
                    tempstore=inp_data.read()
                    store.append(tempstore)
                    names.append(files[x])

        if userargs.ranking:

            for i in xrange(int(userargs.ranking)):
                with open(files[i]) as inp_data:
                    tempstore=inp_data.read()
                    store.append(tempstore)
                    names.append(files[i])

        return store,names

###########################################################
####################### Testing ###########################
###########################################################

def main():

    ParsedocObj1 = Parsedoc(os.path.relpath('../testfile_amazon_rewievs/1.txt'))
    print ParsedocObj1.docid
    print ParsedocObj1.content

if __name__=='__main__':

    main()
