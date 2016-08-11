import pandas as pd
import math
from query import *

class Ranking(object):

    def __init__(self,query,inv_index,corpussize, userargs):

        self.userargs=userargs
        self.query=query
        self.corpussize=corpussize
        self.inv_index=inv_index
        self.ranking=self.cosinesimilarity(self.query,self.inv_index,self.userargs)
        self.ranking.to_csv('../ranking.csv')


    def cosinesimilarity(self,query,inv_index,userargs):

        # Fill two dictionaries scores and magnitude.
        # Each dictionary contains information to Numerator
        # and denominator for a cosine similarity calculation
        # for each 'relevant' document. 'Relevant' documents
        # are all documents out of the postingslists of query terms.
        scores={}
        magnitude={}

        if userargs.eval == 'prox':

            dist = self.proximityranking(query,inv_index)

        # For every term in the query
        for term in query.terms:

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

        if userargs.eval == 'prox':

            for doc in scores:

                if doc in dist:

                    scores[doc] = scores[doc] + math.exp(-dist[doc]+4)

                else:

                    scores[doc] = scores[doc]

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
        cosinesimilarity['Cosine_Similarity_Score']=cosinesimilarity['Numerator']/(cosinesimilarity['Denominator'])**0.5

        sortedcosine=cosinesimilarity.sort(['Cosine_Similarity_Score'],ascending=False)

        return sortedcosine

    def proximityranking(self,query,inv_index):

        dist = {}
        dist_tmp = {}
        dist_termpairs = {}

        # For every possible combination of terms
        # in a query:
        for term_id1 in range(len(query.terms)):

            term1 = query.terms[term_id1]

            for term_id2 in range(term_id1+1,len(query.terms)):

                doc_dist = {}

                term2 = query.terms[term_id2]

                # If the terms are distinct:
                if term1 != term2:

                    if term1 in inv_index and term2 in inv_index:

                        postlist1 = inv_index[term1]
                        postlist2 = inv_index[term2]

                        for doc in postlist1.position:

                            if doc in postlist2.position:

                                for pos1 in postlist1.position[doc]:

                                    for pos2 in postlist2.position[doc]:

                                        if doc in doc_dist:

                                            doc_dist[doc].append(math.fabs(pos1-pos2))
                                            doc_dist[doc]=[min(doc_dist[doc])]

                                        else:

                                            doc_dist[doc] = [math.fabs(pos1-pos2)]

                            dist_termpairs[(term1,term2)] = doc_dist

        for termpair in dist_termpairs:

            for doc in dist_termpairs[termpair]:

                if doc in dist:

                    dist[doc].append(dist_termpairs[termpair][doc])
                    dist[doc]=[min(dist[doc])]

                else:

                    dist[doc] = [dist_termpairs[termpair][doc]]

        for doc in dist:

            dist[doc] = dist[doc][0][0]

        return dist




    def tfidf_query(self,term,postlist,query):

        # Compute tf-idf for a term and a given query.

        tf = 1+math.log(float(query.terms.count(term)),10)

        idf = math.log((float(self.corpussize)/postlist.postingslist_len),10)

        return tf*idf


    def tfidf_doc(self,postlist,doc):

        # Compute tf-idf for a term and a given document.

        tf_list = postlist.tf

        tf = tf_list[doc]

        idf = math.log((float(self.corpussize)/postlist.postingslist_len),10)

        return tf*idf
