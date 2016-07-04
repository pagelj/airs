# -*- coding: utf-8 -*-
"""
@author: Prajit,Janis

Program will randomly take an arbitrary N number of documents from the 
repository and calculate the N*N matrix as the output.

Order of Execution of the user subprograms
1. CosineSimilarity()
    2. filereader()

    3. in loop:
        normalizer()

    4. in loop:
        termfreq()
    
    5. allnormalizer()

    6. in loop:
        idfreq()

    
    7. cosinelooper()
        in loop:
            8.  cosinesim()
            9.  square()      
"""   
from collections import Counter
import re,os,random as r,math,pandas as pd


""" 

FUNCTION FILEREADER
Function that takes a directory path and returns the text of each file in that 
directory
Input: Directory Path
Output: 1. A List with the content of each file in the directory
        2. The file names in a List
   
We take a random set of N files from the directory each time, 
and to keep consistency, 
we CAN use the seed function for consistency

"""
def filereader(directory):
    
#    r.seed(20)
# store is a list to hold the file contents    
    store=[]
    tempstore=[]
# names is a list to hold the file names       
    names=[]
# The below code will traverse the given directory and store all the file names 
#    in it    
    os.chdir(directory)
    for dirpath, dirs, files in os.walk(directory):
        print files[0]
#choices will store the random N files we will use in the experiment        
    choices=r.sample(xrange(len(files)),len(files))
    for x in choices:
        with open(files[x]) as inp_data:
            tempstore=inp_data.readlines()
            store.append(tempstore)
            names.append(files[x])
#    print names
    return store,names
    
""" 

FUNCTION NORMALIZER
Function that takes the text in a file and returns the tokenixed text with the frequency
Input: A single file's content
Output: 1. A special dictionary format which has a word as the key and its frequency at the value
        2. The list format of the above dictionary, which has only the words in the file

"""    

    
def normalizer(content):
    counts = Counter()
#We use REs to tokenize the text and we take only terms defined as words by RE standard    
    words = re.compile(r'\w+')

    for ele in content:
        counts.update(words.findall(ele.lower()))
#    print counts,list(counts)
    return counts,list(counts)

""" 

FUNCTION ALLNORMALIZER
Function that takes ALL the texts from the chosen files and returns the 
tokenixed text with the frequency
Input: All the file's content
Output: 1. A special dictionary format which has a word as the key and its 
            frequency at the value


"""


def allnormalizer(content):
    counts=Counter()
    words = re.compile(r'\w+')
#Similar to the normalizer() function, but it is now done for all documents
    for ele in content:
        for elem in ele:
            counts.update(words.findall(elem.lower()))
    return counts

""" 

FUNCTION TERMFREQ
Function that calculates the term frequency for each word in the input document
Input: A single file's content
Output: The tf for each word in the document

"""

           
def termfreq(counts):

#total will calculate the length of the particular document (only tokens)    
    total=sum(counts.values())
    for ele in counts:
        counts[ele]=counts[ele]/float(total)
    return counts

""" 

FUNCTION IDFREQ
Function that calculates the idf of each word encountered in the overall 
Content dictionary
Input:  1. A single word from the overall Content dictionary
        2. The overall Content dictionary [key- term, value- frequency]
Output: The idf for each word from all documents

"""

 
def idfreq(term, content):
    num = 0
    temp=[]
    for ele in content:
        temp=content.get(ele)
        if term in temp:
            num = num + 1
    print num,len(content)
    if num > 0:
        return 0.0 + math.log(float(len(content)) / num)
    else:
        return 0.0

""" 

FUNCTION SQUARE
Function that simply calculates the square of the input 
Input:  A numeric value
Output: The square of the input number

"""


def square(x):
    return x**2


""" 

FUNCTION COSINESIM
Function that calculates the Cosine Similarity of the input documents
Input:  Two documents
Output: A single float value which is the cosine similarity for the input 
        documents

"""

        
def cosinesim(d1,d2):
    num=pd.Series(d1.values*d2.values,index=d1.index)
#    print num
    num=num.sum(axis=1)
#   The numerator is the product of the weights of each respective word
    sqd1=d1.apply(square)
    den1=math.sqrt(sqd1.sum(axis=1))
    
    sqd2=d2.apply(square)
    den2=math.sqrt(sqd2.sum(axis=1))
    den=den1*den2
    return num/den


""" 

FUNCTION COSINELOOPER
Function that calculates the Cosine Similarity for all pair of documents
Input:  The tfidf matrix which was previously constructed
Output: A N*N cosine similarity matrix, where N is the number of documents
"""            
        
        
def cosinelooper(tfidf):
    simmatr=pd.DataFrame(index=tfidf.index,columns=tfidf.index)
    for i in xrange(len(tfidf.index)):
        for j in xrange(len(tfidf.index)):
            simmatr.iloc[i,j]=cosinesim(tfidf.iloc[i],tfidf.iloc[j])
    return simmatr
    
    

"""
Order of Execution of the user subprograms

1. filereader()

2. in loop:
    normalizer()

3. in loop:
    termfreq()
    
4. allnormalizer()

5. in loop:
    idfreq()


6. cosinelooper()
    in loop:
    7.  cosinesim()
    8.  square()      
"""   


""" 
The "Main"program for the task
"""
def CosineSimilarity(directory):
    
    content,names=filereader(directory)
    print "The files chosen and their contents are \n"
    for i in xrange(len(names)):
        print "Filename="+str(names[i])
        print "Content="+str(content[i])[1:-1]
        print "\n"

    counts={}
    termfreqeuncy={}
    idfrequency={}
    allwords={}
    for i in xrange(len(names)):
        counts[names[i]],allwords[names[i]]=normalizer(content[i]) 

    print counts
    for i in xrange(len(names)):
        termfreqeuncy[names[i]]=termfreq(counts[names[i]])
    print termfreqeuncy
    
    allcount=allnormalizer(content)
    allterms=list(allcount)
    for term in allterms:
       idfrequency[term]=idfreq(term,allwords)
    print 'IDF' ,idfrequency
    tf=pd.DataFrame(termfreqeuncy,columns=names,index=allterms)
    tf=tf.fillna(0)
    print tf
    idf1=pd.Series(idfrequency,index=allterms)
    idf=pd.DataFrame(idf1)
    print 'IDF2',idf
    tfidf=pd.DataFrame(tf.values*idf.values,columns=tf.columns,index=idf.index)
    tfidf=tfidf.transpose()
    matr=cosinelooper(tfidf)
    print "The Final Cosine Similarity Matrix is as below \n"
    print matr
    
