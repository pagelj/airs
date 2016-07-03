import term
import pandas as pd
from postingslist import *
import math

class Ranking(object):

    def __init__(self,query,inv_index,corpussize):

        self.query=query
        self.corpussize=corpussize
        self.inv_index=inv_index
        self.ranking=self.cosinesimilarity(self.query,self.inv_index)
        self.ranking.to_csv('../ranking.csv')

    def cosinesimilarity(self,query,inv_index):

        # Fill two dictionaries scores and magnitude.
        # Each dictionary contains information to Numerator
        # and denominator for a cosine similarity calculation
        # for each 'relevant' document. 'Relevant' documents
        # are all documents out of the postingslists of query terms.
        scores={}
        magnitude={}

        # For every term in the query
        for term in query.query:

            # If the term is not in the index, its
            # contribution to the tf-idf values is zero.
            # Therefor continue with the next term.
            if term in inv_index:

                # Get the postingslist of the term.
                postlist = inv_index[term]

                # For every document in the postingslist of the query term:
                for doc in postlist.postingslist:

                    # Get the tf-idf values and sum them up for each document.
                    if doc in scores:

                        scores[doc] += self.tfidf_query(term,postlist,query)*self.tfidf_doc(postlist,doc)

                    else:

                        scores[doc] = self.tfidf_query(term,postlist,query)*self.tfidf_doc(postlist,doc)



            else:

                continue

        # Saves the scores for the documents in a data frame.
        scoresrep=pd.DataFrame(scores.values(),index=scores.keys(),columns=['Numerator'])

        # For every term in the index, calculate
        # the denominator.
        for term in inv_index.keys():

            # Get the postingslist.
            postlist = self.inv_index[term]

            # Calculate the value only for documents
            # of the postingslist which are in scores.

            for doc in scores.keys():

                if doc in postlist.postingslist:

                    if doc in magnitude:

                        magnitude[doc] += self.tfidf_doc(postlist,doc)**2

                    else:

                        magnitude[doc] = self.tfidf_doc(postlist,doc)**2

        magrep=pd.DataFrame(magnitude.values(),index=scores.keys(),columns=['Denominator'])

        cosinesimilarity=pd.concat([scoresrep,magrep],axis=1)
        cosinesimilarity['Cosine_Similarity']=cosinesimilarity['Numerator']/(cosinesimilarity['Denominator'])**0.5

        sortedcosine=cosinesimilarity.sort(['Cosine_Similarity'],ascending=False)

        return sortedcosine


    def tfidf_query(self,term,postlist,query):

        # Compute tf-idf for a term and a given query.

        tf = 1+math.log(float(query.query.count(term)),10)

        idf = math.log((float(self.corpussize)/postlist.postingslist_len),10)

        return tf*idf


    def tfidf_doc(self,postlist,doc):

        # Compute tf-idf for a term and a given document.

        tf_list = postlist.tf

        tf = tf_list[doc]

        idf = math.log((float(self.corpussize)/postlist.postingslist_len),10)

        return tf*idf
