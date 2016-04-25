#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Query

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

import re


pattern = r'[&| ]'

class Query(object):

    def __init__(self):

        self.userinput = raw_input('Please enter your query.')


    def process_query(self):

        if re.search(pattern, self.userinput):

            self.query = re.split(pattern, self.userinput)
        
###########################################################
####################### Testing ###########################
###########################################################

def main():

    pass

if __name__=='__main__':

    main()
