texts <- c("3624.txt",
           "6730.txt",
           "3267.txt",
           "4908.txt",
           "9844.txt",
           "3788.txt",
           "5009.txt",
           "4769.txt",
           "3187.txt",
           "76.txt",
           "8710.txt",
           "5460.txt",
           "8413.txt",
           "1730.txt",
           "8541.txt",
           "9442.txt",
           "6497.txt",
           "7191.txt",
           "4406.txt",
           "3170.txt",
           "6258.txt",
           "5839.txt",
           "639.txt",
           "6201.txt",
           "9516.txt",
           "4444.txt",
           "826.txt",
           "9122.txt",
           "2180.txt",
           "6770.txt",
           "621.txt",
           "9523.txt",
           "5376.txt",
           "6226.txt",
           "177.txt",
           "7404.txt")

annofiller<-function(i)
{
  file.show(i,title=i)
  crow=c()
  #input<-"1"
  input = readline(prompt="Enter 0 for complete irrelevancy or 1 for some relevancy to the queries :")
  while(input!="0" && input!="1")
  {
    input = as.integer(readline(prompt="Please enter 0 for irrelevancy and 1 for relevancy: "))
  }
  if (input=="0")
  {
    return(rep.int(0,length(queries)))
  }
  else
  {
    for(query in queries)
    {
      print(query)
      input = readline(prompt="Enter 0 for irrelevancy and 1 for relevancy: ")
      #input<-"1"
      while(input!="0" && input!="1")
      {
        input = as.integer(readline(prompt="Please enter 0 for irrelevancy and 1 for relevancy: "))
      }
      crow<-cbind(crow,as.integer(input))
    }
    return(crow)
  }
}

sortrows<-c()
cosinedf<-read.csv("C:/Users/Prajit Dhar/Desktop/IR/cosinedf.csv",row.names = 1)
queries<-c("camera good","camera good quality","camera good quality cheap","camera good quality expensive","camera with long battery runtime","lightweight camera","camera with good memory","phone camera with good resolution","camera sony","hd camera","good resolution mobile","I need a good camera with high resolution preferably cheap","small optical camera","32gb camera sd card","64gb camera","tv with big screen high resolution","phone with the best resolution","outdoor camera","camera internet","camera low price","camera high memory","phone cheap good quality","phone camera resolution","mobile big storage","phone display","iphone 5 opinion","mobile samsung good quality","latest cameras","tablet screen","gift camera for my wife")

for(i in 1:ncol(cosinedf))
{
  sortrows<-c(sortrows,row.names(cosinedf[order(cosinedf[,i],decreasing = TRUE)[1:150],]))
}

myrows<-unique(sortrows)
fnames<-list.files("/home/pagel/git/bitbucket/airs/amazon_reviews/")

annotations<-read.csv("/home/pagel/git/bitbucket/airs/scripts/annotations.csv",row.names = 1)
start<-sum(!is.na(annotations[1]))+1
newmyrows<-myrows[myrows>start]
setwd("/home/pagel/git/bitbucket/airs/amazon_reviews/")

for(i in texts)
{
  annotations[i,]<-annofiller(i)
}

write.csv(annotations, "annotations_test.csv",na="NA",row.names = TRUE)