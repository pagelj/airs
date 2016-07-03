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
from postingslist import *
from porter import *


def natural_sortkey(string):

    # Function for sorting integer parts of
    # a string

    tokenize = re.compile(r'(\d+)|(\D+)').findall
    return tuple(int(num) if num else alpha for num, alpha in tokenize(string))

pattern = r'[& ]'

class Query(object):

    def __init__(self,query_input,query_type):

        if query_type == 'interactive':

            self.userinput = str(raw_input('\n\nPlease enter your query.\n\n'))

            self.tokens = self.process_query(self.userinput)

            self.terms = terminator(self.tokens)

        elif query_type == 'automatic':

            self.userinput = query_input

            self.tokens = self.process_query(query_input)

            self.terms = terminator(self.tokens)

    def process_query(self,query_input):

        query_split = re.split(pattern,query_input)

        return query_split

    def return_postingslist(self, query, terms):

        postingslists = []

        for word in query:

            if word in terms:

                postingslists.append(terms[word])

            else:

                empty_postingslist = Postingslist('','')

                postingslists.append(empty_postingslist)

        return postingslists

    def logical_and(self, postingslists):

        # intersect all postingslists of the entered query words

        if len(postingslists) == 0:

            intersection = Postingslist('','')

            return intersection

        elif len(postingslists) == 1:

            intersection = Postingslist('','')
            intersection._update_postingslist(postingslists[0].postingslist)

            return intersection

        else:

            postingslist1=postingslists.pop(0)

            postingslist2=postingslists.pop(0)

            intersection = set(postingslist1.postingslist).intersection(set(postingslist2.postingslist))

            while postingslists != []:

                postingslist3=postingslists.pop(0)

                intersection = set(postingslist3.postingslist).intersection(set(intersection))

            intersection_obj = Postingslist('','')

            intersection_obj._update_postingslist(sorted(list(intersection), key=natural_sortkey))

            return intersection_obj

def terminator(tokens):

    special_char = r"""[!,."']"""

    terms = [x.lower() for x in tokens]
    newterms = []

    for term in terms:

        #if re.match(special_char,term):

        #    continue

        # lemmatize clitics

        if term == 'an':

            newterms.append(stem('a'))

        elif term == "'m":

            newterms.append(stem('am'))

        elif term == "'re":

            newterms.append(stem('are'))

        elif term == "'d":

            newterms.append(stem('would'))

        elif term == "'ll":

            newterms.append(stem('will'))

        elif term == "'t" or term == "'nt":

            newterms.append(stem('not'))

        else:

            newterms.append(stem(term))

    return newterms

###########################################################
####################### Testing ###########################
###########################################################

def main():

    query = Query()

if __name__=='__main__':

    main()
