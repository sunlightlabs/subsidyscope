#!/usr/bin/env python
import os
import re
import csv
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from decimal import Decimal
from tax_expenditures.models import Expenditure

def save_description(year, id, paragraphs):
    
    final_text = ''
    
    for paragraph in paragraphs:
        final_text += '<p>%s</p>' % (paragraph)
    
    try:
        
        expenditure = Expenditure.objects.get(source=Expenditure.SOURCE_TREASURY, analysis_year=year, item_number=id)
        
        print 'Loading item %d: %s' % (id, expenditure.name)
        
        expenditure.description= final_text
        expenditure.save()
        
        expenditure.group.description = final_text
        expenditure.group.save()
    except:
        print "Item %d not found" % (id)
    

def process_file(filename, year):
    
    for expenditure in Expenditure.objects.filter(source=Expenditure.SOURCE_TREASURY, analysis_year=year):
        expenditure.description = ''
        expenditure.save()

    file = open (filename, 'r')
    
    line_id = 1
    description = '' 
    paragraphs = []
    
    for line in file.readlines():
        line = line.strip()
        line_regex = re.compile('^%d\. ' % (line_id))
        
        if not line:
            if not description == '': 
                paragraphs.append(description)
                description = ''
            
            continue
                
            
        if line_regex.match(line):
            
            if not description == '': 
                paragraphs.append(description)
                description = ''
            
            if len(paragraphs):
                save_description(year, line_id - 1, paragraphs)
                description = ''
                paragraphs = []
        
            line = line_part = line_regex.sub('', line)
                
            line_id += 1
        
        if line[-1] == '-':
            line = line[:-1]
        else:
            line += ' '
            
        description += line
    
    save_description(year, line_id - 1, paragraphs)
        
        
process_file('data/omb_ap/spec2011_descriptions.txt', 2011)     


