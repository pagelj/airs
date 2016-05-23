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

def natural_sortkey(string):

    # Function for sorting integer parts of
    # a string

    tokenize = re.compile(r'(\d+)|(\D+)').findall
    return tuple(int(num) if num else alpha for num, alpha in tokenize(string))

pattern = r'[& ]'

class Query(object):

    def __init__(self):

        self.userinput = str(raw_input('Please enter your query.\n\n'))
        self.query = self.process_query()

    def process_query(self):

        return re.split(pattern,self.userinput)

    def return_postingslist(self, query, terms):

        postingslists = []

        for word in query:

            if word in terms:

                postingslists.append(terms[word].postingslist.values()[0])

            else:

                postingslists.append([])

        return postingslists

    def logical_and(self, postingslists):

        # intersect all postingslists of the entered query words

        if len(postingslists) == 0:

            return None

        elif len(postingslists) == 1:

            return postingslists[0]

        else:

            postingslist1=postingslists.pop(0)

            postingslist2=postingslists.pop(0)

            intersection = set(postingslist1).intersection(set(postingslist2))

            while postingslists != []:

                postingslist3=postingslists.pop(0)

                intersection = set(postingslist3).intersection(set(intersection))

            return sorted(list(intersection), key=natural_sortkey)

###########################################################
####################### Testing ###########################
###########################################################

def main():

    pass

if __name__=='__main__':

    main()
