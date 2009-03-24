import os, sys, SubsidyExtractor, pickle, urllib2, re, datetime
import BeautifulSoup
import OpenAnything
from bailout.models import TreasuryTenYearBondQuote


class TreasuryTenYearExtractor(SubsidyExtractor.SubsidyExtractor):
    
    URL = 'http://research.stlouisfed.org/fred2/data/DGS10.txt'
    
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

        re_bond_entry_line = re.compile('^(\d{4})\-(\d{2})\-(\d{2})\s{2,}(\d*\.\d*)$')
        re_numeral = re.compile('\d')

        for retrieved_file in self._retrieved_files.values():
            for line in open(retrieved_file,'r'):
                m = re_bond_entry_line.match(line.strip())
                if m:
                    date = datetime.datetime(int(m.group(1)),int(m.group(2)),int(m.group(3)))
                    price = m.group(4)
                    
                    # is this one of those weird '.' lines?
                    if not re_numeral.match(price):
                        price = None
                    
                    # insert or update the quote                        
                    bond_quote, bond_quote_was_created = TreasuryTenYearBondQuote.objects.get_or_create(date=date, defaults={'price': price, 'datarun': self._datarun})                                        
                    if bond_quote_was_created:
                        self._records_inserted = self._records_inserted + 1
                    else:
                        if bond_quote.price!=price:
                            bond_quote.price = price
                            bond_quote.datarun = self._datarun
                            bond_quote.save()
                            self._records_updated = self._records_updated + 1
        

        # record what we've just done
        self._record_stats()
    

if __name__=='__main__':   
    if sys.argv[1]=='test':
        import doctest
        doctest.testmod()        
    else:
        main()
   
