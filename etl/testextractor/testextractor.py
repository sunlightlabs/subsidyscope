import os, sys, SubsidyExtractor, pickle, urllib2, re
import BeautifulSoup
import OpenAnything

class TarpExtractor(SubsidyExtractor.SubsidyExtractor):
    
    URL = 'http://www.ustreas.gov/initiatives/eesa/transactions.shtml'
    
    # set up directory for storing data
    def __init__(self, directory):
        SubsidyExtractor.SubsidyExtractor.__init__(self,directory)
             
    def ready(self):
        return True
        
    def get_data(self):        
        print "getting data"
        # run parent method to log beginning of run
        # SubsidyExtractor.SubsidyExtractor.get_data(self)        
        pass
                    
    def process_data(self):
        print "processing data"
        pass
    

if __name__=='__main__':   
    if sys.argv[1]=='test':
        import doctest
        doctest.testmod()        
    else:
        main()
   
