#!/bin/python

import bailout.models
import etl.models
import csv
import re
import time
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
        
    def convert_isoformat_string_to_date(self, date_string):        
        date_parts = date_string.split(' ')
        return datetime.utcfromtimestamp(time.mktime(time.strptime(date_parts[0], '%Y-%m-%d')))        
    
    def display_broken_row(self, stream, message, record):
        print >>stream, message 
        row = []
        TW = TarpWriter()
        for field in TW.CSV_LAYOUT:
            row.append(record[field])
        writer = csv.writer(stream)
        writer.writerow(row)
        print
        del writer
        del TW
        del row
    
    def import_record(self, record):
        """import a single TARP record"""
        # TODO: deal with entries that have an existing institution record
        
        if record['institution_is_new']=='YES':     
            
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
            T.date = self.convert_isoformat_string_to_date(record.get('transaction_date'))
            T.price_paid = record.get('transaction_price_paid')
            T.description = record.get('transaction_description')
            T.pricing_mechanism = record.get('transaction_pricing_mechanism')
            T.transaction_type = record.get('transaction_transaction_type')
            T.program = record.get('transaction_program', 'CPP')
            T.datarun = self.datarun
            T.save()
            
        if record['institution_is_new']=='NO':
            institution_id = record.get('institution_existing_id').strip()
            if len(institution_id)==0:
                err_msg = "### Error! No ID for following row:"
                self.display_broken_row(sys.stderr, err_msg, record)
                return
            I = bailout.models.Institution.objects.filter(id=int(institution_id))
            if len(I)!=1:
                err_msg =  "### Error! Looked for institution ID %s and found %d results. Line follows:" % (record.get('institution_existing_id'), len(I))
                self.display_broken_row(sys.stderr, err_msg, record)
                return
            else:
                I = I[0]
                T = bailout.models.Transaction()
                T.institution = I                
                T.date = self.convert_isoformat_string_to_date(record.get('transaction_date'))
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
