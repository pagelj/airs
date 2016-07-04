#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS) - Tokenizer

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

################################################
##################### Import ###################
################################################

import re


################################################
##################### Classes ##################
################################################

class Tokenizer(object):


    def __init__(self, text):

        """
        Create object for storing tokenized text
        """
        self.text = text
        #self.tokenized = self._simple_tokenize(self.text)
        self.tokenized = self._complex_tokenize(self.text)

        second_tokenization = []
        for token in self.tokenized:

            second_tokenization.append(self._complex_tokenize(token)[0])

        self.tokenized = second_tokenization


    def __str__(self):

        # Function for displaying customized output
        # of object print.
        # Now Tokenizer instances are printed
        # as a list of the tokenized text.

        return str(self.tokenized)

    def _tokenlist(self):

        # getter function

        return self.tokenized

    def _simple_tokenize(self, text):

        # define punctuations
        punctuation = r'[^a-zA-Z\d\s]'

        # split the text at whitespaces
        text = text.split()

        # create list to store further
        # tokenized tokens
        text_new = []

        # iterate through all tokens.

        for token in text:

            if re.search(punctuation, token):

                token = re.sub(r'(' + punctuation + ')', r' \1 ', token)
                text_new.extend(token.split())

            else:

                text_new.append(token)

        return text_new


    def _complex_tokenize(self, text):

        """
        More advanced tokenization function
        """


        # define punctuations
        punctuation = r'[^a-zA-Z\d\s]'
        # define set of "not-to-separate" english clitics
        en_clitics = r"(?:'t|'ll|'s|'d|'re|'m|'nt)"

        # split the text at whitespaces
        text = text.split()

        # create list to store further
        # tokenized tokens
        text_new = []

        # iterate through all tokens.

        # Instead of the token name, the list
        # position is iterated for accessing
        # neighboring tokens.

        for token_id in range(len(text)):

            token = text[token_id]

            # handling of clitics in English

            if re.search(en_clitics, token):

                token = re.sub(r'(.*)' + '(' + en_clitics + ')', r' \1 \2 ', token)
                text_new.extend(token.split())

            # if the token contains a dot at the end
            elif re.search(r'[.]$', token):

                token = re.sub(r'([.])', r' \1 ', token)

                # split other punctuations
                if re.search(punctuation, token):

                    token = re.sub(r'(' + punctuation + ')', r' \1 ', token)
                    text_new.extend(token.split())

                else:

                    text_new.append(token)

            # if a punctuation occurs at the beginning
            # or the end of the token, separate it

            elif re.search(punctuation, token):

                token = re.sub(r'(' + punctuation + ')', r' \1 ', token)
                text_new.extend(token.split())

            else:

                text_new.append(token)

        return text_new


###########################################################
####################### Testing ###########################
###########################################################

def main():

    Tokenizer1 = Tokenizer("""This is a test sentence. This is another sentence!!! "Why is it so?"
                            He'll never know.... That's a shame. He won't ever do it. I can't tell.
                            Keep dot when it is an abbr. and the following token is lowercased. !Hyphen-Test. -Test test-test""")
    Tokenizer2 = Tokenizer("32gb~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~i")
    print Tokenizer1.tokenized
    print Tokenizer2.tokenized

if __name__=='__main__':

    main()
