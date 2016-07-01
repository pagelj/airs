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
        # print self.inv_index
        self.ranking=self.cosinesimilarity(self.query,self.inv_index)
        #print self.ranking
        self.ranking.to_csv('../ranking.csv')

    def cosinesimilarity(self,query,inv_index):
        #print "\nInverted Index\n",inv_index
        scores={}
        magnitude={}
        terms=[]
        #print "\nQuery\n",query
        #print "\nTerms\n",inv_index.keys()
        for term in query.split():
            #print "\nTerm1\n",term
            if term not in terms:
                terms.append(term)
                if term in inv_index:
                    pl=inv_index[term]
                    postlist=pl.postingslist
                    #print "\nPostings List\n",postlist
                    for doc in postlist:
                        #print "\nDocument\n",doc
                        if doc in scores:
                            #print "\nDocument 1\n",doc
                            scores[doc]+=self.tfidf_query(term,query)*self.tfidf_doc(term,doc)
                        # print scores
                        else:
                            #print "\nDocument 2\n",doc
                            scores[doc]=self.tfidf_query(term,query)*self.tfidf_doc(term,doc)
                            # print scores

            else:
                continue
        # print scores
        #print "\nDoneso\n"
        scoresrep=pd.DataFrame(scores.values(),index=scores.keys(),columns=['Numerator'])
        # print scoresrep
        for term in inv_index.keys():
            #print "\nTerm6\n",term
            for doc in scores.keys():
                #print "\nDocument3\n",doc
                if doc in magnitude:
                    magnitude[doc]+= self.tfidf_doc(term,doc)**2
                else:
                    magnitude[doc]= self.tfidf_doc(term,doc)**2
        # print magnitude
        magrep=pd.DataFrame(magnitude.values(),index=scores.keys(),columns=['Denominator'])
        # print magrep
        cosinesimilarity=pd.concat([scoresrep,magrep],axis=1)
        cosinesimilarity['Cosine_Similarity']=cosinesimilarity['Numerator']/(cosinesimilarity['Denominator'])**0.5
        #print cosinesimilarity
        sortedcosine=cosinesimilarity.sort(['Cosine_Similarity'],ascending=False)
        print query
        print sortedcosine
        print '\n'

        return sortedcosine


    def tfidf_query(self,term,coll):

        #print "\nIn Query\n"
        #print "\nTerm3\n",term
        #print "\nNumerator\n",coll.count(term)
        
        tf = 1+math.log(float(coll.count(term)),10)
        
        #print 'query tf',tf
        #print "\nIDF Documents\n",self.inv_index[term].postingslist_len
        
        idf = math.log((float(self.corpussize)/self.inv_index[term].postingslist_len),10)
        
        #print "\nTerm4\n",term
        #print 'query idf',idf
        #print "\nQuery TF-IDF\n",tf*idf
        
        
        return tf*idf


    def tfidf_doc(self,term,coll):

        #print "\nTerm2\n",term
        #print "\nIn Doc\n"
        doc_content = self.docs[coll].tokens.tokenized

        if term not in doc_content:
            #print "\n Am in you\n"
            return 0
        else:
            
            #print "\nTerm5\n",term
            #print "\nNumerator\n",doc_content.count(term)

            
            tf = 1+math.log(float(doc_content.count(term)),10)
            
            #print 'doc tf',tf
            #print "\nIDF Documents\n",self.inv_index[term].postingslist_len
            
            idf = math.log((float(self.corpussize)/self.inv_index[term].postingslist_len),10)
            
            #print 'doc idf',idf
            #print self.docs[coll].tokens
            #print self.docs[coll]
            #print "\nDoc TF-IDF\n",tf*idf
            
            return tf*idf
