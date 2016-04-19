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
from os import listdir




################################################
##################### Classes ##################
################################################

class Parsedoc(File):

    def __init__(self, input_path):

        self.content = self._parse_doc(input_path)
        self.docid = self.filename





    def _parse_doc(self, input_path):
        
        """Parse the document body"""

        text = []

        files = sorted([f for f in listdir(input_path)],
                       key=lambda x: int(x[:-4]))



        for file in files:

            self.filename = file

            with open(os.path.join(input_path, file)) as f:

                text.append(f.read())

        return text




###########################################################
####################### Testing ###########################
###########################################################

def main():

    ParsedocObj1 = Parsedoc(os.path.expanduser('../testfile_amazon_rewievs'))
    print ParsedocObj1.docs

if __name__=='__main__':

    main()
