from term import *
import pandas as pd
from postingslist import *
import math

class Ranking(object):

    def __init__(self,query,inv_index,docs):

        self.query=query.query

        self.inv_index=inv_index
        self.docs=docs
#        print self.inv_index
        self.ranking=self.CosineSimilarity(self.query,self.inv_index)



    def CosineSimilarity(self,query,inv_index):

        scores={}
        for term in query:

            pl=inv_index[term]
            postlist=pl.postingslist
            #print postlist
            for doc in postlist:

                if doc in scores:
                    scores[doc]+=self.tfidf_query(term,query)*self.tfidf_doc(term,doc)
#                    print scores
                else:
                    scores[doc]=self.tfidf_query(term,query)*self.tfidf_doc(term,doc)
#                    print scores
        print scores
        scores=pd.DataFrame(scores,index=postlist,columns=query)
        print scores
    def tfidf_query(self,term,coll):

        print term
        tf = 1+((math.log(float(coll.count(term))))/(len(coll)))
        print 'query tf',tf
        idf = (float(100)/self.inv_index[term].postingslist_len)
        print 'query idf',idf

        return tf*idf


    def tfidf_doc(self,term,coll):

        doc_content = self.docs[coll].tokens.tokenized

        if term not in doc_content:
            return 0
        else:
            print term
            tf = 1+((math.log(float((doc_content).count(term))))/(len(doc_content)))
            print 'count of term in doc',float((doc_content).count(term))
            print 'len of doc',len(doc_content)
            print 'doc tf',tf
            idf = (float(100)/self.inv_index[term].postingslist_len)
            print 'doc idf',idf
            #print self.docs[coll].tokens
            #print self.docs[coll]
            return tf*idf


    def cosinesim(self,d1,d2):
        num=pd.Series(d1.values*d2.values,index=d1.index)
#        print num
        num=num.sum(axis=1)
#       The numerator is the product of the weights of each respective word
        sqd1=d1.apply(self.square)
        den1=math.sqrt(sqd1.sum(axis=1))

        sqd2=d2.apply(self.square)
        den2=math.sqrt(sqd2.sum(axis=1))
        den=den1*den2
        return num/den

    def cosinelooper(self,tfidf):
        simmatr=pd.DataFrame(index=tfidf.index,columns=tfidf.index)
        for i in xrange(len(tfidf.index)):
            for j in xrange(len(tfidf.index)):
                simmatr.iloc[i,j]=self.cosinesim(tfidf.iloc[i],tfidf.iloc[j])

        return simmatr


    def square(self,x):
        return x**2
