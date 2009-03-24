import os, sys, SubsidyExtractor, pickle, urllib2, re, datetime
import BeautifulSoup
import OpenAnything
from bailout.models import StandardAndPoorQuote


class TreasuryThreeYearExtractor(SubsidyExtractor.SubsidyExtractor):
    
    URL = 'http://finance.yahoo.com/q/hp?s=^GSPC&a=00&b=1&c=2007&d=11&e=31&f=2020&g=d'
    
    # set up directory for storing data
    def __init__(self, directory):
        SubsidyExtractor.SubsidyExtractor.__init__(self,directory)
             
    def ready(self):
        return True
        
    def get_data(self):        
        # run parent method to log beginning of run
        SubsidyExtractor.SubsidyExtractor.get_data(self)
        
        # retrieve HTML
        retrieved_files = self.retrieve_and_store_files(self.URL, [self.URL])
                    
    def process_data(self):                
       
        re_is_date = re.compile('[\d\-]')
               
        for retrieved_file in self._retrieved_files.values():
            for line in open(retrieved_file,'r'):
                line_parts = line.split(',')
                if len(line_parts)==7 and re_is_date.match(line_parts[0]):
                    values = {}
                    
                    date_parts = line_parts[0].strip().split('-')
                    assert len(date_parts)==3, "Date format appears to be invalid: %s" % line_parts[0]

                    values['date'] = datetime.datetime(int(date_parts[0]),int(date_parts[1]),int(date_parts[2])) # there is probably a better, shorter, pythonic way to pass this
                    values['open_price'] = line_parts[1]
                    values['high_price'] = line_parts[2]
                    values['low_price'] = line_parts[3]
                    values['close_price'] = line_parts[4]
                    values['volume'] = line_parts[5]
                    values['close_price_adjusted'] = line_parts[6]
                    values['datarun'] = self._datarun
                                                    
                    # insert or update the quote                        
                    sp_quote, sp_quote_was_created = StandardAndPoorQuote.objects.get_or_create(date=values['date'], defaults=values)                                        
                    if sp_quote_was_created:
                        self._records_inserted = self._records_inserted + 1
                    else:
                        update_record = False
                        for k in values:
                            if getattr(sp_quote,k)!=values[k]:
                                setattr(sp_quote,k,values[k])
                                update_record = True
                        if update_record:
                            sp_quote.save()                            
                            self._records_updated = self._records_updated + 1
        

        # record what we've just done
        self._record_stats()
    

if __name__=='__main__':   
    if sys.argv[1]=='test':
        import doctest
        doctest.testmod()        
    else:
        main()
   
