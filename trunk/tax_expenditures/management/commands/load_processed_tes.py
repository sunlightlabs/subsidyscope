#!/usr/bin/env python

import os, csv
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option
from django.db import connection, transaction
from decimal import Decimal

from tax_expenditures.models import Group, Expenditure, Estimate, GroupDetail, GroupDetailReport, GroupSummary

years = range(2000, 2017)
year_fields = len(years) * 2
name_field = year_fields + 4
notes_field = year_fields + 5

te_tables = ['tax_expenditures_expenditure', 'tax_expenditures_group', 'tax_expenditures_groupdetail', 'tax_expenditures_groupdetailreport', 'tax_expenditures_groupdetailreport_group_source', 'tax_expenditures_groupsummary']

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
            GroupDetail.objects.all().delete()
            GroupDetailReport.objects.all().delete()
            GroupSummary.objects.all().delete()
            
            cursor = connection.cursor()
        
            # Data modifying operation - commit required
            for table in te_tables:
                cursor.execute("ALTER TABLE %s auto_increment=1;" % table)
                transaction.commit_unless_managed()

                       
        
            print 'Loading processed TE data...'
        
            files = os.listdir(options['path'])
            files.sort()
        
            for file in files:
                
                print file
                
                csvfile = csv.reader(open(options['path'] + file, 'rb'))
                
                data = []
            
                csvfile.next() # skip first header line

                for row in csvfile:
                    data.append(row)
                    
                data.reverse()
                
                process_file(data)
                
                
            

            
            print 'Generating TE summary data...'
            
            groups = Group.objects.filter(parent=None)
            
            for group in groups:
                print 'Processing %s...' % group.name
                group.calc_summary()
                
            
            print 'Generating TE detail data...'
            
            groups = Group.objects.filter(parent=None)

            for group in groups:
                print 'Processing %s...' % group.name
                group.calc_detail()
                
                
        else:
             
            print 'Error: --path argument required for input files.'    
            

            
def process_file(data):

    row = data.pop()
    
    if row[0] == '':
        group = Group.objects.create(name=row[1], description=row[36], notes=row[37])
        
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
            group = Group.objects.create(name=row[1], parent=parent)
            group.description = row[name_field]
            group.notes = row[notes_field]
            group.save()
        
        elif row[0] == indent + '+':
            process_expenditure(group, row)
            
        elif row[0] == indent + '#':
            data.append(row)
            process_group(group, data, indent)
            
        else:
            data.append(row)
            return 
            
            

def process_expenditure(group, row):

    
    if row[2] == 'JCT':
        source = Expenditure.SOURCE_JCT
        item_number = None
        
    elif row[2] == 'Treasury':
        source = Expenditure.SOURCE_TREASURY
        
        item_number = int(row[1])
    
    
    name = row[name_field] # 36
    notes = row[notes_field] # 37
    
    analysis_year = int(row[3])
    
    expenditure = Expenditure.objects.create(group=group, name=name, notes=notes, item_number=item_number, source=source, analysis_year=analysis_year)
    
    i = 0 
    
    for year in years:

        corp_raw = row[4 + i]
        indv_raw = row[(year_fields / 2) + 4 + i]
        
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
        
    
