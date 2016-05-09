


class Ranking(object):

    def __init__(self,terms,querypostlist):
        self.terms=terms
        self.querypostlist=querypostlist
        
    
    def CosineSimilarity(self,terms,querypostlist):
        termfreqeuncy={}
        idfrequency={}
        counts={} 
        for i in xrange(len(names)):
            termfreqeuncy[names[i]]=termfreq(counts[names[i]])
        
        print counts
        print termfrequency
        