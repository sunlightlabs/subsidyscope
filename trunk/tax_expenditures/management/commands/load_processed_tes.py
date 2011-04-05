#!/usr/bin/env python

import os, csv
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option
from django.db import connection, transaction
from decimal import Decimal
from django.core import management

from tax_expenditures.models import Group, Expenditure, Estimate, GroupDetail, GroupDetailReport, GroupSummary

years = range(2000, 2017)
year_fields = len(years) * 2
name_field = year_fields + 4
notes_field = year_fields + 5

TREASURY_SOURCES = {}

TREASURY_SOURCES[2011] = 'Description from <a href="http://www.gpoaccess.gov/usbudget/fy11/pdf/spec.pdf">Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2011.</a>'
TREASURY_SOURCES[2012] = 'Description from <a href="http://www.gpoaccess.gov/usbudget/fy12/pdf/BUDGET-2012-PER.pdf">Analytical Perspectives, Budget of the U.S. Government, Fiscal Year 2012.</a>'

te_tables = ['tax_expenditures_expenditure', 'tax_expenditures_group', 'tax_expenditures_groupdetail', 'tax_expenditures_groupdetailreport', 'tax_expenditures_groupdetailreport_group_source', 'tax_expenditures_groupsummary']

class Command(BaseCommand):
    help = "Loads processed TE data files from specified path"
    
    option_list = BaseCommand.option_list + (
        make_option("-p", "--path", dest="path", default=None),
    )

    def handle(self, *args, **options):
        
        if options['path'] is not None:    
            
            print 'Truncating TE database...'
            management.call_command('reset', 'tax_expenditures')            
#            Group.objects.all().delete()
 #           Expenditure.objects.all().delete()
  #          Estimate.objects.all().delete()
    #        GroupDetail.objects.all().delete()
   #         GroupDetailReport.objects.all().delete()
     #       GroupSummary.objects.all().delete()
            
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
       
            for g in Group.objects.filter(notes=''):
                #add treasury description footnotes to groups that don't have them         
                exp = Expenditure.objects.filter(group=g, source=2).order_by('-analysis_year')
                if exp.count() > 0:
                    year = exp[0].analysis_year
                try:
                    g.notes = TREASURY_SOURCES[year]
                except:
                    continue
                g.save()

            for g in Group.objects.all():
                try:
                    g.description = g.description.split("&mdash")[1].strip(';')
                    g.save()
                except:
                    continue

            
        else:
             
            print 'Error: --path argument required for input files.'    
            

            
def process_file(data):

    row = data.pop()
    
    if row[0] == '':
        group = Group.objects.create(name=row[1], description=row[38], notes=row[39])
        print row
        print group.description 
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
#            print group.description
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
        
    
