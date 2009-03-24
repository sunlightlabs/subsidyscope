#!/bin/python

import bailout.models
import etl.models
import csv
import re
from TarpReader import TarpReader
import sys
from datetime import datetime

        
class TarpWriter(TarpReader):
    
    def __init__(self):
        TarpReader.__init__(self)
        
        # create a record of the proceedings...
        datasource, created_new = etl.models.DataSource.objects.get_or_create(name='TARP Importer')
        datarun = bailout.models.DataRun()
        datarun.source = datasource
        datarun.save()
        self.datarun = datarun    
        
        # utility regex for splitting excel dates (bah!)
        self.re_date = re.compile(r'(\d+)[\-\/](\d+)[\-\/](\d+)[^\d]')
        
    
    def import_record(self, record):
        """import a single TARP record"""
        # TODO: deal with entries that have an existing institution record
        
        if record['institution_is_new']=='YES':     
            
            date = self.re_date.search(record.get('transaction_date'))
            year = int(date.group(3))
            month = int(date.group(1))
            day = int(date.group(2))
            if year<100:
                year = year + 2000
            
            # Institution     
            I = bailout.models.Institution()
            I.name = record.get('institution_name')
            I.city = record.get('institution_city')
            I.state = record.get('institution_state')
            I.institution_type = record.get('institution_institution_type', 'CAPITAL PURCHASE PROGRAM') 
            I.datarun = self.datarun       
            I.save()
            
            # Transaction
            T = bailout.models.Transaction()
            T.institution = I
            T.date = datetime(year, month, day)
            T.price_paid = record.get('transaction_price_paid')
            T.description = record.get('transaction_description')
            T.pricing_mechanism = record.get('transaction_pricing_mechanism')
            T.transaction_type = record.get('transaction_transaction_type')
            T.program = record.get('transaction_program', 'CPP')
            T.datarun = self.datarun
            T.save()

            
if __name__ == "__main__":

    TW = TarpWriter()

    reader = csv.reader(sys.stdin)
    for row in reader:
        record = {}
        for i in range(0,len(row)):
            record[TW.CSV_LAYOUT[i]] = row[i]            
        TW.import_record(record)
