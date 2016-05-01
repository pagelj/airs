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

################################################
##################### Classes ##################
################################################

class Postingslist(object):

    def __init__(self, term_id, doc_id):

        self.term_id = term_id
        self.docid = doc_id
        self.postingslist = {term_id: [doc_id]}
        self.postingslist_len = len(self.postingslist)

    def __str__(self):

        return str(self.postingslist)

    def _update_postingslist(self, doc_id):

        for term_id in self.postingslist:

            self.postingslist[term_id].append(doc_id)


###########################################################
####################### Testing ###########################
###########################################################

def main():

    Postingslist_obj1 = Postingslist('word', '1.txt')
    print Postingslist_obj1.postingslist
    Postingslist_obj1._update_postingslist('2.txt')
    print Postingslist_obj1

if __name__=='__main__':

    main()
