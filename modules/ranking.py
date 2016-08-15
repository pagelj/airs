import pandas as pd
import math
import numpy as np
from query import *

class Ranking(object):

    def __init__(self,query,inv_index,corpussize, userargs,doc_obj):

        self.userargs=userargs
        self.doc_obj=doc_obj
        self.query=query
        self.corpussize=corpussize
        self.inv_index=inv_index
        if self.userargs.eval == 'tfidf':
            self.ranking=self.cosinesimilarity()
        elif self.userargs.eval == 'prox':
            self.ranking=self.proximityranking()
        self.ranking.to_csv('../ranking.csv')



        
    def cosinesimilarity(self):
        # Tfmatrix is a 2 dimensional dataframe that will store the tf values
        # of all terms and all documents in the corpus
        tfmatrix=pd.DataFrame(data=0,index=self.inv_index.keys(),columns=self.doc_obj.keys())

        # The dataframe is populated with values from the inverted index
        for term in self.inv_index.keys():

            for doc,tf in self.inv_index[term].tf.items():

                tfmatrix.loc[term,doc]=tf
        
        # the column idfdoc will store the idf values of each term of the inverted index
        tfmatrix['idfdoc']=np.log10(self.corpussize/(tfmatrix!=0).astype(int).sum(axis=1))

        # Another dataframe tdidfdoc is created, 
        # where the tf and idf values (of document terms) are multiplied and stored 
        tfidfdoc=tfmatrix.multiply(tfmatrix['idfdoc'],axis="index")
        tfidfdoc=tfidfdoc.drop('idfdoc',axis=1)
        tfidfdoc.to_csv("tfidfdoc.csv")

        #We now retreive the Query terms before we create the tdiff dataframe for them
        try:

            golddata = read_golddata('golddata.txt')

        except IOError:

            golddata = read_golddata('../golddata.txt')
        queries = golddata.keys()
        
        query_list=[]
        query_list_names=[]
        for query in queries:

            query = Query(query,'automatic')
            query_list.append(query)
            query_list_names.append(query.userinput)

        print "\n\n\n\n\n\n\n"
        
        #Similar to tfmatrix, querymatrix will store the tf values of all the terms in the query
        querymatrix=pd.DataFrame(data=0,index=self.inv_index.keys(),columns=query_list_names)
        querymatrix.to_csv("querymatrix.csv")

        for i in range(len(query_list)):

            for term in query_list[i].terms:
                if term not in self.inv_index.keys():
                    continue

                querymatrix.loc[term,query_list_names[i]]=float(1+np.log10(float(query_list[i].terms.count(term))))

         
        #tfidfquery is the dataframe containing the tfidf values of the query terms
        tfidfquery=querymatrix.multiply(tfmatrix['idfdoc'],axis="index")
        tfidfquery.to_csv("tfidfquery.csv")

        d2=np.sqrt(np.square(tfidfquery).sum(axis=0))

        #The below steps show the calculation of the cosine similarity
        cosinedf=pd.DataFrame(index=self.doc_obj.keys())
        for i in range(len(query_list_names)):
            print query_list_names[i]
            temp=pd.DataFrame(index=self.inv_index.keys())
            temp=tfidfdoc.multiply(tfidfquery.loc[:,query_list_names[i]],axis="index")
            val=d2[i]
            # d1 and d2 are the sum of the tf-idf summations 
            # of doc terms and query terms, respectively
            d1=np.sqrt(np.square(tfidfdoc).sum(axis=0))

            d1=d1*val
            print "\nD1\n",d1


            numerator=temp.sum(axis=0)
            print "\nNumerator\n",numerator
            cosinesimilarity=numerator/d1
            print cosinesimilarity
            tempdf=pd.DataFrame(cosinesimilarity,columns=[query_list_names[i]])
            print tempdf
            cosinedf=pd.concat([cosinedf,tempdf],axis=1)

        
        cosinedf.to_csv("cosinedf.csv")
        

    def proximityranking(self):
        #Proximity retrieves the location of each word in the query and 
        # finds the average distance between the query terms
        #print "\nInverted Index\n",inv_index
        prox={}
        magnitude={}
        terms=[]
        print "\nQuery\n",query
        print "\nTerms\n",inv_index.keys()
        for term in query.split():
            #print "\nTerm1\n",term
            if term not in terms:
                terms.append(term)
                if term in inv_index:
                    pl=inv_index[term]
                    postlist=pl.postingslist
                    print "\nPostings List\n",postlist
                    for doc in postlist:
                        print "\nDocument\n",doc
                        if doc in scores:
                            
                            prox[doc]+=1
                        # print scores
                        else:
                            
                            prox[doc]=1
                            # print scores

            else:
                continue
        # print scores
        #print "\nDoneso\n"
        scoresrep=pd.DataFrame(prox.values(),index=scores.keys(),columns=['Numerator'])

        print scoresrep
        sortedprox=scoresrep.sort(['Value'],ascending=False)

        return sortedcosine
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
