#!/usr/bin/env python

import os, re, csv
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management.base import BaseCommand, make_option

class Command(BaseCommand):
    
    help = "Loads processed TE data files from specified path"
    
    option_list = BaseCommand.option_list + (
        make_option("-p", "--path", dest="path", default=None),
    )

    def handle(self, *args, **options):
        
        if options['path'] is not None:   
            dump_data(options['path'])
        else:
            pass


from decimal import Decimal
from te_importer.models import Category, Expenditure, Estimate

years = range(2000, 2017)

def recurse_category(category, csvfile, indent):
    
    csvfile.writerow([indent, category.name])
    
    indent += '#'
    
    for group in category.expendituregroup_set.all():
        
        row = []
        row.append(indent)
        row.append(group.name)
        
        for field in range(0, 2 + (len(years) * 2)):
            row.append('')
            
        row.append(group.description)
        
        
        csvfile.writerow(row)
        
        for expenditure in group.group.order_by('source', 'analysis_year'):
            
            row = []
            row.append(indent + '+')
            row.append(expenditure.item_number)
            row.append(expenditure.get_source_display())
            row.append(expenditure.analysis_year)
            
            corp_estimates = {}
            indv_estimates = {}
            
            footnotes = {}
            
            for estimate in expenditure.estimate_set.all():
                
                if expenditure.source == Expenditure.SOURCE_JCT and estimate.corporations_amount == 10:
                    corp_estimates[estimate.estimate_year] = '<50'
                elif expenditure.source == Expenditure.SOURCE_JCT and estimate.corporations_amount == -10:
                    corp_estimates[estimate.estimate_year] = '>-50'
                else:
                    corp_estimates[estimate.estimate_year] = estimate.corporations_amount
                
                if expenditure.source == Expenditure.SOURCE_JCT and estimate.individuals_amount == 10:
                    indv_estimates[estimate.estimate_year] = '<50'
                elif expenditure.source == Expenditure.SOURCE_JCT and estimate.individuals_amount == -10:
                    indv_estimates[estimate.estimate_year] = '>-50'
                else:
                    indv_estimates[estimate.estimate_year] = estimate.individuals_amount
                    
                    footnotes[estimate.estimate_year] = estimate.notes
                    
            for year in years:
                if corp_estimates.has_key(year):
                    row.append(corp_estimates[year])
                else:
                    row.append('')
                    
            for year in years:                
                if indv_estimates.has_key(year):
                    row.append(indv_estimates[year])
                else:
                    row.append('')    
            
            row.append(expenditure.name)
            
            for year in years:
                if footnotes.has_key(year):
                    row.append(footnotes[year])
                else:
                    row.append('')
            
            csvfile.writerow(row)                  
                
                
    for subcategory in Category.objects.filter(parent=category):
        
        recurse_category(subcategory, csvfile, indent)
                

def dump_data(path):
    
    for budget_function in Category.objects.filter(parent=None):
        
        file_name = re.sub('[^a-zA-Z]', '_', re.sub(',', '', budget_function.name))
        
        csvfile = csv.writer(open(os.path.join(path, '%s.csv' % (file_name)), 'wb'))
    
        print file_name
        
        corp_years = []
        indv_years = []
        
        for year in years:
            corp_years.append('%d (Corp)' % year)
            indv_years.append('%d (Indv)' % year)
            
        csvfile.writerow(['Indent','Category','Source','Report'] + corp_years + indv_years + ['Expenditure Name'] + ['Expenditure Footnotes'])
        
        recurse_category(budget_function, csvfile, '')
 
        