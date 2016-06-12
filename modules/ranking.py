from term import *
import pandas as pd
from postingslist import *
import math

class Ranking(object):

    def __init__(self,query,inv_index,docs,corpussize):

        self.query=query.query
        self.corpussize=corpussize
        self.inv_index=inv_index
        self.docs=docs
#        print self.inv_index
        self.ranking=self.cosinesimilarity(self.query,self.inv_index)
        print self.ranking
        self.ranking.to_csv('../ranking.csv')

    def cosinesimilarity(self,query,inv_index):

        scores={}
        magnitude={}
        terms=[]
#        print "\nTerms\n",inv_index.keys()
        for term in query:
            if term not in terms:
                terms.append(term)
                if term in inv_index:
                    pl=inv_index[term]
                    postlist=pl.postingslist
    #                print "\nPostings List\n",postlist
                    for doc in postlist:

                        if doc in scores:
    #                        print "\nDocument 1\n",doc
                            scores[doc]+=self.tfidf_query(term,query)*self.tfidf_doc(term,doc)
    #                    print scores
                        else:
    #                        print "\nDocument 2\n",doc
                            scores[doc]=self.tfidf_query(term,query)*self.tfidf_doc(term,doc)
    #                    print scores

            else:
                continue
#        print scores
        scoresrep=pd.DataFrame(scores.values(),index=scores.keys(),columns=['Numerator'])
 #       print scoresrep
        for term in inv_index.keys():
            for doc in scores.keys():
                """
                if doc=='4769.txt':
                    print '\nDoc\n',doc
                    print '\nTerm\n',term
                    if doc in magnitude:
                        magnitude[doc]+= self.tfidf_doc(term,doc)**2
                        print '\nCurrent value\n',magnitude[doc]
                    else:
                        magnitude[doc]= self.tfidf_doc(term,doc)**2
                        print '\nCurrent value\n',magnitude[doc]
                else:
                """
                if doc in magnitude:
                    magnitude[doc]+= self.tfidf_doc(term,doc)**2
                else:
                    magnitude[doc]= self.tfidf_doc(term,doc)**2
#        print magnitude
        magrep=pd.DataFrame(magnitude.values(),index=scores.keys(),columns=['Denominator'])
#        print magrep
        cosinesimilarity=pd.concat([scoresrep,magrep],axis=1)
        cosinesimilarity['Cosine_Similarity']=cosinesimilarity['Numerator']/(cosinesimilarity['Denominator'])**0.5
#        print cosinesimilarity
        sortedcosine=cosinesimilarity.sort(['Cosine_Similarity'],ascending=False)

        return sortedcosine


    def tfidf_query(self,term,coll):

        """
        print "\nTerm\n",term
        print "\nNumerator\n",coll.count(term)
        print "\nDenominator\n",len(coll)
        """
        tf = 1+math.log(float(coll.count(term)),10)
        """
        print 'query tf',tf
        print "\nIDF Documents\n",self.inv_index[term].postingslist_len
        """
        idf = math.log((float(self.corpussize)/self.inv_index[term].postingslist_len),10)
        """
        print 'query idf',idf
        print "\nQuery TF-IDF\n",tf*idf
        """
        return tf*idf


    def tfidf_doc(self,term,coll):

        doc_content = self.docs[coll].tokens.tokenized

        if term not in doc_content:
            return 0
        else:
            """
            print "\nTerm\n",term
            print "\nNumerator\n",doc_content.count(term)
            print "\nDenominator\n",len(doc_content)
            """
            tf = 1+math.log(float(doc_content.count(term)),10)
            """
            print 'doc tf',tf
            print "\nIDF Documents\n",self.inv_index[term].postingslist_len
            """
            idf = math.log((float(self.corpussize)/self.inv_index[term].postingslist_len),10)
            """
            print 'doc idf',idf
            print self.docs[coll].tokens
            print self.docs[coll]
            print "\nDoc TF-IDF\n",tf*idf
            """
            return tf*idf
