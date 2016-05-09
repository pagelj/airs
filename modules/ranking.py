from term import *
import panda as pd

class Ranking(object):

    def __init__(self,terms,querypostlist):
        self.terms=terms.terms
        self.querypostlist=querypostlist
        
    
    def CosineSimilarity(self,terms,querypostlist):
        termfreqeuncy=terms.tf
        names=self.terms
        idfrequency={}
        
        print counts
        print termfrequency
        tf=pd.DataFrame(termfreqeuncy,columns=names,index=querypostlist)
        tf=tf.fillna(0)
#       print tf
        idf1=pd.Series(idfrequency,index=allterms)
        idf=pd.DataFrame(idf1)
 #      print idf
        tfidf=pd.DataFrame(tf.values*idf.values,columns=tf.columns,index=idf.index)
        tfidf=tfidf.transpose()
        matr=cosinelooper(tfidf)
        print "The Final Cosine Similarity Matrix is as below \n"
        print matr
    
    
    def cosinesim(d1,d2):
        num=pd.Series(d1.values*d2.values,index=d1.index)
#        print num
        num=num.sum(axis=1)
#       The numerator is the product of the weights of each respective word
        sqd1=d1.apply(square)
        den1=math.sqrt(sqd1.sum(axis=1))
    
        sqd2=d2.apply(square)
        den2=math.sqrt(sqd2.sum(axis=1))
        den=den1*den2
        return num/den
        