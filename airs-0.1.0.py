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
from modules.parsedoc import *
from modules.tokenizer import *

################################################
##################### Classes ##################
################################################


class System(object):

    # Class for managing and coordinating all the different components
    
    def __init__(self):

        # get the texts

        texts_obj = Parsedoc(os.path.expanduser('testfile_amazon_rewievs'))
        #print text_obj.docs

        text_tokenized_objs = []

        for doc in texts_obj.docs:

            text_tokenized_objs.append(Tokenizer(doc))


        for text_obj in text_tokenized_objs:

            print text_obj.tokenized


###############################################
################# Main ########################
###############################################

def main():

    System1 = System()

if __name__=='__main__':

    main()
