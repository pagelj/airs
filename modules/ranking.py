from term import *
import pandas as pd
from postingslist import *

class Ranking(object):

    def __init__(self,terms,querypostlist,query,idflist):
        
        self.idflist=idflist
        self.query=query
        self.terms=terms
        self.querypostlist=querypostlist
        self.ranking=self.CosineSimilarity(self.terms,self.querypostlist,self.query,self.idflist)

        
    def CosineSimilarity(self,terms,querypostlist,query,idflist):
        termfrequency=[]
        for item in terms:
            if item.name in querypostlist:
#                print item.tf
                termfrequency.append(item.tf)
#        print "Term Frequency \n"
#        print termfrequency   



#        print "Terms Frequency: \n"
#        print termfrequency

        tf=pd.DataFrame(termfrequency,index=querypostlist,columns=query)
        tf=tf.fillna(0)
        tf=tf.transpose()
        print tf
        print tf.shape
#        print idflist
        idflist.update((x, float(y)/100) for x,y in idflist.items())
        newidflist={}
        for key,value in idflist.iteritems():
            if key in query:
                newidflist[key]=value
        print newidflist
        idf=pd.DataFrame(newidflist.values(),index=query)
        print idf
        print idf.shape
        tfidf=pd.DataFrame(tf.values*idf.values, columns=tf.columns, index=tf.index)
        tfidf=tfidf.transpose()
        print tfidf
        matr=self.cosinelooper(tfidf)
        print matr
  
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