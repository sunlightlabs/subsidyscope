#!/usr/bin/env python

#!/usr/bin/env python

import os, csv, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option
from django.db import connection, transaction
from decimal import Decimal

from te_importer.models import ExpenditureGroup, Expenditure, Estimate

years = range(2000, 2017)

year_fields = len(years) * 2
name_field = year_fields + 5
notes_field = year_fields + 6


class Command(BaseCommand):
    help = "Loads processed TE data files from specified path"
    
    option_list = BaseCommand.option_list + (
        make_option("-p", "--path", dest="path", default=None),
    )

    def handle(self, *args, **options):
    
        
        if options['path'] is not None:
            process_file(options['path'])     
    
        else:
            print('No --path specified for descriptions file (e.g. data/omb_ap/ap_footnotes.txt)')     







    
    
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
        
            print year, id
        
        except:
            
            print 'Not found: ', year, id
        
        



