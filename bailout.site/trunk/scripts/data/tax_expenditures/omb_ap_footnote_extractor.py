#!/usr/bin/env python
import os
import re
import csv
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from decimal import Decimal
from tax_expenditures.models import Expenditure


    

def process_file(filename):
    
    file = open (filename, 'r')
    
    for line in file.readlines():
        line = line.strip()
        line_parts = line.split('\t')
        
        id = int(line_parts[0])
        year = int(line_parts[1])
        
        try:
            expenditure = Expenditure.objects.get(source=Expenditure.SOURCE_TREASURY, analysis_year=year, item_number=id)
        
            expenditure.notes = line_parts[2]
        
            expenditure.save()
        
            print year, id, line_parts[2]
        
        except:
            
            print 'Not found: ', year, id
        
        
process_file('data/omb_ap/ap_footnotes.txt')     


