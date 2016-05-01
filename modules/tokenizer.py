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
        self.tokenized = self._simple_tokenize(self.text)
        #self.tokenized = self._complex_tokenize(self.text)

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
        en_special_cases = r"(?:'t|'ll|'s|'d)"

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

            if re.search(en_special_cases, text[token_id]):

                token = re.sub(r'(.*)' + '(' + en_special_cases + ')', r' \1 \2 ', text[token_id])
                text_new.extend(token.split())

            elif re.search(r'[.]', text[token_id]):

                # if the next token begins with a small letter,
                # keep the token as an abbrevation

                try:
                    if text[token_id+1][0].islower():

                        text_new.append(token)

                    else:

                        token = re.sub(r'([.])', r' \1 ', text[token_id])
                        text_new.extend(token.split())

                # If the token with a dot is the last token
                # separate the dot.
                except IndexError:

                    token = re.sub(r'([.])', r' \1 ', text[token_id])
                    text_new.extend(token.split())

            # if a punctuation occurs in the token
            # separate it

            elif re.search(punctuation, text[token_id]):

                token = re.sub(r'(' + punctuation + ')', r' \1 ', text[token_id])
                text_new.extend(token.split())

            else:

                text_new.append(token)

        return text_new


###########################################################
####################### Testing ###########################
###########################################################

def main():

    Tokenizer1 = Tokenizer("""This is a test sentence. This is another sentence!!! "Why is it so?"
                            He'll never know. That's a shame. He won't ever do it. I can't tell.
                            Keep dot when it is an abbr. and the following token is lowercased.""")
    print Tokenizer1.tokenized

if __name__=='__main__':

    main()
