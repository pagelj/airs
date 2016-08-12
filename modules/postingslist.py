#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Postings list

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
08/12/2016

"""

import re
import term
import math
from auxiliary_functions import natural_sortkey

################################################
##################### Classes ##################
################################################


class Postingslist(object):

    # class for representing a postingslist.

    def __init__(self, term_id, docs):

        # Store the connected term, the documents, the term
        # frequency and the positions of the term.
        self.docs = docs
        self.term_id = term_id
        self.postingslist = []
        self.tf = {}
        self.position = {}
        self.postingslist_len = len(self.postingslist)

    def __str__(self):

        return str(self.postingslist)

    def _update_postingslist(self, doc_id):

        # While creating or updating the inverted index, this
        # function constantly updates the postingslist for
        # a given term.

        # This distinction is necessary to check
        # if the input is a document ID as a string
        # or as a list containing this document ID, as
        # both appears.
        if isinstance(doc_id, basestring):

            self.postingslist.append(doc_id)

        else:

            self.postingslist.extend(doc_id)

        self.postingslist = sorted(list(set(self.postingslist)), key=natural_sortkey)

        self.postingslist_len = len(self.postingslist)


    def _gettf(self, doc_id, docs):

        # Function for getting the term frequency
        # during the creation of the inverted index
        # or later updates.

        doc_content = term.terminator(docs[doc_id].tokens.tokenized)

        if self.term_id not in doc_content:

            tf_value = 0

        else:

            tf_value = 1+math.log(float(doc_content.count(self.term_id)),10)

        self.tf[doc_id] = tf_value

    def _getposition(self, doc_id, docs):

        # Function for getting the positions of the term
        # in its documents
        # during the creation of the inverted index
        # or later updates.

        doc_content = term.terminator(docs[doc_id].tokens.tokenized)

        if self.term_id not in doc_content:

            pass

        else:

            for term_position in xrange(len(doc_content)):

                if doc_content[term_position] == self.term_id:

                    if doc_id in self.position:

                        self.position[doc_id].append(term_position)

                    else:

                        self.position[doc_id] = [term_position]



###########################################################
####################### Testing ###########################
###########################################################

def main():

    Postingslist_obj1 = Postingslist('word', '1.txt')
    print Postingslist_obj1.postingslist
    print Postingslist_obj1.postingslist_len
    Postingslist_obj1._update_postingslist('2.txt')
    Postingslist_obj1._update_postingslist('3.txt')
    Postingslist_obj1._update_postingslist('100.txt')
    print Postingslist_obj1.postingslist
    print Postingslist_obj1.postingslist_len

if __name__=='__main__':

    main()
