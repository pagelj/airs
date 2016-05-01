#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Token

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

################################################
##################### Classes ##################
################################################

class Token(object):

    def __init__(self, token):

	# Every Token object has an attribute 'string'
	# which is basically the token itself

        self.string = str(token)
        self.length = len(token)


###########################################################
####################### Testing ###########################
###########################################################

def main():

    pass

if __name__=='__main__':

    main()