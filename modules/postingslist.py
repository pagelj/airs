#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Postings list

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

import re
import term
import math

################################################
##################### Classes ##################
################################################

def natural_sortkey(string):

    # Function for sorting integer parts of
    # a string

    tokenize = re.compile(r'(\d+)|(\D+)').findall
    return tuple(int(num) if num else alpha for num, alpha in tokenize(string))

class Postingslist(object):

    def __init__(self, term_id, docs):

        self.docs = docs
        self.term_id = term_id
        self.postingslist = []
        self.tf = {}
        self.position = {}
        self.postingslist_len = len(self.postingslist)

    def __str__(self):

        return str(self.postingslist)

    def _update_postingslist(self, doc_id):

        if isinstance(doc_id, basestring):

            self.postingslist.append(doc_id)

            self.postingslist = sorted(list(set(self.postingslist)), key=natural_sortkey)

            self.postingslist_len = len(self.postingslist)

        else:

            self.postingslist.extend(doc_id)

            self.postingslist = sorted(list(set(self.postingslist)), key=natural_sortkey)

            self.postingslist_len = len(self.postingslist)


    def _gettf(self, doc_id, docs):

        doc_content = term.terminator(docs[doc_id].tokens.tokenized)

        if self.term_id not in doc_content:

            tf_value = 0

        else:

            tf_value = 1+math.log(float(doc_content.count(self.term_id)),10)

        self.tf[doc_id] = tf_value

    def _getposition(self, doc_id, docs):

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
