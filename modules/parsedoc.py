#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Parse Document

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

################################################
##################### Import ###################
################################################

import os
import re
import random as r


################################################
##################### Classes ##################
################################################

class Parsedoc(object):

    """
    Parsedoc reads in one file a time and provides
    the file content and file id
    """

    def __init__(self, directory, random_number):

        # Store the directory
        self.directory = directory
        # Store the output of filereader as the content and the docid
        self.content, self.docid = self.filereader(self.directory, random_number)

    def filereader(self, directory, random_number):

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

        #choices will store the random N files we will use in the experiment
        if random_number == 'all':

            N = len(files)

        else:

            N = int(random_number)

        choices=r.sample(xrange(len(files)),N)

        for x in choices:
            with open(files[x]) as inp_data:
                tempstore=inp_data.read()
                store.append(tempstore)
                names.append(files[x])
        #print names
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
