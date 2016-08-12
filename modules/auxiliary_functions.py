#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Auxiliary Functions

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
08/12/2016

"""

import re

def natural_sortkey(string):

    # Function for sorting integer parts of
    # a string

    tokenize = re.compile(r'(\d+)|(\D+)').findall
    return tuple(int(num) if num else alpha for num, alpha in tokenize(string))
