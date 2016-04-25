

class File(object):

    def __init__(self, filename):
        self.docid=filename
        self.content=self.filereader(filename)



    def filereader(self,filename):
    
        f = open(filename, 'r')
        content = f.read()
        f.close()
        return content
    
