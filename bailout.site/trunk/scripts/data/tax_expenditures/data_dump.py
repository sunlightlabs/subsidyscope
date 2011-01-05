#!/usr/bin/env python
import os
import re
import csv
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from decimal import Decimal
from te_importer.models import Category, Expenditure, Estimate

years = range(2000, 2016)

def recurse_category(category, csvfile, indent):
    
    csvfile.writerow([indent, category.name])
    
    indent += '#'
    
    for group in category.expendituregroup_set.all():
        
        row = []
        row.append(indent)
        row.append(group.name)
        
        csvfile.writerow(row)
        
        for expenditure in group.group.order_by('source', 'analysis_year'):
            
            row = []
            row.append(indent + '+')
            row.append(expenditure.id)
            row.append(expenditure.get_source_display())
            row.append(expenditure.analysis_year)
            
            corp_estimates = {}
            indv_estimates = {}
            
            footnotes = {}
            
            for estimate in expenditure.estimate_set.all():
                
                if expenditure.source == Expenditure.SOURCE_JCT and estimate.corporations_amount == 10:
                    corp_estimates[estimate.estimate_year] = '<+'
                elif expenditure.source == Expenditure.SOURCE_JCT and estimate.corporations_amount == -10:
                    corp_estimates[estimate.estimate_year] = '<-'
                else:
                    corp_estimates[estimate.estimate_year] = estimate.corporations_amount
                
                if expenditure.source == Expenditure.SOURCE_JCT and estimate.individuals_amount == 10:
                    indv_estimates[estimate.estimate_year] = '<+'
                elif expenditure.source == Expenditure.SOURCE_JCT and estimate.individuals_amount == -10:
                    indv_estimates[estimate.estimate_year] = '<-'
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
                

for budget_function in Category.objects.filter(parent=None):
    
    file_name = re.sub('[^a-zA-Z]', '_', re.sub(',', '', budget_function.name))
    
    csvfile = csv.writer(open('dumps/%s.csv' % (file_name), 'wb'))

    print file_name
    
    csvfile.writerow(['Indent','Category','Source','Report','2000 (Corp)','2001 (Corp)','2002 (Corp)','2003 (Corp)','2004 (Corp)','2005 (Corp)','2006 (Corp)','2007 (Corp)','2008 (Corp)','2009 (Corp)','2010 (Corp)','2011 (Corp)','2012 (Corp)','2013 (Corp)','2014 (Corp)','2015 (Corp)','2000 (Indv)','2001 (Indv)','2002 (Indv)','2003 (Indv)','2004 (Indv)','2005 (Indv)','2006 (Indv)','2007 (Indv)','2008 (Indv)','2009 (Indv)','2010 (Indv)','2011 (Indv)','2012 (Indv)','2013 (Indv)','2014 (Indv)','2015 (Indv)','Expenditure Name'])
    
    recurse_category(budget_function, csvfile, '')
    
    
    
    