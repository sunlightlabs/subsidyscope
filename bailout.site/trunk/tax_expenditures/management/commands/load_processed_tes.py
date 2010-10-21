#!/usr/bin/env python

import os, csv
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option
from decimal import Decimal

from tax_expenditures.models import Group, Expenditure, Estimate

years = range(2000, 2016)

class Command(BaseCommand):
    help = "Loads processed TE data files from specified path"
    
    option_list = BaseCommand.option_list + (
        make_option("-p", "--path", dest="path", default=None),
    )

    def handle(self, *args, **options):
        
        if options['path'] is not None:    
            
            print 'Truncating TE database...'
            
            Group.objects.all().delete()
            Expenditure.objects.all().delete()
            Estimate.objects.all().delete()            
        
            print 'Loading processed TE data...'
        
            for file in os.listdir(options['path']):
                
                print file
                
                csvfile = csv.reader(open(options['path'] + file, 'rb'))
                
                data = []
            
                csvfile.next() # skip first header line

                for row in csvfile:
                    data.append(row)
                    
                data.reverse()
                
                process_file(data)
        else:
             
            print 'Error: --path argument required for input files.'    
            

            
def process_file(data):

    row = data.pop()
    
    if row[0] == '':
        group = Group.objects.create(name=row[1])
        
        process_group(group, data, '')
    else:
        print 'First category not matching signature.'
        
        
        
def process_group(parent, data, indent):
    
    indent += '#'
    
    lines_processed = 0
    
    while len(data):
        
        row = data.pop()
        
        lines_processed += 1
        
        if row[0] == indent:
            print row[1]
            group = Group.objects.create(name=row[1], parent=parent)
        
        elif row[0] == indent + '+':
            process_expenditure(group, row)
            
        elif row[0] == indent + '#':
            data.append(row)
            process_group(group, data, indent)
            
        else:
            data.append(row)
            return 
            
            

def process_expenditure(group, row):
    
    print row[2], row[3]
    
    if row[2] == 'JCT':
        source = Expenditure.SOURCE_JCT
        item_number = None
        
    elif row[2] == 'Treasury':
        source = Expenditure.SOURCE_TREASURY
        
        item_number = int(row[1])

    name = row[36]
    
    analysis_year = int(row[3])
    
    expenditure = Expenditure.objects.create(group=group, name=name, item_number=item_number, source=source, analysis_year=analysis_year)
    
    i = 0 
    
    for year in years:

        corp_raw = row[4 + i]
        indv_raw = row[20 + i]
        
        corp_amount = None
        corp_notes = None
        
        indv_amount = None
        indv_notes = None
        
        if corp_raw == '<50':
            corp_notes = Estimate.NOTE_POSITIVE
        elif corp_raw == '>-50':
            corp_notes = Estimate.NOTE_NEGATIVE
        else:
            try:
                corp_amount = Decimal(corp_raw)
            except:
                corp_amount = None
        
        if indv_raw == '<50':
            indv_notes = Estimate.NOTE_POSITIVE
        elif corp_raw == '>-50':
            indv_notes = Estimate.NOTE_NEGATIVE
        else:
            try:
                indv_amount = Decimal(indv_raw)
            except:
                indv_amount = None
        
        Estimate.objects.create(expenditure=expenditure, estimate_year=year, corporations_amount=corp_amount, individuals_amount=indv_amount, corporations_notes=corp_notes, individuals_notes=indv_notes)
                
        i += 1
        
    
