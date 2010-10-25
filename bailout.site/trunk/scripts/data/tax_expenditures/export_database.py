#!/usr/bin/env python
import os
import re
import csv
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from decimal import Decimal
from tax_expenditures.models import *

years = range(2000, 2016)

def recurse_category(parent, writer, indent):
    
    row = [indent, parent.name]
    row.append(None)
    row.append(None)
    for year in TE_YEARS:
        row.append(None)
        row.append(None)
        
    row.append(parent.description)    

    writer.writerow(row)
        
    for expenditure in parent.expenditure_set.order_by('source', 'analysis_year'):
        
        row = []
        row.append(indent + '+')
        row.append(expenditure.item_number)
        row.append(expenditure.get_source_display())
        row.append(expenditure.analysis_year)
        
        corp_estimates = {}
        indv_estimates = {}
        
        footnotes = {}
        
        for estimate in expenditure.estimate_set.all():
            
            if estimate.corporations_notes == Estimate.NOTE_POSITIVE:
                corp_estimates[estimate.estimate_year] = '<50'
            elif estimate.corporations_notes == Estimate.NOTE_NEGATIVE:
                corp_estimates[estimate.estimate_year] = '>-50'
            else:
                corp_estimates[estimate.estimate_year] = estimate.corporations_amount
            
            if estimate.individuals_notes == Estimate.NOTE_POSITIVE:
                indv_estimates[estimate.estimate_year] = '<50'
            elif estimate.individuals_notes == Estimate.NOTE_NEGATIVE:
                indv_estimates[estimate.estimate_year] = '>-50'
            else:
                indv_estimates[estimate.estimate_year] = estimate.individuals_amount
                
        for year in TE_YEARS:
            if corp_estimates.has_key(year):
                row.append(corp_estimates[year])
            else:
                row.append('')
                
        for year in TE_YEARS:                
            if indv_estimates.has_key(year):
                row.append(indv_estimates[year])
            else:
                row.append('')    
        
        row.append(expenditure.name)
        row.append(expenditure.notes)
        

        writer.writerow(row)                  
            
    indent += '#'

    for subgroup in Group.objects.filter(parent=parent):
        
        recurse_category(subgroup, writer, indent)
                    
                    
for group in Group.objects.filter(parent=None):
    
    file_name = re.sub('[^a-zA-Z]', '_', re.sub(',', '', group.name))
    
    csvfile = csv.writer(open('final_dumps/%s.csv' % (file_name), 'wb'))

    print file_name
    
    csvfile.writerow(['Indent','Category','Source','Report','2000 (Corp)','2001 (Corp)','2002 (Corp)','2003 (Corp)','2004 (Corp)','2005 (Corp)','2006 (Corp)','2007 (Corp)','2008 (Corp)','2009 (Corp)','2010 (Corp)','2011 (Corp)','2012 (Corp)','2013 (Corp)','2014 (Corp)','2015 (Corp)','2000 (Indv)','2001 (Indv)','2002 (Indv)','2003 (Indv)','2004 (Indv)','2005 (Indv)','2006 (Indv)','2007 (Indv)','2008 (Indv)','2009 (Indv)','2010 (Indv)','2011 (Indv)','2012 (Indv)','2013 (Indv)','2014 (Indv)','2015 (Indv)','Description/Expenditure Name', 'Notes'])
    
    recurse_category(group, csvfile, '')

