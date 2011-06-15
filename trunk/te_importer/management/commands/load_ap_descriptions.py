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
        make_option("-s", "--source_year", dest="source_year", default=None),
    )

    def handle(self, *args, **options):
        
        if options['source_year'] is not None:
            source_year = int(options['source_year'])
        else:
            print('No --source_year specified for input data.')
            exit()
        
        if options['path'] is not None:
            process_file(options['path'], source_year)
        else:
            print('No --path specified for descriptions file (e.g. data/omb_ap/spec2011_descriptions.txt)')     


def save_description(year, id, paragraphs):
    
    final_text = ''
    
    for paragraph in paragraphs:
        final_text += '<p>%s</p>' % (paragraph)
    
    try:
        
        expenditure = Expenditure.objects.get(source=Expenditure.SOURCE_TREASURY, analysis_year=year, item_number=id)
        
        print 'Loading item %d: %s' % (id, expenditure.name)
        
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
        line = unicode(line.decode("utf-8"))
        line = line.strip().replace(u'\x96', '-').replace(u'\u20ac', '-').replace(u'\u2013', '-').replace(u'\u2014', '&mdash;').replace(u'\u201c','"').replace(u'\u201d','"').replace(u'\xc2-15', '-').replace(u'\u2019', "'")
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
        
    


